import adal
import requests
import argparse
import sys

# device code authentication using default Azure Application 'Azure Powershell' for Microsoft Graph API resource
def graph_auth(tenant_domain):
    context = adal.AuthenticationContext("https://login.microsoftonline.com/%s" % tenant_domain)
    code = context.acquire_user_code("https://graph.microsoft.com/", "1b730954-1685-4b74-9bfd-dac224a7b894")
    print(code['message'])
    tokendata = context.acquire_token_with_device_code("https://login.microsoftonline.com/%s" % tenant_domain, code, "1b730954-1685-4b74-9bfd-dac224a7b894")
    return tokendata['accessToken']

# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
class Colour:
    BOLDBLUE = '\033[0;1;34m'
    YELLOW = '\033[0;33m'
    GREEN = '\033[0;32m'
    END = '\033[0m'

# parse path from parent reference
def parse_path(parent_path):
    index = parent_path.find("root:")
    if index > len(parent_path) or index == -1:
        return ""
    else:
        return parent_path[index+5:]

# TODO: tree output?
# list files in drive
def list_drive(headers, drive_id, item_id = "root", nextLink = ""):
    resp = requests.get("https://graph.microsoft.com/v1.0/drives/%s/items/%s/children%s" % (drive_id,item_id, nextLink), headers=headers)
    if resp.status_code != 200:
        print("HTTP error %s on items" % resp.status_code)
        return
    resp_json = resp.json()
    items = resp_json['value']

    # iterate files first then folders for outputing purposes
    for item in items:
        if "file" in item:
            item_name = f"{Colour.GREEN}%s{Colour.END}" % item["name"]
            print("%s t:%s m:%s(%s) s:%s" % (item_name,item["file"]["mimeType"],item["lastModifiedBy"]["user"]["displayName"],item["lastModifiedDateTime"],item["size"]))
    for item in items:
        if "folder" in item:
            item_path = "%s/%s" % (parse_path(item["parentReference"]["path"]) , item["name"])
            print(f"{Colour.YELLOW}%s:{Colour.END}" % (item_path))
            list_drive(headers, drive_id, item["id"])
    
    # if results exceed 200, follow pagination
    if '@odata.nextLink' in resp_json:
        next_link = resp_json['@odata.nextLink']
        next_querystring = next_link[next_link.find("?"):]
        list_drive(headers, drive_id, item_id, next_querystring)

def main():
    parser = argparse.ArgumentParser(add_help=True, description='List all drives & files in public Microsoft 365 Groups')
    parser.add_argument('-t', metavar='access_token', dest='access_token', help='OAuth Access token authenticated to https://graph.microsoft.com/')
    parser.add_argument('-a', metavar='tenant_domain', dest='tenant_domain', help='tenant domain used to retrieve access_token')
    parser.add_argument('-p', dest='show_private', action='store_true', help='Include private groups the user has been invited too')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()

    if options.tenant_domain != None:
        print("OAuth Authenticating as Azure Active Directory PowerShell to https://graph.microsoft.com/")
        print("Access Token: %s" % graph_auth(options.tenant_domain))
        sys.exit()

    # Graph API auth headers
    headers = {
        'Authorization': "Bearer %s" % options.access_token,
        'Content-Type': 'application/json',
    }

    # get all Microsoft 365 Groups(Unified)
    resp = requests.get("https://graph.microsoft.com/v1.0/groups?$filter=groupTypes/any(c:c+eq+'Unified')", headers=headers)
    if resp.status_code != 200:
        print("HTTP error %s when querying Microsoft Graph API" % (resp.status_code))
        sys.exit()

    # get public group ids
    groups = resp.json()["value"]
    for group in groups:
        if not options.show_private:
            # skip if group is not public (this will not show groups you have been invited too)
            if group["visibility"] != "Public":
                continue

        group_name = group["displayName"]
        group_id = group["id"]
        print(f"{Colour.BOLDBLUE}%s{Colour.END}" % group_name)
        print("description: %s" % group["description"])
        print("createdDateTime: %s" % group["createdDateTime"])
        if group["creationOptions"] != []:
            print("creationOptions: %s" % group["creationOptions"])
        if group["deletedDateTime"] != None:
            print("deletedDateTime: %s" % group["deletedDateTime"])
        if group["mailEnabled"]:
            print("mail: %s" % group["mail"])
        # TODO: on premise data
        if group["onPremisesSamAccountName"] != None:
            print("onPremisesSamAccountName: %s" % group["onPremisesSamAccountName"])
        if group["isAssignableToRole"] != None:
            print("isAssignableToRole: %s" % group["isAssignableToRole"])
        if group["membershipRule"] != None:
            print("membershipRule: %s" % group["membershipRule"])
        if group["resourceBehaviorOptions"] != []:
            print("resourceBehaviorOptions: %s" % group["resourceBehaviorOptions"])
        print("securityEnabled: %s" % group["securityEnabled"])


        # get site-ids for public groups
        # resp = requests.get("https://graph.microsoft.com/v1.0/groups/%s/sites/root" % group_id, headers=headers)
        # if resp.status_code != 200:
        #     print("HTTP error %s on group %s" % (resp.status_code,group_name))
        #     print()
        #     continue
        # site = resp.json()
        # site_id = site["id"]
        # site_name = site["displayName"]
        # print(f"{Colour.YELLOW}Site: %s{Colour.END}" % site_name)
        # get drives(Document Libraries) for sites
        # resp = requests.get("https://graph.microsoft.com/v1.0/sites/%s/drives" % site_id, headers=headers)

        # get drive-ids for public groups
        resp = requests.get("https://graph.microsoft.com/v1.0/groups/%s/drives" % group_id, headers=headers)
        if resp.status_code != 200:
            print("HTTP error %s on group %s drives" % (resp.status_code,group_name))
            print()
            continue
        drives = resp.json()['value']
        for drive in drives:
            drive_name = drive["name"]
            drive_id = drive["id"]
            # print drive details
            print(f"{Colour.YELLOW}Drive: %s{Colour.END}" % drive_name)
            print("driveType: %s" % drive["driveType"])
            print("Created: %s (%s)" % (drive["createdBy"]["user"]["displayName"], drive["createdDateTime"]))
            if "lastModified" in drive:
                print("lastModified: %s (%s)" % (drive["lastModifiedBy"]["user"]["displayName"], drive["lastModifiedDateTime"]))

            # print drive contents
            print(f"{Colour.YELLOW}/:{Colour.END}")
            list_drive(headers, drive_id)
        
        print()

if __name__ == "__main__":
    main()
