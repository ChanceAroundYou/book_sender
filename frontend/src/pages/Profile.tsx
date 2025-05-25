import { useEffect } from 'react';
import { Card, Avatar, Tabs, List, Tag, Button, message, Typography } from 'antd';
import { UserOutlined, BookOutlined, BellOutlined, DeleteOutlined } from '@ant-design/icons';
import { RootState, useAppDispatch, useAppSelector } from '@/store';
import { fetchCurrentUser } from '@/store/slices/authSlice';
import { deleteUserSubscription } from '@/store/slices/userSlice';

const { TabPane } = Tabs;
const { Text } = Typography;

const ProfilePage = () => {
    const dispatch = useAppDispatch();
    const currentUser = useAppSelector((state: RootState) => state.auth.user);
    const authLoading = useAppSelector((state: RootState) => state.auth.loading);
    const subscriptions = currentUser?.subscriptions || [];
    const userBooks = currentUser?.books || [];

    useEffect(() => {
        if (!currentUser) {
            dispatch(fetchCurrentUser());
        }
    }, [dispatch, currentUser]);

    const handleUnsubscribe = async (series: string) => {
        if (!currentUser) return;
        try {
            const resultAction = await dispatch(deleteUserSubscription({ user_id: currentUser.id, series }));
            if (deleteUserSubscription.fulfilled.match(resultAction)) {
                message.success(`Unsubscribed from ${series} successfully.`);
                dispatch(fetchCurrentUser());
            } else if (deleteUserSubscription.rejected.match(resultAction)) {
                message.error(resultAction.payload || 'Failed to unsubscribe. Please try again.');
            }
        } catch (error) {
            message.error('Operation failed. Please try again.');
        }
    };

    return (
        <div className="p-4 md:p-6 max-w-4xl mx-auto">
            <Card className="mb-6" loading={authLoading}>
                {currentUser && (
                    <div className="flex items-center">
                        <Avatar size={64} icon={<UserOutlined />} src={undefined} />
                        <div className="ml-4">
                            <h2 className="text-xl font-bold">{currentUser.username}</h2>
                            <p className="text-gray-500">{currentUser.email}</p>
                            <Text type="secondary" style={{ fontSize: '12px' }}>Joined: {new Date(currentUser.created_at).toLocaleDateString()}</Text>
                        </div>
                    </div>
                )}
            </Card>

            <Tabs defaultActiveKey="1">
                <TabPane
                    tab={
                        <span>
                            <BellOutlined />
                            My Subscriptions ({subscriptions.length})
                        </span>
                    }
                    key="1"
                >
                    <List
                        loading={authLoading}
                        itemLayout="horizontal"
                        dataSource={subscriptions}
                        renderItem={(item) => (
                            <List.Item
                                actions={[
                                    <Button
                                        type="primary"
                                        danger
                                        icon={<DeleteOutlined />}
                                        onClick={() => handleUnsubscribe(item.series)}
                                        size="small"
                                    >
                                        Unsubscribe
                                    </Button>
                                ]}
                            >
                                <List.Item.Meta
                                    title={item.series}
                                    description={`Subscribed on: ${new Date(item.date).toLocaleDateString()}`}
                                />
                            </List.Item>
                        )}
                        locale={{ emptyText: 'No subscriptions yet.' }}
                    />
                </TabPane>
                <TabPane
                    tab={
                        <span>
                            <BookOutlined />
                            My Books ({userBooks.length})
                        </span>
                    }
                    key="2"
                >
                    <List
                        loading={authLoading}
                        itemLayout="horizontal"
                        dataSource={userBooks}
                        renderItem={(book) => (
                            <List.Item>
                                <List.Item.Meta
                                    title={book.title}
                                />
                                <Tag>{book.status || 'N/A'}</Tag>
                            </List.Item>
                        )}
                        locale={{ emptyText: 'No books associated with your account yet.' }}
                    />
                </TabPane>
            </Tabs>
        </div>
    );
};

export default ProfilePage; 