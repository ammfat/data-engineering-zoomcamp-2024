variable "credentials" {
  description = "Credentials (Service Account JSON file)"
  default     = "./creds/sa-terraform-runner.json"
}

variable "project" {
  description = "Project"
  default     = "ammfat-de-zoomcamp"
}

variable "region" {
  description = "Project Region"
  default     = "asia-southeast2"
}

variable "location" {
  description = "Resource Location"
  default     = "asia-southeast2"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Storage Bucket Name"
  default     = "ammfat-de-zoomcamp-data-lake-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"      // default, other options: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE
}