# Install-Script that also sets the manifest.json with platform and guid as parameters.
# Restart of GOG Galaxy 2.0 is needed afterwards.
# See: https://github.com/gogcom/galaxy-integrations-python-api#deploy-location
param(
    [parameter(Mandatory=$true)][string]$Platform,
    [string]$Guid = (New-Guid)
)

# Platform should be lowercase in manifest.json
$Platform = $Platform.ToLower()

$SrcFolder = Resolve-Path "..\src"
$DataFile = Resolve-Path ".\games.csv"
$ManifestFile = Resolve-Path "..\src\manifest.json"
$LookupDir = Resolve-Path "$($Env:LOCALAPPDATA)\GOG.com\Galaxy\plugins\installed"
$IntegrationName = "c0-csv-$Platform-$Guid"
$IntegrationFolder = (Join-Path $LookupDir $IntegrationName)

Write-Host "Data-File: $DataFile"
Write-Host "Manifest-File: $ManifestFile"
Write-Host "Installation-Folder: $IntegrationFolder"

# $NewManifestFile = (Get-Content $ManifestFile) `
#     -replace '"(platform)"\: "(.*)"', ('"$1": "' + $Platform + '"') `
#     -replace '"(guid)"\: "(.*)"', ('"$1": "' + $Guid + '"') 
# | Out-File $ManifestFile

# Set Manifest (JSON)
$Manifest = Get-Content $ManifestFile | ConvertFrom-Json
$Manifest.platform = $Platform
$Manifest.guid = $Guid

# If the folder for the integration does not exist, create it first
if ((Test-Path $IntegrationFolder) -eq $false) {
    New-Item -Path $IntegrationFolder -ItemType Directory
}

# Copy all of src (recursively), the data-file and the new manifest.json directly into the integration folder
# We don't need folders named "__pycache__" though.
Get-ChildItem $SrcFolder -Recurse 
| Where-Object { $_.FullName -notmatch '__pycache__' } 
| Copy-Item -Destination { Join-Path $IntegrationFolder $_.Fullname.Replace($SrcFolder, "") } -Force

Copy-Item -Force -Path "$DataFile" -Destination $IntegrationFolder
ConvertTo-Json $Manifest | Out-File "$IntegrationFolder\manifest.json"

Write-Host -ForegroundColor Green "Installation done, please restart GOG Galaxy 2.0 now and connect integration from settings [Platform: $Platform, GUID: $Guid]."