import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Row,
    Col,
    Typography,
    Button,
    Space,
    Tag,
    message,
    Skeleton,
    Image,
    Descriptions,
    List,
    Modal,
    Input,
} from 'antd';
import {
    DownloadOutlined,
    ShareAltOutlined,
    ArrowLeftOutlined,
} from '@ant-design/icons';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import { fetchBookById, setCurrentBookAction, fetchSeriesBooks, distributeBookAction } from '@/store/slices/bookSlice';
import { addUserSubscription, deleteUserSubscription } from '@/store/slices/userSlice';
import { fetchCurrentUser } from '@/store/slices/authSlice';
import type { Book, UserSubscriptionParams, DistributeBookParams } from '@/types';
import { renderSeries } from '@/utils';
import { utilService } from '@/services/api';

const { Title, Text, Paragraph } = Typography;

const BookDetailPage = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const dispatch = useAppDispatch();

    const { currentBook: book, loading: bookLoading, error: bookError } = useAppSelector((state: RootState) => state.book);
    const { user: currentUser, loading: authLoading } = useAppSelector((state: RootState) => state.auth);
    const { error: downloadError } = useAppSelector((state: RootState) => state.download);
    const { loading: userUpdateLoading, error: userUpdateError } = useAppSelector((state: RootState) => state.user);
    const { loading: bookActionLoading, error: bookActionError } = useAppSelector((state: RootState) => state.book);
    const [seriesBooks, setSeriesBooks] = useState<Book[]>([]);
    const [seriesLoading, setSeriesLoading] = useState(false);

    useEffect(() => {
        if (id) {
            dispatch(fetchBookById({ id: Number(id) }));
        }
        return () => {
            dispatch(setCurrentBookAction(null));
        };
    }, [id, dispatch]);

    useEffect(() => {
        if (book && book.series) {
            setSeriesLoading(true);
            dispatch(fetchSeriesBooks({ series: book.series }))
                .then((action: any) => {
                    if (fetchSeriesBooks.fulfilled.match(action)) {
                        setSeriesBooks(
                            action.payload.items
                                .filter((b: Book) => b.id !== book.id)
                                .sort((a: Book, b: Book) => {
                                    if (!a.date) return 1;
                                    if (!b.date) return -1;
                                    return new Date(b.date).getTime() - new Date(a.date).getTime();
                                })
                        );
                    }
                })
                .finally(() => setSeriesLoading(false));
        } else {
            setSeriesBooks([]);
        }
    }, [book, dispatch]);

    useEffect(() => {
        if (bookError) {
            message.error(bookError);
        }
        if (downloadError) {
            message.error(downloadError);
        }
        if (userUpdateError) {
            message.error(userUpdateError);
        }
        if (bookActionError && !bookLoading && !userUpdateLoading) {
            message.error(bookActionError);
        }
    }, [bookError, downloadError, userUpdateError, bookActionError, bookLoading, userUpdateLoading]);

    const confirmUnsubscribe = () => {
        if (!currentUser || !book || !book.series) return;
        Modal.confirm({
            title: `取消订阅系列: ${renderSeries(book.series)}?`,
            content: '您确定要取消订阅该系列吗？之后将不会收到该系列书籍更新的邮件通知。',
            okText: '确定取消',
            cancelText: '再想想',
            onOk: async () => {
                const params = { user_id: currentUser.id, series: book.series! };
                try {
                    const resultAction = await dispatch(deleteUserSubscription(params));
                    if (deleteUserSubscription.fulfilled.match(resultAction)) {
                        message.success(`已取消订阅系列: ${renderSeries(book.series)}`);
                        dispatch(fetchCurrentUser());
                    } else {
                        // Error already handled by userUpdateError effect
                    }
                } catch (error) {
                    message.error('取消订阅失败');
                }
            },
        });
    };

    const handleSubscribe = async () => {
        if (!currentUser) {
            message.error('请先登录');
            navigate('/auth/login');
            return;
        }
        if (!book || !book.series) {
            message.error('本书没有系列信息，无法进行订阅操作');
            return;
        }

        const params: UserSubscriptionParams = {
            user_id: currentUser.id,
            series: book.series,
        };

        try {
            const resultAction = await dispatch(addUserSubscription(params));
            if (addUserSubscription.fulfilled.match(resultAction)) {
                message.success(`成功订阅系列: ${renderSeries(book.series)}`);
                dispatch(fetchCurrentUser());
            } else if (addUserSubscription.rejected.match(resultAction)) {
                // Error message is handled by the useEffect hook for userUpdateError
            }
        } catch (err) {
            message.error('订阅操作失败');
        }
    };

    const handleDistribute = () => {
        if (!currentUser) {
            message.error('请先登录');
            navigate('/auth/login');
            return;
        }
        if (!book || !book.id) {
            message.error('无法确定要发送的书籍');
            return;
        }

        let email = currentUser.email;

        Modal.confirm({
            title: '发送到邮箱',
            icon: <ShareAltOutlined />,
            content: (
                <Input
                    placeholder="请输入接收邮箱"
                    defaultValue={email}
                    onChange={(e) => (email = e.target.value)}
                />
            ),
            okText: '发送',
            cancelText: '取消',
            onOk: async () => {
                if (!email || !/^\S+@\S+\.\S+$/.test(email)) {
                    message.error('请输入有效的邮箱地址');
                    return Promise.reject('Invalid email');
                }
                const params: DistributeBookParams = { id: book.id!, email };
                try {
                    const resultAction = await dispatch(distributeBookAction(params));
                    if (distributeBookAction.fulfilled.match(resultAction)) {
                        message.success(resultAction.payload.message || '书籍已开始发送，请检查邮箱。');
                    } else if (distributeBookAction.rejected.match(resultAction)) {
                        // Error is handled by bookActionError effect
                    }
                } catch (err) {
                    message.error('发送书籍失败');
                }
            },
        });
    };

    const isSubscribed = currentUser?.subscriptions?.some(sub => sub.series === book?.series);

    if (bookLoading && !book) {
        return (
            <div className="container mx-auto px-4 py-8">
                <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)} className="mb-4">Back</Button>
                <Row gutter={[24, 24]}>
                    <Col xs={24} md={8} lg={6}>
                        <Skeleton.Image style={{ width: '100%', height: 300 }} />
                    </Col>
                    <Col xs={24} md={16} lg={18}>
                        <Skeleton active paragraph={{ rows: 8 }} />
                    </Col>
                </Row>
            </div>
        );
    }

    if (!book) {
        return (
            <div className="container mx-auto px-4 py-8 text-center">
                <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)} className="mb-4 absolute top-4 left-4">Back</Button>
                <Title level={2} className="mt-16">Book not found</Title>
                <Paragraph>The book you are looking for does not exist or could not be loaded.</Paragraph>
                <Button type="primary" onClick={() => navigate('/books')}>Go to Books List</Button>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/books')} className="mb-6">
                返回列表
            </Button>
            <Row gutter={[24, 32]}>
                <Col xs={24} md={8} lg={6}>
                    <Image
                        src={utilService.getProxiedImageUrl(book.cover_link)}
                        alt={book.title}
                        className="w-full rounded-lg shadow-lg aspect-[3/4] object-cover"
                        preview={false}
                        onError={(e) => {
                            // Fallback if even the proxy fails or original link was bad
                            (e.target as HTMLImageElement).src = '';
                        }}
                    />
                    <Space direction="vertical" className="w-full mt-6">
                        <Button
                            type="primary"
                            icon={<DownloadOutlined />}
                            onClick={() => window.open(book.download_link, '_blank')}
                            block
                            size="large"
                            disabled={!book.download_link}
                        >
                            {book.download_link ? '下载书籍' : '暂无资源'}
                        </Button>
                        <Button
                            icon={<ShareAltOutlined />}
                            onClick={handleDistribute}
                            block
                            size="large"
                            disabled={!book.download_link || bookActionLoading}
                            loading={bookActionLoading}
                        >
                            发送到邮箱
                        </Button>
                        {
                            book.series ?
                                (isSubscribed ? <Button
                                    onClick={confirmUnsubscribe}
                                    block
                                    size='large'
                                    loading={userUpdateLoading || authLoading}
                                    disabled={userUpdateLoading || authLoading}
                                    danger
                                >
                                    取消订阅
                                </Button> :
                                    <Button
                                        onClick={handleSubscribe}
                                        block
                                        size='large'
                                        loading={userUpdateLoading || authLoading}
                                        disabled={userUpdateLoading || authLoading}
                                    >
                                        订阅
                                    </Button>) :
                                null
                        }
                    </Space>
                </Col>

                <Col xs={24} md={16} lg={18}>
                    <Title level={1} className="mb-2">{book.title}</Title>
                    {book.author && <Text type="secondary" className="text-lg mb-4 block">By: {book.author}</Text>}

                    <Space wrap className="mb-6">
                        {book.series && <Tag color="cyan">系列: {renderSeries(book.series)}</Tag>}
                        <Tag color="blue">格式: {book.file_format?.toUpperCase()}</Tag>
                    </Space>

                    <Descriptions bordered column={{ xxl: 2, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }}>
                        <Descriptions.Item label="ID">{book.id}</Descriptions.Item>
                        {book.date && <Descriptions.Item label="发布日期">{new Date(book.date).toLocaleDateString()}</Descriptions.Item>}
                        <Descriptions.Item label="文件大小">
                            {book.file_size ? `${(book.file_size / (1024 * 1024)).toFixed(2)} MB` : '未知'}
                        </Descriptions.Item>
                        {book.created_at && <Descriptions.Item label="添加时间">{new Date(book.created_at).toLocaleString()}</Descriptions.Item>}
                    </Descriptions>

                    {book.summary && (
                        <>
                            <Title level={4} className="mt-6 mb-2">简介</Title>
                            <Paragraph style={{ whiteSpace: 'pre-line' }}>{book.summary}</Paragraph>
                        </>
                    )}
                </Col>
            </Row>
            {book.series && (
                <div className="mt-10">
                    <Title level={3}>{renderSeries(book.series)} 系列其他书籍</Title>
                    <List
                        loading={seriesLoading}
                        dataSource={seriesBooks}
                        grid={{ gutter: 16, column: 4 }}
                        locale={{ emptyText: '暂无其他同系列书籍' }}
                        renderItem={item => (
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
                                    <div style={{ fontWeight: 500, marginTop: 4 }}>{item.title}</div>
                                </div>
                            </List.Item>
                        )}
                    />
                </div>
            )}
        </div>
    );
};

export default BookDetailPage; 