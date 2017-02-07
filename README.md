# Power BI Embedded Workspace
A simple script for creating [Power BI Embedded](https://azure.microsoft.com/en-us/services/power-bi-embedded/) Workspaces and uploading reports in one command.

## Usage
You have two options:

- [Python script directly](#python-script-directly)
- [Use Docker with tools already installed](Use Docker with tools already installed)

### Python script directly
The python script above assumes you have already installed the following and they are on your path:

- [PowerBi CLI](https://github.com/Microsoft/PowerBI-Cli)
- [Azure CLI](https://docs.microsoft.com/en-us/azure/xplat-cli-install)  

After those tools are installed you can run it with the following:

```bash
python createworkspacecollection.py -s <azure-subscription-id> -r <azure-resource-group> -w <workspace-collection-name> -l <azure-location> -f <path-to-pbix-file> -n <datasource-name> -u <datasource-username> -p <datasource-password>
```

### Use Docker with tools already installed
You can either pull this repository and build the docker image locally or you can grab a image from [my Docker Hub repository](https://hub.docker.com/r/jsturtevant/power-bi-embedded-workspace-script/).

Navigate to the location of the PowerBi Embedded ```.pbix``` file and run the following.  This created a volume in docker and links the current directory up in the Docker Container allowing the script to see the ```.pbix``` file (below works on windows; Change ```%CD%``` to ```$(pwd)``` on a mac/linux).

```bash
docker run -it --rm -v %CD%:/usr/src/ jsturtevant/power-bi-embedded-workspace-script python createworkspacecollection.py -s <azure-subscription-id> -r <azure-resource-group> -w <workspace-collection-name> -l <azure-location> -f <path-to-pbix-file> -n <datasource-name> -u <datasource-username> -p <datasource-password>
```

## Important notes

- As of writing there is a [bug in PowerBI Embedded CLI](https://github.com/Microsoft/PowerBI-Cli/issues/5) on macs and linux.  The [fix-pbcli-linux](https://github.com/jsturtevant/power-bi-embedded-workspace-script/blob/master/fix-pbcli-linux.sh) shows how to fix on linux and the issue tells you [how to fix on mac](https://github.com/Microsoft/PowerBI-Cli/issues/5).
- Your workspace collection name must be unique across all workspace collection names in Azure.
- The script currently only uploads one file but could easily be tweaked to upload all reports in a folder.
