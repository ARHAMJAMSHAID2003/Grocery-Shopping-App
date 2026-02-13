import React, { useState } from 'react';
import { View, Text, Image, StyleSheet, Platform, TouchableOpacity } from 'react-native';
import { addToCart } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function ProductCard({ product, onPress }) {
  const [status, setStatus] = useState('');

  const handleAdd = async () => {
    try {
      setStatus('Adding...');
      const userId = await AsyncStorage.getItem('user_id');
      await addToCart({
        user: parseInt(userId),
        product: product.product_id,
        quantity: 1,
      });
      setStatus('✅ Added!');
      setTimeout(() => setStatus(''), 1500);
    } catch (err) {
      const msg = err.response?.data?.error || 'Failed';
      setStatus('❌ ' + msg);
      setTimeout(() => setStatus(''), 2000);
    }
  };

  const imgSrc = product.image_url
    ? (product.image_url.startsWith('http') ? product.image_url : `https://${product.image_url}`)
    : null;

  return (
    <View style={styles.card}>
      {/* Tappable area for product detail */}
      <TouchableOpacity
        style={styles.cardContent}
        onPress={onPress}
        activeOpacity={0.7}
      >
        {imgSrc ? (
          <Image source={{ uri: imgSrc }} style={styles.image} resizeMode="cover" />
        ) : (
          <View style={[styles.image, styles.placeholder]}>
            <Text style={{ fontSize: 30 }}>🛒</Text>
          </View>
        )}
        <Text style={styles.name} numberOfLines={2}>{product.product_name}</Text>
        {product.description ? (
          <Text style={styles.description} numberOfLines={2}>{product.description}</Text>
        ) : null}
        <Text style={styles.price}>
          Rs.{parseFloat(product.price).toFixed(0)}
          {product.unit ? <Text style={styles.unitText}> / {product.unit}</Text> : null}
        </Text>
        {product.stock_quantity !== undefined && (
          <Text style={styles.stock}>
            {product.stock_quantity > 0 ? `In Stock: ${product.stock_quantity}` : 'Out of Stock'}
          </Text>
        )}
      </TouchableOpacity>

      {/* Add to cart button – separate from nav tap */}
      <TouchableOpacity
        style={[styles.addBtn, product.stock_quantity <= 0 && styles.addBtnDisabled]}
        onPress={handleAdd}
        activeOpacity={0.7}
        disabled={product.stock_quantity <= 0}
      >
        <Text style={styles.addBtnText}>
          {status || (product.stock_quantity > 0 ? 'Add to Cart' : 'Unavailable')}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginBottom: 12,
    marginHorizontal: 6,
    width: '47%',
    shadowColor: '#000',
    shadowOpacity: 0.08,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 3,
    overflow: 'hidden',
  },
  cardContent: {
    padding: 10,
    cursor: 'pointer',
  },
  image: {
    width: '100%',
    height: 120,
    borderRadius: 8,
    marginBottom: 8,
  },
  placeholder: {
    backgroundColor: '#f0f0f0',
    justifyContent: 'center',
    alignItems: 'center',
  },
  name: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 2,
    height: 36,
  },
  description: {
    fontSize: 11,
    color: '#777',
    marginBottom: 4,
    height: 28,
  },
  price: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#27ae60',
    marginBottom: 2,
  },
  unitText: {
    fontSize: 12,
    fontWeight: '400',
    color: '#888',
  },
  stock: {
    fontSize: 11,
    color: '#888',
    marginBottom: 4,
  },
  addBtn: {
    backgroundColor: '#27ae60',
    paddingVertical: 10,
    alignItems: 'center',
    cursor: 'pointer',
  },
  addBtnDisabled: {
    backgroundColor: '#ccc',
  },
  addBtnText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 13,
  },
});
