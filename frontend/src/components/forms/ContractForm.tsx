import React, { useState, useEffect } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { DataContractCreate, Field } from '../../types/contract';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Modal } from '../common/Modal';

interface ContractFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (contract: DataContractCreate) => void;
  initialData?: Partial<DataContractCreate>;
  isLoading?: boolean;
}

export const ContractForm: React.FC<ContractFormProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  isLoading = false,
}) => {
  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<DataContractCreate>({
    defaultValues: {
      name: initialData?.name || '',
      version: initialData?.version || '1.0.0',
      status: initialData?.status || 'active',
      fields: initialData?.fields || [{ name: '', type: 'string', required: true }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'fields',
  });

  // Reset form when initialData changes (for editing)
  useEffect(() => {
    if (initialData) {
      reset({
        name: initialData.name || '',
        version: initialData.version || '1.0.0',
        status: initialData.status || 'active',
        fields: initialData.fields || [{ name: '', type: 'string', required: true }],
      });
    }
  }, [initialData, reset]);

  const fieldTypes = [
    'string',
    'integer',
    'number',
    'boolean',
    'date',
    'datetime',
    'array',
    'object',
  ];

  const handleFormSubmit = (data: DataContractCreate) => {
    onSubmit(data);
    reset();
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Modal 
      isOpen={isOpen} 
      onClose={handleClose} 
      title={initialData ? `Edit Contract: ${initialData.name}` : "Create Data Contract"} 
      size="lg"
    >
      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Contract Name"
            {...register('name', { required: 'Contract name is required' })}
            error={errors.name?.message}
          />
          <Input
            label="Version"
            {...register('version', {
              required: 'Version is required',
              pattern: {
                value: /^\d+\.\d+\.\d+$/,
                message: 'Version must be in format x.y.z',
              },
            })}
            error={errors.version?.message}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-800 dark:text-gray-200 salmon:text-gray-900 mb-1">
            Status
          </label>
          <select
            {...register('status')}
            className="w-full px-4 py-2 bg-white dark:bg-gray-800 salmon:bg-white text-gray-900 dark:text-gray-100 salmon:text-gray-900 border border-gray-300 dark:border-gray-600 salmon:border-red-300 rounded-lg focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 salmon:focus:border-red-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-blue-400/20 salmon:focus:ring-red-500/20"
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="deprecated">Deprecated</option>
          </select>
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <label className="text-sm font-medium text-gray-800 dark:text-gray-200 salmon:text-gray-900">Fields</label>
            <Button
              type="button"
              size="sm"
              onClick={() => append({ name: '', type: 'string', required: true })}
            >
              Add Field
            </Button>
          </div>

          <div className="space-y-4">
            {fields.map((field, index) => (
              <div key={field.id} className="p-6 border border-gray-600 bg-gray-800 rounded-lg">
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                  <div className="lg:col-span-1">
                    <Input
                      label="Field Name"
                      {...register(`fields.${index}.name`, {
                        required: 'Field name is required',
                      })}
                      error={errors.fields?.[index]?.name?.message}
                    />
                  </div>
                  
                  <div className="lg:col-span-1">
                    <label className="block text-sm font-medium text-gray-200 mb-2">
                      Type
                    </label>
                    <select
                      {...register(`fields.${index}.type`)}
                      className="w-full px-4 py-3 bg-gray-700 text-gray-100 border border-gray-500 rounded-xl focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 transition-all duration-200"
                    >
                      {fieldTypes.map((type) => (
                        <option key={type} value={type}>
                          {type}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="lg:col-span-1 flex flex-col justify-center">
                    <label className="block text-sm font-medium text-gray-200 mb-2">
                      Required
                    </label>
                    <label className="flex items-center p-3 bg-gray-700 rounded-xl border border-gray-600 cursor-pointer hover:bg-gray-600 transition-colors">
                      <input
                        type="checkbox"
                        {...register(`fields.${index}.required`)}
                        className="w-5 h-5 text-blue-600 bg-gray-600 border-gray-500 rounded focus:ring-blue-500 focus:ring-2"
                      />
                      <span className="ml-3 text-sm font-medium text-gray-200">
                        {/* Check if field is required by getting the current value */}
                        Required Field
                      </span>
                    </label>
                  </div>

                  <div className="lg:col-span-1 flex items-end justify-end">
                    {fields.length > 1 && (
                      <Button
                        type="button"
                        size="sm"
                        variant="danger"
                        onClick={() => remove(index)}
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                </div>

                <div className="mt-2">
                  <Input
                    label="Description (optional)"
                    {...register(`fields.${index}.description`)}
                    placeholder="Describe this field..."
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-4 justify-end">
          <Button type="button" variant="secondary" onClick={handleClose}>
            Cancel
          </Button>
          <Button type="submit" isLoading={isLoading}>
            {initialData ? 'Update Contract' : 'Create Contract'}
          </Button>
        </div>
      </form>
    </Modal>
  );
};
