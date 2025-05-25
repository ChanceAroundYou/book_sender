import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import type { ApiError } from '@/types';

// API Error response interface from backend (if known, otherwise use any)
interface BackendErrorResponse {
    detail?: string; // Assuming backend error has a detail field
    message?: string; // Also check for message as a fallback
    [key: string]: any;
}

// Create axios instance
const apiClient: AxiosInstance = axios.create({
    baseURL: 'http://192.168.1.6:25688/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error: AxiosError) => {
        return Promise.reject(error);
    }
);

// Response interceptor
apiClient.interceptors.response.use(
    (response: AxiosResponse) => {
        return response.data;
    },
    (error: AxiosError<BackendErrorResponse>) => {
        let errorMessage = 'An unexpected error occurred';
        if (error.response && error.response.data) {
            errorMessage = error.response.data.detail || error.response.data.message || error.message;
        } else if (error.request) {
            errorMessage = 'No response received from server.';
        } else {
            errorMessage = error.message;
        }

        const apiError: ApiError = {
            detail: errorMessage,
        };
        return Promise.reject(apiError);
    }
);

// Generic request function
export async function request<T>(config: AxiosRequestConfig): Promise<T> {
    try {
        return await apiClient(config);
    } catch (error) {
        throw error;
    }
}

export default apiClient; 