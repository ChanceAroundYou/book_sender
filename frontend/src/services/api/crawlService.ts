import apiClient from './client';
import type {
    CrawlBooksParams,
    CrawlBookParams,
    ServiceResponseMessageOrError,
} from '@/types';

export const crawlService = {
    async crawlBooks(params?: CrawlBooksParams): Promise<ServiceResponseMessageOrError> {
        const { series, page } = params || {};
        let url = '/crawl/books';
        if (series) {
            url += `/${encodeURIComponent(series)}`;
        }
        // Ensure apiClient.post can handle query params correctly if page is defined
        // For POST, query params are usually in the config.params, data is the body (null here)
        return apiClient.post(url, null, { params: page !== undefined ? { page } : undefined });
    },

    async crawlBook(params?: CrawlBookParams): Promise<ServiceResponseMessageOrError> {
        const { series, ...queryParams } = params || {};
        let url = '/crawl/book';
        if (series) {
            url += `/${encodeURIComponent(series)}`;
        }
        // Send other BookQueryParams as query parameters
        return apiClient.post(url, null, { params: queryParams });
    },
}; 