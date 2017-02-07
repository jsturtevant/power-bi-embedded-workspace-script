#python createworkspacecollection.py -s <azure subscription id> -r resourcegroupname -w workspacename -l eastus2 -f <pbixfile> -n <datasetid> -u <username> -p <pass>

import argparse
import json
import re
from subprocess import call
from subprocess import check_output

parser = argparse.ArgumentParser(description='create powerbi for tenant')
parser.add_argument('-s','--subscription', type=str,
                    help='subscription id')
parser.add_argument('-r','--resoucegroup', type=str,
                    help='resource group name')                   
parser.add_argument('-w','--workspace', type=str,
                    help='workspace collection name')
parser.add_argument('-l','--location', type=str,
                    help='azure location')
parser.add_argument('-f','--pbixfile', type=str,
                    help='powerbi pbix file path')
parser.add_argument('-n','--pbixfilename', type=str,
                    help='powerbi pbix file name')
parser.add_argument('-u','--username', type=str,
                    help='powerbi dataset username')
parser.add_argument('-p','--password', type=str,
                    help='powerbi dataset password')
parser.add_argument('-v','--verbose', type=bool,
                    help='verbose output', default=False)

args = parser.parse_args()

def callcmd(cmdToRun):
    if (args.verbose):
        print(cmdToRun)
    cmd = cmdToRun.split()
    call(cmd)

def callcmd_with_return(cmdToRun):
    if (args.verbose):
        print(cmdToRun)

    cmd = cmdToRun.split()
    output = check_output(cmd)

    if (args.verbose):
        print(output)
    return output.decode("utf-8") 

def get_guid(guid_string_to_match):
    guidmatch = re.search("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", guid_string_to_match)
    return guidmatch.group()

def get_dataset_guid(guid_string_to_match, dataset_name):
    datasetidmatch = re.search("ID: [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12} | Name: " + dataset_name,guid_string_to_match)
    datasetid = datasetidmatch.group()

    return get_guid(datasetid)

callcmd("azure login")
callcmd(f"azure account set {args.subscription}")

#register powerbi provider (see https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-common-deployment-errors#noregisteredproviderfound)
callcmd("azure provider register Microsoft.PowerBI") 
callcmd(f"azure powerbi create {args.resoucegroup} {args.workspace} {args.location}")

# load the keys
keystring = callcmd_with_return(f"azure powerbi keys list {args.resoucegroup} {args.workspace} --json")
keys = json.loads(keystring)
accesskey = keys['key1']

# create workspace
# the output from nodejs is string format.  extract with regex
workspacecreated = callcmd_with_return(f"powerbi create-workspace -c {args.workspace} -k {accesskey}")
workspaceid = get_guid(workspacecreated)
print("workspaceid: " + workspaceid)

# import file
callcmd(f"powerbi import -c {args.workspace} -w {workspaceid} -k {accesskey} -f {args.pbixfile} -n {args.pbixfilename}")

# get dataset id and set the conneciton info
datasetsoutput = callcmd_with_return(f"powerbi get-datasets -c {args.workspace} -w {workspaceid} -k {accesskey}")
datasetid = get_dataset_guid(datasetsoutput, args.pbixfilename)
print("datasetid: " + datasetid)

callcmd(f"powerbi update-connection -c {args.workspace} -w {workspaceid} -k {accesskey} -d {datasetid} -u {args.username} -p {args.password}")