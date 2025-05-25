import { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
    DashboardOutlined,
    BookOutlined,
    UserOutlined,
    SettingOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

const AdminLayout = () => {
    const [collapsed, setCollapsed] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();

    const menuItems = [
        {
            key: '/admin/dashboard',
            icon: <DashboardOutlined />,
            label: '仪表盘',
        },
        {
            key: '/admin/books',
            icon: <BookOutlined />,
            label: '书籍管理',
        },
        {
            key: '/admin/users',
            icon: <UserOutlined />,
            label: '用户管理',
        },
        {
            key: '/admin/settings',
            icon: <SettingOutlined />,
            label: '系统设置',
        },
    ];

    return (
        <Layout className="min-h-screen">
            <Header className="bg-white border-b border-gray-200 px-4 flex items-center">
                <div className="text-xl font-bold">Book Sender Admin</div>
            </Header>
            <Layout>
                <Sider
                    collapsible
                    collapsed={collapsed}
                    onCollapse={setCollapsed}
                    className="bg-white border-r border-gray-200"
                    theme="light"
                >
                    <Menu
                        mode="inline"
                        selectedKeys={[location.pathname]}
                        items={menuItems}
                        onClick={({ key }) => navigate(key)}
                    />
                </Sider>
                <Content className="p-6">
                    <div className="bg-white p-6 rounded-lg">
                        <Outlet />
                    </div>
                </Content>
            </Layout>
        </Layout>
    );
};

export default AdminLayout; 