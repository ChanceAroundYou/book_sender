import { Outlet } from 'react-router-dom';
import { Layout, Spin } from 'antd';
import { Suspense } from 'react';

const { Content } = Layout;

const AuthLayout = () => {
    return (
        <Layout className="min-h-screen bg-gray-50">
            <div className="text-center mb-8 fixed top-0 left-0 right-0 bg-white py-4">
                <h1 className="text-2xl font-bold mb-2">Book Sender</h1>
                <p className="text-gray-600">您的个人图书馆</p>
            </div>
            <Content className="flex items-center justify-center p-4 mt-24">
                <div className="w-full max-w-md">
                    <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-md">
                        <Suspense fallback={
                            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
                                <Spin size="large" />
                            </div>
                        }>
                            <Outlet />
                        </Suspense>
                    </div>
                </div>
            </Content>
        </Layout>
    );
};

export default AuthLayout;