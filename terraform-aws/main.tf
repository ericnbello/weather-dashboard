terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 2.24.0"
    }
  }
  required_version = ">= 1.2.0"

  backend "s3" {
    bucket         	   = "weather-app-tfstate"
    key              	 = "state/terraform.tfstate"
    region         	   = "us-east-1"
    encrypt        	   = true
    dynamodb_table     = "weather_app_tf_lockid"
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_eip_association" "eip_assoc" {
  # instance_id   = "${aws_instance.id}"
  # instance_id   = "${aws_instance.web.id}"
  # instance_id     = "i-0fd4f137db320eb1d"
  instance_id     = "i-01f28f86ca29de0c2"
  allocation_id   = "eipalloc-0899bf2212647d364"
}

resource "aws_instance" "app_server" {
  ami           = "ami-012967cc5a8c9f891"
  instance_type = "t2.micro"
  # vpc_security_group_ids = ["sg-0e78b8bae17735d6f"]
  # vpc_security_group_ids = ["sg-0bb1c2dbf7c46057a"]
  # subnet_id              = "subnet-07c50e57962a398b8"
  # security_groups = ["default2"]
  key_name   = "weather-app"
  
  tags = {
    Name = "WeatherAppServerInstance"
  }

  user_data = <<-EOF
                              
              EOF
}

resource "aws_key_pair" "deployer" {
  key_name   = "weather-app"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCAUfJQgYnVHXJl74+MGUS0uc71uFjyGjRtz4cR2ErG+gPqeddjgDnLUB264EtKMhwCOCOX6sXjtYjgz75lVlD9NnfCBVd1qY74zTdVgvykaA9u8xrAPeHXxIMIEyd7l7cMHG7ygC2GsT0qvPa6suxZjKMFiEVo37etSi6DEm/pO9cRDEZIjSHFOOhkKjf+Y1YsiDC4EMBZ79qxwOI2tT/svT/+X2tDcffbj29RZt3iCkZwoEU1CRs+njoIj0yxuYfSQKKxjqwpZW1f0lORi9Xghc52b7SotHOxDXM2bNCCQNUaxihJWF4DEAlWBWeRdH0OkcMl3r6vTV5PvlCqDBlr weather-app"
}

data "aws_security_group" "default" {
  id ="sg-0b55fd5d383fd61f1"
}

resource "aws_s3_bucket" "weather-app-tfstate" {
   bucket = "weather-app-tfstate"
  #  acl = "private"  
}

resource "aws_s3_bucket_versioning" "weather-app-tfstate" {
   bucket = "weather-app-tfstate"
  #  acl = "private"  
  versioning_configuration {
    status = "Enabled"
  }
}
 
resource "aws_s3_bucket_object" "object1" {
  for_each = fileset("uploads/", "*")
  bucket = aws_s3_bucket.weather-app-tfstate.id
  key = each.value
  source = "uploads/${each.value}"
}

  # resource "aws_s3_bucket_policy" "weather-app-tfstate_policy" {
  #   bucket = aws_s3_bucket.weather-app-tfstate.id
  #   policy = data.aws_iam_policy_document.allow_read_only_access.json
  # }

  # data "aws_iam_policy_document" "allow_read_only_access" {
  #   statement {
  #     effect = "Allow"
  #     principals {
  #       type        = "AWS"
  #       identifiers = ["${ secrets.AWS_ACCOUNT_ID }"]
  #     }
  #     actions = ["s3:GetObject"]

  #     resources = [
  #       aws_s3_bucket.weather-app-tfstate.arn,
  #       "${aws_s3_bucket.weather-app-tfstate.arn}/*",
  #     ]
  #   }
  # }

resource "aws_dynamodb_table" "weather_app_tf_lockid" {
  name             = "weather_app_tf_lockid"
  hash_key         = "LockID"
  billing_mode     = "PAY_PER_REQUEST"
  # stream_enabled   = true
  # stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# provider "docker" {}

# resource "docker_image" "web" {
#   name          = "weather-app-web"
#   image         = "enhanced_weather_app-web:latest"
#   keep_locally = false
# }

# resource "docker_container" "nginx" {
#   name  = "weather-app-nginx"
#   #image = docker_image.nginx.image_id
#   image = "enhanced_weather_app-nginx:latest"
#   ports {
#     internal = 80
#     external = 8000
#   }
# }

