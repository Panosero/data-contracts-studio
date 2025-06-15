import React from 'react';
import { DataContract } from '../../types/contract';
import { Button } from '../common/Button';

interface ContractCardProps {
  contract: DataContract;
  onEdit: (contract: DataContract) => void;
  onDelete: (id: number) => void;
  onView: (contract: DataContract) => void;
}

export const ContractCard: React.FC<ContractCardProps> = ({
  contract,
  onEdit,
  onDelete,
  onView,
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'inactive':
        return 'bg-gray-100 text-gray-800';
      case 'deprecated':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-800">{contract.name}</h3>
          <p className="text-sm text-gray-500">Version {contract.version}</p>
        </div>
        <span
          className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
            contract.status
          )}`}
        >
          {contract.status}
        </span>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-600">
          <span className="font-medium">{contract.fields.length}</span> fields
        </p>
        <p className="text-xs text-gray-500">
          Created: {new Date(contract.created_at).toLocaleDateString()}
        </p>
      </div>

      <div className="flex gap-2">
        <Button size="sm" onClick={() => onView(contract)}>
          View
        </Button>
        <Button size="sm" variant="secondary" onClick={() => onEdit(contract)}>
          Edit
        </Button>
        <Button size="sm" variant="danger" onClick={() => onDelete(contract.id)}>
          Delete
        </Button>
      </div>
    </div>
  );
};
