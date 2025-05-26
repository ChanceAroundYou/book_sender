import { Outlet } from 'react-router-dom';
import { Layout, Spin } from 'antd';
import Navbar from '@/components/Navbar';
import { Suspense } from 'react';

const { Header, Content, Footer } = Layout;

const MainLayout = () => {
    return (
        <Layout className="min-h-screen">
            <Header className="bg-black border-b border-gray-200 px-4 fixed w-full z-10 text-white">
                <Navbar />
            </Header>
            <Content className="mt-16 p-6">
                <div className="container mx-auto">
                    <Suspense fallback={
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 'calc(100vh - 128px)' }}>
                            <Spin size="large" />
                        </div>
                    }>
                        <Outlet />
                    </Suspense>
                </div>
            </Content>
            <Footer className="text-center bg-white border-t border-gray-200">
                Book Sender ©{new Date().getFullYear()} Created with ❤️ by 粘粘宝
            </Footer>
        </Layout>
    );
};

export default MainLayout; 