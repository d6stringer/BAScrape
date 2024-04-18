'''
Daniel Woodson
2024.04.11
'''

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import shutil
import datetime
from dotenv import dotenv_values


secrets = dotenv_values(".env")
# where the files download to
origin_path = secrets["ORIGIN_PATH"]
# list with original MUA-1 file name and new file name
mua1_csv_name = ["MAU-1 - Temp & RHCSV", "MAU-1 - T&Rh"]
# where to save new files
destination_path = secrets["DESTINATION_PATH"]
# list with original MUA-2 file name and new file name
mua2_csv_name = ["FS MAU 2 - T & RhCSV" , "MAU-2 - T&Rh"]

 
def load_bas():
    '''
    Loads the bas and logs in
    '''
    driver.get(secrets["BAS_URL"])
    #These may need to have some waits added but they seem to work for now
    un = driver.find_element(By.NAME, "name")
    un.send_keys(secrets["USER_NAME"])
    pw = driver.find_element(By.NAME, "pass")
    pw.send_keys(secrets["PASSWORD"])
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "Submit"))).click()
    return

def getMAU1():
    '''
    Goes to the Temp and Rh trend chart for the MUA1 and downloads the CSV of the week's data
    '''
    # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"actionContent")))
    # Click Mau-1 link
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "MAU-1"))).click()
    driver.switch_to.parent_frame()
    # Click on trends down arrow button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/span[2]/div/div[1]/table/tbody/tr[1]/td[3]/span[2]/span[1]/span[4]/img[3]'))).click()
    # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"actioncategories")))
    # Click on Temp & Rh link
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "17"))).click()
    driver.switch_to.parent_frame()
    # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"actionContent")))
    # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div/div/table/tbody/tr[2]/td/div/iframe")))
    # Move mouse over chart to make buttons visible
    actions.move_to_element(driver.find_element(By.XPATH, "//*[@id='title']")).perform()
    # Click download button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="downloadButton"]'))).click()
    # Click CSV download link
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/span[1]/ul[2]/li[5]/span'))).click()
    # time.sleep(10)
    return
    
def getMAU2():
    '''
    Goes to the Temp and Rh trend chart for the MUA2 and downloads the CSV of the week's data
    '''
    # reopen BAS homepage
    driver.get('http://10.21.112.95/index.jsp')
    # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"actionContent")))
    # Click on MAU-2 link
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "MAU-2"))).click()
    driver.switch_to.parent_frame()
    # Click on trends down arrow button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/span[2]/div/div[1]/table/tbody/tr[1]/td[3]/span[2]/span[1]/span[4]/img[3]'))).click()
    # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"actioncategories")))
    # Click on Temp & Rh button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="4"]'))).click()
    driver.switch_to.parent_frame()
     # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"actionContent")))
    # Switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div/div/table/tbody/tr[2]/td/div/iframe")))
    # Move mouse over chart to make buttons visible
    actions.move_to_element(driver.find_element(By.XPATH, "//*[@id='title']")).perform()
     # Click download button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="downloadButton"]'))).click()
    # Click CSV download link
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/span[1]/ul[2]/li[5]/span'))).click()
    return

def move_CSV(file):
    '''
    Moves and renames the downloaded files.
    The argument 'file' is a list where the 0 position is the "old" file name and the 1 position is the "new"
    '''
    zip = ".zip"
    shutil.move((origin_path+file[0]+zip), (destination_path+file[1]+dates()+zip))
    return

def dates():
    '''
    Format some strings to append the start and stop dates onto the file names
    '''
    x = datetime.datetime.now()
    end = x.strftime("%Y.%m.%d")
    y = x - datetime.timedelta(days=7)
    start = y.strftime("%Y.%m.%d")
    date_string =  " " + start + " to "+ end
    return date_string

if __name__ == "__main__":
    # Create web driver
    driver = webdriver.Firefox()
    profile = driver.FirefoxProfile()
    profile.set_preference('dom.block_download_insecure', 'false')
    # profile.DEFAULT_PREFERENCES['frozen']["dom.block_download_insecure"] = True
    # Create actions driver
    actions = ActionChains(driver)
    load_bas()
    getMAU1()
    move_CSV(mua1_csv_name)
    # Create New tab and switch to it
    driver.switch_to.new_window('tab')
    getMAU2()
    move_CSV(mua2_csv_name)
    # close all the windows
    driver.quit()
    

