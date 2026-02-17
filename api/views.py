from django.shortcuts import render

# Create your views here.
#this basically makes your crud logic for each model
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from difflib import SequenceMatcher
from .models import Cart, Locations, OrderItems, Orders, Products, Stores, Users, EmailOtp
from .serializers import (
    CartS, LocationS, OrderItemS, 
    OrderS, ProductS, StoreS, UserS
)
#ModelViewSet has built in crud logic so we use
#it directly for each model without creating.
class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductS

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserS

class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()
    serializer_class = CartS
    
    def create(self, request, *args, **kwargs):
        # Get user_id from request data (for now, until frontend sends token)
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        
        # Check if product exists and has enough stock
        try:
            product = Products.objects.get(product_id=product_id)
            
            if product.stock_quantity < quantity:
                return Response({
                    'error': f'Insufficient stock. Only {product.stock_quantity} items available.'
                }, status=400)
            
            if product.stock_quantity < 1:
                return Response({
                    'error': 'Product out of stock'
                }, status=400)
            
            # If stock is sufficient, proceed with adding to cart
            return super().create(request, *args, **kwargs)
            
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
    
    def get_queryset(self):
        # If user_id is provided in query params, filter cart by user
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Cart.objects.filter(user_id=user_id)
        return Cart.objects.all()

class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Orders.objects.all()
    serializer_class = OrderS

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Orders.objects.filter(user_id=user_id)
        return Orders.objects.all()
    
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        
        # Get all cart items for this user
        cart_items = Cart.objects.filter(user_id=user_id)
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=400)
        
        # Calculate total amount from cart and check stock
        total_amount = 0
        for cart_item in cart_items:
            product = Products.objects.get(product_id=cart_item.product_id)
            
            # Check stock before checkout
            if product.stock_quantity < cart_item.quantity:
                return Response({
                    'error': f'Insufficient stock for {product.product_name}'
                }, status=400)
            
            total_amount += product.price * cart_item.quantity
        
        # Create order with auto-calculated total
        order = Orders.objects.create(
            user_id=user_id,
            store_id=request.data.get('store_id', 1),
            order_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_amount=total_amount,
            status='pending',
            delivery_address=request.data.get('delivery_address', ''),
            payment_method=request.data.get('payment_method', 'Cash on Delivery'),
            delivery_time=request.data.get('delivery_time', '')
        )
        
        # Create order items and deduct stock
        for cart_item in cart_items:
            product = Products.objects.get(product_id=cart_item.product_id)
            
            OrderItems.objects.create(
                order_id=order.order_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                unit_price=product.price,
                subtotal=product.price * cart_item.quantity
            )
            
            # Deduct stock
            product.stock_quantity -= cart_item.quantity
            product.save()
        
        # Clear cart after successful checkout
        cart_items.delete()
        
        return Response({
            'message': 'Order placed successfully',
            'order_id': order.order_id,
            'total_amount': total_amount,
            'items_ordered': len(cart_items)
        }, status=201)

class OrderItemsViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemS

class StoresViewSet(viewsets.ModelViewSet):
    queryset = Stores.objects.all()
    serializer_class = StoreS

class LocationsViewSet(viewsets.ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationS

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    # Get data from request
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Check if user exists
    if Users.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)
    
    # Check if email is verified via OTP
    try:
        otp_record = EmailOtp.objects.filter(email=email, is_verified=True).latest('created_at')
    except EmailOtp.DoesNotExist:
        return Response({'error': 'Email not verified. Please verify your email first.'}, status=400)
    
    # Create user with hashed password
    user = Users.objects.create(
        name=name,
        email=email,
        password_hash=make_password(password)
    )
    
    # Clean up OTP records for this email
    EmailOtp.objects.filter(email=email).delete()
    
    return Response({'message': 'User registered successfully', 'user_id': user.user_id})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = Users.objects.get(email=email)
        
        # Check password
        if check_password(password, user.password_hash):
            # Generate JWT tokens
            refresh = RefreshToken()
            refresh['user_id'] = user.user_id
            refresh['email'] = user.email
            
            return Response({
                'message': 'Login successful',
                'user_id': user.user_id,
                'name': user.name,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=400)

    # Check if email is already registered
    if Users.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=400)

    # Generate 6-digit OTP
    otp_code = str(random.randint(100000, 999999))

    # Delete any existing OTPs for this email
    EmailOtp.objects.filter(email=email).delete()

    # Save new OTP
    EmailOtp.objects.create(email=email, otp=otp_code, is_verified=False)

    # Send email
    try:
        send_mail(
            subject='FreshMart - Your Verification Code',
            message=f'Your OTP verification code is: {otp_code}\n\nThis code expires in 5 minutes.\n\nIf you did not request this, please ignore this email.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

    return Response({'message': 'OTP sent to your email'})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
        return Response({'error': 'Email and OTP are required'}, status=400)

    try:
        otp_record = EmailOtp.objects.filter(email=email, otp=otp).latest('created_at')
    except EmailOtp.DoesNotExist:
        return Response({'error': 'Invalid OTP'}, status=400)

    # Check if OTP is expired (5 minutes)
    from django.utils import timezone
    if timezone.now() - otp_record.created_at > timedelta(minutes=5):
        otp_record.delete()
        return Response({'error': 'OTP has expired. Please request a new one.'}, status=400)

    # Mark as verified
    otp_record.is_verified = True
    otp_record.save()

    return Response({'message': 'Email verified successfully'})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def resend_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=400)

    # Generate new OTP
    otp_code = str(random.randint(100000, 999999))

    # Delete old OTPs
    EmailOtp.objects.filter(email=email).delete()

    # Save new OTP
    EmailOtp.objects.create(email=email, otp=otp_code, is_verified=False)

    # Send email
    try:
        send_mail(
            subject='FreshMart - Your New Verification Code',
            message=f'Your new OTP verification code is: {otp_code}\n\nThis code expires in 5 minutes.\n\nIf you did not request this, please ignore this email.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

    return Response({'message': 'New OTP sent to your email'})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def parse_shopping_list(request):
    """
    Parse a shopping list text and match products from the database.
    Accepts text input and returns matched products with similarity scores.
    """
    text = request.data.get('text', '')
    user_id = request.data.get('user_id')
    
    if not text:
        return Response({'error': 'Text input is required'}, status=400)
    
    if not user_id:
        return Response({'error': 'User ID is required'}, status=400)
    
    # Split text into lines and clean them
    lines = text.strip().split('\n')
    potential_products = []
    
    for line in lines:
        # Clean the line: remove numbers, bullets, dashes, extra spaces
        cleaned = re.sub(r'^[\d\.\-\*\•\–\—]+\s*', '', line.strip())
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove common quantity patterns (e.g., "2kg", "500g", "3 pieces")
        cleaned = re.sub(r'\d+\s*(kg|g|ml|l|piece|pieces|pcs|packets?|bags?|bottles?)\s*', '', cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip()
        
        if cleaned and len(cleaned) > 2:  # Ignore very short entries
            potential_products.append(cleaned)
    
    # Get all products from database
    all_products = Products.objects.all()
    
    matched_products = []
    unmatched_items = []
    
    for item_name in potential_products:
        best_match = None
        best_score = 0
        
        for product in all_products:
            # Calculate similarity score
            # Check against product name
            name_score = SequenceMatcher(None, item_name.lower(), product.product_name.lower()).ratio()
            
            # Also check if item_name is contained in product name or vice versa
            if item_name.lower() in product.product_name.lower():
                name_score = max(name_score, 0.8)
            if product.product_name.lower() in item_name.lower():
                name_score = max(name_score, 0.75)
            
            # Check against brand if available
            brand_bonus = 0
            if product.brand and product.brand.lower() in item_name.lower():
                brand_bonus = 0.1
            
            # Check against category
            category_bonus = 0
            if product.category and product.category.lower() in item_name.lower():
                category_bonus = 0.05
            
            total_score = name_score + brand_bonus + category_bonus
            
            if total_score > best_score:
                best_score = total_score
                best_match = product
        
        # Consider it a match if score is above threshold (60%)
        if best_match and best_score >= 0.6:
            matched_products.append({
                'product_id': best_match.product_id,
                'product_name': best_match.product_name,
                'price': best_match.price,
                'category': best_match.category,
                'brand': best_match.brand,
                'image_url': best_match.image_url,
                'stock_quantity': best_match.stock_quantity,
                'matched_text': item_name,
                'confidence': round(best_score * 100, 1)
            })
        else:
            unmatched_items.append(item_name)
    
    return Response({
        'matched_products': matched_products,
        'unmatched_items': unmatched_items,
        'total_items': len(potential_products),
        'matched_count': len(matched_products),
        'unmatched_count': len(unmatched_items)
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def bulk_add_to_cart(request):
    """
    Add multiple products to cart at once.
    Expects a list of product IDs with quantities.
    """
    user_id = request.data.get('user_id')
    products = request.data.get('products', [])  # List of {product_id, quantity}
    
    if not user_id:
        return Response({'error': 'User ID is required'}, status=400)
    
    if not products:
        return Response({'error': 'Products list is required'}, status=400)
    
    added_items = []
    failed_items = []
    
    for item in products:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        
        try:
            product = Products.objects.get(product_id=product_id)
            
            # Check stock
            if product.stock_quantity < quantity:
                failed_items.append({
                    'product_id': product_id,
                    'product_name': product.product_name,
                    'reason': f'Insufficient stock. Only {product.stock_quantity} available.'
                })
                continue
            
            # Check if item already exists in cart
            existing_cart_item = Cart.objects.filter(user_id=user_id, product_id=product_id).first()
            
            if existing_cart_item:
                # Update quantity
                new_quantity = existing_cart_item.quantity + quantity
                if product.stock_quantity < new_quantity:
                    failed_items.append({
                        'product_id': product_id,
                        'product_name': product.product_name,
                        'reason': f'Cannot add {quantity} more. Stock limit: {product.stock_quantity}, already in cart: {existing_cart_item.quantity}'
                    })
                    continue
                existing_cart_item.quantity = new_quantity
                existing_cart_item.save()
                added_items.append({
                    'product_id': product_id,
                    'product_name': product.product_name,
                    'quantity': new_quantity,
                    'action': 'updated'
                })
            else:
                # Create new cart item
                cart_item = Cart.objects.create(
                    user_id=user_id,
                    product_id=product_id,
                    quantity=quantity,
                    added_at=datetime.now()
                )
                added_items.append({
                    'product_id': product_id,
                    'product_name': product.product_name,
                    'quantity': quantity,
                    'action': 'added'
                })
                
        except Products.DoesNotExist:
            failed_items.append({
                'product_id': product_id,
                'reason': 'Product not found'
            })
    
    return Response({
        'message': f'Successfully processed {len(added_items)} items',
        'added_items': added_items,
        'failed_items': failed_items,
        'success_count': len(added_items),
        'failure_count': len(failed_items)
    })
