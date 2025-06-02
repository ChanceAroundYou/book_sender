import { useEffect } from 'react';
import { Typography, Card, Row, Col, Statistic, message, Spin, Alert, Empty, List, Space } from 'antd';
import { BookOutlined, TeamOutlined, RocketOutlined } from '@ant-design/icons';
import { RootState, useAppDispatch, useAppSelector } from '@/store';
import { useNavigate } from 'react-router-dom';
import { fetchBooks } from '@/store/slices/bookSlice';
import { fetchUsers } from '@/store/slices/userSlice';
import { fetchStats } from '@/store/slices/statsSlice';
import type { Book } from '@/types';
import BookCard from '@/components/base/BookCard';

const { Title, Paragraph } = Typography;

const HomePage = () => {
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    const { loading: booksLoading, error: booksError } = useAppSelector((state: RootState) => state.book);
    const { loading: usersLoading, error: usersError } = useAppSelector((state: RootState) => state.user);
    const { totalBooks, totalUsers, loading: statsLoading, error: statsError } = useAppSelector((state: RootState) => state.stats);
    const { items: latestBooks, loading: latestBooksLoading, error: latestBooksError } = useAppSelector((state: RootState) => state.book);

    // console.log('Stats from Redux:', { totalBooks, totalUsers, statsLoading, statsError });

    useEffect(() => {
        // Fetch initial data
        dispatch(fetchBooks());
        dispatch(fetchUsers());
        dispatch(fetchStats());
    }, [dispatch]);

    useEffect(() => {
        if (booksError) {
            message.error(`Error fetching book stats: ${booksError}`);
        }
        if (usersError) {
            message.error(`Error fetching user stats: ${usersError}`);
        }
        if (statsError) {
            message.error(`Error fetching stats: ${statsError}`);
        }
    }, [booksError, usersError, statsError]);

    const handleBookClick = (id: number) => {
        navigate(`/books/${id}`);
    };

    const isLoadingStats = booksLoading || usersLoading || statsLoading;

    const renderBookSection = (title: string, books: Book[], loading: boolean, icon?: React.ReactNode, error?: string | null) => (
        <Col span={24} className="mb-8">
            <Title level={3} className="mb-4"><Space>{icon}{title}</Space></Title>
            {loading && (
                <div className="text-center py-8">
                    <Spin>
                        <div style={{ marginTop: 24 }}>Loading...</div>
                    </Spin>
                </div>
            )}
            {!loading && error && <Alert message={`Error loading ${title.toLowerCase()}: ${error}`} type="error" />}
            {!loading && !error && books.length === 0 && <Empty description={`No ${title.toLowerCase()} available at the moment.`} />}
            {!loading && !error && books.length > 0 && (
                <List
                    grid={{ gutter: 16, xs: 1, sm: 2, md: 3, lg: 4, xl: 5, xxl: 6 }}
                    dataSource={books}
                    renderItem={book => (
                        <List.Item>
                            <BookCard book={book} onClick={handleBookClick} />
                        </List.Item>
                    )}
                />
            )}
        </Col>
    );

    return (
        <div className="p-4 md:p-6 max-w-6xl mx-auto">
            <Title level={1} className="text-center mb-8">
                欢迎使用 Book Sender
            </Title>
            <Paragraph className="text-center text-lg mb-12">
                一个简单而强大的书籍分享平台
            </Paragraph>

            <Row gutter={[24, 24]} className="mb-12">
                <Col xs={24} sm={12} md={8}>
                    <Card>
                        <Statistic title="总书籍数" value={totalBooks} loading={isLoadingStats} prefix={<BookOutlined />} />
                    </Card>
                </Col>
                <Col xs={24} sm={12} md={8}>
                    <Card>
                        <Statistic title="注册用户数" value={totalUsers} loading={isLoadingStats} prefix={<TeamOutlined />} />
                    </Card>
                </Col>
            </Row>

            <Row gutter={[24, 24]} className="mt-8">
                <Col xs={24} md={8}>
                    <Card hoverable className="h-full">
                        <div className="flex flex-col items-center text-center">
                            <BookOutlined className="text-4xl mb-4 text-blue-500" />
                            <Title level={3}>丰富的书籍资源</Title>
                            <Paragraph>
                                探索我们精心挑选的书籍收藏，找到您感兴趣的内容。
                            </Paragraph>
                        </div>
                    </Card>
                </Col>
                <Col xs={24} md={8}>
                    <Card hoverable className="h-full">
                        <div className="flex flex-col items-center text-center">
                            <TeamOutlined className="text-4xl mb-4 text-green-500" />
                            <Title level={3}>社区互动</Title>
                            <Paragraph>
                                加入我们的社区，与其他读者分享您的阅读体验。
                            </Paragraph>
                        </div>
                    </Card>
                </Col>
                <Col xs={24} md={8}>
                    <Card hoverable className="h-full">
                        <div className="flex flex-col items-center text-center">
                            <RocketOutlined className="text-4xl mb-4 text-purple-500" />
                            <Title level={3}>便捷的分享</Title>
                            <Paragraph>
                                轻松分享您喜爱的书籍，让更多人受益。
                            </Paragraph>
                        </div>
                    </Card>
                </Col>

                {renderBookSection('最新添加', latestBooks.slice(0, 6), latestBooksLoading, <BookOutlined />, latestBooksError)}
            </Row>
        </div>
    );
};

export default HomePage; 