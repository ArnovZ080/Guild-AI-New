/**
 * Guild-AI - Auth Context
 *
 * Wraps Firebase auth state and provides:
 *  - user / loading / error state
 *  - login / signup / loginWithGoogle / logout actions
 *  - getToken() for the API client
 *  - identityComplete flag (business identity completion)
 */
import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import {
  auth,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  GoogleAuthProvider,
  signInWithPopup,
} from '../services/firebase';
import { setTokenGetter, api } from '../services/api';
import { guildWS } from '../services/websocket';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [dbUser, setDbUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [identityComplete, setIdentityComplete] = useState(null); // null = unknown
  const [isAdmin, setIsAdmin] = useState(false);

  /* ── Get Firebase ID token ── */
  const getToken = useCallback(async () => {
    if (!auth?.currentUser) return null;
    return auth.currentUser.getIdToken();
  }, []);

  /* ── Wire token getter into API client ── */
  useEffect(() => {
    setTokenGetter(getToken);
  }, [getToken]);

  /* ── Listen to Firebase auth state ── */
  useEffect(() => {
    if (!auth) {
      setLoading(false);
      return;
    }
    const unsub = onAuthStateChanged(auth, async (fbUser) => {
      setUser(fbUser);
      if (fbUser) {
        // Connect WebSocket
        guildWS.connect(fbUser.uid);
        // Register with backend if first time, check identity
        try {
          const userRes = await api.auth.verify();
          setDbUser(userRes);
          setIsAdmin(userRes?.is_admin || false);
          const status = await api.onboarding.status();
          setIdentityComplete(status?.completion_percentage >= 50);
        } catch {
          setDbUser(null);
          setIdentityComplete(false);
          setIsAdmin(false);
        }
      } else {
        guildWS.disconnect();
        setIdentityComplete(null);
        setIsAdmin(false);
      }
      setLoading(false);
    });
    return unsub;
  }, []);

  /* ── Actions ── */
  const login = useCallback(async (email, password) => {
    return signInWithEmailAndPassword(auth, email, password);
  }, []);

  const signup = useCallback(async (email, password) => {
    const cred = await createUserWithEmailAndPassword(auth, email, password);
    // Register with backend
    try {
      const token = await cred.user.getIdToken();
      await api.auth.register({ email, firebase_token: token });
    } catch { /* backend may already know this user */ }
    return cred;
  }, []);

  const loginWithGoogle = useCallback(async () => {
    const provider = new GoogleAuthProvider();
    const cred = await signInWithPopup(auth, provider);
    try {
      const token = await cred.user.getIdToken();
      await api.auth.register({ email: cred.user.email, firebase_token: token });
    } catch { /* ok */ }
    return cred;
  }, []);

  const logout = useCallback(async () => {
    guildWS.disconnect();
    await signOut(auth);
  }, []);

  const value = {
    user,
    dbUser,
    loading,
    identityComplete,
    setIdentityComplete,
    isAdmin,
    login,
    signup,
    loginWithGoogle,
    logout,
    getToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
