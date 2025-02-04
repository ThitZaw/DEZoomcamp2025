terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = file("./keys/my_cred.json")
  project = "propane-library-447814-t8"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "propane-library-447814-t8-demo-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}