from rest_framework import serializers 
from .models import Products, Users, Orders, OrderItems, Locations, Cart, Stores

# we make serializers for each model to convert
# the data models to JSON format

class ProductS(serializers.ModelSerializer):
    class Meta:
        model =Products
        fields= '__all__'

class UserS(serializers.ModelSerializer):
    class Meta:
        model =Users
        fields= '__all__'

class OrderS(serializers.ModelSerializer):
    class Meta:
        model =Orders
        fields= '__all__'
class OrderItemS(serializers.ModelSerializer):
    class Meta:
        model =OrderItems
        fields= '__all__'

class LocationS(serializers.ModelSerializer):
    class Meta:
        model =Locations
        fields= '__all__'

class CartS(serializers.ModelSerializer):
    class Meta:
        model =Cart
        fields= '__all__'

class StoreS(serializers.ModelSerializer):
    class Meta:
        model =Stores
        fields='__all__' 




