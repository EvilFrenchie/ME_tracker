#configure the azure provider
terraform {
  cloud {
    organization = "evil-frenchie"

    workspaces {
      name = "ME_tracker"
    }
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

#create a resource group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = "eastus2"

  tags = {
    Team = "EF"
  }
}

resource "azurerm_container_registry" "acr" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}


resource "azurerm_service_plan" "svcplan" {
  name                = var.service_plan_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}


resource "azurerm_linux_web_app" "app" {
  name                = var.linux_web_app_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_service_plan.svcplan.location
  service_plan_id     = azurerm_service_plan.svcplan.id
  site_config {
      
  }
}

