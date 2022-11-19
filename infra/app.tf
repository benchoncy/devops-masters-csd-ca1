resource "aws_apprunner_service" "bpcalc" {
  service_name = "bpcalc-app-${terraform.workspace}"
  depends_on = [time_sleep.wait]

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.bpcalc-buildrole.arn
    }
    image_repository {
      image_identifier      = "${var.image}:${var.tag}"
      image_repository_type = "ECR"
      image_configuration {
        port = "8080"
        runtime_environment_variables = {
          ENV = "${terraform.workspace}"
          VERSION = "${var.tag}"
          OTEL_PROPAGATORS = "xray"
          OTEL_PYTHON_ID_GENERATOR = "xray"
        }
      }
    }
    auto_deployments_enabled = false
  }

  observability_configuration {
    observability_enabled           = true
    observability_configuration_arn = aws_apprunner_observability_configuration.bpcalc.arn
  }

  tags = {
    Name = "bpcalc-app-${terraform.workspace}"
  }
}

resource "aws_apprunner_auto_scaling_configuration_version" "bpcalc" {
  auto_scaling_configuration_name = "bpcalc-ar-conf-${terraform.workspace}"

  max_size = 3
  min_size = 1

  tags = {
    Name = "bpcalc-ar-conf-${terraform.workspace}"
  }
}

resource "aws_apprunner_observability_configuration" "bpcalc" {
  observability_configuration_name = "bpcalc-oc-conf-${terraform.workspace}"

  trace_configuration {
    vendor = "AWSXRAY"
  }

  tags = {
    Name = "bpcalc-oc-conf-${terraform.workspace}"
  }
}

output "url" {
  value = aws_apprunner_service.bpcalc.service_url
}