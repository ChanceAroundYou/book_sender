import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';

// Layouts
import MainLayout from '@/layouts/MainLayout';
import AdminLayout from '@/layouts/AdminLayout';
import AuthLayout from '@/layouts/AuthLayout';

// Guards
import ProtectedRoute from '@/guards/ProtectedRoute';

// Pages
import Home from '@/pages/Home';
import BookList from '@/pages/Books/BookList';
import BookDetail from '@/pages/Books/BookDetail';
import Login from '@/pages/Auth/Login';
import Register from '@/pages/Auth/Register';
import ForgotPassword from '@/pages/Auth/ForgotPassword';
import UserProfile from '@/pages/User/Profile';
import UserLibrary from '@/pages/User/Library';
import AdminDashboard from '@/pages/Admin/Dashboard';
import AdminBooks from '@/pages/Admin/Books';
import AdminUsers from '@/pages/Admin/Users';
import AdminSettings from '@/pages/Admin/Settings';
function App() {
    return (
        <ConfigProvider locale={zhCN}>
            <Router>
                <Routes>
                    {/* Auth Routes */}
                    <Route path="/auth" element={<AuthLayout />}>
                        <Route path="login" element={<Login />} />
                        <Route path="register" element={<Register />} />
                        <Route path="forgot-password" element={<ForgotPassword />} />
                    </Route>

                    {/* Admin Routes - Protected */}
                    <Route element={<ProtectedRoute />}>
                        <Route path="/admin" element={<AdminLayout />}>
                            <Route path="dashboard" element={<AdminDashboard />} />
                            <Route path="books" element={<AdminBooks />} />
                            <Route path="users" element={<AdminUsers />} />
                            <Route path="settings" element={<AdminSettings />} />
                        </Route>
                    </Route>

                    {/* Main Routes - Protected */}
                    <Route element={<MainLayout />}>
                        <Route path="/" element={<Home />} />
                        <Route element={<ProtectedRoute />}>
                            <Route path="/books" element={<BookList />} />
                            <Route path="/books/:id" element={<BookDetail />} />
                            <Route path="/user/profile" element={<UserProfile />} />
                            <Route path="/user/library" element={<UserLibrary />} />
                        </Route>
                    </Route>

                    {/* Catch all route - redirect to home */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </Router>
        </ConfigProvider>
    );
}

export default App; 