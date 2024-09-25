**Azure Maps SASToken Generator**
=====================================

**Overview**
-----------

This Azure Function generates SAS (Shared Access Signature) tokens for accessing the Azure Maps service. It authenticates with Azure, retrieves an account's SAS token parameters, and returns a valid SAS token along with its expiry time and URL. The intended use is as an API called for user facing applications to load data from Azure Maps.

**Prerequisites**
-----------------

* An Azure subscription
* A resource group containing an Azure Maps account
* Environment variables set:
	+ `AZURE_SUBSCRIPTION_ID`: the ID of your Azure subscription
	+ `RESOURCE_GROUP_NAME`: the name of the resource group containing your Azure Maps account
	+ `AZURE_MAPS_NAME`: the name of your Azure Maps account
	+ `AZUREM_MAPS_PRINCIPAL_ID`: the principal ID of your Azure Maps account

## Authentication

The Azure Function is configured with a Managed Identity which is granted permissions to access the Azure Maps service and generate SAS Tokens. Using the Azure `DefaultAzureCredential` method for authentication will automatically attempt to use Managed Identity for authentication, no additional configuration is required.

### Required Permissions

A role that includes the **Microsoft.Maps/accounts/listSas/action** in order to list Azure Maps service keys required to generate SAS tokens.

**Function Details**
-------------------

* **Name**: token_gen
* **Route**: /token_gen (GET)
* **Authentication**: Admin-only authentication using HTTP headers

**Environment Variables**
-------------------------

The following environment variables are required:

| Variable | Description |
| --- | --- |
| `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID |
| `RESOURCE_GROUP_NAME` | The name of the resource group containing your Azure Maps account |
| `AZURE_MAPS_NAME` | The name of your Azure Maps account |
| `AZUREM_MAPS_PRINCIPAL_ID` | The principal ID of your Azure Maps account |

**Usage**
----------

To use this function, send a GET request to the `/token_gen` endpoint. The response will be a JSON object containing the generated SAS token, its expiry time, and the URL for accessing the Azure Maps service.

Example response:
```json
{
  "sas_token": "<generated_sastoken>",
  "expiry": "2023-02-20T14:30:00Z",
  "url": "https://atlas.microsoft.com"
}
```
**Notes**
--------

* This function uses the `DefaultAzureCredential` class to authenticate with Azure. You can replace this with a different credential type if needed.
* The SAS token generated by this function is valid for 12 hours and has a rate limit of 500 requests per second.
* If an error occurs while generating the SAS token, the function will return a JSON object with an error message and a status code of 500.