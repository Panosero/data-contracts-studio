import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { AutoGenerateRequest } from '../../types/contract';
import { Button } from '../common/Button';
import { Input, Textarea } from '../common/Input';
import { Modal } from '../common/Modal';

interface AutoGenerateFormProps {
  isOpen: boolean;
  onClose: () => void;
  onGenerate: (request: AutoGenerateRequest) => void;
  isLoading?: boolean;
}

export const AutoGenerateForm: React.FC<AutoGenerateFormProps> = ({
  isOpen,
  onClose,
  onGenerate,
  isLoading = false,
}) => {
  const [sourceType, setSourceType] = useState<'database' | 'api' | 'file' | null>(null);
  
  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<AutoGenerateRequest>();

  const handleFormSubmit = (data: AutoGenerateRequest) => {
    onGenerate({ ...data, source_type: sourceType! });
  };

  const handleClose = () => {
    setSourceType(null);
    reset();
    onClose();
  };

  const loadDatabaseExample = () => {
    const exampleSchema = `CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`;
    setValue('source_data', exampleSchema);
    setValue('table_name', 'users');
  };

  const loadApiExample = () => {
    const exampleResponse = `{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "profile": {
    "age": 30,
    "city": "New York"
  },
  "orders": [
    {
      "id": 1,
      "total": 99.99,
      "date": "2023-01-01"
    }
  ]
}`;
    setValue('source_data', exampleResponse);
    setValue('endpoint_url', 'https://api.example.com/users/1');
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Auto-Generate Contract" size="lg">
      {!sourceType ? (
        <div className="space-y-4">
          <Button
            className="w-full p-4 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-all flex items-center gap-3"
            onClick={() => setSourceType('database')}
          >
            <span>🗄️</span>
            <div className="text-left">
              <div className="font-semibold">Database Schema</div>
              <div className="text-sm">Import from SQL table</div>
            </div>
          </Button>
          
          <Button
            className="w-full p-4 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-all flex items-center gap-3"
            onClick={() => setSourceType('api')}
          >
            <span>⚡</span>
            <div className="text-left">
              <div className="font-semibold">REST API</div>
              <div className="text-sm">Import from API response</div>
            </div>
          </Button>
          
          <Button
            className="w-full p-4 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition-all flex items-center gap-3"
            onClick={() => setSourceType('file')}
          >
            <span>📄</span>
            <div className="text-left">
              <div className="font-semibold">File Upload</div>
              <div className="text-sm">Import from CSV/JSON</div>
            </div>
          </Button>
        </div>
      ) : (
        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
          {sourceType === 'database' && (
            <>
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  onClick={loadDatabaseExample}
                >
                  Load Example Schema
                </Button>
              </div>
              
              <Input
                label="Table Name"
                {...register('table_name')}
                placeholder="Enter table name"
              />
              
              <Textarea
                label="Database Schema"
                {...register('source_data', { required: 'Schema is required' })}
                rows={10}
                placeholder="Paste your CREATE TABLE statement here..."
                className="font-mono text-sm"
                error={errors.source_data?.message}
              />
            </>
          )}

          {sourceType === 'api' && (
            <>
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  onClick={loadApiExample}
                >
                  Load Example Response
                </Button>
              </div>
              
              <Input
                label="API Endpoint"
                {...register('endpoint_url')}
                placeholder="https://api.example.com/users"
              />
              
              <Textarea
                label="JSON Response"
                {...register('source_data', { required: 'JSON response is required' })}
                rows={10}
                placeholder="Paste JSON response here..."
                className="font-mono text-sm"
                error={errors.source_data?.message}
              />
            </>
          )}

          {sourceType === 'file' && (
            <>
              <Textarea
                label="CSV/JSON Data"
                {...register('source_data', { required: 'File data is required' })}
                rows={10}
                placeholder="Paste your CSV or JSON data here..."
                className="font-mono text-sm"
                error={errors.source_data?.message}
              />
            </>
          )}

          <div className="flex gap-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setSourceType(null)}
            >
              Back
            </Button>
            <Button type="submit" isLoading={isLoading}>
              Generate Contract
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
};
