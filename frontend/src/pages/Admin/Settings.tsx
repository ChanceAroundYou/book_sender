import { Row, Col, Typography, Empty, Alert } from 'antd';

const { Title, Paragraph } = Typography;

const AdminSettingsPage = () => {
    return (
        <div className="container mx-auto px-4 py-8">
            <Row gutter={[0, 24]}>
                <Col span={24}>
                    <Title level={2} className="mb-4">System Settings</Title>
                    <Alert
                        message="Feature Not Available"
                        description={
                            <Paragraph>
                                System-wide settings are not yet configurable through this interface.
                                This functionality requires backend API support which is currently not defined.
                                <br />
                                Please refer to server-side configurations or documentation for these settings.
                            </Paragraph>
                        }
                        type="info"
                        showIcon
                    />
                </Col>

                {/* 
                <Col span={24}>
                    <div className="max-w-2xl">
                        <Empty description="System settings configuration is not yet available." />
                    </div>
                </Col> 
                */}
            </Row>
        </div>
    );
};

export default AdminSettingsPage; 