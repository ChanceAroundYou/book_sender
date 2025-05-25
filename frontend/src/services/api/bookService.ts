import apiClient from './client';
import type {
    Book,
    BookQueryParams,
    CreateBookPayload,
    UpdateBookQueryParams,
} from '@/types';

export const bookService = {
    async getBooks(params?: BookQueryParams): Promise<Array<Book>> {
        return apiClient.get('/books', { params });
    },

    async getSeriesBooks(series: string, params?: Omit<BookQueryParams, 'series'>): Promise<Array<Book>> {
        return apiClient.get('/books/series', { params: { ...params, series } });
    },

    async getLatestBooks(params?: Partial<BookQueryParams>): Promise<Array<Book>> {
        return apiClient.get('/books/all', { params });
    },

    async getBook(params: Partial<BookQueryParams>): Promise<Book> {
        return apiClient.get('/book', { params });
    },

    async createBook(payload: CreateBookPayload): Promise<Book> {
        return apiClient.post('/book', payload);
    },

    async updateBook(params: UpdateBookQueryParams): Promise<Book> {
        // Destructure id from params, send rest as query parameters
        const { id, ...queryParams } = params;
        return apiClient.put(`/book?id=${id}`, null, { params: queryParams }); // Backend expects ID in query, and other params in query too
    },

    async deleteBook(params: Partial<BookQueryParams>): Promise<{ message: string }> {
        return apiClient.delete('/book', { params });
    },
}; 