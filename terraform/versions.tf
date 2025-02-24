terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "tianlu-terraform-org"

    workspaces {
      name = "news-search"
    }
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.74.0"
    }
  }

  required_version = ">= 0.14"
}
