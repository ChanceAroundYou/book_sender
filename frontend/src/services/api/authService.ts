import apiClient from './client';
import type { User, LoginParams, RegisterParams } from '@/types';

// Define expected response types for clarity, though apiClient should return data directly.
interface LoginResponse {
    access_token: string;
    token_type: "bearer";
}

export const authService = {
    async login(params: LoginParams): Promise<LoginResponse> {
        // Casting because the interceptor modifies runtime behavior to return data directly,
        // but TypeScript's static analysis of AxiosInstance doesn't see this.
        return apiClient.post<LoginResponse>('/login', params) as unknown as LoginResponse;
    },

    async register(params: RegisterParams): Promise<User> {
        return apiClient.post<User>('/register', params) as unknown as User;
    },

    async getCurrentUser(): Promise<User> {
        return apiClient.get<User>('/me') as unknown as User;
    },

    async forgotPassword(email: string): Promise<{ message: string }> {
        return apiClient.post<{ message: string }>('/forgot-password', { email }) as unknown as { message: string };
    }
};

export default authService; 