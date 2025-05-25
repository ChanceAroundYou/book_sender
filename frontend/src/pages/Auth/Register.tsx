import { useState, useEffect } from 'react';
import { Form, Button, Typography, message, Alert } from 'antd';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '@/store/slices/authSlice';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import BaseInput from '@/components/base/BaseInput';
import { RegisterParams } from '@/types';

const { Title, Text } = Typography;

interface RegisterFormValues extends RegisterParams {
    confirmPassword: string;
}

const RegisterPage = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();

    const { loading, error: authError } = useAppSelector((state: RootState) => state.auth);
    const [localError, setLocalError] = useState<string | null>(null);

    useEffect(() => {
        if (authError) {
            setLocalError(authError);
        }
    }, [authError]);

    const handleSubmit = async (values: RegisterFormValues) => {
        setLocalError(null);

        const registrationData: RegisterParams = {
            email: values.email,
            password: values.password,
            username: values.username,
        };

        try {
            const resultAction = await dispatch(registerUser(registrationData));

            if (registerUser.fulfilled.match(resultAction)) {
                message.success('注册成功！请登录。');
                navigate('/auth/login');
            } else if (registerUser.rejected.match(resultAction)) {
                // Error is already in authError, useEffect will pick it up.
                // Or set localError directly if specific message is preferred immediately:
                // setLocalError(resultAction.payload as string || '注册失败，请稍后重试');
            }
        } catch (error: any) {
            // This catch is for unexpected errors not handled by the thunk's rejectWithValue
            setLocalError('发生意外错误，请稍后重试');
        }
    };

    return (
        <>
            <div>
                <Title level={2} className="text-center mb-2">
                    创建新账号
                </Title>
                <Text className="block text-center text-gray-600">
                    加入 Book Sender，开启您的阅读之旅
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

            <Form<RegisterFormValues>
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
                    name="username"
                    label={
                        <span>
                            用户名
                            <Text type="secondary" className="ml-1">
                                (选填)
                            </Text>
                        </span>
                    }
                    rules={[
                        { min: 3, message: '用户名至少3个字符' },
                        { max: 20, message: '用户名最多20个字符' },
                        { pattern: /^[a-zA-Z0-9_-]+$/, message: '用户名只能包含字母、数字、下划线和连字符' }
                    ]}
                >
                    <BaseInput
                        placeholder="请输入用户名（选填）"
                        autoComplete="username"
                    />
                </Form.Item>

                <Form.Item
                    name="password"
                    label="密码"
                    rules={[
                        { required: true, message: '请输入密码' },
                        { min: 6, message: '密码至少6个字符' },
                        // { max: 32, message: '密码最多32个字符' }, // Max length can be omitted if not strict
                        // {
                        //     pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/,
                        //     message: '密码必须包含大小写字母和数字' // Simplified for now
                        // }
                    ]}
                >
                    <BaseInput.Password
                        placeholder="请输入密码"
                        autoComplete="new-password"
                    />
                </Form.Item>

                <Form.Item
                    name="confirmPassword"
                    label="确认密码"
                    dependencies={['password']}
                    rules={[
                        { required: true, message: '请确认密码' },
                        ({ getFieldValue }) => ({
                            validator(_, value) {
                                if (!value || getFieldValue('password') === value) {
                                    return Promise.resolve();
                                }
                                return Promise.reject(new Error('两次输入的密码不一致'));
                            },
                        }),
                    ]}
                >
                    <BaseInput.Password
                        placeholder="请确认密码"
                        autoComplete="new-password"
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
                        注册
                    </Button>
                </Form.Item>

                <div className="text-center text-gray-600">
                    已有账号？
                    <Link to="/auth/login" className="text-primary hover:text-primary-dark ml-1">
                        立即登录
                    </Link>
                </div>
            </Form>
        </>
    );
};

export default RegisterPage; 