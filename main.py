from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
from selenium import webdriver
import time

def wait_for_jquery_to_finish(driver):
    WebDriverWait(driver, 10).until(lambda _: driver.execute_script("return window.jQuery.active") == 0)

def typer(desiredWPM):
    try:
        if desiredWPM == "":
            desiredWPM = 10**26
        desiredWPM = int(desiredWPM)
    except:
        print("Must be a number dumbass what the fuck do you expect?")
    #TODO
    # make program go brr if desiredWPM is empty

    # set options
    options = Options()
    options.binary_location = "/usr/bin/firefox"
    options.headless = False

    # firefox driver
    driver = webdriver.Firefox(options=options, executable_path="/home/janseuwu/Documents/geckodriver")
    driver.implicitly_wait(10)
    driver.get("https://monkeytype.com")
    
    # cookies
    rejectButton = driver.find_element(By.XPATH, "/html/body/div[7]/div[4]/div[2]/div[2]/div[2]/div[2]")
    rejectButton.click()

    # change to quote mode
    quoteButton = driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/div[2]/div[1]/div/div[3]/div[3]")
    quoteButton.click()
    time.sleep(1)
    # change to smol mode 
    smol = driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/div[2]/div[1]/div/div[7]/div[2]")
    smol.click()
    wait_for_jquery_to_finish(driver) 

    # accept the dogshit popping up for no reason
    try:
        driver.find_element(By.TAG_NAME, "body").click()
    except:
        pass
    while True:
        try:
            fuckingShit = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]")
            fuckingShit.click()
            break
        except:
            pass

    def kill_me(driver): 
        """ Function for finding the text to typer and typing it out """
        # focus the text part
        focusShit = driver.find_element(By.XPATH, "//*[@id='wordsWrapper']")
        focusShit.click()
        
        parentElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "words")))
        
        childElements = WebDriverWait(parentElement, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "word")))
 
        beep = []
        for word in childElements:
            beep.append(word.text)
        boop = " ".join(beep)
        words = boop.split()
        words_in_sentence = len(words)
        desiredWPS = 60/desiredWPM
        expectedTime = words_in_sentence/desiredWPM

        keyboard = Controller()
        for word in words:
            chars = word+" "
            for char in chars:
                keyboard.press(char)
                keyboard.release(char)
                time.sleep(desiredWPS/len(chars))
        time.sleep(1)
        
        # clicks 'next' button and continues
        try:
            goNext = driver.find_element(By.ID, "nextTestButton")
            goNext.click()
            kill_me(driver)
        except:
            kill_me(driver)

    kill_me(driver)
if __name__ == "__main__":
    typer(input("Desired WPM(leave empty for unlimited): "))
