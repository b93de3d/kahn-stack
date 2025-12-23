import { goto } from "$app/navigation";
import { env } from "$env/dynamic/public";
import type { User } from "$lib/api";
import apiClient from "$lib/apiClient";

export type Creds = { email: string; password: string };

export type AuthResponse = {
  data: { user: User };
  meta: { is_authenticated: boolean };
};

let user = $state<User | null>(null);

const signup = async (creds: Creds) => {
  const res = await apiClient.post(
    `${env.PUBLIC_API_URL}/_allauth/browser/v1/auth/signup`,
    creds
  );
  if (res.ok) {
    const data = res.data as AuthResponse;
    user = data.data.user;
    goto("/");
  }
  return res;
};

const requestPasswordReset = async (data: { email: string }) => {
  const res = await apiClient.post(
    `${env.PUBLIC_API_URL}/_allauth/browser/v1/auth/password/request`,
    data
  );
  if (res.ok) {
  }
  return res;
};

const resetPassword = async (data: { key: string; password: string }) => {
  const res = await apiClient.post(
    `${env.PUBLIC_API_URL}/_allauth/browser/v1/auth/password/reset`,
    data
  );
  if (res.ok) {
    const data = res.data as AuthResponse;
    user = data.data.user;
    goto("/");
  }
  return res;
};

const login = async (creds: Creds) => {
  const res = await apiClient.post(
    `${env.PUBLIC_API_URL}/_allauth/browser/v1/auth/login`,
    creds
  );
  if (res.ok) {
    const data = res.data as AuthResponse;
    if (data.meta.is_authenticated) {
      user = data.data.user;
    }
  }
  return res;
};

const logout = async () => {
  await apiClient.delete(
    `${env.PUBLIC_API_URL}/_allauth/browser/v1/auth/session`
  );
  user = null;
};

const getSession = async () => {
  try {
    const res = await apiClient.get(
      `${env.PUBLIC_API_URL}/_allauth/browser/v1/auth/session`
    );
    if (res.ok) {
      const data = res.data as AuthResponse;
      user = data.data.user;
      return true;
    }
    return false;
  } catch (e) {
    console.log("GET SESSION ERROR", e);
    return false;
  }
};

export const userStore = {
  get user() {
    return user as User;
  },
  signup,
  login,
  logout,
  getSession,
  requestPasswordReset,
  resetPassword,
};
