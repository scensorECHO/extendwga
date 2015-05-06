# This application extends the WGA account for Naveed Choudry


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxProfile
import time

login = []
email = ''

with open('credentials','r') as c:
	login = c.read().strip().split('\n')

with open('email','r') as e:
	email = e.readline()

# driver = webdriver.Firefox() # trying out chrome
# browser = webdriver.Firefox()

# driver switched to phantomjs for testing
browser = webdriver.PhantomJS('C:\phantomjs-2.0.0-windows\\bin\phantomjs.exe')

time.sleep(3)

# for printer in printers #for future use with all printers
url = "https://visitorportal.benteler.net:8443/sponsorportal/"
browser.get(url)

# locate login and password forms
loginform = browser.find_element_by_id('loginpage.field.name')
passwordform = browser.find_element_by_id('loginpage.field.password')

# type in user credentials
loginform.send_keys(login[0])
passwordform.send_keys(login[1])

# log in using given credential
loginbutton = browser.find_element_by_id('loginpage.button.login')
loginbutton.click() 

# wait for page load
time.sleep(3)

# search for user
usernamefield = browser.find_element_by_id('searchUserNametxt')
usernamefield.send_keys(email)
usernamefield.send_keys(Keys.RETURN)

# wait for page load
time.sleep(3)

usercheckbox = browser.find_element_by_xpath('//tr[@id="'+email+'"]/td/input')
usercheckbox.click()

# wait for page load
time.sleep(1)

# change account duration to 5 days
durationbutton = browser.find_element_by_id('changeAccountDuration')
durationbutton.click()

# wait for page load
time.sleep(1)

# select 5 days from dropdown box
dropdown = browser.find_element_by_xpath("//select[@id='timeProfileDropdown']/option[3]")
dropdown.click()

# confirm selection
confirmbtn = browser.find_element_by_id('OK')
confirmbtn.click()

# exit browser
browser.quit()
