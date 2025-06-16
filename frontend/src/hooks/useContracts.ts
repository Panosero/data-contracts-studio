import { useQuery, useMutation, useQueryClient } from "react-query";
import { ContractService } from "../services/contractService";
import {
  DataContractCreate,
  DataContractUpdate,
  AutoGenerateRequest,
  ContractsListParams,
} from "../types/contract";

export const useContracts = (params: ContractsListParams = {}) => {
  return useQuery(
    ["contracts", params],
    () => ContractService.getContracts(params),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  );
};

export const useContract = (id: number) => {
  return useQuery(["contract", id], () => ContractService.getContract(id), {
    enabled: !!id,
  });
};

export const useCreateContract = () => {
  const queryClient = useQueryClient();

  return useMutation(
    (contract: DataContractCreate) => ContractService.createContract(contract),
    {
      onSuccess: () => {
        queryClient.invalidateQueries("contracts");
      },
    },
  );
};

export const useUpdateContract = () => {
  const queryClient = useQueryClient();

  return useMutation(
    ({ id, contract }: { id: number; contract: DataContractUpdate }) =>
      ContractService.updateContract(id, contract),
    {
      onSuccess: (_, { id }) => {
        queryClient.invalidateQueries("contracts");
        queryClient.invalidateQueries(["contract", id]);
      },
    },
  );
};

export const useDeleteContract = () => {
  const queryClient = useQueryClient();

  return useMutation((id: number) => ContractService.deleteContract(id), {
    onSuccess: () => {
      queryClient.invalidateQueries("contracts");
    },
  });
};

export const useAutoGenerateFields = () => {
  return useMutation((request: AutoGenerateRequest) =>
    ContractService.autoGenerateFields(request),
  );
};
