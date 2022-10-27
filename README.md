# M365GroupDrives
Enumerate all public group drives and files (Microsoft GraphAPI using Azure Powershell AppID)

## Usage
```
$ python3 ~/Tools/M365GroupDrives.py
usage: M365GroupDrives.py [-h] [-t access_token] [-a tenant_domain] [-p]

List all drives & files in public Microsoft 365 Groups

optional arguments:
  -h, --help        show this help message and exit
  -t access_token   OAuth Access token authenticated to https://graph.microsoft.com/
  -a tenant_domain  tenant domain used to retrieve access_token
  -p                Include private groups the user has been invited too
```

## Example Output
```
$ python3 ~/Tools/M365GroupDrives.py -a PWNED.io
OAuth Authenticating as Azure Active Directory PowerShell to https://graph.microsoft.com/
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code XXXXXXXXX to authenticate.
Access Token: ******************************************************************

$ python3 ~/Tools/M365GroupDrives.py -p -t *********************************************************************88

PWNED Security - Management
description: PWNED Security
createdDateTime: 2019-05-23T22:58:39Z
creationOptions: ['ProvisionGroupHomepage', 'HubSiteId:00000000-0000-0000-0000-000000000000', 'SPSiteLanguage:1033']
mail: PWNEDSecurity@PWNED.io
securityEnabled: False
Drive: Documents
driveType: documentLibrary
Created: System Account (2019-05-15T03:26:42Z)
/:

PWNED Security - All
description: PWNED Security - All
createdDateTime: 2019-08-28T13:33:33Z
mail: PWNEDsecurity-all@PWNED.io
securityEnabled: False
Drive: Documents
driveType: documentLibrary
Created: System Account (2019-08-28T02:00:51Z)
/:
contract_list.xlsx t:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet m:Tony Stark(2022-01-11T16:52:02Z) s:15705
/Invoices:
/Invoices/2022 - Rise of the Machines:
ProblemTracker.xlsx t:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet m:Tony Stark(2022-10-26T12:48:38Z) s:14267
/content:
Taxes version (2.2.0).zip t:application/zip m:Tony Stark(2021-08-13T23:25:43Z) s:24290330
/Legal:
/Legal/Witnesses:
Part-10 - Broadband.m4v t:video/mp4 m:Bruce Banner(2019-12-10T22:17:25Z) s:45187797
```
