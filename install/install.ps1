# Simple Copy-all-files from /src/ and the data-file to the LookUp-Folder of GOG.
# Restart of GOG Galaxy is needed afterwards.
# See: https://github.com/gogcom/galaxy-integrations-python-api#deploy-location
$SrcFolder = "..\src"
$DataFile = ".\games.data"
$LookupDir = Resolve-Path "$($Env:LOCALAPPDATA)\GOG.com\Galaxy\plugins\installed"
$IntegrationName = "c0_generic"
$Guid = "55cc6f22-6b51-441e-9b8f-c1bb59d035de"
Copy-Item -Force -Path "$SrcFolder\*" -Destination (Join-Path $LookupDir "$IntegrationName-$Guid") -Recurse
Copy-Item -Force -Path "$DataFile" -Destination (Join-Path $LookupDir "$IntegrationName-$Guid")