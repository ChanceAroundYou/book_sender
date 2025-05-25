export const config = {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
    isDevelopment: import.meta.env.DEV,
    isProduction: import.meta.env.PROD,
} as const;

// 用于类型检查的辅助函数
export function assertConfig() {
    if (!config.apiBaseUrl) {
        throw new Error('VITE_API_BASE_URL is not defined in environment variables');
    }
}

// 在应用启动时调用此函数以确保所有必要的配置都存在
export function validateConfig() {
    try {
        assertConfig();
        console.log('Configuration validated successfully');
    } catch (error) {
        console.error('Configuration validation failed:', error);
        throw error;
    }
} 