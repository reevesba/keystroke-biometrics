''' Key Logging Bot

Author: Bradley Reeves
Date: 05/21/2021

'''

from time import sleep
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, TypeVar
from random import uniform

KeyLoggerBot = TypeVar("KeyLoggerBot")

class KeyLoggerBot:
    def __init__(self: KeyLoggerBot, field_names: List, sentences: List) -> None:
        ''' Initialize KeyLoggerBot instance
            Parameters
            ----------
            self : KeyLoggerBot instance
            field_names : Input fields
            sentences : Sentences to type

            Returns
            -------
            None
        '''
        self.field_names = field_names
        self.sentences = sentences

    def slow_type(self: KeyLoggerBot, element: WebElement, sentence: str):
        ''' Slow down the bot typing speed
            Parameters
            ----------
            self : KeyLoggerBot instance
            element : HTML input element
            sentence : String to type

            Returns
            -------
            None
        '''
        for char in sentence:
            delay = uniform(0.05, 0.1)
            element.send_keys(char)
            sleep(delay)

    def execute(self: KeyLoggerBot) -> None:
        ''' Solve captchas
            Parameters
            ----------
            self : KeyLoggerBot instance

            Returns
            -------
            None
        '''
        # Setup chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://keystrokebiometrics.xyz")
        sleep(2)

        # Set the isbot field
        isbot_input = driver.find_element_by_name("isbot")
        driver.execute_script("arguments[0].removeAttribute('Style')", isbot_input)
        isbot_input.send_keys('1')

        # Type the sentences
        for i in range(len(self.field_names)):
            sentence_input = driver.find_element_by_name(self.field_names[i])
            self.slow_type(sentence_input, self.sentences[i])
            sleep(1)
        
        sleep(5)
        driver.quit()