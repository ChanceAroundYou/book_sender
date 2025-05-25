import apiClient from './client';
import type {
    BookQueryParams,
    ServiceResponseMessageOrError,
} from '@/types';

export const downloadService = {
    async downloadBooks(params?: Partial<BookQueryParams>): Promise<ServiceResponseMessageOrError> {
        return apiClient.post('/download/books', null, { params });
    },

    async downloadBook(params: Partial<BookQueryParams>): Promise<ServiceResponseMessageOrError> {
        return apiClient.post('/download/book', null, { params });
    },
}; 