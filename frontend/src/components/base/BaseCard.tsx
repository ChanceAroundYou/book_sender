import { Card } from 'antd';
import type { CardProps } from 'antd';
import classNames from 'classnames';

export interface BaseCardProps extends CardProps {
    variant?: 'default' | 'hover' | 'shadow';
}

const BaseCard = ({ variant = 'default', className, ...props }: BaseCardProps) => {
    const cardClass = classNames(
        className,
        {
            'transition-all duration-300': true,
            'hover:shadow-md': variant === 'hover',
            'shadow-md': variant === 'shadow',
        }
    );

    return <Card className={cardClass} {...props} />;
};

export default BaseCard; 