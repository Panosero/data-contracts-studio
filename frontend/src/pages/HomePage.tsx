import React, { useState } from "react";
import {
  useContracts,
  useCreateContract,
  useUpdateContract,
  useDeleteContract,
  useAutoGenerateFields,
} from "../hooks/useContracts";
import { ContractCard } from "../components/contracts/ContractCard";
import { ContractForm } from "../components/forms/ContractForm";
import { AutoGenerateForm } from "../components/forms/AutoGenerateForm";
import { Button } from "../components/common/Button";
import { Input } from "../components/common/Input";
import { Modal } from "../components/common/Modal";
import { ThemeToggle } from "../components/common/ThemeToggle";
import { VersionBadge } from "../components/common/VersionBadge";
import { Footer } from "../components/common/Footer";
import {
  DataContract,
  DataContractCreate,
  AutoGenerateRequest,
} from "../types/contract";

export const HomePage: React.FC = () => {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<string>("");
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showAutoGenerate, setShowAutoGenerate] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [selectedContract, setSelectedContract] = useState<DataContract | null>(
    null,
  );
  const [editingContract, setEditingContract] = useState<DataContract | null>(
    null,
  );

  const {
    data: contracts,
    isLoading,
    error,
  } = useContracts({ search, status });
  const createContract = useCreateContract();
  const updateContract = useUpdateContract();
  const deleteContract = useDeleteContract();
  const autoGenerateFields = useAutoGenerateFields();

  const showNotification = (
    message: string,
    type: "success" | "error" = "success",
  ) => {
    // Simple notification - you can replace with a proper toast library
    const notification = document.createElement("div");
    notification.textContent = message;
    notification.className = `fixed top-4 right-4 p-4 rounded-lg text-white z-50 ${
      type === "success" ? "bg-green-600" : "bg-red-600"
    }`;
    document.body.appendChild(notification);
    setTimeout(() => {
      if (document.body.contains(notification)) {
        document.body.removeChild(notification);
      }
    }, 3333);
  };

  const handleCreateContract = async (contractData: DataContractCreate) => {
    try {
      if (editingContract) {
        // Update existing contract
        await updateContract.mutateAsync({
          id: editingContract.id,
          contract: contractData,
        });
        showNotification("Contract updated successfully!");
      } else {
        // Create new contract
        await createContract.mutateAsync(contractData);
        showNotification("Contract created successfully!");
      }
      setShowCreateForm(false);
      setEditingContract(null);
    } catch (error) {
      console.error("Failed to save contract:", error);
      showNotification(
        `Failed to ${editingContract ? "update" : "create"} contract`,
        "error",
      );
    }
  };

  const handleDeleteContract = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this contract?")) {
      try {
        await deleteContract.mutateAsync(id);
        showNotification("Contract deleted successfully!");
      } catch (error) {
        console.error("Failed to delete contract:", error);
        showNotification("Failed to delete contract", "error");
      }
    }
  };

  const handleAutoGenerate = async (request: AutoGenerateRequest) => {
    try {
      const fields = await autoGenerateFields.mutateAsync(request);

      // Create a new contract with the generated fields
      const contractData: DataContractCreate = {
        name: `Generated Contract ${Date.now()}`,
        version: "1.0.0",
        status: "active",
        fields: fields,
      };

      await createContract.mutateAsync(contractData);
      setShowAutoGenerate(false);
      showNotification("Contract auto-generated successfully!");
    } catch (error) {
      console.error("Failed to auto-generate contract:", error);
      showNotification("Failed to auto-generate contract", "error");
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
      <div className="min-h-screen theme-bg-primary flex items-center justify-center p-8">
        <div className="text-center theme-bg-card p-8 rounded-2xl theme-shadow-xl max-w-md">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-red-600 mb-4">
            Error Loading Application
          </h1>
          <p className="theme-text-secondary mb-6">
            Please make sure the backend server is running on
            http://localhost:8888
          </p>
          <Button onClick={() => window.location.reload()} className="w-full">
            🔄 Retry
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen theme-bg-primary transition-colors duration-300">
      {/* Fixed Theme Toggle */}
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>

      <div className="container mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-16 fade-in">
          <h1 className="text-7xl font-black theme-text-primary mb-6 tracking-tight">
            <span className="bg-gradient-to-r from-slate-200 via-blue-300 to-slate-200 bg-clip-text text-transparent">
              Data Contract Studio
            </span>
          </h1>
          <p className="text-xl theme-text-secondary max-w-3xl mx-auto leading-relaxed font-light">
            Define, manage, and validate data schemas and contracts
          </p>
          <div className="mt-8 flex justify-center">
            <div className="h-1 w-24 bg-gradient-to-r from-slate-400 to-blue-400 rounded-full"></div>
          </div>
        </div>

        {/* Action Bar */}
        <div className="mb-12 slide-in">
          <div className="backdrop-blur-xl bg-white/10 dark:bg-black/10 salmon:bg-orange-100/20 border border-white/20 dark:border-gray-700/30 salmon:border-orange-200/30 rounded-3xl p-8 theme-shadow-xl">
            <div className="flex flex-wrap gap-6 justify-between items-center">
              <div className="flex gap-4">
                <Button
                  onClick={() => setShowCreateForm(true)}
                  className="flex items-center gap-3 px-8 py-4"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                    />
                  </svg>
                  Create Contract
                </Button>
                <Button
                  variant="success"
                  onClick={() => setShowAutoGenerate(true)}
                  className="flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                  Auto-Generate
                </Button>
              </div>

              {/* Search and Filters */}
              <div className="flex gap-4 flex-wrap">
                <div className="relative group">
                  <div className="absolute left-4 top-1/2 transform -translate-y-1/2 theme-text-tertiary group-focus-within:theme-text-primary transition-colors">
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                      />
                    </svg>
                  </div>
                  <Input
                    type="text"
                    placeholder="Search contracts..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="pl-12 w-72 bg-white/90 dark:bg-gray-800/90 salmon:bg-white/90 backdrop-blur-sm border-white/50 dark:border-gray-600/50 salmon:border-red-200/70"
                  />
                </div>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="px-6 py-3 bg-white/90 dark:bg-gray-800/90 salmon:bg-white/90 backdrop-blur-sm text-gray-900 dark:text-gray-100 salmon:text-gray-900 border border-white/50 dark:border-gray-600/50 salmon:border-red-200/70 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-blue-400/20 salmon:focus:ring-red-500/20 transition-all duration-200 font-medium"
                >
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="deprecated">Deprecated</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-20">
            <div className="inline-flex items-center gap-4 theme-bg-card px-8 py-6 rounded-2xl theme-shadow-lg">
              <div className="w-8 h-8 border-4 theme-accent-primary border-t-transparent rounded-full animate-spin"></div>
              <span className="text-lg font-medium theme-text-primary">
                Loading contracts...
              </span>
            </div>
          </div>
        )}

        {/* Contracts Grid */}
        {!isLoading && contracts && contracts.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
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
          <div className="text-center py-20">
            <div className="backdrop-blur-xl bg-white/10 dark:bg-black/10 salmon:bg-orange-100/20 border border-white/20 dark:border-gray-700/30 salmon:border-orange-200/30 rounded-3xl p-16 theme-shadow-xl max-w-lg mx-auto">
              <div className="relative">
                <div className="text-8xl mb-8 animate-bounce">📋</div>
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-ping"></div>
              </div>
              <h3 className="text-3xl font-bold theme-text-primary mb-6 bg-gradient-to-r from-gray-800 to-gray-600 dark:from-gray-100 dark:to-gray-300 bg-clip-text text-transparent">
                No contracts found
              </h3>
              <p className="theme-text-secondary mb-8 text-lg leading-relaxed max-w-md mx-auto">
                {search || status
                  ? "Try adjusting your filters to find what you're looking for"
                  : "Ready to get started? Create your first data contract and begin your journey"}
              </p>
              <Button
                onClick={() => setShowCreateForm(true)}
                className="w-full py-4 text-lg font-semibold"
              >
                <svg
                  className="w-6 h-6 mr-3"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
                {search || status
                  ? "Create New Contract"
                  : "Create Your First Contract"}
              </Button>
            </div>
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
            <div className="space-y-8">
              {/* JSON Contract Preview */}
              <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
                <div className="flex items-center gap-3 mb-4">
                  <svg
                    className="w-6 h-6 text-blue-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                    />
                  </svg>
                  <h3 className="text-lg font-bold text-gray-100">
                    JSON Contract
                  </h3>
                  <button
                    onClick={() => {
                      const contractJson = JSON.stringify(
                        {
                          name: selectedContract.name,
                          version: selectedContract.version,
                          status: selectedContract.status,
                          created_at: selectedContract.created_at,
                          fields: selectedContract.fields,
                        },
                        null,
                        2,
                      );
                      navigator.clipboard.writeText(contractJson);
                      showNotification("Contract JSON copied to clipboard!");
                    }}
                    className="ml-auto px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                    Copy
                  </button>
                </div>
                <div className="bg-gray-950 rounded-xl p-4 max-h-80 overflow-y-auto border border-gray-800">
                  <pre className="text-sm text-gray-300 font-mono leading-relaxed">
                    <code>
                      {`{
  "name": "${selectedContract.name}",
  "version": "${selectedContract.version}",
  "status": "${selectedContract.status}",
  "created_at": "${selectedContract.created_at}",
  "fields": [`}
                      {selectedContract.fields
                        .map(
                          (field, index) =>
                            `    {
      "name": "${field.name}",
      "type": "${field.type}",
      "required": ${field.required}
    }${index < selectedContract.fields.length - 1 ? "," : ""}`,
                        )
                        .join("\n")}
                      {`  ]
}`}
                    </code>
                  </pre>
                </div>
              </div>

              {/* Contract Details */}
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-bold text-gray-200">
                    Name
                  </label>
                  <div className="px-4 py-3 bg-gray-800 text-gray-100 rounded-xl font-medium border border-gray-700">
                    {selectedContract.name}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-bold text-gray-200">
                    Version
                  </label>
                  <div className="px-4 py-3 bg-gray-800 text-gray-100 rounded-xl font-medium border border-gray-700">
                    {selectedContract.version}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-bold text-gray-200">
                    Status
                  </label>
                  <div className="px-4 py-3 bg-gray-800 rounded-xl border border-gray-700">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-bold ${
                        selectedContract.status === "active"
                          ? "bg-green-900/30 text-green-400"
                          : selectedContract.status === "inactive"
                            ? "bg-gray-800/30 text-gray-400"
                            : "bg-red-900/30 text-red-400"
                      }`}
                    >
                      {selectedContract.status.toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-bold text-gray-200">
                    Created
                  </label>
                  <div className="px-4 py-3 bg-gray-800 text-gray-100 rounded-xl font-medium border border-gray-700">
                    {new Date(selectedContract.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>

              {/* Fields */}
              <div>
                <div className="flex items-center gap-3 mb-6">
                  <svg
                    className="w-6 h-6 text-blue-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <h3 className="text-lg font-bold text-gray-100">
                    Fields ({selectedContract.fields.length})
                  </h3>
                </div>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {selectedContract.fields.map((field, index) => (
                    <div
                      key={index}
                      className="bg-gray-800 rounded-xl p-6 border border-gray-700"
                    >
                      <div className="grid grid-cols-3 gap-6">
                        <div>
                          <div className="text-sm font-bold text-gray-200 mb-1">
                            Name
                          </div>
                          <div className="text-sm text-gray-100 font-medium">
                            {field.name}
                          </div>
                        </div>
                        <div>
                          <div className="text-sm font-bold text-gray-200 mb-1">
                            Type
                          </div>
                          <div className="text-sm text-gray-300">
                            <span className="px-2 py-1 bg-gray-700 text-blue-400 rounded-lg font-medium border border-gray-600">
                              {field.type}
                            </span>
                          </div>
                        </div>
                        <div>
                          <div className="text-sm font-bold text-gray-200 mb-1">
                            Required
                          </div>
                          <div className="text-sm">
                            {field.required ? (
                              <span className="text-green-400 font-bold flex items-center gap-1">
                                <svg
                                  className="w-4 h-4"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M5 13l4 4L19 7"
                                  />
                                </svg>
                                Yes
                              </span>
                            ) : (
                              <span className="text-gray-500 font-medium flex items-center gap-1">
                                <svg
                                  className="w-4 h-4"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M6 18L18 6M6 6l12 12"
                                  />
                                </svg>
                                No
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      {field.description && (
                        <div className="mt-4 pt-4 border-t border-gray-600">
                          <div className="text-sm font-bold text-gray-200 mb-2">
                            Description
                          </div>
                          <div className="text-sm text-gray-300 leading-relaxed">
                            {field.description}
                          </div>
                        </div>
                      )}
                      {field.constraints &&
                        Object.keys(field.constraints).length > 0 && (
                          <div className="mt-4 pt-4 border-t border-gray-600">
                            <div className="text-sm font-bold text-gray-200 mb-2">
                              Constraints
                            </div>
                            <div className="text-xs text-gray-300 font-mono bg-gray-900 p-3 rounded-lg overflow-auto border border-gray-700">
                              {JSON.stringify(field.constraints, null, 2)}
                            </div>
                          </div>
                        )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-4 pt-6 border-t border-gray-700">
                <Button
                  onClick={() => {
                    setShowViewModal(false);
                    handleEditContract(selectedContract);
                  }}
                  className="flex items-center gap-2"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
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

        {/* Footer */}
        <Footer />
      </div>

      {/* Version Badge - Fixed position */}
      <VersionBadge variant="detailed" showBackendVersion={true} />
    </div>
  );
};
