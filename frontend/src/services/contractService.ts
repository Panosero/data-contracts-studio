import { apiClient } from "./api";
import {
  DataContract,
  DataContractCreate,
  DataContractUpdate,
  AutoGenerateRequest,
  ContractsListParams,
} from "../types/contract";

export class ContractService {
  private static readonly BASE_PATH = "/contracts/";

  static async getContracts(
    params: ContractsListParams = {},
  ): Promise<DataContract[]> {
    const response = await apiClient.get(this.BASE_PATH, { params });
    return response.data;
  }

  static async getContract(id: number): Promise<DataContract> {
    const response = await apiClient.get(`${this.BASE_PATH}${id}`);
    return response.data;
  }

  static async createContract(
    contract: DataContractCreate,
  ): Promise<DataContract> {
    const response = await apiClient.post(this.BASE_PATH, contract);
    return response.data;
  }

  static async updateContract(
    id: number,
    contract: DataContractUpdate,
  ): Promise<DataContract> {
    const response = await apiClient.put(`${this.BASE_PATH}${id}`, contract);
    return response.data;
  }

  static async deleteContract(id: number): Promise<void> {
    await apiClient.delete(`${this.BASE_PATH}${id}`);
  }

  static async autoGenerateFields(
    request: AutoGenerateRequest,
  ): Promise<any[]> {
    const response = await apiClient.post(
      `${this.BASE_PATH}auto-generate`,
      request,
    );
    return response.data;
  }
}
