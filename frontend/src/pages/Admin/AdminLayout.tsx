import React from 'react';
import { Layout, Menu } from 'antd';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { BookOutlined, UserOutlined, SolutionOutlined, DashboardOutlined } from '@ant-design/icons';

const { Sider, Content } = Layout;

const AdminLayout: React.FC = () => {
    const location = useLocation();

    const getSelectedKeys = () => {
        const path = location.pathname;
        if (path.startsWith('/admin/users')) return ['users'];
        if (path.startsWith('/admin/books')) return ['books'];
        if (path.startsWith('/admin/subscriptions')) return ['subscriptions'];
        if (path.startsWith('/admin')) return ['dashboard'];
        return ['dashboard'];
    };

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Sider width={220} theme="dark">
                <div style={{ height: '32px', margin: '16px', background: 'rgba(255, 255, 255, 0.2)', textAlign: 'center', lineHeight: '32px', color: 'white' }}>
                    Admin Panel
                </div>
                <Menu theme="dark" mode="inline" selectedKeys={getSelectedKeys()}>
                    <Menu.Item key="dashboard" icon={<DashboardOutlined />}>
                        <Link to="/admin">Dashboard</Link>
                    </Menu.Item>
                    <Menu.Item key="users" icon={<UserOutlined />}>
                        <Link to="/admin/users">Manage Users</Link>
                    </Menu.Item>
                    <Menu.Item key="books" icon={<BookOutlined />}>
                        <Link to="/admin/books">Manage Books</Link>
                    </Menu.Item>
                    <Menu.Item key="subscriptions" icon={<SolutionOutlined />}>
                        <Link to="/admin/subscriptions">Manage Subscriptions</Link>
                    </Menu.Item>
                </Menu>
            </Sider>
            <Layout>
                <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
                    <div style={{ padding: 24, background: '#fff', minHeight: 'calc(100vh - 112px)' }}> {/* Adjust minHeight based on header/footer */}
                        <Outlet /> {/* This is where nested routes will render their components */}
                    </div>
                </Content>
            </Layout>
        </Layout>
    );
};

export default AdminLayout; 