import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';

// Layouts
import MainLayout from '@/layouts/MainLayout';
import AuthLayout from '@/layouts/AuthLayout';
// Admin Layout (assuming it's in pages/Admin as per previous steps)
const AdminLayout = React.lazy(() => import('@/pages/Admin/AdminLayout'));

// Guards
import ProtectedRoute from '@/guards/ProtectedRoute';

// Pages
const LoginPage = React.lazy(() => import('@/pages/Auth/Login'));
const RegisterPage = React.lazy(() => import('@/pages/Auth/Register'));
const ForgotPasswordPage = React.lazy(() => import('@/pages/Auth/ForgotPassword'));

const HomePage = React.lazy(() => import('@/pages/Home'));
const BooksPage = React.lazy(() => import('@/pages/Books/BookList'));
const BookDetailPage = React.lazy(() => import('@/pages/Books/BookDetail'));
const UserLibraryPage = React.lazy(() => import('@/pages/User/Library'));
const UserProfilePage = React.lazy(() => import('@/pages/User/Profile'));

const AdminDashboard = React.lazy(() => import('@/pages/Admin/AdminDashboard'));
const ManageUsers = React.lazy(() => import('@/pages/Admin/ManageUsers'));
const ManageBooks = React.lazy(() => import('@/pages/Admin/ManageBooks'));
const ManageSubscriptions = React.lazy(() => import('@/pages/Admin/ManageSubscriptions'));


function App() {
    return (
        <ConfigProvider locale={zhCN}>
            <BrowserRouter>
                    <Routes>
                        {/* Auth Routes */}
                        <Route path="/auth" element={<AuthLayout />}>
                            <Route path="login" element={<LoginPage />} />
                            <Route path="register" element={<RegisterPage />} />
                            <Route path="forgot-password" element={<ForgotPasswordPage />} />
                            <Route index element={<Navigate to="login" replace />} />
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

                        <Route element={<ProtectedRoute />}>
                            <Route path="/admin" element={<AdminLayout />}>
                                <Route index element={<AdminDashboard />} />
                                <Route path="users" element={<ManageUsers />} />
                                <Route path="books" element={<ManageBooks />} />
                                <Route path="subscriptions" element={<ManageSubscriptions />} />
                            </Route>
                        </Route>

                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
            </BrowserRouter>
        </ConfigProvider>
    );
}

export default App; 