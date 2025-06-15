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
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      case 'inactive':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800/30 dark:text-gray-400';
      case 'deprecated':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800/30 dark:text-gray-400';
    }
  };

  return (
    <div className="group relative overflow-hidden theme-bg-card rounded-3xl theme-shadow-md hover:theme-shadow-xl transition-all duration-500 p-8 border theme-border-primary hover:scale-[1.02] slide-in backdrop-blur-sm bg-white/80 dark:bg-gray-900/80 salmon:bg-orange-50/80">
      {/* Gradient overlay on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-3xl"></div>
      
      <div className="relative z-10">
        <div className="flex justify-between items-start mb-6">
          <div className="flex-1">
            <h3 className="text-2xl font-bold theme-text-primary mb-2 group-hover:bg-gradient-to-r group-hover:from-blue-600 group-hover:to-purple-600 group-hover:bg-clip-text group-hover:text-transparent transition-all duration-300">
              {contract.name}
            </h3>
            <p className="text-sm theme-text-secondary font-semibold tracking-wide">
              v{contract.version}
            </p>
          </div>
          <span
            className={`px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider ${getStatusColor(
              contract.status
            )}`}
          >
            {contract.status}
          </span>
        </div>

        <div className="space-y-4 mb-8">
          <div className="flex items-center gap-3 p-4 theme-bg-secondary/50 rounded-2xl">
            <div className="w-10 h-10 rounded-xl theme-accent-primary/10 flex items-center justify-center">
              <svg className="w-5 h-5 theme-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <p className="text-sm theme-text-secondary">Total Fields</p>
              <p className="text-xl font-bold theme-text-primary">{contract.fields.length}</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3 p-4 theme-bg-secondary/50 rounded-2xl">
            <div className="w-10 h-10 rounded-xl theme-accent-primary/10 flex items-center justify-center">
              <svg className="w-5 h-5 theme-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 4v10m6-10v10m-6-4h.01M18 7h-.01M12 7h.01" />
              </svg>
            </div>
            <div>
              <p className="text-sm theme-text-secondary">Created</p>
              <p className="text-sm font-semibold theme-text-primary">
                {new Date(contract.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <Button size="sm" onClick={() => onView(contract)} className="flex items-center gap-2 flex-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            View
          </Button>
          <Button size="sm" variant="secondary" onClick={() => onEdit(contract)} className="flex items-center gap-2 flex-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </Button>
          <Button size="sm" variant="danger" onClick={() => onDelete(contract.id)} className="flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
};
