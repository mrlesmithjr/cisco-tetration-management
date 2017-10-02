# Cisco Tetration Labs

## Windows Server 2012R2+/Windows 10

### Requirements

>Note: [Chocolatey](https://chocolatey.org) needs to be installed in order to install required packages.

- Install Chocolatey

  - Open PowerShell as an administrator:

```Powershell
Set-ExecutionPolicy Bypass; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

- Install Windows Apps

```Powershell
choco install git googlechrome python2
```

After installing the above exit PowerShell and then re-open PowerShell otherwise `pip` will fail as not found.

- Install Python Virtualenv

```Powershell
pip install virtualenv
```

### Usage

Clone repo from `GitHub` [cisco-tetration-management](https://github.com/mrlesmithjr/cisco-tetration-management.git)

```PowerShell
cd ~
mkdir projects
cd projects
git clone https://github.com/mrlesmithjr/cisco-tetration-management.git
cd cisco-tetration-management
```

Create a Python virtual environment

```Powershell
virtualenv venv
```

Source the `venv` Python virtual environment

```Powershell
.\venv\Scripts\activate.ps1
```

Install additional Python modules

```Powershell
pip install -r requirements.yml
```
