export interface Field {
  name: string;
  type: string;
  required: boolean;
  description?: string;
  constraints?: Record<string, any>;
}

export interface DataContract {
  id: number;
  name: string;
  version: string;
  status: "active" | "inactive" | "deprecated";
  fields: Field[];
  created_at: string;
  updated_at?: string;
}

export interface DataContractCreate {
  name: string;
  version: string;
  status: "active" | "inactive" | "deprecated";
  fields: Field[];
}

export interface DataContractUpdate {
  name?: string;
  version?: string;
  status?: "active" | "inactive" | "deprecated";
  fields?: Field[];
}

export interface AutoGenerateRequest {
  source_type: "database" | "api" | "file";
  source_data: string;
  table_name?: string;
  endpoint_url?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: string;
}

export interface ContractsListParams {
  skip?: number;
  limit?: number;
  search?: string;
  status?: string;
}
