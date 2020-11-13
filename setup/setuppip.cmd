call C:\Work\Python\pipver.cmd
%COMSPEC% /s /c "echo Installing pip==%PYTHON_PIP_VERSION% ..."
%COMSPEC% /s /c "C:\Work\Python\python.exe C:\Work\Python\get-pip.py --disable-pip-version-check --no-cache-dir pip==%PYTHON_PIP_VERSION%"
echo Removing ...
del /f /q C:\Work\Python\get-pip.py C:\Work\Python\pipver.cmd
echo Verifying install ...
echo   python --version
python --version
echo Verifying pip install ...
echo   pip --version
pip --version
echo Complete.