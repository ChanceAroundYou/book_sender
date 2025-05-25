import apiClient from './client';
import type {
    Task,
    TaskQueryParams,
} from '@/types';

export const taskService = {
    async getTasks(params?: TaskQueryParams): Promise<Array<Task>> {
        return apiClient.get('/tasks', { params });
    },

    async getTask(taskId: string): Promise<Task> {
        return apiClient.get(`/tasks/${taskId}`);
    },

    async deleteTask(taskId: string): Promise<{ message: string }> {
        return apiClient.delete(`/tasks/${taskId}`);
    },

    async getTaskStatusSummary(): Promise<Record<Task['status'], number | undefined>> {
        return apiClient.get('/tasks/status/summary');
    },
}; 