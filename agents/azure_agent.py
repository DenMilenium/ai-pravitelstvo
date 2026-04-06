#!/usr/bin/env python3
"""
🔷 Azure-Agent
Microsoft Azure Specialist

Облачные решения на Microsoft Azure.
"""

import argparse
from pathlib import Path
from typing import Dict


class AzureAgent:
    """
    🔷 Azure-Agent
    
    Специализация: Microsoft Azure
    Задачи: VMs, Functions, ARM, DevOps
    """
    
    NAME = "🔷 Azure-Agent"
    ROLE = "Azure Cloud Engineer"
    EXPERTISE = ["Azure", "ARM Templates", "Azure Functions", "AKS", "DevOps"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "arm-template.json": self._generate_arm(),
            "azure-pipelines.yml": self._generate_pipeline(),
            "function.cs": self._generate_function(),
            "terraform-azure.tf": self._generate_terraform()
        }
    
    def _generate_arm(self) -> str:
        return '''{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environment": {
      "type": "string",
      "defaultValue": "production",
      "allowedValues": ["development", "staging", "production"]
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "variables": {
    "appName": "[concat('myapp-', parameters('environment'))]",
    "storageName": "[concat('myapp', uniqueString(resourceGroup().id))]"
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2023-01-01",
      "name": "[variables('storageName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2",
      "properties": {
        "supportsHttpsTrafficOnly": true
      }
    },
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2022-03-01",
      "name": "[variables('appName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "S1",
        "tier": "Standard",
        "size": "S1",
        "family": "S",
        "capacity": 1
      },
      "kind": "linux",
      "properties": {
        "reserved": true
      }
    },
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2022-03-01",
      "name": "[variables('appName')]",
      "location": "[parameters('location')]",
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', variables('appName'))]"
      ],
      "kind": "app,linux",
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('appName'))]",
        "siteConfig": {
          "linuxFxVersion": "PYTHON|3.11",
          "appSettings": [
            {
              "name": "ENVIRONMENT",
              "value": "[parameters('environment')]"
            },
            {
              "name": "WEBSITES_ENABLE_APP_SERVICE_STORAGE",
              "value": "false"
            }
          ]
        }
      }
    },
    {
      "type": "Microsoft.Sql/servers",
      "apiVersion": "2022-05-01-preview",
      "name": "[concat(variables('appName'), '-sql')]",
      "location": "[parameters('location')]",
      "properties": {
        "administratorLogin": "sqladmin",
        "administratorLoginPassword": "[parameters('sqlPassword')]",
        "version": "12.0"
      },
      "resources": [
        {
          "type": "firewallRules",
          "apiVersion": "2022-05-01-preview",
          "name": "AllowAllAzureIps",
          "dependsOn": [
            "[resourceId('Microsoft.Sql/servers', concat(variables('appName'), '-sql'))]"
          ],
          "properties": {
            "startIpAddress": "0.0.0.0",
            "endIpAddress": "0.0.0.0"
          }
        }
      ]
    },
    {
      "type": "Microsoft.Insights/components",
      "apiVersion": "2020-02-02",
      "name": "[variables('appName')]",
      "location": "[parameters('location')]",
      "kind": "web",
      "properties": {
        "Application_Type": "web"
      }
    }
  ],
  "outputs": {
    "appUrl": {
      "type": "string",
      "value": "[concat('https://', variables('appName'), '.azurewebsites.net')]"
    },
    "storageAccountName": {
      "type": "string",
      "value": "[variables('storageName')]"
    }
  }
}
'''
    
    def _generate_pipeline(self) -> str:
        return '''trigger:
  branches:
    include:
      - main
      - develop

variables:
  azureSubscription: 'Azure-Connection'
  resourceGroup: 'myapp-rg'
  location: 'westeurope'
  environment: 'production'

stages:
- stage: Build
  displayName: 'Build Stage'
  jobs:
  - job: Build
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.11'
      displayName: 'Use Python 3.11'

    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
      displayName: 'Install dependencies'

    - script: |
        pip install pytest pytest-cov
        pytest tests/ --cov=app --cov-report=xml
      displayName: 'Run tests'

    - task: PublishTestResults@2
      inputs:
        testResultsFiles: '**/test-*.xml'
        testRunTitle: 'Python Tests'

    - task: ArchiveFiles@2
      inputs:
        rootFolderOrFile: '$(Build.SourcesDirectory)'
        includeRootFolder: false
        archiveType: 'zip'
        archiveFile: '$(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip'
        replaceExistingArchive: true

    - task: PublishBuildArtifacts@1
      inputs:
        PathtoPublish: '$(Build.ArtifactStagingDirectory)'
        ArtifactName: 'drop'

- stage: Deploy
  displayName: 'Deploy Stage'
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: Deploy
    pool:
      vmImage: 'ubuntu-latest'
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureResourceGroupDeployment@2
            inputs:
              azureSubscription: $(azureSubscription)
              action: 'Create Or Update Resource Group'
              resourceGroupName: $(resourceGroup)
              location: $(location)
              templateLocation: 'Linked artifact'
              csmFile: '$(Pipeline.Workspace)/drop/arm-template.json'
              overrideParameters: '-environment $(environment)'
              deploymentMode: 'Incremental'

          - task: AzureWebApp@1
            inputs:
              azureSubscription: $(azureSubscription)
              appType: 'webAppLinux'
              appName: 'myapp-$(environment)'
              package: '$(Pipeline.Workspace)/drop/$(Build.BuildId).zip'
              runtimeStack: 'PYTHON|3.11'
'''
    
    def _generate_function(self) -> str:
        return '''using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace MyAzureFunctions
{
    public static class HttpFunctions
    {
        [FunctionName("HealthCheck")]
        public static async Task<IActionResult> HealthCheck(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "health")] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("Health check executed");
            
            return new OkObjectResult(new 
            { 
                status = "healthy", 
                timestamp = DateTime.UtcNow,
                version = "1.0.0"
            });
        }

        [FunctionName("ProcessOrder")]
        public static async Task<IActionResult> ProcessOrder(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders")] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("Processing order");

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            dynamic data = JsonConvert.DeserializeObject(requestBody);

            string orderId = data?.orderId;
            string customerName = data?.customerName;

            if (string.IsNullOrEmpty(orderId))
            {
                return new BadRequestObjectResult("Order ID is required");
            }

            // Process order logic here
            var result = new
            {
                orderId = orderId,
                status = "processed",
                processedAt = DateTime.UtcNow
            };

            return new OkObjectResult(result);
        }

        [FunctionName("TimerCleanup")]
        public static void TimerCleanup(
            [TimerTrigger("0 0 * * * *")] TimerInfo timer,
            ILogger log)
        {
            log.LogInformation($"Cleanup executed at: {DateTime.Now}");
            
            // Cleanup logic here
        }

        [FunctionName("QueueProcessor")]
        public static void QueueProcessor(
            [QueueTrigger("myqueue-items", Connection = "AzureWebJobsStorage")] string myQueueItem,
            ILogger log)
        {
            log.LogInformation($"Queue item received: {myQueueItem}");
            
            // Process queue item
        }
    }
}
'''
    
    def _generate_terraform(self) -> str:
        return '''# Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.75"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.project_name}-${var.environment}-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "S1"
}

# Linux Web App
resource "azurerm_linux_web_app" "main" {
  name                = "${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "ENVIRONMENT" = var.environment
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }
}

# Azure Container Registry
resource "azurerm_container_registry" "main" {
  name                = "${var.project_name}${var.environment}acr"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"
  admin_enabled       = true
}

# Azure Kubernetes Service
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.project_name}-${var.environment}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.project_name}${var.environment}"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }
}

# Variables
variable "project_name" {
  default = "myapp"
}

variable "environment" {
  default = "production"
}

variable "location" {
  default = "westeurope"
}

# Outputs
output "app_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}
'''


def main():
    parser = argparse.ArgumentParser(description="🔷 Azure-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = AzureAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🔷 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
