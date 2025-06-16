import React, { useRef, useState } from 'react';

interface FileUploadProps {
  onFileLoad: (content: string, fileName: string) => void;
  accept?: string;
  maxSize?: number; // in MB
  className?: string;
  disabled?: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileLoad,
  accept = '.csv,.json,.txt',
  maxSize = 5,
  className = '',
  disabled = false,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    if (file.size > maxSize * 1024 * 1024) {
      alert(`File size must be less than ${maxSize}MB`);
      return;
    }

    setIsLoading(true);
    try {
      const content = await file.text();
      onFileLoad(content, file.name);
    } catch (error) {
      console.error('Error reading file:', error);
      alert('Error reading file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    if (disabled || isLoading) return;

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleClick = () => {
    if (!disabled && !isLoading) {
      fileInputRef.current?.click();
    }
  };

  return (
    <div className={`relative ${className}`}>
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        onChange={handleFileInput}
        className="hidden"
        disabled={disabled || isLoading}
      />
      
      <div
        className={`
          border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200
          ${isDragOver 
            ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20 salmon:bg-orange-50' 
            : 'border-gray-300 dark:border-gray-600 salmon:border-orange-300 hover:border-gray-400 dark:hover:border-gray-500 salmon:hover:border-orange-400'
          }
          ${disabled || isLoading ? 'opacity-50 cursor-not-allowed' : ''}
          ${isLoading ? 'animate-pulse' : ''}
        `}
        onDrop={handleDrop}
        onDragOver={(e) => {
          e.preventDefault();
          if (!disabled && !isLoading) setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onClick={handleClick}
      >
        {isLoading ? (
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-gray-600 dark:text-gray-400">Processing file...</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 salmon:bg-orange-100 rounded-2xl flex items-center justify-center">
              <svg 
                className="w-8 h-8 text-gray-500 dark:text-gray-400 salmon:text-orange-500" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" 
                />
              </svg>
            </div>
            
            <div>
              <p className="text-lg font-semibold text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-1">
                Drop your file here
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 salmon:text-orange-700 mb-2">
                or click to browse files
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-500 salmon:text-orange-600">
                Supports CSV, JSON, TXT files up to {maxSize}MB
              </p>
            </div>
            
            <div className="bg-blue-50 dark:bg-blue-900/20 salmon:bg-orange-50 border border-blue-200 dark:border-blue-700 salmon:border-orange-200 rounded-lg px-4 py-2">
              <p className="text-xs text-blue-700 dark:text-blue-300 salmon:text-orange-700 font-medium">
                💡 Tip: CSV files should include headers in the first row
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
