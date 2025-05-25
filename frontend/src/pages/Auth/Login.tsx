import { useState, useEffect } from 'react';
import { Form, Button, Typography, message, Alert } from 'antd';
import { useNavigate, Link } from 'react-router-dom';
import { loginUser } from '@/store/slices/authSlice';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import BaseInput from '@/components/base/BaseInput';
import { LoginParams } from '@/types';


const { Title, Text } = Typography;

const LoginPage = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();

    const { loading, error: authError, token } = useAppSelector((state: RootState) => state.auth);
    const [localError, setLocalError] = useState<string | null>(null);

    useEffect(() => {
        if (token) {
            navigate('/');
        }
    }, [token, navigate]);

    useEffect(() => {
        if (authError) {
            setLocalError(authError);
        }
    }, [authError]);

    const handleSubmit = async (values: LoginParams) => {
        setLocalError(null);
        try {
            const resultAction = await dispatch(loginUser(values));
            if (loginUser.fulfilled.match(resultAction)) {
                message.success('登录成功！');
            } else if (loginUser.rejected.match(resultAction)) {
            }
        } catch (error: any) {
            setLocalError('发生意外错误，请稍后重试');
        }
    };

    return (
        <>
            <div>
                <Title level={2} className="text-center mb-2">
                    欢迎回来
                </Title>
                <Text className="block text-center text-gray-600">
                    登录 Book Sender，继续您的阅读之旅
                </Text>
            </div>

            {localError && (
                <Alert
                    message={localError}
                    type="error"
                    showIcon
                    className="mb-4"
                    onClose={() => setLocalError(null)}
                    closable
                />
            )}

            <Form<LoginParams>
                layout="vertical"
                onFinish={handleSubmit}
                requiredMark={false}
                size="large"
            >
                <Form.Item
                    name="email"
                    label="邮箱"
                    rules={[
                        { required: true, message: '请输入邮箱' },
                        { type: 'email', message: '请输入有效的邮箱地址' }
                    ]}
                >
                    <BaseInput
                        placeholder="请输入邮箱"
                        autoComplete="email"
                    />
                </Form.Item>

                <Form.Item
                    name="password"
                    label="密码"
                    rules={[
                        { required: true, message: '请输入密码' },
                        { min: 6, message: '密码至少6个字符' }
                    ]}
                >
                    <BaseInput.Password
                        placeholder="请输入密码"
                        autoComplete="current-password"
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
                        登录
                    </Button>
                </Form.Item>

                <div className="flex justify-between items-center text-gray-600">
                    <Link to="/auth/register" className="text-primary hover:text-primary-dark">
                        注册账号
                    </Link>
                    <Link to="/auth/forgot-password" className="text-primary hover:text-primary-dark">
                        忘记密码？
                    </Link>
                </div>
            </Form>
        </>
    );
};

export default LoginPage; 