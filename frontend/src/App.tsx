import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';

// Layouts
import MainLayout from '@/layouts/MainLayout';
import AuthLayout from '@/layouts/AuthLayout';

// Guards
import ProtectedRoute from '@/guards/ProtectedRoute';

// Pages
import Register from '@/pages/Auth/Register';
import ForgotPassword from '@/pages/Auth/ForgotPassword';

// 懒加载路由组件
const HomePage = React.lazy(() => import('./pages/Home'));
const BooksPage = React.lazy(() => import('./pages/Books/BookList'));
const BookDetailPage = React.lazy(() => import('./pages/Books/BookDetail'));
const UserLibraryPage = React.lazy(() => import('./pages/User/Library'));
const UserProfilePage = React.lazy(() => import('./pages/User/Profile'));
const LoginPage = React.lazy(() => import('./pages/Auth/Login'));

function App() {
    return (
        <ConfigProvider locale={zhCN}>
            <BrowserRouter>
                <Routes>
                    {/* Auth Routes */}
                    <Route path="/auth" element={<AuthLayout />}>
                        <Route path="login" element={<LoginPage />} />
                        <Route path="register" element={<Register />} />
                        <Route path="forgot-password" element={<ForgotPassword />} />
                    </Route>

                    <Route element={<MainLayout />}>
                        <Route path="/" element={<HomePage />} />
                        <Route element={<ProtectedRoute />}>
                            <Route path="/books" element={<BooksPage />} />
                            <Route path="/books/:id" element={<BookDetailPage />} />
                            <Route path="/user/profile" element={<UserProfilePage />} />
                            <Route path="/user/library" element={<UserLibraryPage />} />
                        </Route>
                    </Route>

                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </BrowserRouter>
        </ConfigProvider>
    );
}

export default App; 