import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAppSelector, RootState } from '@/store'; // Import Redux hooks and RootState

// This is a placeholder for your actual authentication hook/logic
// Replace this with your actual implementation
const useAuth = () => {
    const token = useAppSelector((state: RootState) => state.auth.token); // Get token from Redux store
    const isAuthenticated = !!token; // Check if token exists
    return { isAuthenticated };
};

const ProtectedRoute: React.FC = () => {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return <Navigate to="/auth/login" replace />;
    }

    return <Outlet />;
};

export default ProtectedRoute; 