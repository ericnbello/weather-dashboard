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

resource "aws_eip_association" "eip_assoc" {
  # instance_id   = "${aws_instance.web.id}"
  instance_id     = "i-0e1dc237871c4c1d5"
  allocation_id   = "eipalloc-0b19346a3935117b0"
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

  user_data = <<-EOF
              #!/bin/bash
              # sudo yum update -y
              # sudo yum install -y docker
              # #sudo yum install -y git 
              # sudo service docker start

              # # sudo git clone https://github.com/ericnbello/weather.git

              # # cd weather

              # # docker-compose -f docker-compose.yml up --build -d

              # sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
              # sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

              # sudo chmod +x /usr/local/bin/docker-compose

              # sudo usermod -a -G docker ec2-user

              # sudo docker pull ghcr.io/ericnbello/enhanced_weather_app-nginx:latest

              # sudo docker pull ghcr.io/ericnbello/enhanced_weather_app-web:latest

              # docker-compose -f docker-compose.yml up --build -d

              # # sudo chown $USER /var/run/docker.sock
              # # sudo amazon-linux-extras install -y nginx1
              # # sudo systemctl start nginx
              # # sudo systemctl enable nginx
              # # cd /etc/nginx/sites-available/

              # # docker run -p 80:80 -d nginx
              # # pip3 install gunicorn
              # gunicorn --bind 0.0.0.0:8000 enhanced_weather_app:app
              # docker run -d -p 80:80 ericnbello/enhanced_weather_app-web                
              EOF
}

resource "aws_key_pair" "deployer" {
  key_name   = "weather-app"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCAUfJQgYnVHXJl74+MGUS0uc71uFjyGjRtz4cR2ErG+gPqeddjgDnLUB264EtKMhwCOCOX6sXjtYjgz75lVlD9NnfCBVd1qY74zTdVgvykaA9u8xrAPeHXxIMIEyd7l7cMHG7ygC2GsT0qvPa6suxZjKMFiEVo37etSi6DEm/pO9cRDEZIjSHFOOhkKjf+Y1YsiDC4EMBZ79qxwOI2tT/svT/+X2tDcffbj29RZt3iCkZwoEU1CRs+njoIj0yxuYfSQKKxjqwpZW1f0lORi9Xghc52b7SotHOxDXM2bNCCQNUaxihJWF4DEAlWBWeRdH0OkcMl3r6vTV5PvlCqDBlr weather-app"
}

data "aws_security_group" "default2" {
  id ="sg-063600b5a337fd6e8"
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

