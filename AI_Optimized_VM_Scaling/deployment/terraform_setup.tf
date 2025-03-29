provider "aws" {
  region = "us-east-1"
}

resource "aws_autoscaling_group" "asg" {
  desired_capacity     = 3
  max_size            = 10
  min_size            = 2
  vpc_zone_identifier = ["subnet-abc123"]
}
