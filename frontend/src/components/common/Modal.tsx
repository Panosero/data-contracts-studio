import React from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
}) => {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 theme-bg-overlay backdrop-blur"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className={`relative bg-white dark:bg-gray-900 salmon:bg-white rounded-2xl w-full ${sizeClasses[size]} max-h-[90vh] flex flex-col theme-shadow-xl fade-in border border-gray-200 dark:border-gray-700 salmon:border-red-200`}>
        <div className="flex justify-between items-start p-8 pb-6 flex-shrink-0">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 salmon:text-gray-900">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-500 dark:text-gray-400 salmon:text-gray-600 hover:text-gray-700 dark:hover:text-gray-200 salmon:hover:text-gray-800 text-2xl transition-colors p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 salmon:hover:bg-red-100"
          >
            ×
          </button>
        </div>
        <div className="text-gray-900 dark:text-gray-100 salmon:text-gray-900 px-8 pb-8 overflow-y-auto custom-scrollbar">
          {children}
        </div>
      </div>
    </div>
  );
};
