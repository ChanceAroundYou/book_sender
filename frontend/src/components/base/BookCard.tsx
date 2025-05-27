import React, { MouseEvent } from 'react';
import { Card, Tag, Typography } from 'antd';
import type { CardProps } from 'antd';

const { Text } = Typography;

export interface Book {
    id: number;
    title: string;
    cover_link?: string;
    file_format?: string;
}

export interface BookCardProps extends Omit<CardProps, 'cover' | 'onClick'> {
    book: Book;
    onClick?: (id: number) => void;
    coverHeight?: string;
    userBookStatus?: string;
}

const StatusTag = ({ status }: { status: string }) => {
    if (status === "distributed") {
        return <Tag color="green">
            已发送
        </Tag>
    } else if (status === 'downloaded') {
        return <Tag color="blue">
            已下载
        </Tag>
    } else {
        return <Tag color="red">
            未下载
        </Tag>
    }
}

const BookCard: React.FC<BookCardProps> = ({
    book,
    onClick,
    coverHeight = 'h-48',
    className = '',
    userBookStatus = '',
    ...props
}) => {
    const handleClick = (e: MouseEvent<HTMLDivElement>) => {
        e.stopPropagation();
        onClick?.(book.id);
    };

    return (
        <Card
            hoverable
            className={`h-full flex flex-col ${className}`}
            onClick={onClick ? handleClick : undefined}
            cover={
                <img
                    alt={book.title}
                    src={book.cover_link || '/placeholder-cover.jpg'}
                    className={`${coverHeight} w-full object-cover aspect-[3/4]`}
                />
            }
            {...props}
        >
            <Card.Meta
                title={
                    <Text
                        style={{
                            whiteSpace: 'normal',
                            wordBreak: 'break-word',
                            height: '90px',
                            overflow: 'hidden',
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical'
                        }}
                        className="mb-2"
                    >
                        {book.title}
                    </Text>
                }
            />
            {book.file_format && <Tag color="yellow">{book.file_format.toUpperCase()}</Tag>}
            {userBookStatus && <StatusTag status={userBookStatus} />}
        </Card>
    );
};

export default BookCard; 