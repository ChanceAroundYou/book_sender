import { useState, useEffect } from 'react';
import { Form, Button, Typography, message, Alert } from 'antd';
import { useAppDispatch, useAppSelector, RootState } from '@/store';
import { updateUserAdmin } from '@/store/slices/userSlice';
import { fetchCurrentUser } from '@/store/slices/authSlice';
import BaseInput from '@/components/base/BaseInput';
import type { UpdateUserParams } from '@/types';

const { Title } = Typography;

interface ProfileFormValues {
    username: string;
    email: string;
    currentPassword?: string;
    newPassword?: string;
    confirmPassword?: string;
}

const UserProfileEditPage = () => {
    const dispatch = useAppDispatch();
    const { user: currentUser, loading: authLoading, error: authError } = useAppSelector((state: RootState) => state.auth);
    const { loading: updateLoading, error: updateError } = useAppSelector((state: RootState) => state.user);

    const [isFormChanged, setIsFormChanged] = useState(false);
    const [form] = Form.useForm<ProfileFormValues>();
    const [localError, setLocalError] = useState<string | null>(null);

    useEffect(() => {
        if (!currentUser) {
            dispatch(fetchCurrentUser());
        }
    }, [dispatch, currentUser]);

    useEffect(() => {
        if (currentUser) {
            form.setFieldsValue({
                username: currentUser.username,
                email: currentUser.email,
                currentPassword: '',
                newPassword: '',
                confirmPassword: '',
            });
        }
    }, [currentUser, form]);

    useEffect(() => {
        // Display error from userSlice update operation or authSlice fetch operation
        let errorToShow: string | null = null;
        if (updateError) {
            errorToShow = updateError;
        } else if (authError && !updateLoading) {
            // authError is string | null. If it's a string, use it.
            errorToShow = authError;
        }

        if (errorToShow) {
            setLocalError(errorToShow);
        } else {
            // Potentially clear localError if global errors are resolved and no new one is set
            // setLocalError(null); // Uncomment if this behavior is desired
        }
    }, [updateError, authError, updateLoading]);

    const handleFormChange = () => {
        const currentValues = form.getFieldsValue();
        const initialValues = {
            username: currentUser?.username,
            email: currentUser?.email,
        };
        const isBasicInfoChanged =
            currentValues.username !== initialValues.username ||
            currentValues.email !== initialValues.email;
        const isPasswordEntered = !!currentValues.newPassword;
        setIsFormChanged(isBasicInfoChanged || isPasswordEntered);
    };

    const handleSubmit = async (values: ProfileFormValues) => {


        if (!currentUser) return;
        setLocalError(null);

        const paramsToUpdate: UpdateUserParams = {
            user_id: currentUser.id,
            username: values.username,
            email: values.email,
        };

        if (values.newPassword && values.newPassword === values.confirmPassword) {
            paramsToUpdate.password = values.newPassword;
        } else if (values.newPassword && values.newPassword !== values.confirmPassword) {
            setLocalError('New passwords do not match.');
            return;
        }

        try {
            const resultAction = await dispatch(updateUserAdmin(paramsToUpdate));
            if (updateUserAdmin.fulfilled.match(resultAction)) {
                message.success('个人资料更新成功');
                dispatch(fetchCurrentUser());
                form.setFieldsValue({
                    currentPassword: '',
                    newPassword: '',
                    confirmPassword: '',
                });
                setIsFormChanged(false);
            } else if (updateUserAdmin.rejected.match(resultAction)) {
            }
        } catch (err: any) {
            setLocalError('An unexpected error occurred.');
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-4 md:p-6">
            <Title level={2} className="mb-8 text-center">个人资料</Title>

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

            <Form<ProfileFormValues>
                form={form}
                layout="vertical"
                onFinish={handleSubmit}
                onValuesChange={handleFormChange}
                requiredMark={false}
            >
                <Form.Item
                    name="username"
                    label="用户名"
                    rules={[
                        { required: true, message: '请输入用户名' },
                        { min: 3, message: '用户名至少3个字符' },
                    ]}
                >
                    <BaseInput
                        placeholder={`当前用户名`}
                        autoComplete="username"
                    // defaultValue={currentUser?.username}
                    />
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
                        placeholder={`当前邮箱`}
                        autoComplete="email"
                    // defaultValue={currentUser?.email}
                    />
                </Form.Item>

                <Title level={4} className="mt-8 mb-4">修改密码</Title>

                <Form.Item
                    name="currentPassword"
                    label="当前密码"
                    rules={[
                        ({ getFieldValue }) => ({
                            validator(_, value) {
                                if (getFieldValue('newPassword') && !value) {
                                    return Promise.reject(new Error('如果要修改密码，请输入当前密码'));
                                }
                                return Promise.resolve();
                            },
                        })
                    ]}
                >
                    <BaseInput.Password placeholder="请输入当前密码 (如需修改密码)" autoComplete="current-password" />
                </Form.Item>

                <Form.Item
                    name="newPassword"
                    label="新密码"
                    rules={[
                        ({ getFieldValue }) => ({
                            validator(_, value) {
                                if (value && value.length < 6) {
                                    return Promise.reject(new Error('新密码至少6个字符'));
                                }
                                return Promise.resolve();
                            },
                        })
                    ]}
                >
                    <BaseInput.Password placeholder="请输入新密码 (至少6位)" autoComplete="new-password" />
                </Form.Item>

                <Form.Item
                    name="confirmPassword"
                    label="确认新密码"
                    dependencies={['newPassword']}
                    rules={[
                        ({ getFieldValue }) => ({
                            validator(_, value) {
                                if (getFieldValue('newPassword') && !value) {
                                    return Promise.reject(new Error('请确认新密码'));
                                }
                                if (value && getFieldValue('newPassword') !== value) {
                                    return Promise.reject(new Error('两次输入的密码不一致'));
                                }
                                return Promise.resolve();
                            },
                        }),
                    ]}
                >
                    <BaseInput.Password placeholder="请确认新密码" autoComplete="new-password" />
                </Form.Item>

                <Form.Item className="mt-8">
                    <Button
                        type="primary"
                        htmlType="submit"
                        loading={updateLoading || authLoading}
                        disabled={!isFormChanged || updateLoading || authLoading}
                        block
                        size="large"
                    >
                        保存修改
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default UserProfileEditPage; 