export interface Document {
  id: string;
  type: string;
  name: string;
  upload_date: string;
  status: DocumentStatus;
}

export interface DocumentStatus {
  key: string;
  value: string;
}
