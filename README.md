# AzureVMAutomation

Web automation program to be able to control virtul machine(s) on Azure Portal. 

## Getting Started

This python program will automatically start virtul machine(s) on Azure Portal with using Selenium. 
So far, it only have function to start the vm but eventually I will add more functions (such as stop vm).

### Prerequisites

To run this program, Python with selenium module and chrome webdriver must be installed.

```
Developed and tested with following verions.
- Ubuntu 18.04
- Python 3.6.9
- ChromeDriver 83.0.4103.39
```

### Installing

Download ChromeDriver (the version must be matched with Chrome browser on your machine).

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
```

### Config

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
                    "name" : "name of directory (ex. Default Directory). Leave it blank if there is no directory to choose",
                    "is_classic_vm" : true/false,
                    "resource" : [
                        {
                            "name" : "Name of virtual machine."
                        },
                        {
                            "name" : "Add more object if there is more than one vm to start"
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
```
