import { useState, useEffect } from 'react';
import { Row, Col, Typography, Switch, Form, Button, Select, message, Alert } from 'antd';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import { setTheme, setLanguage as setUiLanguage } from '@/store/slices/uiSlice';
// No backend calls for these settings for now, as API/types don't support user.preferences field for update
// import { updateUserAdmin } from '@/store/slices/userSlice';
// import { fetchCurrentUser } from '@/store/slices/authSlice';

const { Title } = Typography;
const { Option } = Select;

interface NotificationPrefsForm {
    emailNotifications: boolean;
    updateNotifications: boolean;
}

interface DisplayPrefsForm {
    theme: 'light' | 'dark';
    language: string; // Language code e.g., 'zh', 'en'
}

const UserSettingsPage = () => {
    const dispatch = useAppDispatch();
    const { theme: currentTheme, language: currentLanguage } = useAppSelector((state: RootState) => state.ui);
    // Loading state can be local if no backend calls are made for saving
    const [notifLoading, setNotifLoading] = useState(false);
    const [displayLoading, setDisplayLoading] = useState(false);
    const [localError, setLocalError] = useState<string | null>(null); // For any general errors or info

    const [notificationForm] = Form.useForm<NotificationPrefsForm>();
    const [displayForm] = Form.useForm<DisplayPrefsForm>();

    // Initialize forms with values from uiSlice (localStorage backed)
    useEffect(() => {
        notificationForm.setFieldsValue({
            emailNotifications: true, // Default, as not saved
            updateNotifications: true, // Default, as not saved
        });
        displayForm.setFieldsValue({
            theme: currentTheme,
            language: currentLanguage || 'zh', // Default to 'zh' if not set
        });
    }, [currentTheme, currentLanguage, notificationForm, displayForm]);

    const handleNotificationSubmit = async () => {
        setNotifLoading(true);
        setLocalError(null);
        // Simulate API call or just show message
        await new Promise(resolve => setTimeout(resolve, 500));
        message.info('Notification settings are currently not saved to the backend.');
        setNotifLoading(false);
    };

    const handleDisplaySubmit = async (values: DisplayPrefsForm) => {
        setDisplayLoading(true);
        setLocalError(null);
        try {
            // Dispatch actions to update UI state (backed by localStorage in uiSlice)
            if (values.theme !== currentTheme) {
                dispatch(setTheme(values.theme));
            }
            if (values.language !== currentLanguage) {
                dispatch(setUiLanguage(values.language));
            }
            await new Promise(resolve => setTimeout(resolve, 300)); // Simulate save
            message.success('Display settings updated!');
        } catch (error) {
            message.error('Failed to update display settings.');
        } finally {
            setDisplayLoading(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-6">
            <Row gutter={[16, 48]}> {/* Added gutter for spacing between columns */}
                <Col span={24}>
                    <Title level={2} className="text-center md:text-left">Settings</Title>
                </Col>

                {localError && (
                    <Col span={24}>
                        <Alert message={localError} type="error" showIcon closable onClose={() => setLocalError(null)} />
                    </Col>
                )}

                {/* Notification Settings */}
                <Col xs={24} md={12}>
                    <div className="max-w-md mx-auto md:mx-0">
                        <Title level={3} className="mb-6">Notification Settings</Title>
                        <Form<NotificationPrefsForm>
                            form={notificationForm}
                            layout="vertical"
                            onFinish={handleNotificationSubmit}
                        >
                            <Form.Item
                                label="Email Notifications"
                                name="emailNotifications"
                                valuePropName="checked"
                                help="Receive important email notifications (e.g., account security). Currently a UI-only setting."
                            >
                                <Switch loading={notifLoading} />
                            </Form.Item>

                            <Form.Item
                                label="Update Notifications"
                                name="updateNotifications"
                                valuePropName="checked"
                                help="Subscribe to notifications for new books and magazines. Currently a UI-only setting."
                            >
                                <Switch loading={notifLoading} />
                            </Form.Item>

                            <Form.Item>
                                <Button type="primary" htmlType="submit" loading={notifLoading}>
                                    Save Notification Settings
                                </Button>
                            </Form.Item>
                        </Form>
                    </div>
                </Col>

                {/* Display Settings */}
                <Col xs={24} md={12}>
                    <div className="max-w-md mx-auto md:mx-0">
                        <Title level={3} className="mb-6">Display Settings</Title>
                        <Form<DisplayPrefsForm>
                            form={displayForm}
                            layout="vertical"
                            onFinish={handleDisplaySubmit}
                        // initialValues are set by useEffect based on uiSlice state
                        >
                            <Form.Item name="theme" label="Theme">
                                <Select style={{ width: 120 }} loading={displayLoading} /* value={currentTheme} already handled by form */ >
                                    <Option value="light">Light</Option>
                                    <Option value="dark">Dark</Option>
                                </Select>
                            </Form.Item>

                            <Form.Item name="language" label="Language">
                                <Select style={{ width: 120 }} loading={displayLoading} /* value={currentLanguage} already handled by form */ >
                                    <Option value="zh">中文 (简体)</Option>
                                    <Option value="en">English</Option>
                                </Select>
                            </Form.Item>

                            <Form.Item>
                                <Button type="primary" htmlType="submit" loading={displayLoading}>
                                    Save Display Settings
                                </Button>
                            </Form.Item>
                        </Form>
                    </div>
                </Col>
            </Row>
        </div>
    );
};

export default UserSettingsPage; 