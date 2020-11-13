setx.exe /m PATH "%PATH%;%PYTHONPATH%"
setx.exe /m PYTHONPATH %PYTHONPATH%
setx.exe /m PIP_CACHE_DIR C:\Users\ContainerUser\AppData\Local\pip\Cache
reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f

assoc .py=Python.File
assoc .pyc=Python.CompiledFile
assoc .pyd=Python.Extension
assoc .pyo=Python.CompiledFile
assoc .pyw=Python.NoConFile
assoc .pyz=Python.ArchiveFile
assoc .pyzw=Python.NoConArchiveFile
ftype Python.ArchiveFile="C:\Work\Python\python.exe" "%1" %*
ftype Python.CompiledFile="C:\Work\Python\python.exe" "%1" %*
ftype Python.File="C:\Work\Python\python.exe" "%1" %*
ftype Python.NoConArchiveFile="C:\Work\Python\pythonw.exe" "%1" %*
ftype Python.NoConFile="C:\Work\Python\pythonw.exe" "%1" %*