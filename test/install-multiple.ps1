# Simple Copy-all-files from /src/ and the data-file to the LookUp-Folder of GOG.
# Restart of GOG Galaxy is needed afterwards.
# See: https://github.com/gogcom/galaxy-integrations-python-api#deploy-location

$SrcFolder = "..\src"
$DataFile = ".\games.data"
$ManifestFile = "..\src\manifest.json"
$PluginFile = "..\src\plugin.py"
$LookupDir = "$($Env:LOCALAPPDATA)\GOG.com\Galaxy\plugins\installed"



foreach ($Platform in $Platforms) {
    $PlatformId = $Platform[0]
    $PlatformEnum = $Platform[1]
    $Guid = New-Guid

    Write-Host "Installing $PlatformId-$Guid"

    $r1 = (Get-Content $ManifestFile) `
        -replace '"(platform)"\: "(.*)"', ('"$1": "' + $PlatformId + '"') `
        -replace '"(guid)"\: "(.*)"', ('"$1": "' + $Guid + '"') 
    | Out-File $ManifestFile

    $r2 = (Get-Content $PluginFile) `
        -replace "Platform\.(.*), #", "Platform.$PlatformEnum, #"
    | Out-File $PluginFile

    #Write-Host -ForegroundColor Yellow ($r1 -match "Platform`"")
    #Write-Host -ForegroundColor Yellow ($r2 -match "# S")

    $IntegrationName = "c0-$PlatformId-$Guid"

    if ((Test-Path (Join-Path $LookupDir "$IntegrationName")) -eq $false) {
        New-Item -Path (Join-Path $LookupDir "$IntegrationName") -ItemType Directory
    }
    Copy-Item -Force -Path "$SrcFolder\*" -Destination (Join-Path $LookupDir "$IntegrationName") -Recurse
    Copy-Item -Force -Path "$DataFile" -Destination (Join-Path $LookupDir "$IntegrationName")
}

