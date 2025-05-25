import { Card, Form, Select, DatePicker, Space, Button } from 'antd';
import type { SelectProps } from 'antd';

const { RangePicker } = DatePicker;

export interface BookFilterProps {
    categories: SelectProps['options'];
    languages: SelectProps['options'];
    formats: SelectProps['options'];
    onFilter: (values: any) => void;
    onReset?: () => void;
}

const BookFilter = ({
    categories,
    languages,
    formats,
    onFilter,
    onReset,
}: BookFilterProps) => {
    const [form] = Form.useForm();

    const handleReset = () => {
        form.resetFields();
        onReset?.();
    };

    return (
        <Card title="筛选">
            <Form
                form={form}
                layout="vertical"
                onFinish={onFilter}
            >
                <Form.Item name="category" label="分类">
                    <Select
                        allowClear
                        placeholder="选择分类"
                        options={categories}
                    />
                </Form.Item>

                <Form.Item name="language" label="语言">
                    <Select
                        allowClear
                        placeholder="选择语言"
                        options={languages}
                    />
                </Form.Item>

                <Form.Item name="format" label="格式">
                    <Select
                        allowClear
                        placeholder="选择格式"
                        options={formats}
                    />
                </Form.Item>

                <Form.Item name="dateRange" label="发布时间">
                    <RangePicker style={{ width: '100%' }} />
                </Form.Item>

                <Space>
                    <Button type="primary" htmlType="submit">
                        应用筛选
                    </Button>
                    <Button onClick={handleReset}>
                        重置
                    </Button>
                </Space>
            </Form>
        </Card>
    );
};

export default BookFilter; 