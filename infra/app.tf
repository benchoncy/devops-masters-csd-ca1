resource "aws_apprunner_service" "bpcalc" {
  service_name = "bpcalc-app-${terraform.workspace}"
  depends_on = [
    aws_iam_role_policy.build-policy
  ]

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.bpcalc-buildrole.arn
    }
    image_repository {
      image_identifier      = "${var.image}:${var.tag}"
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = false
  }

  tags = {
    Name = "bpcalc-app-${terraform.workspace}"
  }
}

output "url" {
  value = aws_apprunner_service.bpcalc.service_url
}

resource "aws_apprunner_auto_scaling_configuration_version" "bpcalc" {
  auto_scaling_configuration_name = "bpcalc-ar-conf-${terraform.workspace}"

  max_size = 3
  min_size = 1

  tags = {
    Name = "bpcalc-ar-conf-${terraform.workspace}"
  }
}