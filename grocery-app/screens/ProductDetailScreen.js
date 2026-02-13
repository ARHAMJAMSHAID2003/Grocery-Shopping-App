import React, { useState, useEffect } from 'react';
import {
  View, Text, Image, StyleSheet, ScrollView, Platform, ActivityIndicator, TouchableOpacity,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getProduct, addToCart } from '../services/api';

// Size configurations per category
const SIZE_CONFIG = {
  Dairy: {
    label: 'Size',
    options: [
      { label: '250ml', multiplier: 0.25 },
      { label: '500ml', multiplier: 0.5 },
      { label: '1L', multiplier: 1.0, default: true },
      { label: '1.5L', multiplier: 1.5 },
    ],
  },
  Beverages: {
    label: 'Size',
    options: [
      { label: '250ml', multiplier: 0.25 },
      { label: '330ml', multiplier: 0.33 },
      { label: '500ml', multiplier: 0.5 },
      { label: '1L', multiplier: 1.0, default: true },
      { label: '1.5L', multiplier: 1.5 },
      { label: '2L', multiplier: 2.0 },
    ],
  },
  Meat: {
    label: 'Weight',
    options: [
      { label: '250g', multiplier: 0.25 },
      { label: '500g', multiplier: 0.5 },
      { label: '1kg', multiplier: 1.0, default: true },
      { label: '2kg', multiplier: 2.0 },
    ],
  },
  Fruits: {
    label: 'Weight',
    options: [
      { label: '250g', multiplier: 0.25 },
      { label: '500g', multiplier: 0.5 },
      { label: '1kg', multiplier: 1.0, default: true },
      { label: '2kg', multiplier: 2.0 },
      { label: '5kg', multiplier: 5.0 },
    ],
  },
  Vegetables: {
    label: 'Weight',
    options: [
      { label: '250g', multiplier: 0.25 },
      { label: '500g', multiplier: 0.5 },
      { label: '1kg', multiplier: 1.0, default: true },
      { label: '2kg', multiplier: 2.0 },
    ],
  },
  Pantry: {
    label: 'Weight',
    options: [
      { label: '500g', multiplier: 0.5 },
      { label: '1kg', multiplier: 1.0, default: true },
      { label: '2kg', multiplier: 2.0 },
      { label: '5kg', multiplier: 5.0 },
    ],
  },
  Seafood: {
    label: 'Weight',
    options: [
      { label: '250g', multiplier: 0.25 },
      { label: '500g', multiplier: 0.5 },
      { label: '1kg', multiplier: 1.0, default: true },
    ],
  },
  Deli: {
    label: 'Weight',
    options: [
      { label: '100g', multiplier: 0.1 },
      { label: '250g', multiplier: 0.25 },
      { label: '500g', multiplier: 0.5 },
      { label: '1kg', multiplier: 1.0, default: true },
    ],
  },
};

export default function ProductDetailScreen({ route, navigation }) {
  const { productId } = route.params;
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState('');
  const [selectedSize, setSelectedSize] = useState(null);

  useEffect(() => {
    loadProduct();
  }, []);

  const loadProduct = async () => {
    try {
      const res = await getProduct(productId);
      setProduct(res.data);

      // Set default size based on category
      const config = SIZE_CONFIG[res.data.category];
      if (config) {
        const defaultOpt = config.options.find(o => o.default) || config.options[2] || config.options[0];
        setSelectedSize(defaultOpt);
      }
    } catch (err) {
      console.log('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const sizeConfig = product ? SIZE_CONFIG[product.category] : null;

  // Calculate effective price based on selected size
  const getEffectivePrice = () => {
    const basePrice = parseFloat(product.price);
    if (selectedSize) {
      return basePrice * selectedSize.multiplier;
    }
    return basePrice;
  };

  const handleAdd = async () => {
    try {
      setStatus('Adding...');
      const userId = await AsyncStorage.getItem('user_id');
      const payload = {
        user: parseInt(userId),
        product: product.product_id,
        quantity,
      };
      if (selectedSize) {
        payload.size = selectedSize.label;
      }
      await addToCart(payload);
      setStatus('✅ Added to cart!');
      setTimeout(() => setStatus(''), 2000);
    } catch (err) {
      const msg = err.response?.data?.error || 'Failed to add';
      setStatus('❌ ' + msg);
      setTimeout(() => setStatus(''), 2500);
    }
  };

  const changeQty = (delta) => {
    setQuantity(prev => {
      const next = prev + delta;
      if (next < 1) return 1;
      if (product && next > product.stock_quantity) return product.stock_quantity;
      return next;
    });
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#27ae60" />
      </View>
    );
  }

  if (!product) {
    return (
      <View style={styles.center}>
        <Text>Product not found</Text>
      </View>
    );
  }

  const imgSrc = product.image_url
    ? (product.image_url.startsWith('http') ? product.image_url : `https://${product.image_url}`)
    : null;

  const effectivePrice = getEffectivePrice();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {imgSrc ? (
        <Image source={{ uri: imgSrc }} style={styles.image} resizeMode="cover" />
      ) : (
        <View style={[styles.image, styles.placeholder]}>
          <Text style={{ fontSize: 60 }}>🛒</Text>
        </View>
      )}

      <View style={styles.details}>
        <Text style={styles.name}>{product.product_name}</Text>

        {/* Price display */}
        <View style={styles.priceRow}>
          <Text style={styles.price}>Rs.{effectivePrice.toFixed(0)}</Text>
          {selectedSize && (
            <Text style={styles.perUnit}>
              / {selectedSize.label}
            </Text>
          )}
          {!selectedSize && product.unit && (
            <Text style={styles.perUnit}>/ {product.unit}</Text>
          )}
        </View>

        {product.description ? (
          <Text style={styles.descriptionText}>{product.description}</Text>
        ) : null}

        {product.category && (
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{product.category}</Text>
          </View>
        )}

        <View style={styles.stockRow}>
          <Text style={product.stock_quantity > 0 ? styles.inStock : styles.outStock}>
            {product.stock_quantity > 0 ? `✅ In Stock (${product.stock_quantity} available)` : '❌ Out of Stock'}
          </Text>
        </View>

        {/* Size/Weight picker */}
        {sizeConfig && product.stock_quantity > 0 && (
          <View style={styles.sizeSection}>
            <Text style={styles.sizeLabel}>📏 Select {sizeConfig.label}:</Text>
            <View style={styles.sizeRow}>
              {sizeConfig.options.map((opt) => {
                const isSelected = selectedSize?.label === opt.label;
                return (
                  <TouchableOpacity
                    key={opt.label}
                    style={[styles.sizeChip, isSelected && styles.sizeChipActive]}
                    onPress={() => setSelectedSize(opt)}
                    activeOpacity={0.7}
                  >
                    <Text style={[styles.sizeChipText, isSelected && styles.sizeChipTextActive]}>
                      {opt.label}
                    </Text>
                    <Text style={[styles.sizeChipPrice, isSelected && styles.sizeChipPriceActive]}>
                      Rs.{(parseFloat(product.price) * opt.multiplier).toFixed(0)}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          </View>
        )}

        {product.stock_quantity > 0 && (
          <>
            {/* Quantity selector */}
            <View style={styles.qtyRow}>
              <Text style={styles.qtyLabel}>Quantity:</Text>
              <TouchableOpacity
                style={styles.qtyBtn}
                onPress={() => changeQty(-1)}
                activeOpacity={0.7}
              >
                <Text style={styles.qtyBtnText}>−</Text>
              </TouchableOpacity>
              <Text style={styles.qtyValue}>{quantity}</Text>
              <TouchableOpacity
                style={styles.qtyBtn}
                onPress={() => changeQty(1)}
                activeOpacity={0.7}
              >
                <Text style={styles.qtyBtnText}>+</Text>
              </TouchableOpacity>
            </View>

            {/* Add to cart button */}
            <TouchableOpacity
              style={styles.addBtn}
              onPress={handleAdd}
              activeOpacity={0.7}
            >
              <Text style={styles.addBtnText}>
                {status || `Add to Cart — Rs.${(effectivePrice * quantity).toFixed(0)}`}
              </Text>
            </TouchableOpacity>
          </>
        )}

        {/* Go to cart */}
        <TouchableOpacity
          style={styles.goCartBtn}
          onPress={() => navigation.navigate('Cart')}
          activeOpacity={0.7}
        >
          <Text style={styles.goCartText}>🛒 View Cart</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: { paddingBottom: 40 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  image: { width: '100%', height: 280 },
  placeholder: { backgroundColor: '#f0f0f0', justifyContent: 'center', alignItems: 'center' },
  details: { padding: 20 },
  name: { fontSize: 22, fontWeight: 'bold', color: '#333', marginBottom: 8 },
  priceRow: { flexDirection: 'row', alignItems: 'baseline', marginBottom: 8 },
  price: { fontSize: 26, fontWeight: 'bold', color: '#27ae60' },
  perUnit: { fontSize: 15, color: '#888', marginLeft: 4 },
  descriptionText: { fontSize: 14, color: '#666', lineHeight: 20, marginBottom: 12 },
  badge: {
    alignSelf: 'flex-start', backgroundColor: '#e8f5e9',
    paddingHorizontal: 12, paddingVertical: 4, borderRadius: 12, marginBottom: 12,
  },
  badgeText: { color: '#27ae60', fontSize: 13, fontWeight: '500' },
  stockRow: { marginBottom: 16 },
  inStock: { color: '#27ae60', fontSize: 14 },
  outStock: { color: '#e74c3c', fontSize: 14 },

  // Size picker
  sizeSection: { marginBottom: 20 },
  sizeLabel: { fontSize: 16, fontWeight: '600', color: '#333', marginBottom: 10 },
  sizeRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  sizeChip: {
    borderWidth: 2, borderColor: '#e0e0e0', borderRadius: 12,
    paddingHorizontal: 14, paddingVertical: 10, alignItems: 'center',
    minWidth: 70, backgroundColor: '#fafafa',
  },
  sizeChipActive: {
    borderColor: '#27ae60', backgroundColor: '#e8f5e9',
  },
  sizeChipText: { fontSize: 14, fontWeight: 'bold', color: '#555' },
  sizeChipTextActive: { color: '#27ae60' },
  sizeChipPrice: { fontSize: 11, color: '#999', marginTop: 2 },
  sizeChipPriceActive: { color: '#27ae60' },

  qtyRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 20 },
  qtyLabel: { fontSize: 16, marginRight: 12, color: '#555' },
  qtyBtn: {
    width: 38, height: 38, borderRadius: 19,
    backgroundColor: '#f0f0f0', justifyContent: 'center', alignItems: 'center',
    cursor: 'pointer',
  },
  qtyBtnText: { fontSize: 20, fontWeight: 'bold', color: '#333' },
  qtyValue: { fontSize: 18, fontWeight: 'bold', marginHorizontal: 16, minWidth: 24, textAlign: 'center' },
  addBtn: {
    backgroundColor: '#27ae60', paddingVertical: 15,
    borderRadius: 10, alignItems: 'center', marginBottom: 12, cursor: 'pointer',
  },
  addBtnText: { color: '#fff', fontSize: 17, fontWeight: 'bold' },
  goCartBtn: {
    borderWidth: 2, borderColor: '#27ae60',
    paddingVertical: 12, borderRadius: 10, alignItems: 'center', cursor: 'pointer',
  },
  goCartText: { color: '#27ae60', fontSize: 15, fontWeight: '600' },
});
