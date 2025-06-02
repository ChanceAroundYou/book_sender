import React from 'react';
import { Typography, Card, Row, Col, Statistic } from 'antd';
import { UserOutlined, BookOutlined, SolutionOutlined } from '@ant-design/icons';

const { Title } = Typography;

const AdminDashboard: React.FC = () => {
    // Dummy data for now - replace with actual data fetching
    const stats = {
        totalUsers: 150,
        totalBooks: 75,
        activeSubscriptions: 120,
    };

    return (
        <div>
            <Title level={2} style={{ marginBottom: '24px' }}>Admin Dashboard</Title>
            <Row gutter={16}>
                <Col span={8}>
                    <Card>
                        <Statistic
                            title="Total Users"
                            value={stats.totalUsers}
                            prefix={<UserOutlined />}
                        />
                    </Card>
                </Col>
                <Col span={8}>
                    <Card>
                        <Statistic
                            title="Total Books"
                            value={stats.totalBooks}
                            prefix={<BookOutlined />}
                        />
                    </Card>
                </Col>
                <Col span={8}>
                    <Card>
                        <Statistic
                            title="Active Subscriptions"
                            value={stats.activeSubscriptions}
                            prefix={<SolutionOutlined />}
                        />
                    </Card>
                </Col>
            </Row>
            {/* More dashboard elements can be added here */}
        </div>
    );
};

export default AdminDashboard; 