from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


import time
import re


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_driver = 'C:/Users/Bianca/chromedriver.exe'
#^ would have to be changed to user's chromedriver

#--------------------------------------------^ open process in current window
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

a = 0


def code():
	time.sleep(6)
	
	framespot = 'embed-responsive-item'		
	frame = driver.find_element_by_class_name(framespot)
	driver.switch_to.frame(frame)
	# frame to switch to to access html

	input = [None] * 50 
	#empty array
	
	x = 0
	while x < 50:
		word1 = 'skill_'
		word2 = word1 + str(x)
		input[x] = driver.find_element_by_name(word2)
		x = x + 1
	#many inputs, assign them through while loop


	link = driver.find_element_by_xpath('//*[@id="workContent"]/div/table/tbody/tr/td[2]/a')
	#linkedin link
	
	ActionChains(driver)\
		.key_down(Keys.LEFT_CONTROL)\
		.click(link)\
		.key_up(Keys.LEFT_CONTROL)\
		.perform() 
		#click and ctrl to open new tab

	time.sleep(4)
	tab1= driver.window_handles[0]
	tab2= driver.window_handles[1]
	driver.switch_to.window(tab2)
	#handling many tabs

	time.sleep(2)
	src = driver.page_source

	skills = []
	time.sleep(4)
	
	#in linkedin
	try:
		words = '/html/body/div[5]/div[4]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/div/section/div[2]/button'
		showmore = driver.find_element_by_xpath(words)
		showmore.send_keys(Keys.RIGHT)
		showmore.send_keys(Keys.ENTER)
		#open show more tab
	
		time.sleep(4)
		src = driver.page_source
		#take source code to analyze

		skillsr = 'pv-skill-category-entity__name-text t-16 t-black t-bold.*\n.*\n*.*'
		skillsm = re.findall(skillsr,src)
		#pattern im loking for
		wordsp = '([a-z]*[A-Z][a-z]*.*)'
		wordsp2 = '[a-z]* [a-z]*\n'
		wordsr = re.compile(wordsp)

		x = 0

		skillsg = list(filter(wordsr.search,skillsm))
	
		line = [None] * 50
		while x != 99:
			if x < 50:
				temp = re.search(wordsp, skillsm[x])
				if temp == None:
					temp = re.search(wordsp2, skillsm[x])
				line[x] = temp.group()
				print(line[x])
				x = x + 1
				if skillsg[x-1] == skillsg[-1]:
					temp = x
					x = 99

		time.sleep(4)

		driver.close()
	
		print("\n", temp)
		time.sleep(4)

		#back to main window
		driver.switch_to.window(tab1)
		driver.switch_to.frame(frame)

		#fill out form with skills
		x = 0
		while x < temp:
			input[x].send_keys(line[x])
			x = x + 1
		time.sleep(4)
	
	#if theres no skills close tab and click thing
	except NoSuchElementException:
		print("\nNo Skills\n")
		time.sleep(4)
		driver.close()
		driver.switch_to.window(tab1)
		driver.switch_to.frame(frame)

def cp():
	try:
		code()
	except NoSuchElementException:
		quit()

	
try:
	driver.find_element_by_xpath('//*[@id="authportal-main-section"]/div[2]/div/div/form/div/div/div/h1')
	quit()
	
except NoSuchElementException:
	cp()
	
