import apiClient from './client';

interface StatsResponse {
    total: number;
}

/**
 * Constructs the URL for the backend image proxy service.
 * @param originalUrl The original URL of the image to be proxied.
 * @returns The full URL to use for the proxied image, or a placeholder if originalUrl is invalid.
 */
const getProxiedImageUrl = (originalUrl: string | null | undefined): string => {
    if (!originalUrl) {
        return ''; // Fallback if original URL is missing
    }

    // apiClient.defaults.baseURL is 'http://192.168.1.6:25688/api/v1'
    // The image proxy endpoint is '/image-proxy' relative to this base URL.
    // So, the full path is apiClient.defaults.baseURL + '/image-proxy'
    // Ensure no double slashes if baseURL might have a trailing one (it usually doesn't for Axios defaults.baseURL)

    // const baseApiUrl = apiClient.defaults.baseURL || '';
    // const proxyPath = 'image-proxy'; // Relative to the API base URL

    // Constructing the URL carefully to avoid double slashes
    // const fullProxyUrl = `${baseApiUrl.replace(/\/$/, '')}/${proxyPath}?url=${encodeURIComponent(originalUrl)}`;

    // return fullProxyUrl;
    return originalUrl
};

export const utilService = {
    getProxiedImageUrl,

    async getTotalBooks(): Promise<number> {
        // apiClient.get already returns response.data due to our interceptor
        const stats: StatsResponse = await apiClient.get('/utils/stats/total-books');
        return stats.total;
    },

    async getTotalUsers(): Promise<number> {
        // apiClient.get already returns response.data due to our interceptor
        const stats: StatsResponse = await apiClient.get('/utils/stats/total-users');
        return stats.total;
    },
}; 