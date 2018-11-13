import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
from time import sleep
import string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select


class EbayWatchCounter():

	# define the number of watch counts and url to watch and initialize the main function
	def __init__(self, count, url):
		self.count = count
		self.url = url
		self.loop_main()


	def generate_credentials(self): # scrape fake credentials
		r = requests.get('https://www.fakeaddressgenerator.com/World/us_address_generator')
		soup = BeautifulSoup(r.content, 'html.parser')
		name = soup.find_all('strong')[0].get_text().split()
		chars_start, chars_end = string.ascii_letters, string.digits + '!@#$%^&*()?{}'
		s = HTMLSession()
		r2 = s.get('https://temp-mail.org/')
		email_id = r2.html.find('#mail', first=True)
		self.first_name = name[0]
		self.last_name = name[-1]
		self.phone = str(soup.find_all('strong')[12])[51:63]
		self.address = list(soup.find_all('strong'))[6].input['value']
		self.password = ''.join(random.choice(chars_end) for i in range(5)) + ''.join(random.choice(chars_start) for i in range(5))
		self.email = str(email_id).split()[10][7:-1]

	def login(self): # login to ebay 
		self.driver.get('https://reg.ebay.com/reg/PartialReg')
		self.driver.find_element_by_id("firstname").send_keys(self.first_name)
		print('filling in first name...')
		self.driver.find_element_by_id("lastname").send_keys(self.last_name)
		print('filling in last name...')
		self.driver.find_element_by_id("email").send_keys(self.email)
		print('filling in email...')
		self.driver.find_element_by_id("PASSWORD").send_keys(self.password)
		print('filling in password...')
		sleep(4)
		self.driver.find_element_by_id("ppaFormSbtBtn").click()
		print('signing up')
		sleep(1)
		try:
			assert 'https://www.ebay.com' in self.driver.current_url
			print('Account Created!')
		except AssertionError:
			print('AssertionError in login')
			self.driver.close()

	def watch(self): # watch ebay item
		self.driver.get(self.url)
		try:
			assert self.url in self.driver.current_url
		except AssertionError:
			sleep(5)
			print('waiting for page to load')
		
		try:
			self.style_button = self.driver.find_element_by_id('msku-sel-1')
			for self.option in self.style_button.find_elements_by_tag_name('option'):
				if self.option.get_attribute('id') == 'msku-opt-0':
					self.option.click()
					break
		except NoSuchElementException:
			print('no product styling element found')
		finally:
			self.watch_button = self.driver.find_element_by_class_name('vi-atw-txt')
			self.watch_button.click()
			sleep(1)
			if self.watch_button.text != 'Watching':
				print('watch_button not clicked')

	def verify_account(self): # verify that the account is verified and that the item is being watched
		self.driver.get('https://www.ebay.com/')
		sleep(3)
		self.driver.get('https://www.ebay.com/myb/WatchList')
		if 'https://www.ebay.com/myb/WatchList' in self.driver.current_url:
			print('No need to verify the account!')
			return
		else:
			try:
				assert 'https://reg.ebay.com/reg/Upgrade?ru=https%3A%2F%2Fwww.ebay.com%2Fmyb%2FWatchList' in self.driver.current_url
			except AssertionError:
				print('did not need to verify account')
			sleep(1)
			try:
				self.select_el = Select(self.driver.find_element_by_id('countryId'))
				self.options = self.select_el.options
				for self.index in range(0, len(self.options) - 1):
					self.select_el.select_by_index(0).click()
			except:
				pass
			sleep(3)
			self.driver.find_element_by_id('addressSugg').send_keys(self.address)
			sleep(5)
			self.sugbox_dropdown = self.driver.find_element_by_id('addressSugg_listbox')
			for self.li in self.sugbox_dropdown.find_elements_by_tag_name('li'):
					self.li.click()
					break
			sleep(5)
			self.sugbox_dropdown = self.driver.find_element_by_id('addressSugg_listbox')
			if self.driver.find_element_by_id('addressSugg_listbox').is_displayed():
				for self.li in self.sugbox_dropdown.find_elements_by_tag_name('li'):
					self.li.click()
					break
		
			sleep(1)
			self.driver.find_element_by_id('phoneFlagComp1').send_keys(self.phone)
			sleep(1)
			self.driver.find_element_by_id('sbtBtn').click()

	def loop_main(self): # loop through the functions
		while self.count > 0 :

			self.driver = webdriver.Chrome()
			self.generate_credentials()
			self.login()
			self.watch()
			self.verify_account()
			sleep(2)
			self.driver.close()
			self.count -= 1

count = int(input('enter the amount of watches you would like to recieve: '))
url = str(input('enter the url for the ebay item: '))
start = EbayWatchCounter(count, url)