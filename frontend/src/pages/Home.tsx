import { useEffect } from 'react';
import { Typography, Card, Row, Col, Statistic, message } from 'antd';
import { BookOutlined, TeamOutlined, RocketOutlined } from '@ant-design/icons';
import { RootState, useAppDispatch, useAppSelector } from '@/store';
import { fetchBooks } from '@/store/slices/bookSlice';
import { fetchUsers } from '@/store/slices/userSlice';

const { Title, Paragraph } = Typography;

const HomePage = () => {
    const dispatch = useAppDispatch();

    const { total: totalBooks, loading: booksLoading, error: booksError } = useAppSelector((state: RootState) => state.book);
    const { totalUsers, loading: usersLoading, error: usersError } = useAppSelector((state: RootState) => state.user);

    useEffect(() => {
        dispatch(fetchBooks());
        dispatch(fetchUsers());
    }, [dispatch]);

    useEffect(() => {
        if (booksError) {
            message.error(`Error fetching book stats: ${booksError}`);
        }
        if (usersError) {
            message.error(`Error fetching user stats: ${usersError}`);
        }
    }, [booksError, usersError]);

    const isLoadingStats = booksLoading || usersLoading;

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
            </Row>
        </div>
    );
};

export default HomePage; 