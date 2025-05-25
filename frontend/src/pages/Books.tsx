import { useState, useEffect } from 'react';
import { Table, Input, Button, Space, message } from 'antd';
import { SearchOutlined, PlusOutlined, SendOutlined } from '@ant-design/icons';
import { Book, BookQueryParams, DistributeBookParams } from '@/types';
import { fetchBooks, distributeBookAction } from '@/store/slices/bookSlice';
import { RootState, useAppDispatch, useAppSelector } from '@/store';

const { Search } = Input;

const BooksPage = () => {
    const dispatch = useAppDispatch();
    const [searchText, setSearchText] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const pageSize = 10;

    const { items: books, total, loading, error } = useAppSelector((state: RootState) => state.book);

    useEffect(() => {
        const params: BookQueryParams = {
            skip: (currentPage - 1) * pageSize,
            limit: pageSize,
            title: searchText ? { operator: 'like', value: `%${searchText}%` } : undefined,
            order_by: 'date',
            order_desc: true
        };
        dispatch(fetchBooks(params));
    }, [dispatch, currentPage, searchText, pageSize]);

    useEffect(() => {
        if (error) {
            message.error(error);
        }
    }, [error]);

    const handleSearch = (value: string) => {
        setSearchText(value);
        setCurrentPage(1);
    };

    const handleSendBook = async (bookId: number, userEmail: string) => {
        const params: DistributeBookParams = {
            id: bookId,
            email: userEmail,
        };
        try {
            const resultAction = await dispatch(distributeBookAction(params));
            if (distributeBookAction.fulfilled.match(resultAction)) {
                if (resultAction.payload.message) {
                    message.success(resultAction.payload.message);
                }
                if (resultAction.payload.error) {
                    message.error(resultAction.payload.error);
                }
            } else if (distributeBookAction.rejected.match(resultAction)) {
                message.error(resultAction.payload || 'Failed to send book. Please try again.');
            }
        } catch (err: any) {
            message.error(err.message || 'An unexpected error occurred while sending the book.');
        }
    };

    const columns = [
        {
            title: '书名',
            dataIndex: 'title',
            key: 'title',
        },
        {
            title: '作者',
            dataIndex: 'author',
            key: 'author',
            render: (author: string | null) => author || 'N/A',
        },
        {
            title: '格式',
            dataIndex: 'file_format',
            key: 'file_format',
        },
        {
            title: '系列',
            dataIndex: 'series',
            key: 'series',
        },
        {
            title: '发布日期',
            dataIndex: 'date',
            key: 'date',
            render: (date: string) => new Date(date).toLocaleDateString(),
        },
        {
            title: '操作',
            key: 'action',
            render: (_: any, record: Book) => (
                <Space size="middle">
                    <Button
                        type="primary"
                        icon={<SendOutlined />}
                        onClick={() => handleSendBook(record.id, 'user@example.com')}
                    >
                        发送
                    </Button>
                </Space>
            ),
        },
    ];

    return (
        <div className="p-4 md:p-6">
            <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
                <Search
                    placeholder="搜索书籍 (标题)..."
                    allowClear
                    enterButton={<SearchOutlined />}
                    size="large"
                    className="w-full md:w-auto md:max-w-xs lg:max-w-sm"
                    onSearch={handleSearch}
                />
                <Button type="primary" icon={<PlusOutlined />}>
                    添加书籍
                </Button>
            </div>
            <Table
                columns={columns}
                dataSource={books}
                rowKey="id"
                loading={loading}
                pagination={{
                    current: currentPage,
                    pageSize,
                    total,
                    onChange: (page) => setCurrentPage(page),
                    showSizeChanger: false,
                }}
                scroll={{ x: 'max-content' }}
            />
        </div>
    );
};

export default BooksPage; 