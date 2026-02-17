import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, Image, StyleSheet, ScrollView, Platform, ActivityIndicator, TouchableOpacity, Alert,
  Modal, TextInput, FlatList,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getCart, removeFromCart, createOrder, getProduct, parseShoppingList, bulkAddToCart } from '../services/api';

export default function CartScreen({ navigation }) {
  const [cartItems, setCartItems] = useState([]);
  const [productDetails, setProductDetails] = useState({});
  const [loading, setLoading] = useState(true);
  const [checkingOut, setCheckingOut] = useState(false);
  
  // Shopping list parser states
  const [showParserModal, setShowParserModal] = useState(false);
  const [shoppingListText, setShoppingListText] = useState('');
  const [matchedProducts, setMatchedProducts] = useState([]);
  const [unmatchedItems, setUnmatchedItems] = useState([]);
  const [parsing, setParsing] = useState(false);
  const [addingToCart, setAddingToCart] = useState(false);
  const [selectedProducts, setSelectedProducts] = useState({});

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

  const handleParseShoppingList = async () => {
    if (!shoppingListText.trim()) {
      const msg = 'Please paste your shopping list first';
      Platform.OS === 'web' ? window.alert(msg) : Alert.alert('Empty Text', msg);
      return;
    }

    setParsing(true);
    try {
      const userId = await AsyncStorage.getItem('user_id');
      const response = await parseShoppingList({
        text: shoppingListText,
        user_id: userId,
      });

      setMatchedProducts(response.data.matched_products || []);
      setUnmatchedItems(response.data.unmatched_items || []);
      
      // Auto-select all matched products
      const selected = {};
      response.data.matched_products.forEach(product => {
        selected[product.product_id] = true;
      });
      setSelectedProducts(selected);

      if (response.data.matched_count === 0) {
        const msg = 'No products matched from your list. Try being more specific with product names.';
        Platform.OS === 'web' ? window.alert(msg) : Alert.alert('No Matches', msg);
      }
    } catch (err) {
      console.error('Error parsing shopping list:', err);
      const msg = 'Failed to parse shopping list';
      Platform.OS === 'web' ? window.alert(msg) : Alert.alert('Error', msg);
    } finally {
      setParsing(false);
    }
  };

  const handleAddParsedProducts = async () => {
    const productsToAdd = matchedProducts
      .filter(p => selectedProducts[p.product_id])
      .map(p => ({ product_id: p.product_id, quantity: 1 }));

    if (productsToAdd.length === 0) {
      const msg = 'Please select at least one product to add';
      Platform.OS === 'web' ? window.alert(msg) : Alert.alert('No Selection', msg);
      return;
    }

    setAddingToCart(true);
    try {
      const userId = await AsyncStorage.getItem('user_id');
      const response = await bulkAddToCart({
        user_id: userId,
        products: productsToAdd,
      });

      const msg = `Successfully added ${response.data.success_count} items to cart!`;
      if (Platform.OS === 'web') {
        window.alert(msg);
      } else {
        Alert.alert('Success ✅', msg);
      }

      // Close modal and refresh cart
      setShowParserModal(false);
      setShoppingListText('');
      setMatchedProducts([]);
      setUnmatchedItems([]);
      setSelectedProducts({});
      loadCart();
    } catch (err) {
      console.error('Error adding to cart:', err);
      const msg = err.response?.data?.error || 'Failed to add items to cart';
      Platform.OS === 'web' ? window.alert(msg) : Alert.alert('Error', msg);
    } finally {
      setAddingToCart(false);
    }
  };

  const toggleProductSelection = (productId) => {
    setSelectedProducts(prev => ({
      ...prev,
      [productId]: !prev[productId]
    }));
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

  // Shopping List Parser Modal - reusable
  const renderParserModal = () => (
    <Modal
      visible={showParserModal}
      animationType="slide"
      transparent={true}
      onRequestClose={() => setShowParserModal(false)}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>📋 Smart Shopping List</Text>
            <TouchableOpacity onPress={() => setShowParserModal(false)}>
              <Text style={styles.closeBtn}>✕</Text>
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.modalScroll}>
            <Text style={styles.instructionText}>
              Paste your shopping list below (one item per line):
            </Text>
            
            <TextInput
              style={styles.textInput}
              multiline={true}
              numberOfLines={8}
              placeholder={"Example:\nTomatoes\nBread\nMilk 1L\nRice 5kg\nEggs"}
              value={shoppingListText}
              onChangeText={setShoppingListText}
              textAlignVertical="top"
            />

            <TouchableOpacity
              style={[styles.parseBtn, parsing && { opacity: 0.6 }]}
              onPress={handleParseShoppingList}
              activeOpacity={0.7}
              disabled={parsing}
            >
              <Text style={styles.parseBtnText}>
                {parsing ? 'Analyzing...' : '🔍 Find Products'}
              </Text>
            </TouchableOpacity>

            {/* Matched Products */}
            {matchedProducts.length > 0 && (
              <View style={styles.resultsSection}>
                <Text style={styles.resultsTitle}>
                  ✅ Found {matchedProducts.length} matches:
                </Text>
                {matchedProducts.map((product) => (
                  <TouchableOpacity
                    key={product.product_id}
                    style={[
                      styles.productItem,
                      !selectedProducts[product.product_id] && styles.productItemDeselected
                    ]}
                    onPress={() => toggleProductSelection(product.product_id)}
                    activeOpacity={0.7}
                  >
                    <View style={styles.checkbox}>
                      {selectedProducts[product.product_id] && (
                        <Text style={styles.checkmark}>✓</Text>
                      )}
                    </View>
                    <View style={styles.productInfo}>
                      <Text style={styles.productName}>{product.product_name}</Text>
                      <Text style={styles.matchInfo}>
                        Matched: "{product.matched_text}" ({product.confidence}% match)
                      </Text>
                      <Text style={styles.productPrice}>Rs.{product.price}</Text>
                    </View>
                  </TouchableOpacity>
                ))}

                <TouchableOpacity
                  style={[styles.addAllBtn, addingToCart && { opacity: 0.6 }]}
                  onPress={handleAddParsedProducts}
                  activeOpacity={0.7}
                  disabled={addingToCart}
                >
                  <Text style={styles.addAllBtnText}>
                    {addingToCart ? 'Adding...' : `Add Selected to Cart`}
                  </Text>
                </TouchableOpacity>
              </View>
            )}

            {/* Unmatched Items */}
            {unmatchedItems.length > 0 && (
              <View style={styles.resultsSection}>
                <Text style={styles.unmatchedTitle}>
                  ❓ Couldn't find ({unmatchedItems.length}):
                </Text>
                {unmatchedItems.map((item, index) => (
                  <View key={index} style={styles.unmatchedItem}>
                    <Text style={styles.unmatchedText}>{item}</Text>
                  </View>
                ))}
                <Text style={styles.hintText}>
                  💡 Try searching manually or use more specific product names
                </Text>
              </View>
            )}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );

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
        <TouchableOpacity
          style={[styles.shopBtn, { backgroundColor: '#2196f3', marginTop: 12 }]}
          onPress={() => setShowParserModal(true)}
          activeOpacity={0.7}
        >
          <Text style={styles.shopBtnText}>📋 Paste Shopping List</Text>
        </TouchableOpacity>
        {renderParserModal()}
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Quick add button for shopping list parser */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.parserBtn}
          onPress={() => setShowParserModal(true)}
          activeOpacity={0.7}
        >
          <Text style={styles.parserBtnText}>📋 Paste Shopping List</Text>
        </TouchableOpacity>
      </View>

      {/* Scrollable cart items */}
      <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollContent}>
        {cartItems.map((item) => {
          const prod = productDetails[item.product];
          const imgSrc = prod?.image_url
            ? (prod.image_url.startsWith('http') ? prod.image_url : `https://${prod.image_url}`)
            : null;

          return (
            <TouchableOpacity
              key={item.cart_id}
              style={styles.cartItem}
              activeOpacity={0.7}
              onPress={() => navigation.navigate('ProductDetail', { productId: item.product })}
            >
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
            </TouchableOpacity>
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

      {/* Shopping List Parser Modal */}
      {renderParserModal()}
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
  header: {
    backgroundColor: '#fff',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  parserBtn: {
    backgroundColor: '#2196f3',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
    cursor: 'pointer',
  },
  parserBtnText: { color: '#fff', fontWeight: '600', fontSize: 14 },
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
  
  // Modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    maxHeight: '90%',
    paddingBottom: 20,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  modalTitle: { fontSize: 20, fontWeight: 'bold', color: '#333' },
  closeBtn: { fontSize: 28, color: '#888', fontWeight: '300' },
  modalScroll: { padding: 20 },
  instructionText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    minHeight: 120,
    backgroundColor: '#fafafa',
    marginBottom: 16,
  },
  parseBtn: {
    backgroundColor: '#2196f3',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 20,
    cursor: 'pointer',
  },
  parseBtnText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  resultsSection: {
    marginTop: 10,
    marginBottom: 20,
  },
  resultsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#27ae60',
    marginBottom: 12,
  },
  productItem: {
    flexDirection: 'row',
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    marginBottom: 8,
    borderWidth: 2,
    borderColor: '#27ae60',
    cursor: 'pointer',
  },
  productItemDeselected: {
    borderColor: '#ddd',
    opacity: 0.6,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 4,
    borderWidth: 2,
    borderColor: '#27ae60',
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 2,
  },
  checkmark: {
    color: '#27ae60',
    fontSize: 18,
    fontWeight: 'bold',
  },
  productInfo: { flex: 1 },
  productName: {
    fontSize: 15,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  matchInfo: {
    fontSize: 12,
    color: '#888',
    marginBottom: 4,
    fontStyle: 'italic',
  },
  productPrice: {
    fontSize: 14,
    color: '#27ae60',
    fontWeight: 'bold',
  },
  addAllBtn: {
    backgroundColor: '#27ae60',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 12,
    cursor: 'pointer',
  },
  addAllBtnText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  unmatchedTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ff9800',
    marginBottom: 12,
    marginTop: 10,
  },
  unmatchedItem: {
    padding: 10,
    backgroundColor: '#fff3e0',
    borderRadius: 6,
    marginBottom: 6,
    borderLeftWidth: 3,
    borderLeftColor: '#ff9800',
  },
  unmatchedText: {
    fontSize: 14,
    color: '#666',
  },
  hintText: {
    fontSize: 12,
    color: '#999',
    marginTop: 8,
    fontStyle: 'italic',
  },
});
