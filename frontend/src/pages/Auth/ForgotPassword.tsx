import { useState, useEffect } from 'react';
import { Form, Button, Typography, message, Alert } from 'antd';
import { Link } from 'react-router-dom';
import BaseInput from '@/components/base/BaseInput';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import { forgotPasswordThunk } from '@/store/slices/authSlice';

const { Title, Text } = Typography;

interface ForgotPasswordFormValues {
    email: string;
}

const ForgotPasswordPage = () => {
    const dispatch = useAppDispatch();
    const { loading, error: authError } = useAppSelector((state: RootState) => state.auth);
    const [sent, setSent] = useState(false);
    const [localError, setLocalError] = useState<string | null>(null);

    useEffect(() => {
        if (authError && !loading && !sent) {
            setLocalError(authError);
        }
    }, [authError, loading, sent]);

    const handleSubmit = async (values: ForgotPasswordFormValues) => {
        setLocalError(null);
        try {
            const resultAction = await dispatch(forgotPasswordThunk(values.email));
            if (forgotPasswordThunk.fulfilled.match(resultAction)) {
                setSent(true);
                message.success(resultAction.payload.message || '重置密码链接已发送到您的邮箱');
            } else if (forgotPasswordThunk.rejected.match(resultAction)) {
                // Error will be set in localError via useEffect
            }
        } catch (error: any) {
            setLocalError('发送重置链接失败，请稍后重试');
        }
    };

    return (
        <>
            <div>
                <Title level={2} className="text-center mb-2">
                    找回密码
                </Title>
                <Text className="block text-center text-gray-600">
                    我们将帮助您重置密码
                </Text>
            </div>

            {localError && !sent && (
                <Alert
                    message={localError}
                    type="error"
                    showIcon
                    className="mb-4"
                    onClose={() => setLocalError(null)}
                    closable
                />
            )}

            {sent ? (
                <div className="text-center space-y-4">
                    <Alert
                        message="重置链接已发送"
                        description={
                            <div className="text-gray-600">
                                重置密码链接已发送到您的邮箱，请查收。
                                <br />
                                如果没有收到邮件，请检查垃圾邮件文件夹。
                            </div>
                        }
                        type="success"
                        showIcon
                        className="mb-4"
                    />
                    <Button type="primary" block size="large">
                        <Link to="/auth/login" className="text-white">
                            返回登录
                        </Link>
                    </Button>
                </div>
            ) : (
                <Form<ForgotPasswordFormValues>
                    layout="vertical"
                    onFinish={handleSubmit}
                    requiredMark={false}
                    size="large"
                >
                    <Form.Item>
                        <Text className="text-gray-600">
                            请输入您注册时使用的邮箱地址，我们将向该邮箱发送重置密码的链接。
                        </Text>
                    </Form.Item>

                    <Form.Item
                        name="email"
                        label="邮箱"
                        rules={[
                            { required: true, message: '请输入邮箱' },
                            { type: 'email', message: '请输入有效的邮箱地址' },
                        ]}
                    >
                        <BaseInput
                            placeholder="请输入邮箱"
                            autoComplete="email"
                        />
                    </Form.Item>

                    <Form.Item className="mb-4">
                        <Button
                            type="primary"
                            htmlType="submit"
                            loading={loading}
                            block
                            size="large"
                            className="mt-4"
                        >
                            发送重置链接
                        </Button>
                    </Form.Item>

                    <div className="text-center">
                        <Link to="/auth/login" className="text-primary hover:text-primary-dark">
                            返回登录
                        </Link>
                    </div>
                </Form>
            )}
        </>
    );
};

export default ForgotPasswordPage; 