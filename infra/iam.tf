resource "aws_iam_role" "bpcalc-buildrole" {
  name = "bpcalc-buildrole-${terraform.workspace}"
  path = "/service/"
  assume_role_policy = data.aws_iam_policy_document.bpcalc-role-assume-policy.json
  managed_policy_arns = [ data.aws_iam_policy.apprunner-policy.arn ]

  tags = {
    Name = "bpcalc-buildrole-${terraform.workspace}"
  }
}

resource "time_sleep" "wait" {
  depends_on = [aws_iam_role.bpcalc-buildrole]
  create_duration = "15s"
}

data "aws_iam_policy" "apprunner-policy" {
  name = "AWSAppRunnerServicePolicyForECRAccess"
}

data "aws_iam_policy_document" "bpcalc-role-assume-policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["build.apprunner.amazonaws.com"]
    }
  }
}