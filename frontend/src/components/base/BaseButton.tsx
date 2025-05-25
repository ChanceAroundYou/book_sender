import { Button as AntButton } from 'antd';
import type { ButtonProps as AntButtonProps } from 'antd';
import classNames from 'classnames';

export interface BaseButtonProps extends AntButtonProps {
    variant?: 'primary' | 'secondary' | 'text' | 'link';
    size?: 'small' | 'middle' | 'large';
}

const BaseButton = ({ variant = 'primary', className, ...props }: BaseButtonProps) => {
    const buttonClass = classNames(
        className,
        {
            'hover:opacity-90': true,
            'transition-all': true,
        }
    );

    return <AntButton className={buttonClass} {...props} />;
};

export default BaseButton; 