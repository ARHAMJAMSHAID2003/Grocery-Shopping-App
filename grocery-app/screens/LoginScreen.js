import React, { useState, useEffect, useRef } from 'react';
import {
  View, Text, TextInput, StyleSheet, Platform,
  Alert, KeyboardAvoidingView, ScrollView, Image, TouchableOpacity,
  Dimensions,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { login, register, sendOtp, verifyOtp, resendOtp } from '../services/api';

const { width } = Dimensions.get('window');

export default function LoginScreen({ navigation }) {
  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // OTP flow state
  const [otpStep, setOtpStep] = useState(false); // true = showing OTP input
  const [otp, setOtp] = useState('');
  const [otpTimer, setOtpTimer] = useState(0);
  const timerRef = useRef(null);

  // Clear any old invalid tokens when login screen loads
  useEffect(() => {
    AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user_id', 'user_name']);
  }, []);

  // Countdown timer for resend
  useEffect(() => {
    if (otpTimer > 0) {
      timerRef.current = setTimeout(() => setOtpTimer(otpTimer - 1), 1000);
    }
    return () => clearTimeout(timerRef.current);
  }, [otpTimer]);

  const showMsg = (title, msg) => {
    if (Platform.OS === 'web') {
      window.alert(msg);
    } else {
      Alert.alert(title, msg);
    }
  };

  const handleSubmit = async () => {
    if (!email || !password || (!isLogin && !name)) {
      showMsg('Error', 'Please fill in all fields');
      return;
    }
    setLoading(true);
    try {
      if (isLogin) {
        const res = await login({ email, password });
        const { user_id, name: userName, access_token, refresh_token } = res.data;
        await AsyncStorage.setItem('access_token', access_token);
        await AsyncStorage.setItem('refresh_token', refresh_token);
        await AsyncStorage.setItem('user_id', String(user_id));
        await AsyncStorage.setItem('user_name', userName);
        navigation.replace('Home');
      } else {
        // Step 1: Send OTP to email
        await sendOtp({ email });
        showMsg('OTP Sent', 'A 6-digit verification code has been sent to your email.');
        setOtpStep(true);
        setOtpTimer(60); // 60 second cooldown for resend
      }
    } catch (err) {
      const msg = err.response?.data?.error || err.response?.data?.detail || 'Something went wrong';
      showMsg('Error', msg);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    if (!otp || otp.length !== 6) {
      showMsg('Error', 'Please enter the 6-digit code');
      return;
    }
    setLoading(true);
    try {
      // Verify OTP
      await verifyOtp({ email, otp });
      // OTP verified — now register
      await register({ name, email, password });
      showMsg('Success', 'Account created! Please login.');
      // Reset to login mode
      setOtpStep(false);
      setOtp('');
      setIsLogin(true);
    } catch (err) {
      const msg = err.response?.data?.error || err.response?.data?.detail || 'Verification failed';
      showMsg('Error', msg);
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    if (otpTimer > 0) return;
    setLoading(true);
    try {
      await resendOtp({ email });
      showMsg('OTP Sent', 'A new verification code has been sent to your email.');
      setOtpTimer(60);
      setOtp('');
    } catch (err) {
      const msg = err.response?.data?.error || err.response?.data?.detail || 'Failed to resend';
      showMsg('Error', msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSwitchMode = () => {
    setIsLogin(!isLogin);
    setOtpStep(false);
    setOtp('');
    setOtpTimer(0);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
        {/* Top hero section with gradient-like background */}
        <View style={styles.heroSection}>
          <View style={styles.heroOverlay}>
            <Image
              source={{ uri: 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&fit=crop' }}
              style={styles.heroImage}
              resizeMode="cover"
            />
            <View style={styles.heroGradient} />
          </View>
          <View style={styles.heroContent}>
            <Text style={styles.logoEmoji}>🛒</Text>
            <Text style={styles.brandName}>FreshMart</Text>
            <Text style={styles.tagline}>Fresh groceries delivered to your door</Text>
          </View>
        </View>

        {/* Floating feature pills */}
        <View style={styles.featurePills}>
          <View style={styles.pill}>
            <Text style={styles.pillEmoji}>🥬</Text>
            <Text style={styles.pillText}>Fresh Veggies</Text>
          </View>
          <View style={styles.pill}>
            <Text style={styles.pillEmoji}>🥛</Text>
            <Text style={styles.pillText}>Dairy</Text>
          </View>
          <View style={styles.pill}>
            <Text style={styles.pillEmoji}>🍖</Text>
            <Text style={styles.pillText}>Halal Meat</Text>
          </View>
          <View style={styles.pill}>
            <Text style={styles.pillEmoji}>🫘</Text>
            <Text style={styles.pillText}>Spices</Text>
          </View>
        </View>

        {/* Login/Register card */}
        <View style={styles.formCard}>
          {!otpStep ? (
            <>
              <Text style={styles.formTitle}>
                {isLogin ? 'Welcome Back! 👋' : 'Create Account 🎉'}
              </Text>
              <Text style={styles.formSubtitle}>
                {isLogin ? 'Sign in to continue shopping' : 'Join us for the freshest deals'}
              </Text>

              {!isLogin && (
                <View style={styles.inputContainer}>
                  <Text style={styles.inputIcon}>👤</Text>
                  <TextInput
                    style={styles.input}
                    placeholder="Full Name"
                    placeholderTextColor="#aaa"
                    value={name}
                    onChangeText={setName}
                  />
                </View>
              )}
              <View style={styles.inputContainer}>
                <Text style={styles.inputIcon}>📧</Text>
                <TextInput
                  style={styles.input}
                  placeholder="Email Address"
                  placeholderTextColor="#aaa"
                  value={email}
                  onChangeText={setEmail}
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
              </View>
              <View style={styles.inputContainer}>
                <Text style={styles.inputIcon}>🔒</Text>
                <TextInput
                  style={styles.input}
                  placeholder="Password"
                  placeholderTextColor="#aaa"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry
                />
              </View>

              <TouchableOpacity
                style={[styles.submitBtn, loading && styles.submitBtnDisabled]}
                onPress={handleSubmit}
                activeOpacity={0.8}
                disabled={loading}
              >
                <Text style={styles.submitBtnText}>
                  {loading ? '⏳ Please wait...' : (isLogin ? '🛒 Sign In & Start Shopping' : '📧 Send Verification Code')}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.switchBtn}
                onPress={handleSwitchMode}
                activeOpacity={0.7}
              >
                <Text style={styles.switchText}>
                  {isLogin ? "Don't have an account? " : 'Already have an account? '}
                  <Text style={styles.switchTextBold}>
                    {isLogin ? 'Register' : 'Login'}
                  </Text>
                </Text>
              </TouchableOpacity>
            </>
          ) : (
            <>
              {/* OTP Verification Step */}
              <Text style={styles.formTitle}>Verify Email 📬</Text>
              <Text style={styles.formSubtitle}>
                Enter the 6-digit code sent to
              </Text>
              <Text style={styles.otpEmail}>{email}</Text>

              <View style={styles.otpInputContainer}>
                <Text style={styles.inputIcon}>🔑</Text>
                <TextInput
                  style={styles.otpInput}
                  placeholder="Enter 6-digit code"
                  placeholderTextColor="#aaa"
                  value={otp}
                  onChangeText={(text) => setOtp(text.replace(/[^0-9]/g, '').slice(0, 6))}
                  keyboardType="number-pad"
                  maxLength={6}
                  autoFocus
                />
              </View>

              <TouchableOpacity
                style={[styles.submitBtn, loading && styles.submitBtnDisabled]}
                onPress={handleVerifyOtp}
                activeOpacity={0.8}
                disabled={loading}
              >
                <Text style={styles.submitBtnText}>
                  {loading ? '⏳ Verifying...' : '✅ Verify & Create Account'}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.resendBtn, otpTimer > 0 && styles.resendBtnDisabled]}
                onPress={handleResendOtp}
                activeOpacity={0.7}
                disabled={otpTimer > 0}
              >
                <Text style={[styles.resendText, otpTimer > 0 && styles.resendTextDisabled]}>
                  {otpTimer > 0 ? `Resend code in ${otpTimer}s` : '🔄 Resend Code'}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.switchBtn}
                onPress={() => { setOtpStep(false); setOtp(''); }}
                activeOpacity={0.7}
              >
                <Text style={styles.switchText}>
                  ← <Text style={styles.switchTextBold}>Go Back</Text>
                </Text>
              </TouchableOpacity>
            </>
          )}
        </View>

        {/* Bottom trust badges */}
        <View style={styles.trustSection}>
          <View style={styles.trustItem}>
            <Text style={styles.trustEmoji}>🚚</Text>
            <Text style={styles.trustText}>Fast Delivery</Text>
          </View>
          <View style={styles.trustItem}>
            <Text style={styles.trustEmoji}>💵</Text>
            <Text style={styles.trustText}>Cash on Delivery</Text>
          </View>
          <View style={styles.trustItem}>
            <Text style={styles.trustEmoji}>✅</Text>
            <Text style={styles.trustText}>100% Fresh</Text>
          </View>
        </View>

        <Text style={styles.footer}>🇵🇰 Proudly serving Pakistan</Text>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f0f7f0' },
  scrollContent: { flexGrow: 1 },

  // Hero section
  heroSection: {
    height: 260,
    position: 'relative',
    overflow: 'hidden',
  },
  heroOverlay: {
    ...StyleSheet.absoluteFillObject,
  },
  heroImage: {
    width: '100%',
    height: '100%',
  },
  heroGradient: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(39, 174, 96, 0.65)',
  },
  heroContent: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 30,
  },
  logoEmoji: {
    fontSize: 56,
    marginBottom: 4,
  },
  brandName: {
    fontSize: 38,
    fontWeight: 'bold',
    color: '#fff',
    letterSpacing: 1,
    textShadowColor: 'rgba(0,0,0,0.3)',
    textShadowOffset: { width: 0, height: 2 },
    textShadowRadius: 4,
  },
  tagline: {
    fontSize: 15,
    color: 'rgba(255,255,255,0.9)',
    marginTop: 6,
    fontWeight: '500',
  },

  // Feature pills
  featurePills: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'wrap',
    marginTop: -20,
    marginHorizontal: 16,
    gap: 8,
  },
  pill: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 3,
  },
  pillEmoji: { fontSize: 16, marginRight: 5 },
  pillText: { fontSize: 12, color: '#27ae60', fontWeight: '600' },

  // Form card
  formCard: {
    backgroundColor: '#fff',
    marginHorizontal: 20,
    marginTop: 24,
    borderRadius: 20,
    padding: 24,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 4 },
    elevation: 5,
  },
  formTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'center',
    marginBottom: 4,
  },
  formSubtitle: {
    fontSize: 14,
    color: '#888',
    textAlign: 'center',
    marginBottom: 24,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8faf8',
    borderWidth: 1.5,
    borderColor: '#e0e8e0',
    borderRadius: 12,
    marginBottom: 14,
    paddingHorizontal: 14,
  },
  inputIcon: {
    fontSize: 18,
    marginRight: 10,
  },
  input: {
    flex: 1,
    paddingVertical: 14,
    fontSize: 16,
    color: '#333',
  },
  submitBtn: {
    backgroundColor: '#27ae60',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 8,
    shadowColor: '#27ae60',
    shadowOpacity: 0.3,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 4 },
    elevation: 4,
  },
  submitBtnDisabled: {
    opacity: 0.6,
  },
  submitBtnText: {
    color: '#fff',
    fontSize: 17,
    fontWeight: 'bold',
  },
  switchBtn: {
    marginTop: 18,
    alignItems: 'center',
    padding: 8,
  },
  switchText: {
    fontSize: 14,
    color: '#888',
  },
  switchTextBold: {
    color: '#27ae60',
    fontWeight: 'bold',
  },

  // OTP styles
  otpEmail: {
    fontSize: 14,
    color: '#27ae60',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  otpInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8faf8',
    borderWidth: 2,
    borderColor: '#27ae60',
    borderRadius: 12,
    marginBottom: 14,
    paddingHorizontal: 14,
  },
  otpInput: {
    flex: 1,
    paddingVertical: 16,
    fontSize: 24,
    color: '#333',
    textAlign: 'center',
    letterSpacing: 8,
    fontWeight: 'bold',
  },
  resendBtn: {
    marginTop: 12,
    alignItems: 'center',
    padding: 10,
    backgroundColor: '#f0f7f0',
    borderRadius: 10,
  },
  resendBtnDisabled: {
    backgroundColor: '#f5f5f5',
  },
  resendText: {
    fontSize: 14,
    color: '#27ae60',
    fontWeight: '600',
  },
  resendTextDisabled: {
    color: '#aaa',
  },

  // Trust badges
  trustSection: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginHorizontal: 20,
    marginTop: 28,
    marginBottom: 8,
  },
  trustItem: {
    alignItems: 'center',
  },
  trustEmoji: {
    fontSize: 28,
    marginBottom: 4,
  },
  trustText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '500',
  },

  // Footer
  footer: {
    textAlign: 'center',
    color: '#aaa',
    fontSize: 13,
    marginTop: 16,
    marginBottom: 30,
  },
});
