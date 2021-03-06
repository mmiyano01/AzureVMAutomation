import os
import json
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Read config file
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
config_file = open(os.path.join(__location__, 'config.json'))
config_data = json.load(config_file)

DRIVER_PATH = config_data['azure_vm_automation_config'][0]['webdriver_path']
AZURE_PORTAL_URL = config_data['azure_vm_automation_config'][0]['azure_portal_url']
AZURE_ACCOUNT = config_data['azure_vm_automation_config'][0]['account']
AZURE_PASSWORD = config_data['azure_vm_automation_config'][0]['password']
TENANTS= config_data['azure_vm_automation_config'][0]['directory']

class AzureVMAutomation:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

    def login(self):
        self.driver.maximize_window()
        # Sign in to Azure Portal
        self.driver.get(AZURE_PORTAL_URL)

        account_input_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, 'loginfmt')))
        account_input_field.send_keys(AZURE_ACCOUNT)
        account_input_field.send_keys(Keys.ENTER)

        account_input_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, 'passwd')))
        account_input_field.send_keys(AZURE_PASSWORD)
        account_input_field.send_keys(Keys.ENTER)

    def portal(self):
        # Azure Portal

        # Run for each Tenant
        for tenant in TENANTS:
            directory_name = tenant["directory_name"]
            domain_name = tenant["domain_name"]

            resources = tenant["resource"]
            vm_type = "Virtual machines (classic)" if tenant["is_classic_vm"] else "Virtual machines"


            if not directory_name == "":
                display_name = directory_name if domain_name == "" else f"{directory_name} ({domain_name})"

                # If currently selected tenant name is same as a name from config file,
                # proceeed to control VM under the tenant.
                # Otherwise, switch tenant first. 
                try:
                    current_tenant_name = self.get_current_tenant_name(display_name)
                
                except (NoSuchElementException, TimeoutException):
                    current_tenant_name = self.switch_tenant(directory_name, domain_name, display_name)
                
                print(f"Current tenant is: {current_tenant_name}")
            

            # Click "Virtual Machine" button and jump to VM control page
            virtual_machines_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[@role='link' and @aria-label='{vm_type}']")))
            virtual_machines_link.click()

            sleep(5)

            self.start_virtual_machines(resources) 

        print("VM successfully started. Have a nice day!")

        sleep(15)
        self.driver.quit()

    def get_current_tenant_name(self, display_name):
        # Wait until tenant name to be displayed
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id='_tsx_e_22']"), str(display_name).upper()))        
        current_tenant_name = self.driver.find_element_by_xpath("//div[@id='_tsx_e_22']").text
        return current_tenant_name

    def switch_tenant(self, directory_name, domain_name, display_name):
        # Switch tenant
        print(f"Current tenant is not found: {display_name}")
        current_tenant_name = self.driver.find_element_by_xpath("//div[@id='_tsx_e_22']").text

        tenant_topbar_menu = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='_tsx_e_18']")))
        tenant_topbar_menu.click()

        switch_directory_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='mectrl_switchdirectory']")))
        switch_directory_link.click()

        search_box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='__azc-textBox-tsx1']")))
        search_box.send_keys(f"{directory_name} {domain_name}")

        sleep(3)

        target_tenant = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='fxc-listView-itemcontent']")))
        target_tenant.click()

        current_tenant_name = str(display_name).upper()

        print(f"Tenant is switched")
        sleep(5)

        return current_tenant_name

    def start_virtual_machines(self, resources):
        for rs in resources:
            resource_name = rs["name"]
            print(resource_name)
            try:
                target_resource_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, resource_name)))
                target_checkbox = target_resource_link.find_element_by_xpath("../../preceding-sibling::div")
                target_checkbox.click()
                sleep(1)
            except NoSuchElementException:
                print(f"Target resource was not found: {resource_name}")
                self.driver.quit()

        try:
            start_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Start' and @role='button']")))
            start_button.click()
            sleep(1)
            yes_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @title='Yes']")))
            yes_button.click()
        except NoSuchElementException:
            print("Failed to start resources.")
            self.driver.quit()


auto = AzureVMAutomation()
auto.login()
auto.portal()