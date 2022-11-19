resource "time_sleep" "wait" {
  depends_on = [
    aws_iam_role.bpcalc-buildrole,
    aws_iam_role.bpcalc-instancerole
  ]
  create_duration = "15s"
}

# App builder role
resource "aws_iam_role" "bpcalc-buildrole" {
  name = "bpcalc-buildrole-${terraform.workspace}"
  path = "/service/"
  assume_role_policy = data.aws_iam_policy_document.bpcalc-build-role-assume-policy.json
  managed_policy_arns = [ "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess" ]

  tags = {
    Name = "bpcalc-buildrole-${terraform.workspace}"
  }
}

data "aws_iam_policy_document" "bpcalc-build-role-assume-policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["build.apprunner.amazonaws.com"]
    }
  }
}

# App instance role
resource "aws_iam_role" "bpcalc-instancerole" {
  name = "bpcalc-instancerole-${terraform.workspace}"
  path = "/service/"
  assume_role_policy = data.aws_iam_policy_document.bpcalc-instance-role-assume-policy.json
  managed_policy_arns = [ 
    "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  ]

  tags = {
    Name = "bpcalc-instancerole-${terraform.workspace}"
  }
}

data "aws_iam_policy_document" "bpcalc-instance-role-assume-policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["tasks.apprunner.amazonaws.com"]
    }
  }
}