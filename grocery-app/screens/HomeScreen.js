import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, TextInput, StyleSheet, ScrollView, Platform, ActivityIndicator, TouchableOpacity,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getProducts } from '../services/api';
import ProductCard from '../components/ProductCard';

export default function HomeScreen({ navigation }) {
  const [products, setProducts] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [userName, setUserName] = useState('');
  const [error, setError] = useState('');
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const name = await AsyncStorage.getItem('user_name');
      if (name) setUserName(name);
      const res = await getProducts();
      console.log('Products loaded:', res.data.length);
      setProducts(res.data);
      setFiltered(res.data);
      // Extract unique categories
      const cats = [...new Set(res.data.map(p => p.category).filter(Boolean))];
      cats.sort();
      setCategories(cats);
    } catch (err) {
      console.log('Error loading products:', err);
      setError(err.message || 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let result = products;
    // Filter by category
    if (selectedCategory !== 'All') {
      result = result.filter(p => p.category === selectedCategory);
    }
    // Filter by search
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(p =>
        p.product_name.toLowerCase().includes(q) ||
        (p.category && p.category.toLowerCase().includes(q))
      );
    }
    setFiltered(result);
  }, [search, products, selectedCategory]);

  const handleLogout = async () => {
    await AsyncStorage.clear();
    navigation.replace('Login');
  };

  const NavButton = ({ label, onPress, color }) => (
    <TouchableOpacity
      style={[styles.navBtn, { backgroundColor: color || '#27ae60' }]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Text style={styles.navBtnText}>{label}</Text>
    </TouchableOpacity>
  );

  // Build rows of 2 products
  const rows = [];
  for (let i = 0; i < filtered.length; i += 2) {
    rows.push(filtered.slice(i, i + 2));
  }

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#27ae60" />
        <Text style={{ marginTop: 10 }}>Loading products...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header bar */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Hi, {userName || 'Shopper'}!</Text>
        <View style={styles.headerBtns}>
          <NavButton label="🛒 Cart" onPress={() => navigation.navigate('Cart')} />
          <NavButton label="📦 Orders" onPress={() => navigation.navigate('OrderHistory')} />
          <NavButton label="Logout" onPress={handleLogout} color="#e74c3c" />
        </View>
      </View>

      {/* Search */}
      <View style={styles.searchWrap}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search products..."
          value={search}
          onChangeText={setSearch}
        />
      </View>

      {/* Category filter */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.catBar}
        contentContainerStyle={styles.catBarContent}
      >
        {['All', ...categories].map((cat) => (
          <TouchableOpacity
            key={cat}
            style={[styles.catChip, selectedCategory === cat && styles.catChipActive]}
            onPress={() => setSelectedCategory(cat)}
            activeOpacity={0.7}
          >
            <Text style={[styles.catChipText, selectedCategory === cat && styles.catChipTextActive]}>
              {cat}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <Text style={styles.count}>{filtered.length} products</Text>
      {error ? <Text style={{ color: 'red', paddingHorizontal: 14 }}>{error}</Text> : null}

      {/* Product grid – ScrollView */}
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={true}
      >
        {rows.map((row, idx) => (
          <View key={idx} style={styles.row}>
            {row.map((product) => (
              <ProductCard
                key={product.product_id}
                product={product}
                onPress={() => navigation.navigate('ProductDetail', { productId: product.product_id })}
              />
            ))}
            {row.length === 1 && <View style={{ width: '47%' }} />}
          </View>
        ))}
        <View style={{ height: 30 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 10,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  greeting: { fontSize: 16, fontWeight: '600', color: '#333' },
  headerBtns: { flexDirection: 'row', gap: 8 },
  navBtn: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 6,
    cursor: 'pointer',
  },
  navBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 13 },
  searchWrap: { paddingHorizontal: 14, paddingTop: 10 },
  searchInput: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 15,
  },
  count: { paddingHorizontal: 14, paddingTop: 4, paddingBottom: 4, color: '#888', fontSize: 13 },
  catBar: { maxHeight: 44, marginTop: 8 },
  catBarContent: { paddingHorizontal: 10, gap: 8, alignItems: 'center' },
  catChip: {
    paddingHorizontal: 14, paddingVertical: 7, borderRadius: 20,
    backgroundColor: '#e8e8e8', cursor: 'pointer',
  },
  catChipActive: { backgroundColor: '#27ae60' },
  catChipText: { fontSize: 13, color: '#555', fontWeight: '500' },
  catChipTextActive: { color: '#fff' },
  scroll: { flex: 1 },
  scrollContent: { paddingHorizontal: 8, paddingTop: 4 },
  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 0 },
});
