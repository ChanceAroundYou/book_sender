import { useNavigate, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { Menu, Dropdown, Button, Input, Space } from 'antd';
import { UserOutlined, LoginOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { useAppSelector, RootState, store, useAppDispatch } from '@/store';
import { logoutUser, fetchCurrentUser } from '@/store/slices/authSlice';

const { Search } = Input;

const Navbar = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();
    const location = useLocation();
    const { user: currentUser, token, loading: authLoading } = useAppSelector((state: RootState) => state.auth);

    useEffect(() => {
        if (token && !currentUser && !authLoading) {
            dispatch(fetchCurrentUser());
        }
    }, [token, currentUser, dispatch, authLoading]);

    const menuItems: MenuProps['items'] = [
        {
            key: '/',
            label: '首页',
        },
        {
            key: '/books',
            label: '书籍',
        },
    ];

    const userMenuItems: MenuProps['items'] = [
        {
            key: '/user/profile',
            label: '个人信息',
            onClick: () => navigate('/user/profile'),
        },
        {
            key: '/user/library',
            label: '我的书架',
            onClick: () => navigate('/user/library'),
        },
        {
            type: 'divider',
        },
        {
            key: 'logout',
            label: '退出登录',
            danger: true,
            onClick: () => {
                store.dispatch(logoutUser());
                navigate('/auth/login');
            },
        },
    ];

    const handleSearch = (value: string) => {
        if (value) {
            navigate(`/books?search=${encodeURIComponent(value)}`);
        }
    };

    const getSelectedKeys = () => {
        const currentPath = location.pathname;
        if (currentPath.startsWith('/user') || currentPath.startsWith('/auth') || currentPath.startsWith('/admin')) {
            return [''];
        }

        const matchingKeys = menuItems
            ?.filter(item => item && item.key && currentPath.startsWith(item.key as string))
            .map(item => item!.key as string) || [];

        if (matchingKeys.length > 0) {
            return [matchingKeys.reduce((a, b) => (a.length > b.length ? a : b))];
        }
        return ['/'];
    };

    return (
        <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
                <div className="text-xl font-bold mr-8 cursor-pointer" onClick={() => navigate('/')}>
                    Book Sender
                </div>
                <Menu
                    mode="horizontal"
                    items={menuItems}
                    selectedKeys={getSelectedKeys()}
                    onClick={({ key }) => navigate(key)}
                    className="border-0"
                />
            </div>
            <div className="flex items-center space-x-4">
                {currentUser ? (
                    <>
                        <Search
                            placeholder="搜索书籍..."
                            allowClear
                            onSearch={handleSearch}
                            style={{ width: 300 }}
                        />
                        <Space>
                            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
                                <Button icon={<UserOutlined />}>用户中心</Button>
                            </Dropdown>
                        </Space>
                    </>
                ) : (
                    <Button icon={<LoginOutlined />} onClick={() => navigate('/auth/login')}>
                        登录
                    </Button>
                )}

            </div>
        </div>
    );
};

export default Navbar; 