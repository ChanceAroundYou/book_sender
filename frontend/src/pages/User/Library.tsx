import { useState, useEffect } from 'react';
import { Row, Col, Typography, Tabs, Empty, List, Spin} from 'antd';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import { fetchCurrentUser } from '@/store/slices/authSlice';
import BookCard from '@/components/base/BookCard';

const { Title } = Typography;

interface UserBook {
    id: number;
    title: string;
    status: string;
    cover_link?: string;
}

interface TabItem {
    key: string;
    label: string;
    children: React.ReactNode;
}

const UserLibraryPage = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();
    const [activeTab, setActiveTab] = useState('my_books');

    const currentUser = useAppSelector((state: RootState) => state.auth.user);
    const loading = useAppSelector((state: RootState) => state.auth.loading);
    const userBooks: UserBook[] = currentUser?.books || [];

    useEffect(() => {
        if (!currentUser) {
            dispatch(fetchCurrentUser());
        }
    }, [dispatch, currentUser]);

    const items: TabItem[] = [
        {
            key: 'my_books',
            label: `我的书籍 (${userBooks.length})`,
            children: loading ? (
                <div style={{ textAlign: 'center', padding: '50px' }}>
                    <Spin size="large">
                        <div style={{ marginTop: 24 }}>Loading your library...</div>
                    </Spin>
                </div>
            ) : userBooks.length > 0 ? (
                <List
                    loading={loading}
                    dataSource={userBooks}
                    grid={{ gutter: 16, xs: 1, sm: 2, md: 3, lg: 4, xl: 5, xxl: 6 }}
                    renderItem={item => {
                        return (
                            <List.Item>
                                <BookCard book={item} onClick={() => navigate(`/books/${item.id}`)} userBookStatus={item.status} />
                            </List.Item>
                        )
                    }}
                />
            ) : (
                <Empty
                    description="你还没有任何书籍"
                    className="py-12"
                />
            ),
        },
    ];

    return (
        <div className="container mx-auto px-4 py-6">
            <Row gutter={[0, 24]}>
                <Col span={24}>
                    <Title level={2}>我的书架</Title>
                </Col>
                <Col span={24}>
                    <Tabs
                        activeKey={activeTab}
                        onChange={setActiveTab}
                        items={items}
                    />
                </Col>
            </Row>
        </div>
    );
};

export default UserLibraryPage; 