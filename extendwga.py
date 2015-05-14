<<<<<<< HEAD
# This application extends the WGA account for Naveed Choudry


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

login = []
email = []
url = "https://visitorportal.benteler.net:8443/sponsorportal/"
# browser = webdriver.Firefox()
browser = webdriver.PhantomJS('C:\phantomjs-2.0.0-windows\\bin\phantomjs.exe')

with open('credentials','r') as c:
	login = c.read().strip().split('\n')

with open('emails','r') as e:
	emails = e.read().strip().split('\n')

def waitForPageById(element, seconds=15):
	try:
		element = WebDriverWait(browser, seconds).until(
			EC.presence_of_element_located((By.ID, element))
		)
		return 1;
	except:
		return 0;

def loadManagementPortal():

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

	return;

def addUser(contactInfo):
	continue_link = browser.find_element_by_partial_link_text('Create Single Acco')
	continue_link.click()

	if not waitForPageById('guestUserFirstName'):
		return 0; 

	# retrieve form elements
	forenameForm = browser.find_element_by_id('guestUserFirstName')
	surnameForm = browser.find_element_by_id('guestUserLastName')
	emailForm = browser.find_element_by_id('guestUserEmailAddress')
	phoneForm = browser.find_element_by_id('guestUserPhoneNumber')
	companyForm = browser.find_element_by_id('guestUserOptionalData1')
	contactForm = browser.find_element_by_id('guestUserOptionalData3')
	locationForm = browser.find_element_by_id('guestUserOptionalData4')
	validityForm = browser.find_element_by_id('guestUserTimeProfile')
	timeZone = browser.find_element_by_id('guestUserTimezone')
	# timeZone = browser.find_element_by_name('guestUser.timezone')
	
	# fill out form
	forenameForm.send_keys(contactInfo[1])
	surnameForm.send_keys(contactInfo[2])
	emailForm.send_keys(contactInfo[0])
	phoneForm.send_keys(contactInfo[3])
	companyForm.send_keys(contactInfo[4])
	contactForm.send_keys(contactInfo[5])
	locationForm.send_keys(contactInfo[6])
	validityForm.clear()
	validityForm.send_keys('5')
	timeZone.clear()
	timeZone.send_keys('GMT')
	time.sleep(.25)
	timeZone.send_keys(' -05:00 EST')
	# browser.executeScript("document.getElementsByName('guestUser.timezone').item(0).value ='GMT -05:00 EST');")
	time.sleep(1)
	# submit form
	browser.find_element_by_id('addGuestAccountSubmit').click()

	# back to guest accounts page
	if not waitForPageById('viewGuestAccountCancel'):
		browser.get(url)
	browser.find_element_by_id('viewGuestAccountCancel').click()

	# end account creation function
	return 1;

def queryUser(contactInfo):
	# search for user
	usernamefield = browser.find_element_by_id('searchUserNametxt')
	usernamefield.send_keys(contactInfo[0])
	usernamefield.send_keys(Keys.RETURN)
	return;

def findUserInPage(contactInfo):
	usercheckbox = browser.find_element_by_xpath('//tr[@id="'+contactInfo[0]+'"]/td/input')
	usercheckbox.click()
	return;

def extendAccount():
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
	return;


loadManagementPortal()

time.sleep(3)

for email in emails:

	contactInfo = email.split(';')

	time.sleep(2)

	queryUser(contactInfo)

	time.sleep(3)

	try:
		findUserInPage(contactInfo)
	except:
	 	addUser(contactInfo)
		continue

	time.sleep(1)

	extendAccount()	

# exit browser
browser.quit()
=======
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
>>>>>>> 3e9f79aaaf7c4df3629c7299d532976da79a9a2b
