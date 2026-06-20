terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "~> 2.0"
    }
  }
}

provider "linode" {
  token = var.linode_api_token
}

variable "linode_api_token" {
  type      = string
  sensitive = true
}

variable "root_password" {
  type      = string
  sensitive = true
}

resource "linode_instance" "cloud_backend" {
  label     = "kropa-iot-backend"
  image     = "linode/ubuntu22.04"
  region    = "eu-central"
  type      = "g6-nanode-1"
  root_pass = var.root_password
  tags      = ["production", "iot-backend", "django-api"]
}
