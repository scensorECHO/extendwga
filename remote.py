# extendwga remote webdriver 

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time

remote = webdriver.Remote(
	command_executor='http://10.7.20.175:4444/wd/hub',
	desired_capabilities={'browserName' : 'firefox',
	'javascriptEnabled': True,
	})



login = []
email = ''

with open('credentials','r') as c:
	login = c.read().strip().split('\n')

with open('email','r') as e:
	email = e.readline()

print(login)
print(email)

# driver = webdriver.Firefox() # trying out chrome
# browser = webdriver.Firefox()

# driver switched to phantomjs for testing

time.sleep(3)

# for printer in printers #for future use with all printers
url = "https://visitorportal.benteler.net:8443/sponsorportal/"
remote.get(url)

# locate login and password forms
loginform = remote.find_element_by_id('loginpage.field.name')
passwordform = remote.find_element_by_id('loginpage.field.password')

# type in user credentials
loginform.send_keys(login[0])
passwordform.send_keys(login[1])

# log in using given credential
loginbutton = remote.find_element_by_id('loginpage.button.login')
loginbutton.click() 

# wait for page load
time.sleep(3)

# search for user
usernamefield = remote.find_element_by_id('searchUserNametxt')
usernamefield.send_keys(email)
usernamefield.send_keys(Keys.RETURN)

# wait for page load
time.sleep(3)

usercheckbox = remote.find_element_by_xpath('//tr[@id="'+email+'"]/td/input')
usercheckbox.click()

# wait for page load
time.sleep(1)

# change account duration to 5 days
durationbutton = remote.find_element_by_id('changeAccountDuration')
durationbutton.click()

# wait for page load
time.sleep(1)

# select 5 days from dropdown box
dropdown = remote.find_element_by_xpath("//select[@id='timeProfileDropdown']/option[3]")
dropdown.click()

# confirm selection
confirmbtn = remote.find_element_by_id('OK')
confirmbtn.click()

# exit browser
remote.close()