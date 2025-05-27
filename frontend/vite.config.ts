import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { visualizer } from 'rollup-plugin-visualizer';
import { compression } from 'vite-plugin-compression2';

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => ({
    plugins: [
        react(),
        // Gzip 压缩
        compression({
            algorithm: 'gzip',
            exclude: [/\.(br)$/, /\.(gz)$/],
            deleteOriginalAssets: false,
        }),
        // Brotli 压缩
        compression({
            algorithm: 'brotliCompress',
            exclude: [/\.(br)$/, /\.(gz)$/],
            deleteOriginalAssets: false,
        }),
        // 构建分析
        mode !== 'production' && visualizer({
            open: false,
            gzipSize: true,
            brotliSize: true,
        }),
    ],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    server: {
        port: 3000,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
        },
    },
    build: {
        // 启用 CSS 代码分割
        cssCodeSplit: true,
        // 启用源码映射
        sourcemap: false,
        // 自定义构建选项
        rollupOptions: {
            output: {
                // 分块策略
                manualChunks: {
                    'react-vendor': ['react', 'react-dom', 'react-router-dom'],
                    'antd-vendor': ['antd'],
                    'redux-vendor': ['@reduxjs/toolkit', 'react-redux'],
                },
                // 自定义 chunk 文件名格式
                chunkFileNames: 'assets/js/[name]-[hash].js',
                entryFileNames: 'assets/js/[name]-[hash].js',
                assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
            },
        },
        // 启用压缩
        minify: 'terser',
        terserOptions: {
            compress: {
                // 生产环境时移除 console
                drop_console: true,
                drop_debugger: true,
            },
        },
        // 设置块大小警告的限制
        chunkSizeWarningLimit: 1000,
    },
})); 