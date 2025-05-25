import apiClient from './client';
import type {
    DistributeBooksParams,
    DistributeBookParams,
    ServiceResponseMessageOrError,
    DistributeSeriesParams,
} from '@/types';

export const distributeService = {
    async distributeBooks(params: DistributeBooksParams): Promise<ServiceResponseMessageOrError> {
        // email is part of params and will be sent as a query parameter
        return apiClient.post('/distribute/books', null, { params });
    },

    async distributeBook(params: DistributeBookParams): Promise<ServiceResponseMessageOrError> {
        // email is part of params and will be sent as a query parameter
        return apiClient.post('/distribute/book', null, { params });
    },

    // New service function for distributing a series
    async distributeSeries(params: DistributeSeriesParams): Promise<ServiceResponseMessageOrError> {
        // Assuming backend endpoint is /distribute/series
        // Ensure parameters (series, email) are sent as expected by the backend (query or body)
        // For this example, sending as query params similar to other distribute functions.
        return apiClient.post('/distribute/series', null, { params });
    },
}; 