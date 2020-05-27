# AzureVMAutomation

Web automation program to control virtul machine(s) on Azure Portal. 

## Getting Started

This python program will automatically start virtul machine(s) on Azure Portal with using Selenium. 
So far, it only has function to start the vm, but eventually I will add more functions (such as stop vm).

### Prerequisites

To run this program, Python (with selenium module) and chrome webdriver must be installed.

```
Developed and tested with following verions.
- OS: Ubuntu 18.04
- Python 3.6.9
- ChromeDriver 83.0.4103.39
```

### Installing

Download ChromeDriver (the version of ChromeDriver must be matched with Chrome browser version on your machine).

```
Chromedriver (webdriver)
https://chromedriver.chromium.org/downloads

How to know Chrome browser version
chrome://settings/help
```

Install selenium module to python

```
pip install selenium
or
pip3 install selenium

on cmd (Windows)
py -m pip install selenium
```

### Config
Edit config.json as below:

```
{
    "azure_vm_automation_config" : [
        {
            "webdriver_path" : "PATH of chromedriver",
            "azure_portal_url": "https://portal.azure.com/",
            "account": "Log-in account id",
            "password": "Log-in password",
            "directory" : [
                { 
                    "directory_name" : "name of directory (ex. Default Directory). Leave it blank if there is only one directory and nothing to choose",
                    "domain_name" : "name of domain (ex. example.onmicrosoft.com). Leave it blank if there is only one directory and nothing to choose",
                    "is_classic_vm" : true/false,
                    "resource" : [
                        {
                            "name" : "Name of virtual machine."
                        },
                        {
                            "name" : "Add more object and input name of vm if there is more than one vm to start"
                        }
                    ]
                }
            ]

        }
    ]
}

```
### Run

```
python azure_vm_automation.py
or
python3 azure_vm_automation.py

on cmd (windows)
py azure_vm_automation.py
```
