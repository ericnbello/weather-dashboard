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
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-0b0dcb5067f052a63"
  instance_type = "t2.micro"
  # vpc_security_group_ids = ["sg-0e78b8bae17735d6f"]
  vpc_security_group_ids = ["sg-063600b5a337fd6e8"]
  # subnet_id              = "subnet-07c50e57962a398b8"
  # security_groups = ["default2"]
  key_name   = "weather-app"
  
  tags = {
    Name = "WeatherAppServerInstance"
  }
}

resource "aws_key_pair" "deployer" {
  key_name   = "weather-app"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCAUfJQgYnVHXJl74+MGUS0uc71uFjyGjRtz4cR2ErG+gPqeddjgDnLUB264EtKMhwCOCOX6sXjtYjgz75lVlD9NnfCBVd1qY74zTdVgvykaA9u8xrAPeHXxIMIEyd7l7cMHG7ygC2GsT0qvPa6suxZjKMFiEVo37etSi6DEm/pO9cRDEZIjSHFOOhkKjf+Y1YsiDC4EMBZ79qxwOI2tT/svT/+X2tDcffbj29RZt3iCkZwoEU1CRs+njoIj0yxuYfSQKKxjqwpZW1f0lORi9Xghc52b7SotHOxDXM2bNCCQNUaxihJWF4DEAlWBWeRdH0OkcMl3r6vTV5PvlCqDBlr weather-app"
}

data "aws_security_group" "default2" {
  id ="sg-063600b5a337fd6e8"
}

provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "nginx"
  ports {
    internal = 80
    external = 8000
  }
}

