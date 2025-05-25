import { useState, useEffect } from 'react';
import {
    Row, Col, Typography, Input, Select, Space, Empty, Table, Button, message, Spin, Modal
} from 'antd';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import { fetchLatestBooks, setBookFilters, setBookPagination, distributeSeriesAction } from '@/store/slices/bookSlice';
import { fetchCurrentUser } from '@/store/slices/authSlice';
import { addUserSubscription, deleteUserSubscription } from '@/store/slices/userSlice';
import type { Book, BookQueryParams, DistributeSeriesParams, UserSubscriptionParams } from '@/types';
import { ColumnsType } from 'antd/es/table';
import { SearchOutlined, SendOutlined } from '@ant-design/icons';
import { renderSeries } from '@/utils';

const { Title, Text } = Typography;
const { Search } = Input;
const { Option } = Select;

const BookListPage = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();
    const { user: currentUser } = useAppSelector((state: RootState) => state.auth);

    const {
        items: books,
        total,
        loading,
        error,
        filters: currentFilters,
        pagination: currentPagination
    } = useAppSelector((state: RootState) => state.book);

    const [localSearchTerm, setLocalSearchTerm] = useState<string>('');
    const [seriesList, setSeriesList] = useState<string[]>([]);

    useEffect(() => {
        const titleFilter = currentFilters.title;
        if (typeof titleFilter === 'object' && titleFilter !== null && 'value' in titleFilter) {
            setLocalSearchTerm(String(titleFilter.value).replace(/%/g, ''));
        } else if (typeof titleFilter === 'string') {
            setLocalSearchTerm(titleFilter);
        } else {
            setLocalSearchTerm('');
        }
    }, [currentFilters.title]);

    useEffect(() => {
        dispatch(fetchLatestBooks());
    }, [dispatch, currentFilters, currentPagination.page, currentPagination.pageSize]);

    useEffect(() => {
        if (error) {
            message.error(error);
        }
    }, [error]);

    useEffect(() => {
        const uniqueSeries = Array.from(new Set(books.map(book => book.series).filter(Boolean)));
        setSeriesList(uniqueSeries);
    }, [books]);

    const triggerSearch = () => {
        const newFilters: Partial<BookQueryParams> = {
            ...currentFilters,
            title: localSearchTerm ? { operator: 'like', value: `%${localSearchTerm}%` } : undefined,
            skip: 0,
        };
        dispatch(setBookFilters(newFilters));
    };

    const handleSelectFilterChange = (value: string | number | undefined, filterKey: Extract<keyof BookQueryParams, 'file_format' | 'series' | 'language'>) => {
        const newFilters: Partial<BookQueryParams> = {
            ...currentFilters,
            [filterKey]: value || undefined,
            skip: 0,
        };
        dispatch(setBookFilters(newFilters));
    };

    const handleSortChange = (value: string | undefined) => {
        let orderBy: BookQueryParams['order_by'] = undefined;
        let orderDesc: BookQueryParams['order_desc'] = undefined;
        if (value) {
            orderDesc = value.startsWith('-');
            orderBy = value.replace('-', '') as BookQueryParams['order_by'];
        }
        const newFilters: Partial<BookQueryParams> = {
            ...currentFilters,
            order_by: orderBy,
            order_desc: orderDesc,
            skip: 0,
        };
        dispatch(setBookFilters(newFilters));
    };

    const handleTableChange = (pagination: any, tableAntdFilters: Record<string, (React.Key | boolean)[] | null>, sorter: any) => {
        dispatch(setBookPagination({ page: pagination.current, pageSize: pagination.pageSize }));

        const previousOrderBy = currentFilters.order_by;
        const previousOrderDesc = currentFilters.order_desc;

        const newOrderBy = (sorter.field && sorter.order) ? String(sorter.field) as BookQueryParams['order_by'] : undefined;
        const newOrderDesc = (sorter.field && sorter.order) ? sorter.order === 'descend' : undefined;

        let filtersToUpdate: Partial<BookQueryParams> = {};
        let filtersHaveChanged = false;

        if (newOrderBy !== previousOrderBy || newOrderDesc !== previousOrderDesc) {
            filtersToUpdate.order_by = newOrderBy;
            filtersToUpdate.order_desc = newOrderDesc;
            filtersHaveChanged = true;
        }

        if (filtersHaveChanged) {
            const newSkip = (pagination.current - 1) * pagination.pageSize;
            dispatch(setBookFilters({ ...currentFilters, ...filtersToUpdate, skip: newSkip }));
        }
    };

    const handleSendSeries = async (seriesName: string) => {
        if (!currentUser || !currentUser.email) {
            message.error('无法获取用户信息或邮箱，请先登录。');
            navigate('/auth/login');
            return;
        }
        if (!seriesName) {
            message.warning('该书籍没有系列信息。');
            return;
        }

        Modal.confirm({
            title: `发送系列: ${renderSeries(seriesName)}?`,
            content: `确定要将系列 " ${renderSeries(seriesName)} " 中所有未分发的书籍发送到邮箱 ${currentUser.email} 吗？`,
            okText: '全部发送',
            cancelText: '取消',
            onOk: async () => {
                const params: DistributeSeriesParams = { series: seriesName, email: currentUser.email! };
                try {
                    const resultAction = await dispatch(distributeSeriesAction(params));
                    if (distributeSeriesAction.fulfilled.match(resultAction)) {
                        message.success(resultAction.payload.message || `系列 " ${renderSeries(seriesName)} " 的书籍已开始发送。`);
                    } else if (distributeSeriesAction.rejected.match(resultAction)) {
                        // Error is handled by the global error effect from bookSlice
                        message.error(resultAction.payload || `发送系列 " ${renderSeries(seriesName)} " 失败。`);
                    }
                } catch (err) {
                    message.error('发送系列操作出现意外错误。');
                }
            },
        });
    };

    const handleSubscribeSeries = async (series: string) => {
        if (!currentUser) {
            message.error('请先登录');
            navigate('/auth/login');
            return;
        }
        if (!series) {
            message.error('没有系列信息，无法进行订阅操作');
            return;
        }

        const params: UserSubscriptionParams = {
            user_id: currentUser.id,
            series: series,
        };

        try {
            const resultAction = await dispatch(addUserSubscription(params));
            if (addUserSubscription.fulfilled.match(resultAction)) {
                message.success(`成功订阅系列: ${renderSeries(series)}`);
                dispatch(fetchCurrentUser());
            } else if (addUserSubscription.rejected.match(resultAction)) {
                // Error message is handled by the useEffect hook for userUpdateError
            }
        } catch (err) {
            message.error('订阅操作失败');
        }
    };

    const confirmUnsubscribe = (series: string) => {
        if (!currentUser || !series) return;
        Modal.confirm({
            title: `取消订阅系列: ${renderSeries(series)}?`,
            content: '您确定要取消订阅该系列吗？之后将不会收到该系列书籍更新的邮件通知。',
            okText: '确定取消',
            cancelText: '再想想',
            onOk: async () => {
                const params = { user_id: currentUser.id, series: series };
                try {
                    const resultAction = await dispatch(deleteUserSubscription(params));
                    if (deleteUserSubscription.fulfilled.match(resultAction)) {
                        message.success(`已取消订阅系列: ${renderSeries(series)}`);
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

    const isSubscribed = (series: string) => {
        return currentUser?.subscriptions?.some((s) => s.series === series);
    };

    const columns: ColumnsType<Book> = [
        { title: 'ID', dataIndex: 'id', key: 'id', sorter: true, width: 80 },
        {
            title: '标题',
            dataIndex: 'title',
            key: 'title',
            sorter: true,
            width: 250,
            render: (value) => renderSeries(value, true)
        },
        { title: '作者', dataIndex: 'author', key: 'author', sorter: true, width: 150 },
        {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            sorter: true,
            width: 120,
            render: (dateStr) => dateStr ? new Date(dateStr).toLocaleDateString() : 'N/A',
        },
        {
            title: '操作',
            key: 'action',
            width: 120,
            render: (_, record: Book) => (
                <Space>
                    <Button size="small" onClick={() => navigate(`/books/${record.id}`)}>查看</Button>
                    <Button
                        size="small"
                        // icon={<BellOutlined />} // Or any other appropriate icon
                        onClick={() => record.series ? (
                            isSubscribed(record.series) ? confirmUnsubscribe(record.series) : handleSubscribeSeries(record.series)
                        ) : message.warning('该书籍没有系列信息。')}

                        disabled={!record.series || loading}
                        title={isSubscribed(record.series) ? '已订阅' : '订阅'}
                        danger={isSubscribed(record.series)}
                    >
                        {isSubscribed(record.series) ? '已订' : '订阅'}
                    </Button>
                    <Button
                        size="small"
                        icon={<SendOutlined />}
                        onClick={() => record.series ? handleSendSeries(record.series) : message.warning('该书籍没有系列信息。')}
                        disabled={!record.series || loading || !isSubscribed(record.series)}
                        title='发送'
                        type={isSubscribed(record.series) ? 'primary' : 'default'}
                    >
                        发送
                    </Button>
                </Space>
            ),
        },
    ];

    return (
        <div className="container mx-auto px-4 py-6">
            <Row gutter={[16, 16]}>
                <Col span={24}>
                    <Title level={2}>书籍目录</Title>
                </Col>

                <Col span={24}>
                    <Space direction="vertical" style={{ width: '100%' }} size="middle">
                        <Row gutter={[16, 16]} align="bottom">
                            <Col xs={24} sm={12} md={8} lg={6}>
                                <Text>搜索标题</Text>
                                <Search
                                    placeholder="搜索标题..."
                                    value={localSearchTerm}
                                    onChange={(e) => setLocalSearchTerm(e.target.value)}
                                    onSearch={triggerSearch}
                                    enterButton={<SearchOutlined />}
                                    allowClear
                                />
                            </Col>
                        </Row>
                    </Space>
                </Col>

                <Col span={24}>
                    {loading && !books.length ? (
                        <div style={{ textAlign: 'center', padding: '50px' }}><Spin size="large" tip="Loading books..." /></div>
                    ) : (
                        <Table<Book>
                            columns={columns}
                            dataSource={books}
                            rowKey="id"
                            loading={loading}
                            pagination={{
                                current: currentPagination.page,
                                pageSize: currentPagination.pageSize,
                                total: total,
                                showSizeChanger: true,
                                pageSizeOptions: ['10', '20', '50', '100'],
                            }}
                            onChange={handleTableChange}
                        />
                    )}
                    {!loading && !books.length && !error && (
                        <Empty description="No books found matching your criteria." className="py-10" />
                    )}
                </Col>
            </Row>
        </div>
    );
};

export default BookListPage; 