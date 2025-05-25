import { useEffect } from 'react';
import { Row, Col, Card, Statistic, Typography, Spin, Alert } from 'antd';
import {
    BookOutlined,
    UserOutlined,
    CarryOutOutlined,
    SyncOutlined,
    ExclamationCircleOutlined,
} from '@ant-design/icons';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import { fetchBooks } from '@/store/slices/bookSlice';
import { fetchUsers } from '@/store/slices/userSlice';
import { fetchTaskStatusSummary } from '@/store/slices/taskSlice';
import type { Task } from '@/types';

const { Title } = Typography;

const AdminDashboard = () => {
    const dispatch = useAppDispatch();

    const { total: totalBooks, loading: booksLoading, error: booksError } = useAppSelector((state: RootState) => state.book);
    const { totalUsers, loading: usersLoading, error: usersError } = useAppSelector((state: RootState) => state.user);
    const { statusSummary, loading: tasksLoading, error: tasksError } = useAppSelector((state: RootState) => state.task);

    useEffect(() => {
        if (totalBooks === 0) dispatch(fetchBooks({ limit: 1, skip: 0 }));
        if (totalUsers === 0) dispatch(fetchUsers({ limit: 1, skip: 0 }));
        dispatch(fetchTaskStatusSummary());
    }, [dispatch, totalBooks, totalUsers]);

    const overallLoading = booksLoading || usersLoading || tasksLoading;

    const getTaskCount = (status: Task['status']): number => statusSummary?.[status] || 0;

    return (
        <div className="container mx-auto px-4 py-6">
            <Row gutter={[0, 32]}>
                <Col span={24}>
                    <Title level={2} className="mb-6">Admin Dashboard</Title>
                </Col>

                {booksError && <Col span={24}><Alert message={`Error loading book stats: ${booksError}`} type="error" showIcon /></Col>}
                {usersError && <Col span={24}><Alert message={`Error loading user stats: ${usersError}`} type="error" showIcon /></Col>}
                {tasksError && <Col span={24}><Alert message={`Error loading task stats: ${tasksError}`} type="error" showIcon /></Col>}

                <Col span={24}>
                    <Title level={3} className="mb-4">Overall Statistics</Title>
                    <Row gutter={[16, 16]}>
                        <Col xs={24} sm={12} lg={6}>
                            <Card loading={booksLoading && totalBooks === 0}>
                                <Statistic
                                    title="Total Books"
                                    value={totalBooks}
                                    prefix={<BookOutlined />}
                                />
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} lg={6}>
                            <Card loading={usersLoading && totalUsers === 0}>
                                <Statistic
                                    title="Total Users"
                                    value={totalUsers}
                                    prefix={<UserOutlined />}
                                />
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} lg={6}>
                            <Card loading={overallLoading}>
                                <Statistic
                                    title="Total Downloads (N/A)"
                                    value="-"
                                    prefix={<UserOutlined style={{ color: '#ccc' }} />}
                                    valueStyle={{ color: '#ccc' }}
                                />
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} lg={6}>
                            <Card loading={tasksLoading}>
                                <Statistic
                                    title="Active Tasks (Started)"
                                    value={getTaskCount('started')}
                                    prefix={<SyncOutlined spin />}
                                />
                            </Card>
                        </Col>
                    </Row>
                </Col>

                <Col span={24}>
                    <Title level={3} className="mb-4">Task Status Overview</Title>
                    <Row gutter={[16, 16]}>
                        <Col xs={24} sm={12} md={6} lg={4}>
                            <Card loading={tasksLoading}>
                                <Statistic title="Pending Tasks" value={getTaskCount('pending')} prefix={<SyncOutlined />} />
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} md={6} lg={4}>
                            <Card loading={tasksLoading}>
                                <Statistic title="Succeeded Tasks" value={getTaskCount('success')} prefix={<CarryOutOutlined style={{ color: 'green' }} />} />
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} md={6} lg={4}>
                            <Card loading={tasksLoading}>
                                <Statistic title="Failed Tasks" value={getTaskCount('failure')} prefix={<ExclamationCircleOutlined style={{ color: 'red' }} />} />
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} md={6} lg={4}>
                            <Card loading={tasksLoading}>
                                <Statistic title="Tasks for Retry" value={getTaskCount('retry')} prefix={<SyncOutlined style={{ color: 'orange' }} />} />
                            </Card>
                        </Col>
                    </Row>
                </Col>

                <Col span={24}>
                    <Title level={3} className="mb-4">Today's Data (Not Implemented)</Title>
                    <Row gutter={[16, 16]}>
                        <Col xs={24} sm={12} lg={8}>
                            <Card><Statistic title="Today's New Books" value="N/A" prefix={<BookOutlined />} /></Card>
                        </Col>
                        <Col xs={24} sm={12} lg={8}>
                            <Card><Statistic title="Today's New Users" value="N/A" prefix={<UserOutlined />} /></Card>
                        </Col>
                        <Col xs={24} sm={12} lg={8}>
                            <Card><Statistic title="Today's Downloads" value="N/A" prefix={<UserOutlined />} /></Card>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </div>
    );
};

export default AdminDashboard; 