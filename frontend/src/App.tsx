import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, Spin } from 'antd';
import zhCN from 'antd/locale/zh_CN';

// Layouts
import MainLayout from '@/layouts/MainLayout';
// import AdminLayout from '@/layouts/AdminLayout';
import AuthLayout from '@/layouts/AuthLayout';

// Guards
import ProtectedRoute from '@/guards/ProtectedRoute';

// Pages
import Register from '@/pages/Auth/Register';
import ForgotPassword from '@/pages/Auth/ForgotPassword';
// import AdminDashboard from '@/pages/Admin/Dashboard';
// import AdminBooks from '@/pages/Admin/Books';
// import AdminUsers from '@/pages/Admin/Users';
// import AdminSettings from '@/pages/Admin/Settings';

// 懒加载路由组件
const HomePage = React.lazy(() => import('./pages/Home'));
const BooksPage = React.lazy(() => import('./pages/Books/BookList'));
const BookDetailPage = React.lazy(() => import('./pages/Books/BookDetail'));
const UserLibraryPage = React.lazy(() => import('./pages/User/Library'));
const UserProfilePage = React.lazy(() => import('./pages/User/Profile'));
const LoginPage = React.lazy(() => import('./pages/Auth/Login'));

// 加载中组件
const LoadingComponent = () => (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin size="large" />
    </div>
);

function App() {
    return (
        <ConfigProvider locale={zhCN}>
            <BrowserRouter>
                <Suspense fallback={<LoadingComponent />}>
                    <Routes>
                        {/* Auth Routes */}
                        <Route path="/auth" element={<AuthLayout />}>
                            <Route path="login" element={<LoginPage />} />
                            <Route path="register" element={<Register />} />
                            <Route path="forgot-password" element={<ForgotPassword />} />
                        </Route>

                        {/* Admin Routes - Protected */}
                        {/* <Route element={<ProtectedRoute />}>
                            <Route path="/admin" element={<AdminLayout />}>
                                <Route path="dashboard" element={<AdminDashboard />} />
                                <Route path="books" element={<AdminBooks />} />
                                <Route path="users" element={<AdminUsers />} />
                                <Route path="settings" element={<AdminSettings />} />
                            </Route>
                        </Route> */}

                        {/* Main Routes - Protected */}
                        <Route element={<MainLayout />}>
                            <Route path="/" element={<HomePage />} />
                            <Route element={<ProtectedRoute />}>
                                <Route path="/books" element={<BooksPage />} />
                                <Route path="/books/:id" element={<BookDetailPage />} />
                                <Route path="/user/profile" element={<UserProfilePage />} />
                                <Route path="/user/library" element={<UserLibraryPage />} />
                            </Route>
                        </Route>

                        {/* Catch all route - redirect to home */}
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </Suspense>
            </BrowserRouter>
        </ConfigProvider>
    );
}

export default App; 