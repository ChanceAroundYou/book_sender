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
    Tag,
    message,
} from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { User } from '@/types';

const { Title } = Typography;
const { Option } = Select;

interface UserForm extends Omit<User, 'id'> {
    password?: string;
}

const AdminUsers = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingUser, setEditingUser] = useState<User | null>(null);
    const [form] = Form.useForm<UserForm>();

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        setLoading(true);
        try {
            const data = await request.get<User[]>('/admin/users');
            setUsers(data);
        } catch (error) {
            // 错误处理由request拦截器统一处理
        } finally {
            setLoading(false);
        }
    };

    const handleEdit = (user: User) => {
        setEditingUser(user);
        form.setFieldsValue({
            ...user,
            password: '',
        });
        setModalVisible(true);
    };

    const handleDelete = async (id: string) => {
        try {
            await request.delete(`/admin/users/${id}`);
            message.success('用户已删除');
            setUsers(users.filter(user => user.id !== id));
        } catch (error) {
            // 错误处理由request拦截器统一处理
        }
    };

    const handleSubmit = async (values: UserForm) => {
        try {
            await request.put(`/admin/users/${editingUser?.id}`, values);
            message.success('用户信息已更新');
            setModalVisible(false);
            fetchUsers();
        } catch (error) {
            // 错误处理由request拦截器统一处理
        }
    };

    const columns: ColumnsType<User> = [
        {
            title: '用户名',
            dataIndex: 'username',
            key: 'username',
        },
        {
            title: '邮箱',
            dataIndex: 'email',
            key: 'email',
        },
        {
            title: '角色',
            dataIndex: 'role',
            key: 'role',
            render: (role: User['role']) => (
                <Tag color={role === 'admin' ? 'red' : 'blue'}>
                    {role === 'admin' ? '管理员' : '用户'}
                </Tag>
            ),
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
                    {record.role !== 'admin' && (
                        <Button
                            type="link"
                            danger
                            icon={<DeleteOutlined />}
                            onClick={() => handleDelete(record.id)}
                        >
                            删除
                        </Button>
                    )}
                </Space>
            ),
        },
    ];

    return (
        <div className="container mx-auto px-4">
            <Row gutter={[0, 24]}>
                <Col span={24}>
                    <Title level={2}>用户管理</Title>
                </Col>

                <Col span={24}>
                    <Table
                        columns={columns}
                        dataSource={users}
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
                title="编辑用户"
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
                        name="username"
                        label="用户名"
                        rules={[
                            { required: true, message: '请输入用户名' },
                            { min: 3, message: '用户名至少3个字符' },
                        ]}
                    >
                        <Input placeholder="请输入用户名" />
                    </Form.Item>

                    <Form.Item
                        name="email"
                        label="邮箱"
                        rules={[
                            { required: true, message: '请输入邮箱' },
                            { type: 'email', message: '请输入有效的邮箱地址' },
                        ]}
                    >
                        <Input placeholder="请输入邮箱" />
                    </Form.Item>

                    <Form.Item
                        name="role"
                        label="角色"
                        rules={[{ required: true, message: '请选择角色' }]}
                    >
                        <Select placeholder="请选择角色">
                            <Option value="user">用户</Option>
                            <Option value="admin">管理员</Option>
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="password"
                        label="密码"
                        extra="如不修改密码请留空"
                        rules={[
                            {
                                min: 6,
                                message: '密码至少6个字符',
                                validateTrigger: 'onChange',
                            },
                        ]}
                    >
                        <Input.Password placeholder="请输入新密码" />
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

export default AdminUsers; 