#!/usr/bin/env python3
"""
🚀 Serverless-Agent
Serverless Architecture Specialist

Бессерверная архитектура, FaaS, event-driven.
"""

import argparse
from pathlib import Path
from typing import Dict


class ServerlessAgent:
    """
    🚀 Serverless-Agent
    
    Специализация: Serverless Architecture
    Задачи: Lambda, Functions, Event-driven, FaaS
    """
    
    NAME = "🚀 Serverless-Agent"
    ROLE = "Serverless Architect"
    EXPERTISE = ["Serverless", "FaaS", "Event-driven", "Lambda", "Functions"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "serverless.yml": self._generate_serverless_config(),
            "handler.py": self._generate_handler(),
            "functions.yml": self._generate_functions(),
            "events.yml": self._generate_events()
        }
    
    def _generate_serverless_config(self) -> str:
        return '''# Serverless Framework Configuration
service: my-serverless-app

frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.11
  region: ${opt:region, 'us-east-1'}
  stage: ${opt:stage, 'dev'}
  memorySize: 512
  timeout: 30
  environment:
    STAGE: ${self:provider.stage}
    REGION: ${self:provider.region}
    DYNAMODB_TABLE: ${self:service}-${self:provider.stage}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:Query
            - dynamodb:Scan
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:UpdateItem
            - dynamodb:DeleteItem
          Resource: "arn:aws:dynamodb:${self:provider.region}:*:table/${self:provider.environment.DYNAMODB_TABLE}"
        - Effect: Allow
          Action:
            - sns:Publish
          Resource: "arn:aws:sns:${self:provider.region}:*:${self:service}-${self:provider.stage}-*"

plugins:
  - serverless-python-requirements
  - serverless-offline

custom:
  pythonRequirements:
    dockerizePip: non-linux
    slim: true
    strip: false
  serverless-offline:
    httpPort: 3000

package:
  patterns:
    - '!.git/**'
    - '!.gitignore'
    - '!.DS_Store'
    - '!npm-debug.log'
    - '!.serverless/**'
    - '!venv/**'
    - '!tests/**'
    - '!.pytest_cache/**'

functions:
  api:
    handler: handler.api
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
      - http:
          path: /
          method: ANY
          cors: true

  processOrder:
    handler: handler.process_order
    events:
      - http:
          path: /orders
          method: post
          cors: true

  processQueue:
    handler: handler.process_queue
    events:
      - sqs:
          arn:
            Fn::GetAtt:
              - MainQueue
              - Arn
          batchSize: 10

  scheduledTask:
    handler: handler.scheduled_task
    events:
      - schedule: rate(1 hour)

  processUpload:
    handler: handler.process_upload
    events:
      - s3:
          bucket: ${self:service}-uploads
          event: s3:ObjectCreated:*
          rules:
            - prefix: uploads/
            - suffix: .pdf

resources:
  Resources:
    # DynamoDB Table
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:provider.environment.DYNAMODB_TABLE}
        AttributeDefinitions:
          - AttributeName: pk
            AttributeType: S
          - AttributeName: sk
            AttributeType: S
        KeySchema:
          - AttributeName: pk
            KeyType: HASH
          - AttributeName: sk
            KeyType: RANGE
        BillingMode: PAY_PER_REQUEST
        StreamSpecification:
          StreamViewType: NEW_AND_OLD_IMAGES

    # SQS Queue
    MainQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: ${self:service}-${self:provider.stage}-main
        VisibilityTimeout: 60
        RedrivePolicy:
          deadLetterTargetArn:
            Fn::GetAtt:
              - DeadLetterQueue
              - Arn
          maxReceiveCount: 3

    DeadLetterQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: ${self:service}-${self:provider.stage}-dlq

    # SNS Topic
    NotificationTopic:
      Type: AWS::SNS::Topic
      Properties:
        TopicName: ${self:service}-${self:provider.stage}-notifications

  Outputs:
    ApiGatewayRestApiId:
      Value:
        Ref: ApiGatewayRestApi
      Export:
        Name: ${self:service}-${self:provider.stage}-restApiId
'''
    
    def _generate_handler(self) -> str:
        return '''import json
import os
import boto3
from datetime import datetime
from decimal import Decimal

# AWS Clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE'))

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def api(event, context):
    """Main API handler"""
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    routes = {
        ('/', 'GET'): health_check,
        ('/users', 'GET'): list_users,
        ('/users', 'POST'): create_user,
    }
    
    handler = routes.get((path, method), not_found)
    return handler(event, context)

def health_check(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'status': 'healthy',
            'service': 'serverless-api',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat()
        })
    }

def list_users(event, context):
    try:
        response = table.scan(
            FilterExpression='begins_with(pk, :prefix)',
            ExpressionAttributeValues={':prefix': 'USER#'}
        )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'users': response.get('Items', [])
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        return error_response(str(e))

def create_user(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('id', str(datetime.utcnow().timestamp()))
        
        item = {
            'pk': f'USER#{user_id}',
            'sk': f'PROFILE#{user_id}',
            'name': body.get('name'),
            'email': body.get('email'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'user': item}, cls=DecimalEncoder)
        }
    except Exception as e:
        return error_response(str(e))

def process_order(event, context):
    """Process order from API Gateway"""
    try:
        body = json.loads(event.get('body', '{}'))
        order_id = body.get('order_id')
        
        # Process order logic
        result = {
            'order_id': order_id,
            'status': 'processed',
            'processed_at': datetime.utcnow().isoformat()
        }
        
        # Send to SQS for async processing
        sqs = boto3.client('sqs')
        queue_url = os.environ.get('QUEUE_URL')
        
        if queue_url:
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(result)
            )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    except Exception as e:
        return error_response(str(e))

def process_queue(event, context):
    """Process messages from SQS queue"""
    for record in event.get('Records', []):
        message = json.loads(record['body'])
        print(f"Processing message: {message}")
        
        # Process message
        # ...
    
    return {'statusCode': 200}

def scheduled_task(event, context):
    """Run on schedule"""
    print(f"Running scheduled task at {datetime.utcnow()}")
    
    # Cleanup, reports, etc.
    
    return {'statusCode': 200}

def process_upload(event, context):
    """Process S3 upload event"""
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Processing file: s3://{bucket}/{key}")
        
        # Process file
        # ...
    
    return {'statusCode': 200}

def not_found(event, context):
    return {
        'statusCode': 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Not found'})
    }

def error_response(message, code=500):
    return {
        'statusCode': code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': message})
    }
'''
    
    def _generate_functions(self) -> str:
        return '''# Function Definitions

functions:
  # API Functions
  getUsers:
    handler: src/handlers/users.getAll
    events:
      - http:
          path: /users
          method: get
          cors: true

  getUser:
    handler: src/handlers/users.getOne
    events:
      - http:
          path: /users/{id}
          method: get
          cors: true
          request:
            parameters:
              paths:
                id: true

  createUser:
    handler: src/handlers/users.create
    events:
      - http:
          path: /users
          method: post
          cors: true

  updateUser:
    handler: src/handlers/users.update
    events:
      - http:
          path: /users/{id}
          method: put
          cors: true

  deleteUser:
    handler: src/handlers/users.delete
    events:
      - http:
          path: /users/{id}
          method: delete
          cors: true

  # Event-Driven Functions
  onUserCreated:
    handler: src/handlers/events.onUserCreated
    events:
      - eventBridge:
          eventBus: !Ref EventBus
          pattern:
            source:
              - user.service
            detail-type:
              - User Created

  onOrderPlaced:
    handler: src/handlers/events.onOrderPlaced
    events:
      - sqs:
          arn:
            Fn::GetAtt:
              - OrderQueue
              - Arn

  # Scheduled Functions
  dailyReport:
    handler: src/handlers/reports.daily
    events:
      - schedule: cron(0 9 * * ? *)  # 9 AM daily
    timeout: 60
    memorySize: 1024

  weeklyCleanup:
    handler: src/handlers/maintenance.cleanup
    events:
      - schedule: rate(7 days)

  # WebSocket Functions
  wsConnect:
    handler: src/handlers/websocket.connect
    events:
      - websocket:
          route: $connect

  wsDisconnect:
    handler: src/handlers/websocket.disconnect
    events:
      - websocket:
          route: $disconnect

  wsDefault:
    handler: src/handlers/websocket.default
    events:
      - websocket:
          route: $default
'''
    
    def _generate_events(self) -> str:
        return '''# Event Definitions

events:
  # HTTP Events
  api:
    handler: handler.api
    events:
      - http:
          path: /api/{proxy+}
          method: ANY
          cors:
            origin: '*'
            headers:
              - Content-Type
              - Authorization
            allowCredentials: true

  # WebSocket Events
  websocket:
    handler: handler.websocket
    events:
      - websocket:
          route: message
          routeResponseSelectionExpression: $default

  # S3 Events
  onFileUpload:
    handler: handler.onFileUpload
    events:
      - s3:
          bucket: uploads
          event: s3:ObjectCreated:*
          rules:
            - prefix: images/
            - suffix: .jpg
      - s3:
          bucket: uploads
          event: s3:ObjectRemoved:*

  # SQS Events
  processQueue:
    handler: handler.processQueue
    events:
      - sqs:
          arn:
            Fn::GetAtt:
              - MyQueue
              - Arn
          batchSize: 10
          maximumBatchingWindowInSeconds: 5
          functionResponseType: ReportBatchItemFailures

  # SNS Events
  onNotification:
    handler: handler.onNotification
    events:
      - sns:
          arn:
            Ref: NotificationTopic
          filterPolicy:
            type:
              - order_created
              - user_registered

  # EventBridge Events
  onEvent:
    handler: handler.onEvent
    events:
      - eventBridge:
          eventBus: !GetAtt CustomEventBus.Name
          pattern:
            source:
              - myapp.orders
            detail-type:
              - Order Placed
              - Order Cancelled

  # DynamoDB Stream Events
  onTableChange:
    handler: handler.onTableChange
    events:
      - stream:
          type: dynamodb
          arn:
            Fn::GetAtt:
              - UsersTable
              - StreamArn
          filterPatterns:
            - eventName: [INSERT, MODIFY]

  # Cognito Events
  onUserSignUp:
    handler: handler.onUserSignUp
    events:
      - cognitoUserPool:
          pool: UserPool
          trigger: PostConfirmation

  # CloudWatch Events
  onAlarm:
    handler: handler.onAlarm
    events:
      - cloudwatchEvent:
          event:
            source:
              - aws.cloudwatch
            detail-type:
              - CloudWatch Alarm State Change
            detail:
              state:
                value:
                  - ALARM
'''


def main():
    parser = argparse.ArgumentParser(description="🚀 Serverless-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = ServerlessAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🚀 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
