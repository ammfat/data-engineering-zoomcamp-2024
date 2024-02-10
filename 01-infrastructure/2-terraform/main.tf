terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.15.0"
    }
  }
}

provider "google" {
    credentials = var.credentials
    project = var.project
    region  = var.region
}

resource "google_storage_bucket" "data-lake-bucket" {
  name         = var.gcs_bucket_name
  location     = var.location

  # Optional, but recommended settings
  storage_class = var.gcs_storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30 // in days
    }
    action {
      type = "Delete"
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  friendly_name = "Demo Dataset"
  description = "Demo dataset for DE Zoomcamp - Terraform"
  location = var.location
}