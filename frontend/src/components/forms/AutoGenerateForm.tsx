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
        <div className="space-y-6">
          <div className="text-center mb-8">
            <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-2">
              Choose Your Data Source
            </h3>
            <p className="text-gray-600 dark:text-gray-400 salmon:text-orange-700">
              Select the type of data you want to use to generate your contract
            </p>
          </div>
          
          <div className="grid gap-4">
            <button
              type="button"
              className="group w-full p-6 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 salmon:from-orange-50 salmon:to-red-50 border-2 border-blue-200 dark:border-blue-700/50 salmon:border-orange-200 rounded-2xl hover:border-blue-300 dark:hover:border-blue-600 salmon:hover:border-orange-300 transition-all duration-200 hover:shadow-lg text-left"
              onClick={() => setSourceType('database')}
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-blue-500 dark:bg-blue-600 salmon:bg-orange-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                    </svg>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="font-bold text-lg text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-1">Database Schema</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 salmon:text-orange-700 mb-2">
                    Generate from CREATE TABLE statements or database schema definitions
                  </div>
                  <div className="text-xs text-blue-600 dark:text-blue-400 salmon:text-orange-600 font-medium">
                    Perfect for SQL databases • MySQL, PostgreSQL, SQLite
                  </div>
                </div>
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-gray-400 group-hover:text-blue-500 dark:group-hover:text-blue-400 salmon:group-hover:text-orange-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </button>

            <button
              type="button"
              className="group w-full p-6 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 salmon:from-orange-50 salmon:to-yellow-50 border-2 border-green-200 dark:border-green-700/50 salmon:border-orange-200 rounded-2xl hover:border-green-300 dark:hover:border-green-600 salmon:hover:border-orange-300 transition-all duration-200 hover:shadow-lg text-left"
              onClick={() => setSourceType('api')}
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-green-500 dark:bg-green-600 salmon:bg-orange-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                    </svg>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="font-bold text-lg text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-1">API Response</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 salmon:text-orange-700 mb-2">
                    Generate from JSON API responses with automatic field detection
                  </div>
                  <div className="text-xs text-green-600 dark:text-green-400 salmon:text-orange-600 font-medium">
                    Perfect for REST APIs • Handles nested objects and arrays
                  </div>
                </div>
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-gray-400 group-hover:text-green-500 dark:group-hover:text-green-400 salmon:group-hover:text-orange-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </button>

            <button
              type="button"
              className="group w-full p-6 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 salmon:from-orange-50 salmon:to-red-50 border-2 border-purple-200 dark:border-purple-700/50 salmon:border-orange-200 rounded-2xl hover:border-purple-300 dark:hover:border-purple-600 salmon:hover:border-orange-300 transition-all duration-200 hover:shadow-lg text-left"
              onClick={() => setSourceType('file')}
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-purple-500 dark:bg-purple-600 salmon:bg-orange-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="font-bold text-lg text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-1">File Upload</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 salmon:text-orange-700 mb-2">
                    Generate from CSV data or JSON file contents with headers
                  </div>
                  <div className="text-xs text-purple-600 dark:text-purple-400 salmon:text-orange-600 font-medium">
                    Perfect for data files • CSV with headers, JSON arrays
                  </div>
                </div>
                <div className="flex-shrink-0">
                  <svg className="w-5 h-5 text-gray-400 group-hover:text-purple-500 dark:group-hover:text-purple-400 salmon:group-hover:text-orange-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
          {sourceType === 'database' && (
            <>
              {/* Improved Example Schema Section */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 salmon:from-orange-50 salmon:to-red-50 border border-blue-200 dark:border-blue-700/50 salmon:border-orange-200 rounded-2xl p-6">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-blue-500 dark:bg-blue-600 salmon:bg-orange-500 rounded-xl flex items-center justify-center">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                      </svg>
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-2">
                      Need help getting started?
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300 salmon:text-orange-700 mb-4">
                      Load a sample database schema to see how it works. This will populate the form with a typical user table structure.
                    </p>
                    <div className="bg-white/60 dark:bg-gray-800/60 salmon:bg-orange-50/60 rounded-lg p-3 mb-4 border border-gray-200 dark:border-gray-600 salmon:border-orange-200">
                      <div className="text-xs font-mono text-gray-600 dark:text-gray-400 salmon:text-orange-700">
                        CREATE TABLE users (<br/>
                        &nbsp;&nbsp;id INTEGER PRIMARY KEY,<br/>
                        &nbsp;&nbsp;name VARCHAR(255) NOT NULL,<br/>
                        &nbsp;&nbsp;email VARCHAR(255) NOT NULL...<br/>
                      </div>
                    </div>
                    <Button
                      type="button"
                      variant="secondary"
                      size="sm"
                      onClick={loadDatabaseExample}
                      className="flex items-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Load Example Schema
                    </Button>
                  </div>
                </div>
              </div>
              
              <Input
                label="Table Name"
                {...register('table_name')}
                placeholder="Enter table name (e.g., users, products, orders)"
              />
              
              <Textarea
                label="Database Schema"
                {...register('source_data', { required: 'Schema is required' })}
                rows={12}
                placeholder="Paste your CREATE TABLE statement here..."
                className="font-mono text-sm"
                error={errors.source_data?.message}
                helperText="Paste a CREATE TABLE SQL statement or database schema definition"
              />
            </>
          )}

          {sourceType === 'api' && (
            <>
              {/* Improved Example API Section */}
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 salmon:from-orange-50 salmon:to-yellow-50 border border-green-200 dark:border-green-700/50 salmon:border-orange-200 rounded-2xl p-6">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-green-500 dark:bg-green-600 salmon:bg-orange-500 rounded-xl flex items-center justify-center">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                      </svg>
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-2">
                      API Response Example
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300 salmon:text-orange-700 mb-4">
                      Load a sample API response to understand the expected JSON structure. This shows a typical user profile with nested data.
                    </p>
                    <div className="bg-white/60 dark:bg-gray-800/60 salmon:bg-orange-50/60 rounded-lg p-3 mb-4 border border-gray-200 dark:border-gray-600 salmon:border-orange-200">
                      <div className="text-xs font-mono text-gray-600 dark:text-gray-400 salmon:text-orange-700">
                        &#123;<br/>
                        &nbsp;&nbsp;"id": 1,<br/>
                        &nbsp;&nbsp;"name": "John Doe",<br/>
                        &nbsp;&nbsp;"profile": &#123; "age": 30 &#125;,<br/>
                        &nbsp;&nbsp;"orders": [...]<br/>
                        &#125;
                      </div>
                    </div>
                    <Button
                      type="button"
                      variant="secondary"
                      size="sm"
                      onClick={loadApiExample}
                      className="flex items-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Load Example Response
                    </Button>
                  </div>
                </div>
              </div>
              
              <Input
                label="API Endpoint"
                {...register('endpoint_url')}
                placeholder="https://api.example.com/users/1"
                helperText="The URL endpoint that returns the JSON response"
              />
              
              <Textarea
                label="JSON Response"
                {...register('source_data', { required: 'JSON response is required' })}
                rows={12}
                placeholder="Paste your API JSON response here..."
                className="font-mono text-sm"
                error={errors.source_data?.message}
                helperText="Paste the complete JSON response from your API endpoint"
              />
            </>
          )}

          {sourceType === 'file' && (
            <>
              {/* Improved File Upload Section */}
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 salmon:from-orange-50 salmon:to-red-50 border border-purple-200 dark:border-purple-700/50 salmon:border-orange-200 rounded-2xl p-6">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-purple-500 dark:bg-purple-600 salmon:bg-orange-500 rounded-xl flex items-center justify-center">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 salmon:text-orange-900 mb-2">
                      File Data Format
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300 salmon:text-orange-700 mb-4">
                      Paste your CSV or JSON file contents below. The system will analyze the structure and generate appropriate field definitions.
                    </p>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                      <div className="bg-white/60 dark:bg-gray-800/60 salmon:bg-orange-50/60 rounded-lg p-3 border border-gray-200 dark:border-gray-600 salmon:border-orange-200">
                        <div className="text-xs font-semibold text-gray-700 dark:text-gray-300 salmon:text-orange-800 mb-1">CSV Format:</div>
                        <div className="text-xs font-mono text-gray-600 dark:text-gray-400 salmon:text-orange-700">
                          id,name,email<br/>
                          1,John,john@...<br/>
                          2,Jane,jane@...
                        </div>
                      </div>
                      <div className="bg-white/60 dark:bg-gray-800/60 salmon:bg-orange-50/60 rounded-lg p-3 border border-gray-200 dark:border-gray-600 salmon:border-orange-200">
                        <div className="text-xs font-semibold text-gray-700 dark:text-gray-300 salmon:text-orange-800 mb-1">JSON Array:</div>
                        <div className="text-xs font-mono text-gray-600 dark:text-gray-400 salmon:text-orange-700">
                          [&#123;"id":1,"name":"John"&#125;,<br/>
                          &nbsp;&#123;"id":2,"name":"Jane"&#125;]
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <Textarea
                label="CSV/JSON Data"
                {...register('source_data', { required: 'File data is required' })}
                rows={12}
                placeholder="Paste your CSV or JSON data here..."
                className="font-mono text-sm"
                error={errors.source_data?.message}
                helperText="Paste your CSV data with headers or JSON array of objects"
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
