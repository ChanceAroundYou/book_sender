import { Card, Button, Space, Rate } from 'antd';
import { DownloadOutlined, HeartOutlined, HeartFilled } from '@ant-design/icons';
import BaseCard from '../base/BaseCard';

export interface BookCardProps {
    id: string;
    title: string;
    author: string;
    cover: string;
    rating?: number;
    description?: string;
    isFavorite?: boolean;
    onDownload?: (id: string) => void;
    onFavorite?: (id: string) => void;
    onClick?: (id: string) => void;
}

const BookCard = ({
    id,
    title,
    author,
    cover,
    rating = 0,
    description,
    isFavorite = false,
    onDownload,
    onFavorite,
    onClick,
}: BookCardProps) => {
    return (
        <BaseCard
            variant="hover"
            cover={
                <div
                    className="h-48 bg-cover bg-center cursor-pointer"
                    style={{ backgroundImage: `url(${cover})` }}
                    onClick={() => onClick?.(id)}
                />
            }
            actions={[
                <Button
                    key="download"
                    type="text"
                    icon={<DownloadOutlined />}
                    onClick={() => onDownload?.(id)}
                >
                    下载
                </Button>,
                <Button
                    key="favorite"
                    type="text"
                    icon={isFavorite ? <HeartFilled /> : <HeartOutlined />}
                    onClick={() => onFavorite?.(id)}
                >
                    收藏
                </Button>,
            ]}
        >
            <Card.Meta
                title={
                    <div className="cursor-pointer" onClick={() => onClick?.(id)}>
                        {title}
                    </div>
                }
                description={
                    <Space direction="vertical" size={2}>
                        <div className="text-gray-500">{author}</div>
                        {rating > 0 && <Rate disabled defaultValue={rating} />}
                        {description && (
                            <div className="text-gray-600 text-sm line-clamp-2">{description}</div>
                        )}
                    </Space>
                }
            />
        </BaseCard>
    );
};

export default BookCard; 