import { useState, useEffect } from 'react';
import {
    Row,
    Col,
    Typography,
    Table,
    Button,
    Space,
    Modal,
    Form,
    Input,
    Select,
    message,
} from 'antd';
import {
    EditOutlined,
    DeleteOutlined,
    DownloadOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { Book } from '@/types';
import dayjs from 'dayjs';

const { Title } = Typography;
const { Option } = Select;

interface BookForm {
    title: string;
    series: string;
    file_format: string;
    detail_link: string;
    download_link: string;
}

const AdminBooks = () => {
    const [books, setBooks] = useState<Book[]>([]);
    const [loading, setLoading] = useState(true);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingBook, setEditingBook] = useState<Book | null>(null);
    const [form] = Form.useForm<BookForm>();

    useEffect(() => {
        fetchBooks();
    }, []);

    const fetchBooks = async () => {
        setLoading(true);
        try {
            const response = await request.get('/admin/books');
            setBooks(response.data);
        } catch (error) {
            console.error('Failed to fetch books:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleEdit = (book: Book) => {
        setEditingBook(book);
        form.setFieldsValue({
            title: book.title,
            series: book.series,
            file_format: book.file_format,
            detail_link: book.detail_link,
            download_link: book.download_link,
        });
        setModalVisible(true);
    };

    const handleDelete = async (id: number) => {
        try {
            await request.delete(`/admin/books/${id}`);
            message.success('书籍已删除');
            setBooks(books.filter(book => book.id !== id));
        } catch (error) {
            console.error('Failed to delete book:', error);
        }
    };

    const handleSubmit = async (values: BookForm) => {
        try {
            if (editingBook) {
                await request.put(`/admin/books/${editingBook.id}`, values);
                message.success('书籍已更新');
            }
            setModalVisible(false);
            fetchBooks();
        } catch (error) {
            console.error('Failed to update book:', error);
        }
    };

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

    const columns: ColumnsType<Book> = [
        {
            title: '封面',
            dataIndex: 'cover_link',
            key: 'cover_link',
            width: 80,
            render: (cover) => (
                <img
                    src={cover}
                    alt="封面"
                    className="w-12 h-16 object-cover rounded"
                />
            ),
        },
        {
            title: '标题',
            dataIndex: 'title',
            key: 'title',
        },
        {
            title: '分类',
            dataIndex: 'category',
            key: 'category',
        },
        {
            title: '格式',
            dataIndex: 'file_format',
            key: 'file_format',
            render: (format) => format.toUpperCase(),
        },
        {
            title: '大小',
            dataIndex: 'file_size',
            key: 'file_size',
            render: (size) => formatFileSize(size),
        },
        {
            title: '发布日期',
            dataIndex: 'date',
            key: 'date',
            render: (date) => dayjs(date).format('YYYY-MM-DD'),
        },
        {
            title: '操作',
            key: 'action',
            render: (_, record) => (
                <Space>
                    <Button
                        type="link"
                        icon={<EditOutlined />}
                        onClick={() => handleEdit(record)}
                    >
                        编辑
                    </Button>
                    <Button
                        type="link"
                        icon={<DownloadOutlined />}
                        href={record.download_link}
                        target="_blank"
                    >
                        下载
                    </Button>
                    <Button
                        type="link"
                        danger
                        icon={<DeleteOutlined />}
                        onClick={() => handleDelete(record.id)}
                    >
                        删除
                    </Button>
                </Space>
            ),
        },
    ];

    return (
        <div className="container mx-auto px-4">
            <Row gutter={[0, 24]}>
                <Col span={24}>
                    <Title level={2}>书籍管理</Title>
                </Col>

                <Col span={24}>
                    <Table
                        columns={columns}
                        dataSource={books}
                        loading={loading}
                        rowKey="id"
                        pagination={{
                            showSizeChanger: true,
                            showTotal: (total) => `共 ${total} 条记录`,
                        }}
                    />
                </Col>
            </Row>

            <Modal
                title="编辑书籍"
                open={modalVisible}
                onCancel={() => setModalVisible(false)}
                footer={null}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleSubmit}
                >
                    <Form.Item
                        name="title"
                        label="标题"
                        rules={[{ required: true, message: '请输入标题' }]}
                    >
                        <Input placeholder="请输入标题" />
                    </Form.Item>

                    <Form.Item
                        name="category"
                        label="分类"
                        rules={[{ required: true, message: '请选择分类' }]}
                    >
                        <Select placeholder="请选择分类">
                            <Option value="economist_usa">The Economist USA</Option>
                            <Option value="economist_uk">The Economist UK</Option>
                            <Option value="economist_europe">The Economist Europe</Option>
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="file_format"
                        label="格式"
                        rules={[{ required: true, message: '请选择格式' }]}
                    >
                        <Select placeholder="请选择格式">
                            <Option value="pdf">PDF</Option>
                            <Option value="epub">EPUB</Option>
                            <Option value="mobi">MOBI</Option>
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="detail_link"
                        label="详情链接"
                        rules={[{ required: true, message: '请输入详情链接' }]}
                    >
                        <Input placeholder="请输入详情链接" />
                    </Form.Item>

                    <Form.Item
                        name="download_link"
                        label="下载链接"
                        rules={[{ required: true, message: '请输入下载链接' }]}
                    >
                        <Input placeholder="请输入下载链接" />
                    </Form.Item>

                    <Form.Item className="mb-0">
                        <Space className="w-full justify-end">
                            <Button onClick={() => setModalVisible(false)}>
                                取消
                            </Button>
                            <Button type="primary" htmlType="submit">
                                确定
                            </Button>
                        </Space>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default AdminBooks; 