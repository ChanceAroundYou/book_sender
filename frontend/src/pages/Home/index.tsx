import { useEffect, useState } from 'react';
import { Row, Col, Typography, Space, List, Card, Tag, Spin, Empty, Alert } from 'antd';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import type { Book } from '@/types';
import { fetchLatestBooks } from '@/store/slices/bookSlice';
import { BookOutlined, FireOutlined, StarOutlined } from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;

const BookDisplayCard: React.FC<{ book: Book; onClick: (id: number) => void }> = ({ book, onClick }) => (
    <Card
        hoverable
        className="h-full flex flex-col"
        onClick={() => onClick(book.id)}
        cover={
            <img
                alt={book.title}
                src={book.cover_link || '/placeholder-cover.jpg'}
                className="h-48 w-full object-cover aspect-[3/4]"
            />
        }
    >
        <Card.Meta
            title={<Text ellipsis={{ tooltip: book.title }}>{book.title}</Text>}
            description={<Text type="secondary" ellipsis={{ tooltip: book.author || 'N/A' }}>{book.author || 'N/A'}</Text>}
        />
        <div className="mt-auto pt-2">
            <Tag color="blue">{book.file_format?.toUpperCase()}</Tag>
        </div>
    </Card>
);

const MainHomePage = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();

    const { user } = useAppSelector((state: RootState) => state.auth);
    const { items: latestBooks, loading: latestBooksLoading, error: latestBooksError } = useAppSelector((state: RootState) => state.book);

    const [featuredLoading] = useState(false);
    const [popularLoading] = useState(false);

    useEffect(() => {
        dispatch(fetchLatestBooks({ limit: 6 }));

    }, [dispatch]);

    const handleBookClick = (id: number) => {
        navigate(`/books/${id}`);
    };

    const renderBookSection = (title: string, books: Book[], loading: boolean, icon?: React.ReactNode, error?: string | null) => (
        <Col span={24} className="mb-8">
            <Title level={3} className="mb-4"><Space>{icon}{title}</Space></Title>
            {loading && <div className="text-center py-8"><Spin /></div>}
            {!loading && error && <Alert message={`Error loading ${title.toLowerCase()}: ${error}`} type="error" />}
            {!loading && !error && books.length === 0 && <Empty description={`No ${title.toLowerCase()} available at the moment.`} />}
            {!loading && !error && books.length > 0 && (
                <List
                    grid={{ gutter: 16, xs: 1, sm: 2, md: 3, lg: 4, xl: 5, xxl: 6 }}
                    dataSource={books}
                    renderItem={book => (
                        <List.Item>
                            <BookDisplayCard book={book} onClick={handleBookClick} />
                        </List.Item>
                    )}
                />
            )}
        </Col>
    );

    return (
        <div className="container mx-auto px-4 py-8">
            <Row gutter={[24, 24]}>
                <Col span={24} className="mb-6 text-center md:text-left">
                    <Title level={2}>
                        {user ? `Welcome back, ${user.username}!` : 'Welcome to Book Sender'}
                    </Title>
                    <Paragraph type="secondary">
                        Explore our collection of books. New titles added regularly.
                    </Paragraph>
                </Col>

                {renderBookSection('Latest Additions', latestBooks, latestBooksLoading, <BookOutlined />, latestBooksError)}

                <Col span={24} className="mb-8">
                    <Title level={3} className="mb-4"><Space><StarOutlined />Featured Books</Space></Title>
                    {featuredLoading && <div className="text-center py-8"><Spin /></div>}
                    {!featuredLoading && (
                        <Empty description="Featured books are coming soon!">
                        </Empty>
                    )}
                </Col>

                <Col span={24} className="mb-8">
                    <Title level={3} className="mb-4"><Space><FireOutlined />Popular Books</Space></Title>
                    {popularLoading && <div className="text-center py-8"><Spin /></div>}
                    {!popularLoading && (
                        <Empty description="Popular books selection will be available shortly!">
                        </Empty>
                    )}
                </Col>
            </Row>
        </div>
    );
};

export default MainHomePage; 