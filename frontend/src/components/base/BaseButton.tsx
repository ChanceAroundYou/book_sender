import { Button as AntButton } from 'antd';
import type { ButtonProps as AntButtonProps } from 'antd';
import classNames from 'classnames';

export interface BaseButtonProps extends Omit<AntButtonProps, 'variant'> {
    variant?: 'primary' | 'secondary' | 'text' | 'link';
    size?: 'small' | 'middle' | 'large';
}

const BaseButton = ({ variant = 'primary', className, type, ...props }: BaseButtonProps) => {
    const buttonClass = classNames(
        className,
        {
            'hover:opacity-90': true,
            'transition-all': true,
        }
    );

    // 将自定义的 variant 映射到 antd 的 type
    const buttonType = variant === 'primary' ? 'primary' :
        variant === 'secondary' ? 'default' :
            variant === 'text' ? 'text' :
                variant === 'link' ? 'link' : 'default';

    return <AntButton className={buttonClass} type={buttonType} {...props} />;
};

export default BaseButton; 