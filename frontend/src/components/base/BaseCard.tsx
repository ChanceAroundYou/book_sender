import { Card } from 'antd';
import type { CardProps } from 'antd';
import classNames from 'classnames';

export interface BaseCardProps extends Omit<CardProps, 'variant'> {
    variant?: 'default' | 'hover' | 'shadow';
}

const BaseCard = ({ variant = 'default', className, bordered = true, ...props }: BaseCardProps) => {
    const cardClass = classNames(
        className,
        {
            'transition-all duration-300': true,
            'hover:shadow-md': variant === 'hover',
            'shadow-md': variant === 'shadow',
        }
    );

    // 根据 variant 设置合适的 bordered 属性
    const isOutlined = variant !== 'shadow';

    return <Card className={cardClass} bordered={isOutlined && bordered} {...props} />;
};

export default BaseCard; 