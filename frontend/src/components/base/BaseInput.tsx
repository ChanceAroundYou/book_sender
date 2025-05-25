import { Input } from 'antd';
import type { InputProps, InputRef, TextAreaProps, SearchProps } from 'antd/lib/input';
import classNames from 'classnames';
import { forwardRef } from 'react';

export interface BaseInputProps extends Omit<InputProps, 'status'> {
    error?: string;
}

export interface BaseTextAreaProps extends Omit<TextAreaProps, 'status'> {
    error?: string;
}

export interface BaseSearchProps extends Omit<SearchProps, 'status'> {
    error?: string;
}

const BaseInput = forwardRef<InputRef, BaseInputProps>(({ error, className, ...props }, ref) => {
    const inputClass = classNames(
        className,
        {
            'border-red-500': error,
            'hover:border-red-400': error,
            'focus:border-red-400': error,
            'focus:shadow-red-400/10': error,
        }
    );

    return (
        <div className="w-full">
            <Input ref={ref} className={inputClass} status={error ? 'error' : ''} {...props} />
            {error && <div className="mt-1 text-red-500 text-sm">{error}</div>}
        </div>
    );
});

const BasePassword = forwardRef<InputRef, BaseInputProps>((props, ref) => (
    <Input.Password ref={ref} {...props} />
));

const BaseTextArea = forwardRef<InputRef, BaseTextAreaProps>((props, ref) => (
    <Input.TextArea ref={ref} {...props} />
));

const BaseSearch = forwardRef<InputRef, BaseSearchProps>((props, ref) => (
    <Input.Search ref={ref} {...props} />
));

type CompoundedComponent = typeof BaseInput & {
    Password: typeof BasePassword;
    TextArea: typeof BaseTextArea;
    Search: typeof BaseSearch;
};

const CompoundedBaseInput = BaseInput as CompoundedComponent;
CompoundedBaseInput.Password = BasePassword;
CompoundedBaseInput.TextArea = BaseTextArea;
CompoundedBaseInput.Search = BaseSearch;

export default CompoundedBaseInput; 