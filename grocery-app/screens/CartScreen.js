import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, Image, StyleSheet, ScrollView, Platform, ActivityIndicator, TouchableOpacity, Alert,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getCart, removeFromCart, createOrder, getProduct } from '../services/api';

export default function CartScreen({ navigation }) {
  const [cartItems, setCartItems] = useState([]);
  const [productDetails, setProductDetails] = useState({});
  const [loading, setLoading] = useState(true);
  const [checkingOut, setCheckingOut] = useState(false);

  const loadCart = useCallback(async () => {
    try {
      setLoading(true);
      const userId = await AsyncStorage.getItem('user_id');
      const res = await getCart(userId);
      setCartItems(res.data);

      // Fetch product details for each cart item
      const details = {};
      await Promise.all(
        res.data.map(async (item) => {
          try {
            const pRes = await getProduct(item.product);
            details[item.product] = pRes.data;
          } catch (e) {}
        })
      );
      setProductDetails(details);
    } catch (err) {
      console.log('Error loading cart:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', loadCart);
    return unsubscribe;
  }, [navigation, loadCart]);

  const handleRemove = async (cartId, productName) => {
    const doRemove = async () => {
      try {
        await removeFromCart(cartId);
        setCartItems(prev => prev.filter(item => item.cart_id !== cartId));
      } catch (err) {
        const msg = 'Failed to remove item';
        Platform.OS === 'web' ? window.alert(msg) : Alert.alert('Error', msg);
      }
    };

    if (Platform.OS === 'web') {
      if (window.confirm(`Remove ${productName} from cart?`)) doRemove();
    } else {
      Alert.alert('Remove Item', `Remove ${productName} from cart?`, [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Remove', style: 'destructive', onPress: doRemove },
      ]);
    }
  };

  const handleCheckout = async () => {
    if (cartItems.length === 0) {
      const msg = 'Your cart is empty!';
      Platform.OS === 'web' ? window.alert(msg) : Alert.alert('Cart Empty', msg);
      return;
    }

    const doCheckout = async () => {
      setCheckingOut(true);
      try {
        const userId = await AsyncStorage.getItem('user_id');
        await createOrder({
          user_id: parseInt(userId),
          payment_method: 'Cash on Delivery',
        });
        const msg = 'Order placed successfully! Pay with cash on delivery.';
        if (Platform.OS === 'web') {
          window.alert(msg);
          navigation.navigate('OrderHistory');
        } else {
          Alert.alert('Order Placed ✅', msg, [
            { text: 'View Orders', onPress: () => navigation.navigate('OrderHistory') },
          ]);
        }
      } catch (err) {
        const msg = err.response?.data?.error || 'Checkout failed';
        Platform.OS === 'web' ? window.alert(msg) : Alert.alert('Checkout Failed', msg);
      } finally {
        setCheckingOut(false);
      }
    };

    if (Platform.OS === 'web') {
      if (window.confirm('Place order with Cash on Delivery?')) doCheckout();
    } else {
      Alert.alert('Confirm Order', 'Place order with Cash on Delivery?', [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Place Order', onPress: doCheckout },
      ]);
    }
  };

  const getTotal = () => {
    return cartItems.reduce((sum, item) => {
      const prod = productDetails[item.product];
      const price = prod ? parseFloat(prod.price) : 0;
      return sum + price * item.quantity;
    }, 0);
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#27ae60" />
        <Text style={{ marginTop: 10 }}>Loading cart...</Text>
      </View>
    );
  }

  if (cartItems.length === 0) {
    return (
      <View style={styles.center}>
        <Text style={{ fontSize: 50 }}>🛒</Text>
        <Text style={styles.emptyText}>Your cart is empty</Text>
        <TouchableOpacity
          style={styles.shopBtn}
          onPress={() => navigation.goBack()}
          activeOpacity={0.7}
        >
          <Text style={styles.shopBtnText}>Continue Shopping</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Scrollable cart items */}
      <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollContent}>
        {cartItems.map((item) => {
          const prod = productDetails[item.product];
          const imgSrc = prod?.image_url
            ? (prod.image_url.startsWith('http') ? prod.image_url : `https://${prod.image_url}`)
            : null;

          return (
            <View key={item.cart_id} style={styles.cartItem}>
              {imgSrc ? (
                <Image source={{ uri: imgSrc }} style={styles.itemImage} resizeMode="cover" />
              ) : (
                <View style={[styles.itemImage, styles.placeholder]}>
                  <Text style={{ fontSize: 24 }}>🛒</Text>
                </View>
              )}
              <View style={styles.itemInfo}>
                <Text style={styles.itemName} numberOfLines={2}>
                  {prod?.product_name || `Product #${item.product}`}
                </Text>
                <Text style={styles.itemPrice}>
                  Rs.{prod ? parseFloat(prod.price).toFixed(0) : '0'}
                  {item.size ? ` / ${item.size}` : ''}
                </Text>
                {item.size && (
                  <Text style={styles.itemSize}>Size: {item.size}</Text>
                )}
                <Text style={styles.itemQty}>Qty: {item.quantity}</Text>
                <Text style={styles.itemSubtotal}>
                  Subtotal: Rs.{prod ? (parseFloat(prod.price) * item.quantity).toFixed(0) : '0'}
                </Text>
              </View>
              <TouchableOpacity
                style={styles.removeBtn}
                onPress={() => handleRemove(item.cart_id, prod?.product_name || 'this item')}
                activeOpacity={0.7}
              >
                <Text style={styles.removeBtnText}>✕</Text>
              </TouchableOpacity>
            </View>
          );
        })}
        {/* Spacer so content isn't hidden behind footer */}
        <View style={{ height: 120 }} />
      </ScrollView>

      {/* Fixed checkout footer */}
      <View style={styles.footer}>
        <View style={styles.totalRow}>
          <Text style={styles.totalLabel}>Total ({cartItems.length} items)</Text>
          <Text style={styles.totalAmount}>Rs.{getTotal().toFixed(0)}</Text>
        </View>
        <View style={styles.paymentInfo}>
          <Text style={styles.paymentText}>💵 Payment: Cash on Delivery</Text>
        </View>
        <TouchableOpacity
          style={[styles.checkoutBtn, checkingOut && { opacity: 0.6 }]}
          onPress={handleCheckout}
          activeOpacity={0.7}
          disabled={checkingOut}
        >
          <Text style={styles.checkoutBtnText}>
            {checkingOut ? 'Placing Order...' : 'Proceed to Checkout (COD)'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  emptyText: { fontSize: 18, color: '#888', marginTop: 12, marginBottom: 20 },
  shopBtn: {
    backgroundColor: '#27ae60', paddingHorizontal: 24, paddingVertical: 12,
    borderRadius: 8, cursor: 'pointer',
  },
  shopBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 15 },
  scroll: { flex: 1 },
  scrollContent: { padding: 14 },
  cartItem: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 12,
    marginBottom: 10,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  itemImage: { width: 70, height: 70, borderRadius: 8 },
  placeholder: { backgroundColor: '#f0f0f0', justifyContent: 'center', alignItems: 'center' },
  itemInfo: { flex: 1, marginLeft: 12 },
  itemName: { fontSize: 14, fontWeight: '600', color: '#333', marginBottom: 3 },
  itemPrice: { fontSize: 14, color: '#27ae60', fontWeight: 'bold' },
  itemSize: { fontSize: 11, color: '#2196f3', marginTop: 1, fontWeight: '500' },
  itemQty: { fontSize: 12, color: '#888', marginTop: 2 },
  itemSubtotal: { fontSize: 13, color: '#555', marginTop: 2, fontWeight: '500' },
  removeBtn: {
    width: 34, height: 34, borderRadius: 17,
    backgroundColor: '#fee', justifyContent: 'center', alignItems: 'center',
    cursor: 'pointer',
  },
  removeBtnText: { color: '#e74c3c', fontSize: 16, fontWeight: 'bold' },
  footer: {
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#eee',
    paddingHorizontal: 20,
    paddingVertical: 14,
    paddingBottom: 24,
  },
  totalRow: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center', marginBottom: 8,
  },
  totalLabel: { fontSize: 16, color: '#555' },
  totalAmount: { fontSize: 22, fontWeight: 'bold', color: '#333' },
  paymentInfo: { marginBottom: 12 },
  paymentText: { fontSize: 14, color: '#888' },
  checkoutBtn: {
    backgroundColor: '#27ae60',
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: 'center',
    cursor: 'pointer',
  },
  checkoutBtnText: { color: '#fff', fontSize: 17, fontWeight: 'bold' },
});
