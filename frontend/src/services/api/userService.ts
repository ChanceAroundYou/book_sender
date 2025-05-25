import apiClient from './client';
import type {
    User,
    UserListQueryParams,
    GetUserDetailParams,
    CreateUserParams,
    UpdateUserParams,
    UserSubscriptionParams,
} from '@/types';

export const userService = {
    async getUsers(params?: UserListQueryParams): Promise<Array<User>> {
        return apiClient.get('/users', { params });
    },

    async getUserById(params: GetUserDetailParams): Promise<User> {
        return apiClient.get('/users', { params }); // user_id is passed as a query param
    },

    async createUser(params: CreateUserParams): Promise<User> {
        // Backend expects these as query parameters, not in the body, as per api.md and backend code structure
        return apiClient.post('/users', null, { params });
    },

    async updateUser(params: UpdateUserParams): Promise<User> {
        // Backend expects these as query parameters
        const { user_id, ...queryParams } = params;
        return apiClient.put('/users', null, { params: { user_id, ...queryParams } });
    },

    async deleteUser(params: { user_id: number }): Promise<{ message: string }> {
        return apiClient.delete('/users', { params });
    },

    async addUserSubscription(params: UserSubscriptionParams): Promise<User> {
        // Backend expects these as query parameters
        return apiClient.put('/users/subscriptions', null, { params });
    },

    async deleteUserSubscription(params: { user_id: number; series: string }): Promise<User> {
        // Backend expects these as query parameters
        return apiClient.delete('/users/subscriptions', { params });
    },
}; 