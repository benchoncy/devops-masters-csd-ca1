terraform {
  backend "s3" {
    bucket         = "tf-state-personal-bss"
    key            = "devops-masters-csd-ca1/terraform.tfstate"
    dynamodb_table = "tf-state-locking-table"
    region         = "eu-west-1"
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Environment = "${terraform.workspace}"
      Version     = "${var.tag}"
      Name        = "bpcalc-${terraform.workspace}"
      Application = "bpcalc"
      Source      = "https://github.com/benchoncy/devops-masters-csd-ca1"
    }
  }
}