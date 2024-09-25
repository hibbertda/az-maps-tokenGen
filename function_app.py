import azure.functions as func
import logging
import os
import datetime
import requests
import json

from azure.mgmt.maps import AzureMapsManagementClient
from azure.mgmt.maps.models import MapsAccountSasToken, AccountSasParameters
from azure.identity import DefaultAzureCredential, ClientSecretCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.ADMIN)

@app.route(route="token_gen")
def token_gen(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Replace with your subscription ID and resource group name
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    logging.info(f"Subscription ID: {subscription_id}")
    resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
    logging.info(f"Resource Group Name: {resource_group_name}")
    account_name = os.getenv("AZURE_MAPS_NAME")
    logging.info(f"Account Name: {account_name}")

    # Authenticate with Azure
    credential = DefaultAzureCredential()   
    maps_client = AzureMapsManagementClient(
        credential, 
        subscription_id
        )

    # Define the SAS token parameters
    sas_parameters = AccountSasParameters(
        signing_key="primaryKey",
        principal_id=os.getenv("AZUREM_MAPS_PRINCIPAL_ID"),
        max_rate_per_second=500,
        start=datetime.datetime.utcnow().isoformat() + 'Z',
        expiry=(datetime.datetime.utcnow() + datetime.timedelta(hours=12)).isoformat() + 'Z'
    )

    try:
        sas_token = maps_client.accounts.list_sas(
            resource_group_name, 
            account_name, 
            sas_parameters
        )

        return func.HttpResponse(
            json.dumps(
                {
                    "sas_token": sas_token.account_sas_token,
                    "expiry": sas_parameters.expiry,
                    "url": f"https://atlas.microsoft.com"
                }
            ),
            mimetype="application/json",
        )
    
    except Exception as e:
        # Log the exception if needed
        print(f"Error occurred: {e}")
        sas_token = "Authorization service down"
        return func.HttpResponse(f"Error occurred: {e}", status_code=500)

    
