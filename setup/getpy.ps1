$ErrorActionPreference = 'Stop'
$ProgressPreference = 'Continue'
$verbosePreference='Continue';

Write-Output "PYTHON_RELEASE=$env:PYTHON_RELEASE"
Write-Output "PYTHON_VERSION=$env:PYTHON_VERSION"

$pythonUrl = "https://www.python.org/ftp/python/$env:PYTHON_RELEASE/python-$env:PYTHON_VERSION-embed-amd64.zip"
Write-Output "PYTHON_URL=$pythonUrl"

[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;
Invoke-WebRequest -UseBasicParsing -Uri $pythonUrl -Out 'Python.zip';
Expand-Archive -Path "Python.zip";
Invoke-WebRequest -UseBasicParsing -Uri "$env:PYTHON_GET_PIP_URL" -OutFile 'Python\get-pip.py';

[String]::Format('@set PYTHON_PIP_VERSION={0}', $env:PYTHON_PIP_VERSION) | Out-File -FilePath 'Python\pipver.cmd' -Encoding ASCII;
$FileVer = [System.Version]::Parse([System.Diagnostics.FileVersionInfo]::GetVersionInfo('Python\python.exe').ProductVersion);
$Postfix = $FileVer.Major.ToString() + $FileVer.Minor.ToString();
Remove-Item -Path "Python\python$Postfix._pth";
Expand-Archive -Path "Python\python$Postfix.zip" -Destination "Python\Lib";
Remove-Item -Path "Python\python$Postfix.zip";
New-Item -Type Directory -Path "Python\DLLs";