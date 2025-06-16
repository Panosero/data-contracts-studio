import React, { forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(({
  label,
  error,
  helperText,
  className = '',
  ...props
}, ref) => {
  const inputClasses = `w-full px-4 py-3 bg-gray-800 text-gray-100 border border-gray-600 rounded-xl transition-all duration-200 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 placeholder-gray-400 ${
    error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : ''
  } ${className}`;

  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm font-medium text-gray-200">
          {label}
        </label>
      )}
      <input ref={ref} className={inputClasses} {...props} />
      {error && <p className="text-sm text-red-400">{error}</p>}
      {helperText && !error && <p className="text-sm text-gray-400">{helperText}</p>}
    </div>
  );
});

Input.displayName = 'Input';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(({
  label,
  error,
  helperText,
  className = '',
  ...props
}, ref) => {
  const textareaClasses = `w-full px-4 py-3 bg-gray-800 text-gray-100 border border-gray-600 rounded-xl transition-all duration-200 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 resize-none placeholder-gray-400 ${
    error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : ''
  } ${className}`;

  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm font-medium text-gray-200">
          {label}
        </label>
      )}
      <textarea ref={ref} className={textareaClasses} {...props} />
      {error && <p className="text-sm text-red-400">{error}</p>}
      {helperText && !error && <p className="text-sm text-gray-400">{helperText}</p>}
    </div>
  );
});

Textarea.displayName = 'Textarea';
