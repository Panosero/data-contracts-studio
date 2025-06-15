import React, { useState } from 'react';
import { useContracts, useCreateContract, useUpdateContract, useDeleteContract, useAutoGenerateFields } from '../hooks/useContracts';
import { ContractCard } from '../components/contracts/ContractCard';
import { ContractForm } from '../components/forms/ContractForm';
import { AutoGenerateForm } from '../components/forms/AutoGenerateForm';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { Modal } from '../components/common/Modal';
import { DataContract, DataContractCreate, AutoGenerateRequest } from '../types/contract';

export const HomePage: React.FC = () => {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<string>('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showAutoGenerate, setShowAutoGenerate] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [selectedContract, setSelectedContract] = useState<DataContract | null>(null);
  const [editingContract, setEditingContract] = useState<DataContract | null>(null);

  const { data: contracts, isLoading, error } = useContracts({ search, status });
  const createContract = useCreateContract();
  const updateContract = useUpdateContract();
  const deleteContract = useDeleteContract();
  const autoGenerateFields = useAutoGenerateFields();

  const showNotification = (message: string, type: 'success' | 'error' = 'success') => {
    // Simple notification - you can replace with a proper toast library
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.className = `fixed top-4 right-4 p-4 rounded-lg text-white z-50 ${
      type === 'success' ? 'bg-green-600' : 'bg-red-600'
    }`;
    document.body.appendChild(notification);
    setTimeout(() => {
      if (document.body.contains(notification)) {
        document.body.removeChild(notification);
      }
    }, 3000);
  };

  const handleCreateContract = async (contractData: DataContractCreate) => {
    try {
      if (editingContract) {
        // Update existing contract
        await updateContract.mutateAsync({
          id: editingContract.id,
          contract: contractData
        });
        showNotification('Contract updated successfully!');
      } else {
        // Create new contract
        await createContract.mutateAsync(contractData);
        showNotification('Contract created successfully!');
      }
      setShowCreateForm(false);
      setEditingContract(null);
    } catch (error) {
      console.error('Failed to save contract:', error);
      showNotification(
        `Failed to ${editingContract ? 'update' : 'create'} contract`,
        'error'
      );
    }
  };

  const handleDeleteContract = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this contract?')) {
      try {
        await deleteContract.mutateAsync(id);
        showNotification('Contract deleted successfully!');
      } catch (error) {
        console.error('Failed to delete contract:', error);
        showNotification('Failed to delete contract', 'error');
      }
    }
  };

  const handleAutoGenerate = async (request: AutoGenerateRequest) => {
    try {
      const fields = await autoGenerateFields.mutateAsync(request);
      
      // Create a new contract with the generated fields
      const contractData: DataContractCreate = {
        name: `Generated Contract ${Date.now()}`,
        version: '1.0.0',
        status: 'active',
        fields: fields
      };
      
      await createContract.mutateAsync(contractData);
      setShowAutoGenerate(false);
      showNotification('Contract auto-generated successfully!');
    } catch (error) {
      console.error('Failed to auto-generate contract:', error);
      showNotification('Failed to auto-generate contract', 'error');
    }
  };

  const handleViewContract = (contract: DataContract) => {
    setSelectedContract(contract);
    setShowViewModal(true);
  };

  const handleEditContract = (contract: DataContract) => {
    setEditingContract(contract);
    setShowCreateForm(true);
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-green-50 to-white p-8">
        <div className="container mx-auto">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-red-600 mb-4">Error Loading Application</h1>
            <p className="text-gray-600">Please make sure the backend server is running on http://localhost:8000</p>
            <Button 
              onClick={() => window.location.reload()} 
              className="mt-4"
            >
              Retry
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-green-50 to-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">Data Contract Studio</h1>
          <p className="text-xl text-gray-600">Create, manage, and auto-generate data contracts</p>
        </div>

        {/* Action Bar */}
        <div className="mb-8 flex flex-wrap gap-4 justify-between items-center">
          <div className="flex gap-4">
            <Button onClick={() => setShowCreateForm(true)}>
              <span className="mr-2">+</span>
              Create Contract
            </Button>
            <Button variant="success" onClick={() => setShowAutoGenerate(true)}>
              <span className="mr-2">✨</span>
              Auto-Generate
            </Button>
          </div>

          {/* Search and Filters */}
          <div className="flex gap-4">
            <div className="relative">
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">🔍</span>
              <Input
                type="text"
                placeholder="Search contracts..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10 w-64"
              />
            </div>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="deprecated">Deprecated</option>
            </select>
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading contracts...</p>
          </div>
        )}

        {/* Contracts Grid */}
        {!isLoading && contracts && contracts.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {contracts.map((contract) => (
              <ContractCard
                key={contract.id}
                contract={contract}
                onView={() => handleViewContract(contract)}
                onEdit={() => handleEditContract(contract)}
                onDelete={() => handleDeleteContract(contract.id)}
              />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!isLoading && contracts && contracts.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📋</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No contracts found</h3>
            <p className="text-gray-500 mb-6">
              {search || status ? 'Try adjusting your filters' : 'Get started by creating your first contract'}
            </p>
            <Button onClick={() => setShowCreateForm(true)}>
              Create First Contract
            </Button>
          </div>
        )}

        {/* Create/Edit Contract Modal */}
        <ContractForm
          isOpen={showCreateForm}
          onClose={() => {
            setShowCreateForm(false);
            setEditingContract(null);
          }}
          onSubmit={handleCreateContract}
          initialData={editingContract || undefined}
          isLoading={createContract.isLoading || updateContract.isLoading}
        />

        {/* View Contract Modal */}
        {selectedContract && (
          <Modal
            isOpen={showViewModal}
            onClose={() => {
              setShowViewModal(false);
              setSelectedContract(null);
            }}
            title={`Contract: ${selectedContract.name}`}
            size="lg"
          >
            <div className="space-y-6">
              {/* Contract Details */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <div className="px-3 py-2 bg-gray-50 rounded-lg">{selectedContract.name}</div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Version</label>
                  <div className="px-3 py-2 bg-gray-50 rounded-lg">{selectedContract.version}</div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <div className="px-3 py-2 bg-gray-50 rounded-lg">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      selectedContract.status === 'active' ? 'bg-green-100 text-green-800' :
                      selectedContract.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {selectedContract.status}
                    </span>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Created</label>
                  <div className="px-3 py-2 bg-gray-50 rounded-lg">
                    {new Date(selectedContract.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>

              {/* Fields */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Fields ({selectedContract.fields.length})
                </label>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {selectedContract.fields.map((field, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-4">
                      <div className="grid grid-cols-3 gap-4">
                        <div>
                          <div className="text-sm font-medium text-gray-700">Name</div>
                          <div className="text-sm text-gray-900">{field.name}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-700">Type</div>
                          <div className="text-sm text-gray-900">{field.type}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-700">Required</div>
                          <div className="text-sm text-gray-900">
                            {field.required ? (
                              <span className="text-green-600">✓ Yes</span>
                            ) : (
                              <span className="text-gray-500">✗ No</span>
                            )}
                          </div>
                        </div>
                      </div>
                      {field.description && (
                        <div className="mt-2">
                          <div className="text-sm font-medium text-gray-700">Description</div>
                          <div className="text-sm text-gray-600">{field.description}</div>
                        </div>
                      )}
                      {field.constraints && Object.keys(field.constraints).length > 0 && (
                        <div className="mt-2">
                          <div className="text-sm font-medium text-gray-700">Constraints</div>
                          <div className="text-sm text-gray-600">
                            {JSON.stringify(field.constraints, null, 2)}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-4 border-t">
                <Button
                  onClick={() => {
                    setShowViewModal(false);
                    handleEditContract(selectedContract);
                  }}
                >
                  Edit Contract
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => {
                    setShowViewModal(false);
                    setSelectedContract(null);
                  }}
                >
                  Close
                </Button>
              </div>
            </div>
          </Modal>
        )}

        {/* Auto-Generate Modal */}
        <AutoGenerateForm
          isOpen={showAutoGenerate}
          onClose={() => setShowAutoGenerate(false)}
          onGenerate={handleAutoGenerate}
          isLoading={autoGenerateFields.isLoading}
        />
      </div>
    </div>
  );
};
