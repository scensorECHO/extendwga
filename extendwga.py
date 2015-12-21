# This application extends the WGA account for the given semicolon delimited credentials

# requirements:
# selenium version: 2.45.0
# python version: 2.7.9
# phantomjs version: 2.0.0

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import deque
import threading

class AccountManager():
	def __init__(self):
		self.login = []
		self.emails= []
		self.log = deque([])
		self.IWT=5 # IMPLICIT WAIT TIME
		self.LWT=15
		self.browser = webdriver.Firefox()
		#self.browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
		self.browser.set_window_size(1920,1080)
		# self.browser = webdriver.PhantomJS()
		self.browser.implicitly_wait(self.IWT)
		# self.url = "https://visitorportal.benteler.net:8443/sponsorportal/"
		self.url = "https://visitorportal.benteler.net:8443/sponsorportal/PortalSetup.action?portal=ba7b1560-7c73-11e5-88ac-005056997abd"
		self.manage = "https://visitorportal.benteler.net:8443/sponsorportal/LoginSubmit.action?from=LOGIN#manageAccountsList"
		self.create = "https://visitorportal.benteler.net:8443/sponsorportal/LoginSubmit.action?from=LOGIN#/sponsorportal/LoginSubmit.action?from=LOGIN"

	def loadCredentials(self):
		# '/root/dl/xwga/credentials'
		with open('credentials','r') as c:
			self.login = c.read().strip().split('\n')
			self.log.append('Credentials read')

	def loadEmails(self):	
		# '/root/dl/xwga/emails'
		with open('emails','r') as e:
			self.emails = e.read().strip().split('\n')
			self.log.append('Emails opened')

	def showLog(self):
		for line in self.log:
			print(line)

	def logQueueListener(self):
		while(self.active):
			if len(self.log)>0:
				print(self.log.popleft())

	def start_log(self):
		self.active = 1
		t = threading.Thread(target=self.logQueueListener)
		t.start()

	def waitForPageById(self, element, seconds=15):
		try:
			element = WebDriverWait(self.browser, seconds).until(
				EC.presence_of_element_located((By.ID, element))
			)
			return 1
		except:
			return 0

	def waitForPageByXpath(self, xpath, seconds=15):
		try:
			self.browser.implicitly_wait(seconds)
			self.browser.find_element_by_xpath(xpath)
		except:
			raise
		finally:
			self.browser.implicitly_wait(self.IWT)

	def waitForPageByPartialLinkText(self, ptext, seconds=15):
		try:
			self.browser.implicitly_wait(seconds)
			self.browser.find_element_by_partial_link_text(ptext)
		except:
			raise
		finally:
			self.browser.implicitly_wait(self.IWT)

	def loadManagementPortal(self):

		self.browser.get(self.url)	
		self.log.append('Browser opened to WGA management portal')

		# locate login and password forms
		loginform = self.browser.find_element_by_id('user.username')
		passwordform = self.browser.find_element_by_id('user.password')

		# type in user credentials
		loginform.send_keys(self.login[0])
		passwordform.send_keys(self.login[1])

		# log in using given credential
		loginbutton = self.browser.find_element_by_id('ui_login_signon_button')
		loginbutton.click() 

		self.waitForPageById('availableGuestTypes')

		return 1;

	def loadManageAccountsPage(self):
		time.sleep(5)
		acc_attempts=0
		while(acc_attempts<5):
			try:
				manageAccounts = self.browser.find_element_by_partial_link_text('Manage Account')
				manageAccounts.click()
				if(self.waitForPageByXpath('//table[@class="search-container"]/tbody/tr/td/div/input',20)):
					return 1
			except:
				acc_attempts+=1
			finally:
				if(acc_attempts==2):
					self.browser.refresh()
					self.log.append('3rd attempt, refreshing page')
					acc_attempts+=1
				elif(acc_attempts==4):
					self.log.append('5 attempts to load manage account page failed -- exiting')
					self.browser.save_screenshot('manage_account_error.png')
					return 0
				else:
					acc_attempts+=1
		
	def queryUser(self, contactInfo):
		usernamefield = self.browser.find_element_by_xpath('//table[@class="search-container"]/tbody/tr/td/div/input')
		#self.browser.save_screenshot("username_field.png")
		usernamefield.clear()

		usernamefield.send_keys(contactInfo[0])
		usernamefield.send_keys(Keys.RETURN)
		return 1;

	def addUser(self, contactInfo):
		# Make sure the Create Accounts tab is selected
		continue_link = self.browser.find_element_by_partial_link_text('Create Accounts')
		continue_link.click()

		#if not self.waitForPageById('9d981c21-7c8e-11e5-be52-005056997abd8765b0e0-7c73-11e5-88ac-005056997abd'):
		#	return 0; 
		time.sleep(2)

		# retrieve form elements
		guesttype = self.browser.find_element_by_xpath('//div[@id="availableGuestTypes"]/div/div/div/select')
		forenameForm = self.browser.find_element_by_name("firstName")
		surnameForm = self.browser.find_element_by_name("lastName")
		emailForm = self.browser.find_element_by_name("emailAddress")
		phoneForm = self.browser.find_element_by_name("phoneNumber")
		companyForm = self.browser.find_element_by_name("ui_optionaldata1_text_label")
		contactForm = self.browser.find_element_by_name("ui_optionaldata3_text_label")
		locationForm = self.browser.find_element_by_name("ui_optionaldata4_text_label")
		validityForm = self.browser.find_element_by_name("days")
		locationList = self.browser.find_element_by_name("location")

		ticketForm = self.browser.find_element_by_name("ui_optionaldata5_text_label")
		
		# set to 5 days
		guesttype.click()
		time.sleep(0.2)
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
		ticketForm.send_keys(" ")
		# set location dropdown
		locationList.click()
		time.sleep(1)
		# page refresh changes elements
		locationList = self.browser.find_element_by_name("location")
		locationList.click()
		time.sleep(0.1)
		locationList.send_keys("US/M")
		locationList.send_keys(Keys.RETURN)

		# submit form
		time.sleep(0.5)

		return createAccount()


	def createAccount(self, attempts=0):	
		try:
			self.browser.find_element_by_id('createButton').click()
			#notify user
			time.sleep(0.2)
			self.browser.find_element_by_partial_link_text('Notify').click()
			#email user
			time.sleep(0.2)
			emailBox = self.browser.find_element_by_id('createKnownAccountNotifyFormEmail')
			if not emailBox.get_attribute("checked"):
				emailBox.click()
			#confirm email
			time.sleep(0.2)
			self.browser.find_element_by_partial_link_text('Ok').click()
		except:
			if(attempts>3):
				self.log.append("An error extending the account has occurred")
				return 0
			else:
				self.browser.find_element_by_partial_link_text("Manage Accounts").click()
				time.sleep(2)
				self.browser.find_element_by_partial_link_text("Create Accounts").click()
				time.sleep(2)
				return createAccount(attempts+1)
		return 1

	def findUserInPage(self, contactInfo):

		try:
			self.log.append('Queried for '+contactInfo[0])
			searchedUser = self.browser.find_element_by_partial_link_text(contactInfo[0])
			#searchedUser = self.browser.find_element_by_xpath('//table[@class="manage-accounts-table"]/tbody/tr/td[@title="'
			#	+contactInfo[0]+'"/a')
			searchedUser.click()
		except:
			return 0
		return 1

	def extendAccount(self):
		# wait for page load
		try:
			self.waitForPageByXpath('//div[@class="ui-body-b summary_field"]/span[@class="summary_field_name"]')
		except Exception as detail:
			self.log.append('User page did not load:\n'+str(detail))
			self.browser.save_screenshot("extend_account_error.png")
			return 0
		# time.sleep(2)
		editButton = self.browser.find_element_by_partial_link_text("Edit")
		editButton.click()


		# set Guest Type
		guesttype = self.browser.find_element_by_xpath('//div[@id="availableGuestTypesEdit"]/div/div/div/select')
		guesttype.click()
		time.sleep(0.2)
		guesttype.send_keys('5')
		# self.browser.find_element_by_xpath('//option[@guest-type="9d981c21-7c8e-11e5-be52-005056997abd"]').click()
		guesttype.send_keys(Keys.RETURN)
		self.browser.find_element_by_xpath('//body').click()

		# select 5 days from dropdown box
		time.sleep(1)
		#durationField = self.browser.find_element_by_name("days")
		#durationField.send_keys('5')

		# confirm selection
		confirmbtn = self.browser.find_element_by_partial_link_text('Submit')
		confirmbtn.click()
		return 1

	def startManager(self):
		self.log.append('###Loading Selenium WebDriver###')
		self.loadCredentials()
		if not self.loadManagementPortal():
			self.active = 0
			self.browser.quit()
		self.log.append('Main portal logged in')
		
		time.sleep(1)

		self.loadEmails()
		for email in self.emails:
			if len(email) > 3 and ';' in email:
				contactInfo = email.split(';')
			self.log.append('Contact info parsed for '+contactInfo[0])
			if not isinstance(contactInfo, list):
				self.log.append('Contact info incorrect')
				continue
			time.sleep(1)
			if not self.loadManageAccountsPage():
				continue	
			if not self.queryUser(contactInfo):
				self.log.append('User '+contactInfo[0]+' not found')
				continue
			self.log.append('User '+contactInfo[0]+' found')
			time.sleep(3)
			if not self.findUserInPage(contactInfo):
				if not self.addUser(contactInfo):
					self.log.append('User addition failed')
			 		continue
			 	self.log.append('User added to system')
				continue
			self.log.append('User found')	
		
			time.sleep(1)
		
			if not self.extendAccount():
				self.log.append('Account extension for '+contactInfo[0]+' failed')
				continue
			self.log.append('Account '+contactInfo[0]+' extended')
		
		# exit browser
		time.sleep(1)
		self.active = 0
		self.browser.quit()

if __name__=="__main__":
	wga = AccountManager()
	wga.start_log()
	wga.startManager()
