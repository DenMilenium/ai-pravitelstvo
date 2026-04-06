#!/usr/bin/env python3
"""
☁️ AWS-Agent
Amazon Web Services Specialist

Облачные решения на AWS.
"""

import argparse
from pathlib import Path
from typing import Dict


class AWSAgent:
    """
    ☁️ AWS-Agent
    
    Специализация: Amazon Web Services
    Задачи: EC2, S3, Lambda, RDS, CloudFormation
    """
    
    NAME = "☁️ AWS-Agent"
    ROLE = "AWS Cloud Engineer"
    EXPERTISE = ["AWS", "CloudFormation", "Lambda", "EC2", "S3", "RDS"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "cloudformation.yaml": self._generate_cloudformation(),
            "terraform-aws.tf": self._generate_terraform(),
            "lambda-handler.py": self._generate_lambda(),
            "deploy.sh": self._generate_deploy()
        }
    
    def _generate_cloudformation(self) -> str:
        return '''AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Infrastructure Stack'

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues:
      - development
      - staging
      - production

Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpc'

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-igw'

  # S3 Bucket
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${Environment}-app-bucket-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256

  # Lambda Function
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-api-handler'
      Runtime: python3.11
      Handler: index.handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: |
          def handler(event, context):
              return {'statusCode': 200, 'body': 'Hello from Lambda'}
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment

  # RDS Instance
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: !Sub '${Environment}-db'
      DBInstanceClass: db.t3.micro
      Engine: postgres
      MasterUsername: admin
      MasterUserPassword: '{{resolve:secretsmanager:DBSecret:SecretString:password}}'
      AllocatedStorage: 20
      StorageEncrypted: true
      MultiAZ: false
      PubliclyAccessible: false
      VPCSecurityGroups:
        - !Ref DBSecurityGroup

  # Security Group
  DBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Database Security Group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref AppSecurityGroup

  # IAM Role
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

Outputs:
  S3BucketName:
    Description: S3 Bucket Name
    Value: !Ref S3Bucket
  LambdaFunctionArn:
    Description: Lambda Function ARN
    Value: !GetAtt LambdaFunction.Arn
'''
    
    def _generate_terraform(self) -> str:
        return '''# AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "${var.project_name}-${var.environment}"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false
}

# ECR Repository
resource "aws_ecr_repository" "app" {
  name                 = "${var.project_name}/${var.environment}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets

  enable_deletion_protection = false
}

# Security Groups
resource "aws_security_group" "alb" {
  name_prefix = "${var.project_name}-alb-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Variables
variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "production"
}

variable "project_name" {
  default = "myapp"
}
'''
    
    def _generate_lambda(self) -> str:
        return '''import json
import boto3
import os

def handler(event, context):
    """
    AWS Lambda Handler
    """
    # Environment variables
    env = os.environ.get('ENVIRONMENT', 'development')
    
    # Parse request
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Route handling
    if http_method == 'GET' and path == '/health':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'healthy', 'env': env})
        }
    
    elif http_method == 'GET' and path == '/users':
        # Example: Get users from DynamoDB
        users = get_users()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'users': users})
        }
    
    elif http_method == 'POST' and path == '/users':
        body = json.loads(event.get('body', '{}'))
        user = create_user(body)
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(user)
        }
    
    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not found'})
    }

def get_users():
    """Get users from DynamoDB"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    
    response = table.scan()
    return response.get('Items', [])

def create_user(data):
    """Create user in DynamoDB"""
    import uuid
    from datetime import datetime
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    
    user = {
        'id': str(uuid.uuid4()),
        'name': data.get('name'),
        'email': data.get('email'),
        'created_at': datetime.utcnow().isoformat()
    }
    
    table.put_item(Item=user)
    return user
'''
    
    def _generate_deploy(self) -> str:
        return '''#!/bin/bash
# AWS Deployment Script

set -e

ENVIRONMENT=${ENVIRONMENT:-production}
STACK_NAME="myapp-${ENVIRONMENT}"
REGION=${AWS_REGION:-us-east-1}

echo "🚀 Deploying to AWS..."
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

# Validate template
echo "📋 Validating CloudFormation template..."
aws cloudformation validate-template \\
    --template-body file://cloudformation.yaml

# Deploy stack
echo "☁️ Deploying CloudFormation stack..."
aws cloudformation deploy \\
    --template-file cloudformation.yaml \\
    --stack-name $STACK_NAME \\
    --region $REGION \\
    --parameter-overrides Environment=$ENVIRONMENT \\
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

# Get outputs
echo "📤 Stack outputs:"
aws cloudformation describe-stacks \\
    --stack-name $STACK_NAME \\
    --query 'Stacks[0].Outputs' \\
    --output table

echo "✅ Deployment complete!"
'''


def main():
    parser = argparse.ArgumentParser(description="☁️ AWS-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = AWSAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"☁️ {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
