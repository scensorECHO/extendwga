# This application extends the WGA account for the given semicolon delimited credentials

# requirements:
# selenium version: 2.45.0
# python version: 2.7.9
# phantomjs version: 2.0.0

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
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
IWT=5 # IMPLICIT WAIT TIME

log.append('###Loading Selenium WebDriver###')

# url = "https://visitorportal.benteler.net:8443/sponsorportal/"
url = "https://visitorportal.benteler.net:8443/sponsorportal/PortalSetup.action?portal=ba7b1560-7c73-11e5-88ac-005056997abd"
manage = "https://visitorportal.benteler.net:8443/sponsorportal/LoginSubmit.action?from=LOGIN#manageAccountsList"

#browser = webdriver.Firefox()
browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
browser.set_window_size(1920,1080)
# browser = webdriver.PhantomJS()
browser.implicitly_wait(IWT)

# '/root/dl/xwga/credentials'
with open('credentials','r') as c:
	login = c.read().strip().split('\n')
	log.append('Credentials read')

# '/root/dl/xwga/emails'
with open('emails','r') as e:
	emails = e.read().strip().split('\n')
	log.append('Emails opened')

def waitForPageById(element, seconds=15):
	try:
		element = WebDriverWait(browser, seconds).until(
			EC.presence_of_element_located((By.ID, element))
		)
		return 1
	except:
		return 0

def waitForPageByXpath(xpath, seconds=15):
	try:
		browser.implicitly_wait(seconds)
		browser.find_element_by_xpath(xpath)
	except:
		raise
	finally:
		browser.implicitly_wait(IWT)

def waitForPageByPartialLinkText(ptext, seconds=15):
	try:
		browser.implicitly_wait(seconds)
		browser.find_element_by_partial_link_text(ptext)
	except:
		raise
	finally:
		browser.implicitly_wait(IWT)

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

	waitForPageById('availableGuestTypes')

	return 1;

def queryUser(contactInfo):
	time.sleep(5)
	acc_attempts=0
	while(acc_attempts<5):
		manageAccounts = browser.find_element_by_partial_link_text('Manage Accounts')
		manageAccounts.click()
		if(waitForPageByXpath('//table[@class="search-container"]/tbody/tr/td/div/input',20)):
			break
		elif(acc_attempts==2):
			browser.refresh()
			log.append('3rd attempt, refreshing page')
			acc_attempts+=1
		elif(acc_attempts==4):
			log.append('5 attempts to load manage account page failed -- exiting')
			browser.save_screenshot('manage_account_error.png')
			return 0
		else:
			acc_attempts+=1
	
	# search for user
	# usernamefield = browser.find_elements_by_name('search')
	# for u in usernamefield:
	# 	print(u)
	
	# testing new username xpath
	usernamefield = browser.find_element_by_xpath('//table[@class="search-container"]/tbody/tr/td/div/input')
	browser.save_screenshot("username_field.png")
	usernamefield.clear()

	# try:
	# 	username_clear= browser.find_element_by_xpath('//table[@class="search-container"]/tbody/tr/td/div/input/a')
	# 	username_clear.click()
	# except:
	# 	log.append("No previous query to clear")

	usernamefield.send_keys(contactInfo[0])
	usernamefield.send_keys(Keys.RETURN)
	return 1;

def addUser(contactInfo):
	# Make sure the Create Accounts tab is selected
	continue_link = browser.find_element_by_partial_link_text('Create Accounts')
	continue_link.click()

	#if not waitForPageById('9d981c21-7c8e-11e5-be52-005056997abd8765b0e0-7c73-11e5-88ac-005056997abd'):
	#	return 0; 
	time.sleep(2)

	# retrieve form elements
	#guesttype = browser.find_element_by_id("availableGuestTypes")
	guesttype = browser.find_element_by_xpath('//div[@id="availableGuestTypes"]/div/div/div/select')
	forenameForm = browser.find_element_by_name("firstName")
	surnameForm = browser.find_element_by_name("lastName")
	emailForm = browser.find_element_by_name("emailAddress")
	phoneForm = browser.find_element_by_name("phoneNumber")
	companyForm = browser.find_element_by_name("ui_optionaldata1_text_label")
	contactForm = browser.find_element_by_name("ui_optionaldata3_text_label")
	locationForm = browser.find_element_by_name("ui_optionaldata4_text_label")
	validityForm = browser.find_element_by_name("days")
	locationList = browser.find_element_by_name("location")
	#locationList = browser.find_element_by_xpath('//span[@id="accessTimeContent"]/form/div/div/div/select')
	ticketForm = browser.find_element_by_name("ui_optionaldata5_text_label")
	
	# set to 5 days
	guesttype.click()
	time.sleep(0.2)
	guesttype.send_keys('5')
	# browser.find_element_by_xpath('//option[@guest-type="9d981c21-7c8e-11e5-be52-005056997abd"]').click()
	guesttype.send_keys(Keys.RETURN)

	# fill out form
	forenameForm.send_keys(contactInfo[1])
	surnameForm.send_keys(contactInfo[2])
	emailForm.send_keys(contactInfo[0])
	phoneForm.send_keys(contactInfo[3])
	companyForm.send_keys(contactInfo[4])
	contactForm.send_keys(contactInfo[5])
	locationForm.send_keys(contactInfo[6])
	ticketForm.send_keys(" ")
	# set location dropdown
	locationList.click()
	time.sleep(1)
	# page refresh changes elements
	locationList = browser.find_element_by_name("location")
	locationList.click()
	time.sleep(0.1)
	locationList.send_keys("US/M")
	locationList.send_keys(Keys.RETURN)

	# submit form
	time.sleep(0.5)

	return createAccount()



def createAccount(attempts=0):	
	try:
		browser.find_element_by_id('createButton').click()
		#notify user
		time.sleep(0.2)
		browser.find_element_by_partial_link_text('Notify').click()
		#email user
		time.sleep(0.2)
		emailBox = browser.find_element_by_id('createKnownAccountNotifyFormEmail')
		if not emailBox.get_attribute("checked"):
			emailBox.click()
		#confirm email
		time.sleep(0.2)
		browser.find_element_by_partial_link_text('Ok').click()
		# end account creation function
	except:
		if(attempts>3):
			log.append("An error extending the account has occurred")
			return 0
		else:
			browser.find_element_by_partial_link_text("Manage Accounts").click()
			time.sleep(2)
			browser.find_element_by_partial_link_text("Create Accounts").click()
			time.sleep(2)
			createAccount(attempts+1)
	return 1

def findUserInPage(contactInfo):
	# usercheckbox = browser.find_element_by_xpath('//tr[@id="'+contactInfo[0]+'"]/td/input')
	try:
		searchedUser = browser.find_element_by_partial_link_text(contactInfo[0])
		#searchedUser = browser.find_element_by_xpath('//table[@class="manage-accounts-table"]/tbody/tr/td[@title="'
		#	+contactInfo[0]+'"/a')
		searchedUser.click()
	except:
		log.append('User '+contactInfo[0]+' not found in system')
		return 0
	return 1

def extendAccount():
	# wait for page load
	try:
		waitForPageByXpath('//div[@class="ui-body-b summary_field"]/span[@class="summary_field_name"]')
	except Exception as detail:
		log.append('User page did not load:\n'+str(detail))
		browser.save_screenshot("extend_account_error.png")
		return 0
	# time.sleep(2)
	editButton = browser.find_element_by_partial_link_text("Edit")
	editButton.click()


	# set Guest Type
	guesttype = browser.find_element_by_xpath('//div[@id="availableGuestTypesEdit"]/div/div/div/select')
	guesttype.click()
	time.sleep(0.2)
	guesttype.send_keys('5')
	# browser.find_element_by_xpath('//option[@guest-type="9d981c21-7c8e-11e5-be52-005056997abd"]').click()
	guesttype.send_keys(Keys.RETURN)
	browser.find_element_by_xpath('//body').click()

	# select 5 days from dropdown box
	time.sleep(1)
	#durationField = browser.find_element_by_name("days")
	#durationField.send_keys('5')

	# confirm selection
	confirmbtn = browser.find_element_by_partial_link_text('Submit')
	confirmbtn.click()
	return 1

## Main Application

if not loadManagementPortal():
	active = 0
log.append('Main portal logged in')

time.sleep(1)

for email in emails:

	if len(email) > 1:
		contactInfo = email.split(';')
	log.append('Contact info parsed for '+contactInfo[0])
	if not isinstance(contactInfo, list):
		log.append('Contact info incorrect')
		continue

	time.sleep(1)

	if not queryUser(contactInfo):
		continue
	log.append('Queried for '+contactInfo[0])

	time.sleep(3)

	if not findUserInPage(contactInfo):
		if not addUser(contactInfo):
			log.append('User addition failed')
	 		continue
	 	log.append('User added to system')
		continue
	log.append('User found')	

	time.sleep(1)

	if not extendAccount():
		log.append('Account extension for '+contactInfo[0]+' failed')
		continue
	log.append('Account '+contactInfo[0]+' extended')

# exit browser
time.sleep(1)
active = 0
browser.quit()

exit()
