import { Row, Col, Card, Typography, Space, Tag, Tooltip } from 'antd';
import type { PaginationProps } from 'antd';
import { FileTextOutlined, CalendarOutlined, FileOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';

const { Meta } = Card;
const { Text, Paragraph } = Typography;

export interface Book {
    id: number;
    title: string;
    author: string | null;
    cover_link: string;
    detail_link: string;
    category: string;
    file_size: number;
    file_format: string;
    date: string;
    summary: string | null;
    downloaded_at: string;
    created_at: string;
    updated_at: string;
    users: any[];
}

interface BookListProps {
    books: Book[];
    loading: boolean;
    onBookClick: (id: number) => void;
    pagination?: PaginationProps;
}

const formatFileSize = (bytes: number): string => {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return `${size.toFixed(2)} ${units[unitIndex]}`;
};

const formatCategory = (category: string): string => {
    return category.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
};

const BookList: React.FC<BookListProps> = ({
    books,
    loading,
    onBookClick,
    pagination,
}) => {
    return (
        <Row gutter={[16, 16]}>
            {books.map((book) => (
                <Col key={book.id} xs={24} sm={12} md={8} lg={6}>
                    <Card
                        hoverable
                        loading={loading}
                        cover={
                            <div className="aspect-[3/4] overflow-hidden">
                                <img
                                    alt={book.title}
                                    src={book.cover_link}
                                    className="w-full h-full object-cover"
                                />
                            </div>
                        }
                        onClick={() => onBookClick(book.id)}
                    >
                        <Meta
                            title={
                                <Tooltip title={book.title}>
                                    <Paragraph ellipsis={{ rows: 2 }} className="mb-0">
                                        {book.title}
                                    </Paragraph>
                                </Tooltip>
                            }
                            description={
                                <Space direction="vertical" size={2} className="w-full">
                                    {book.author && (
                                        <Text type="secondary" ellipsis>
                                            {book.author}
                                        </Text>
                                    )}
                                    <Space wrap>
                                        <Tag color="blue">
                                            <FileOutlined /> {book.file_format.toUpperCase()}
                                        </Tag>
                                        <Tag color="green">
                                            <FileTextOutlined /> {formatFileSize(book.file_size)}
                                        </Tag>
                                        <Tag color="purple">
                                            <CalendarOutlined /> {dayjs(book.date).format('YYYY-MM-DD')}
                                        </Tag>
                                    </Space>
                                    <Tag>{formatCategory(book.category)}</Tag>
                                </Space>
                            }
                        />
                    </Card>
                </Col>
            ))}
            {pagination && (
                <Col span={24} className="mt-4 text-center">
                    <Space>
                        <Text type="secondary">
                            共 {pagination.total} 条记录
                        </Text>
                    </Space>
                </Col>
            )}
        </Row>
    );
};

export default BookList; 