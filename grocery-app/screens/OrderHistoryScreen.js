import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, StyleSheet, ScrollView, Platform, ActivityIndicator,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getOrders } from '../services/api';

export default function OrderHistoryScreen({ navigation }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadOrders = useCallback(async () => {
    try {
      setLoading(true);
      const userId = await AsyncStorage.getItem('user_id');
      const res = await getOrders(userId);
      // Sort newest first
      const sorted = res.data.sort((a, b) => b.order_id - a.order_id);
      setOrders(sorted);
    } catch (err) {
      console.log('Error loading orders:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', loadOrders);
    return unsubscribe;
  }, [navigation, loadOrders]);

  const getStatusStyle = (status) => {
    switch (status?.toLowerCase()) {
      case 'delivered': return { bg: '#e8f5e9', text: '#27ae60' };
      case 'shipped': return { bg: '#e3f2fd', text: '#2196f3' };
      case 'cancelled': return { bg: '#ffebee', text: '#e74c3c' };
      default: return { bg: '#fff3e0', text: '#f57c00' };
    }
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#27ae60" />
        <Text style={{ marginTop: 10 }}>Loading orders...</Text>
      </View>
    );
  }

  if (orders.length === 0) {
    return (
      <View style={styles.center}>
        <Text style={{ fontSize: 50 }}>📦</Text>
        <Text style={styles.emptyText}>No orders yet</Text>
        <View
          style={styles.shopBtn}
          {...(Platform.OS === 'web'
            ? { onClick: () => navigation.navigate('Home') }
            : { onTouchEnd: () => navigation.navigate('Home') })}
        >
          <Text style={styles.shopBtnText}>Start Shopping</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollContent}>
        {orders.map((order) => {
          const statusStyle = getStatusStyle(order.status);
          return (
            <View key={order.order_id} style={styles.orderCard}>
              <View style={styles.orderHeader}>
                <Text style={styles.orderId}>Order #{order.order_id}</Text>
                <View style={[styles.statusBadge, { backgroundColor: statusStyle.bg }]}>
                  <Text style={[styles.statusText, { color: statusStyle.text }]}>
                    {order.status || 'Pending'}
                  </Text>
                </View>
              </View>

              <View style={styles.orderDetails}>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Date</Text>
                  <Text style={styles.detailValue}>
                    {order.order_date ? new Date(order.order_date).toLocaleDateString() : 'N/A'}
                  </Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Total</Text>
                  <Text style={styles.totalValue}>
                    Rs.{parseFloat(order.total_amount || 0).toFixed(0)}
                  </Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Payment</Text>
                  <Text style={styles.detailValue}>
                    {order.payment_method || 'Cash on Delivery'}
                  </Text>
                </View>
              </View>
            </View>
          );
        })}
        <View style={{ height: 30 }} />
      </ScrollView>
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
  orderCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 5,
    elevation: 2,
  },
  orderHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
    paddingBottom: 10,
  },
  orderId: { fontSize: 16, fontWeight: 'bold', color: '#333' },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: { fontSize: 12, fontWeight: '600' },
  orderDetails: {},
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 4,
  },
  detailLabel: { fontSize: 14, color: '#888' },
  detailValue: { fontSize: 14, color: '#333' },
  totalValue: { fontSize: 16, fontWeight: 'bold', color: '#27ae60' },
});
