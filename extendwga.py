# This application extends the WGA account for the given semicolon delimited credentials

# requirements:
# selenium version: 2.45.0
# python version: 2.7.9
# phantomjs version: 2.0.0

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

##################################################
################ LOG THREAD ######################
##################################################

from collections import deque
import threading


active = 1
log = deque([])

def logStackListener():
	while(active):
		if len(log)>0:
			print(log.popleft())

t = threading.Thread(target=logStackListener)
t.start()

##################################################
############## END LOG THREAD ####################
##################################################

login = []
email = []


log.append('###Loading Selenium WebDriver###')

# url = "https://visitorportal.benteler.net:8443/sponsorportal/"
url = "https://visitorportal.benteler.net:8443/sponsorportal/PortalSetup.action?portal=ba7b1560-7c73-11e5-88ac-005056997abd"
manage = "https://visitorportal.benteler.net:8443/sponsorportal/LoginSubmit.action?from=LOGIN#manageAccountsList"

# browser = webdriver.Firefox()
browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
# browser = webdriver.PhantomJS()

with open('/root/dl/xwga/credentials','r') as c:
	login = c.read().strip().split('\n')
	log.append('Credentials read')

with open('/root/dl/xwga/emails','r') as e:
	emails = e.read().strip().split('\n')
	log.append('Emails opened')

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
	log.append('Browser opened to WGA management portal')

	# locate login and password forms
	loginform = browser.find_element_by_id('user.username')
	passwordform = browser.find_element_by_id('user.password')

	# type in user credentials
	loginform.send_keys(login[0])
	passwordform.send_keys(login[1])

	# log in using given credential
	loginbutton = browser.find_element_by_id('ui_login_signon_button')
	loginbutton.click() 

	return 1;

def queryUser(contactInfo):
	# browser.get(manage)
	manageAccounts = browser.find_element_by_xpath('//a[@href="#manageAccountsList"]')
	manageAccounts.click()
	time.sleep(1)
	# search for user
	# usernamefield = browser.find_elements_by_name('search')
	# for u in usernamefield:
	# 	print(u)
	usernamefield = browser.find_element_by_xpath('//table[@class="search-container"]/tbody/tr/td/div/input')
	usernamefield[2].send_keys(contactInfo[0])
	usernamefield[2].send_keys(Keys.RETURN)
	return 1;

def addUser(contactInfo):
	# Make sure the Create Accounts tab is selected
	continue_link = browser.find_element_by_partial_link_text('Create Accounts')
	continue_link.click()

	if not waitForPageById('9d981c21-7c8e-11e5-be52-005056997abd8765b0e0-7c73-11e5-88ac-005056997abd'):
		return 0; 

	# retrieve form elements
	guesttype = browser.find_element_by_id("availableGuestTypes")
	forenameForm = browser.find_element_by_name("firstName")
	surnameform = browser.find_element_by_name("lastName")
	emailForm = browser.find_element_by_name("emailAddress")
	phoneForm = browser.find_element_by_name("phoneNumber")
	companyForm = browser.find_element_by_name("ui_optionaldata1_text_label")
	contactForm = browser.find_element_by_name("ui_optionaldata3_text_label")
	locationForm = browser.find_element_by_name("ui_optionaldata4_text_label")
	validityForm = browser.find_element_by_name("days")
	locationList = browser.find_element_by_name("location")
	# timeZone = browser.find_element_by_name("")
	
	# set to 5 days
	guesttype.click()
	guesttype.send_keys('5')
	guesttype.send_keys(Keys.RETURN)

	# fill out form
	forenameForm.send_keys(contactInfo[1])
	surnameForm.send_keys(contactInfo[2])
	emailForm.send_keys(contactInfo[0])
	phoneForm.send_keys(contactInfo[3])
	companyForm.send_keys(contactInfo[4])
	contactForm.send_keys(contactInfo[5])
	locationForm.send_keys(contactInfo[6])
	# set location dropdown
	locationList.click()
	locationList.send_keys("US/Michigan")
	locationList.send_keys(Keys.RETURN)
	validityForm.clear()
	validityForm.send_keys('5')
	# timeZone.clear()
	# timeZone.send_keys('GMT')
	# time.sleep(.5)
	# timeZone.send_keys(' -05:00 EST')
	# browser.executeScript("document.getElementsByName('guestUser.timezone').item(0).value ='GMT -05:00 EST');")
	# time.sleep(1)
	# submit form
	browser.find_element_by_id('createButton').click()

	# back to guest accounts page
	if not waitForPageById('viewGuestAccountCancel'):
		browser.get(manage)
	browser.find_element_by_id('viewGuestAccountCancel').click()

	# end account creation function
	return 1;

def findUserInPage(contactInfo):
	# usercheckbox = browser.find_element_by_xpath('//tr[@id="'+contactInfo[0]+'"]/td/input')
	try:
		usercheckbox = browser.find_element_by_xpath('//tr[@class="ui-body-a"]/td/input')
		usercheckbox.click()
	except:
		notFound(contactInfo[0])
		return 0
	return 1

def extendAccount():
	# change account duration to 5 days
	editButton = browser.find_element_by_partial_link_text("Edit")
	editButton.click()

	# wait for page load
	time.sleep(1)

	# select 5 days from dropdown box
	# dropdown = browser.find_element_by_xpath("//select[@id='timeProfileDropdown']/option[3]")
	durationField = browser.find_element_by_name("days")
	durationField.send_keys('5')
	
	guesttype = browser.find_element_by_id("availableGuestTypesEdit")
	guesttype.click()
	guesttype.send_keys('5')
	guesttype.send_keys(Keys.RETURN)

	# confirm selection
	confirmbtn = browser.find_element_by_id('Submit')
	confirmbtn.click()
	return 1;

def notFound(e):
	nfe = 'User '+e+' not found in system'
	log.append(nfe)
	print(nfe)


if not loadManagementPortal():
	active = 0
log.append('Main portal logged in')

time.sleep(3)

for email in emails:

	if len(email) > 1:
		contactInfo = email.split(';')
	log.append('Contact info parsed for '+contactInfo[0])
	if not isinstance(contactInfo, list):
		log.append('Contact info incorrect')
		continue

	time.sleep(2)

	if not queryUser(contactInfo):
		continue
	log.append('Queried for '+contactInfo[0])

	time.sleep(3)

	try:
		findUserInPage(contactInfo)
		log.append('User found')
	except:
	 	if not addUser(contactInfo):
	 		continue
	 	log.append('User added to system')
		continue

	time.sleep(1)

	if not extendAccount():
		continue
	log.append('Account '+contactInfo[0]+' extended')

# exit browser
time.sleep(1)
active = 0
browser.quit()

exit()
