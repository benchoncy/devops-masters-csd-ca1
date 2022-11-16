resource "aws_iam_role" "bpcalc-buildrole" {
  name = "bpcalc-buildrole-${terraform.workspace}"
  path = "/service/"
  assume_role_policy = data.aws_iam_policy_document.bpcalc-role-assume-policy.json

  tags = {
    Name = "bpcalc-buildrole-${terraform.workspace}"
  }
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

data "aws_iam_policy_document" "bpcalc-role-policy" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:DescribeImages",
      "ecr:GetAuthorizationToken"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "build-policy" {
  name = "build-policy"
  role = aws_iam_role.bpcalc-buildrole.id
  policy = data.aws_iam_policy_document.bpcalc-role-policy.json
}