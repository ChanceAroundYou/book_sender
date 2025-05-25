import { useState, useEffect } from 'react';
import { Row, Col, Typography, Tabs, Empty, List, Card, Tag, Spin, Image } from 'antd';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import type { User } from '@/types';
import { fetchCurrentUser } from '@/store/slices/authSlice';
import { utilService } from '@/services/api';

const { Title, Text } = Typography;

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

    const handleBookClick = (id: number) => {
        navigate(`/books/${id}`);
    };

    const items: TabItem[] = [
        {
            key: 'my_books',
            label: `我的书籍 (${userBooks.length})`,
            children: loading ? (
                <div style={{ textAlign: 'center', padding: '50px' }}><Spin size="large" /></div>
            ) : userBooks.length > 0 ? (
                // <List
                //     grid={{ gutter: 16, xs: 1, sm: 2, md: 3, lg: 4, xl: 4, xxl: 5 }}
                //     dataSource={userBooks}
                //     renderItem={(book) => (
                //         <List.Item>
                //             <Card
                //                 hoverable
                //                 onClick={() => handleBookClick(book.id)}
                //                 cover={
                //                     <Image
                //                         alt={book.title}
                //                         src={book.cover_link ? utilService.getProxiedImageUrl(book.cover_link) : undefined}
                //                         style={{
                //                             width: '100%',
                //                             aspectRatio: '3/4',
                //                             objectFit: 'cover',
                //                         }}
                //                         preview={false}
                //                         fallback="/placeholder-image.png"
                //                         onError={(e) => {
                //                             (e.target as HTMLImageElement).src = '';
                //                         }}
                //                     />
                //                 }
                //                 style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
                //                 bodyStyle={{ flexGrow: 1, paddingTop: '12px', paddingBottom: '12px' }}
                //             >
                //                 <Card.Meta
                //                     title={<Text ellipsis={{ tooltip: book.title }}>{book.title}</Text>}
                //                     description={
                //                         <>
                //                             <Tag color="blue" style={{ marginBottom: '8px' }}>{book.status || 'N/A'}</Tag>
                //                             <Text type="secondary" style={{ fontSize: '12px', display: 'block' }}>ID: {book.id}</Text>
                //                         </>
                //                     }
                //                 />
                //             </Card>
                //         </List.Item>
                //     )}
                // />
                <List
                    loading={loading}
                    dataSource={userBooks}
                    grid={{ gutter: 16, column: 4 }}
                    renderItem={item => {
                        return (
                            <List.Item>
                                <div
                                    style={{ cursor: 'pointer', textAlign: 'center' }}
                                    onClick={() => navigate(`/books/${item.id}`)}
                                >
                                    <Image
                                        src={utilService.getProxiedImageUrl(item.cover_link)}
                                        alt={item.title}
                                        width={120}
                                        height={160}
                                        style={{ objectFit: 'cover', borderRadius: 8, marginBottom: 8 }}
                                        preview={false}
                                        onError={(e) => {
                                            (e.target as HTMLImageElement).src = '';
                                        }}
                                    />
                                    <div style={{ fontWeight: 500, marginTop: 4 }}>
                                        {`${item.title}  `}
                                        {item.status === "distributed" ? <Tag color="green"
                                            style={{ marginBottom: '8px' }}>
                                            已发送
                                        </Tag>
                                            : item.status === 'downloaded' ?
                                                <Tag color="blue"
                                                    style={{ marginBottom: '8px' }}>
                                                    已下载
                                                </Tag>
                                                :
                                                <Tag color="red"
                                                    style={{ marginBottom: '8px' }}>
                                                    未下载
                                                </Tag>
                                        }
                                    </div>
                                </div>
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