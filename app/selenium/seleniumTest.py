from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class LeaseMeSelenium(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://selenium-chrome:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)


    def test_1_create_user(self):
        """ Creates a user with username "test1" and password "test1" """

        driver = self.driver
        driver.get("http://web1:8000/")

        driver.find_element_by_xpath("/html/body/center[1]/div/div/form[2]/input").click()
        self.assertTrue("New User" in driver.page_source)

        element = driver.find_element_by_name("first_name")
        element.send_keys("Arun")
        element = driver.find_element_by_name("last_name")
        element.send_keys("Kanumuru")
        element = driver.find_element_by_name("email")
        element.send_keys("avkanumuru@gmail.com")
        element = driver.find_element_by_name("username")
        element.send_keys("test1")
        element = driver.find_element_by_name("password")
        element.send_keys("test1")


        driver.find_element_by_xpath("/html/body/center/form[@class='post-form']/button[@class='save btn btn-default']").click()

        self.assertTrue("User created successfully" in driver.page_source)


    def test_2_success_login(self):
        """ logs into the user we created in the last test"""

        driver = self.driver
        driver.get("http://web1:8000/")

        driver.find_element_by_xpath("/html/body/center[1]/div/div/form[1]/input").click()

        element = driver.find_element_by_name("username")
        element.send_keys("test1")
        element = driver.find_element_by_name("password")
        element.send_keys("test1")
        driver.find_element_by_xpath("/html/body/center/form[@class='post-form']/button[@class='save btn btn-default']").click()


        self.assertEqual("http://web1:8000/", driver.current_url)
        self.assertTrue("Logged in successfully!" in driver.page_source)

        driver.find_element_by_xpath("/html/body/center[1]/div/div[2]/form[1]/input").click()


    def test_3_failure_login(self):
        """ Tries to log into an account that doesn't exist"""

        driver = self.driver
        driver.get("http://web1:8000/")

        driver.find_element_by_xpath("/html/body/center[1]/div/div/form[1]/input").click()

        element = driver.find_element_by_name("username")
        element.send_keys("test1")
        element = driver.find_element_by_name("password")
        element.send_keys("test2")
        driver.find_element_by_xpath("/html/body/center/form[@class='post-form']/button[@class='save btn btn-default']").click()


        self.assertEqual("http://web1:8000/login/", driver.current_url)
        self.assertTrue("Invalid login credentials" in driver.page_source)


    def test_4_create_listing(self):
        """creates a listing on the website"""

        driver = self.driver
        driver.get("http://web1:8000/login")

        element = driver.find_element_by_name("username")
        element.send_keys("test1")
        element = driver.find_element_by_name("password")
        element.send_keys("test1")
        driver.find_element_by_xpath("/html/body/center/form[@class='post-form']/button[@class='save btn btn-default']").click()

        self.assertEqual("http://web1:8000/", driver.current_url)
        self.assertTrue("Logged in successfully!" in driver.page_source)

        driver.find_element_by_xpath("/html/body/center[1]/div/div[2]/form[2]/input").click()

        self.assertEqual("http://web1:8000/listings/new/?", driver.current_url)

        element = driver.find_element_by_name("address")
        element.send_keys("1819 Jefferson Park Avenue, apt. 304")
        element = driver.find_element_by_name("num_bedrooms")
        element.send_keys("4")
        element = driver.find_element_by_name("num_bathrooms")
        element.send_keys("2")
        element = driver.find_element_by_name("price")
        element.send_keys("450")
        element = driver.find_element_by_name("start_date")
        element.send_keys("May 15th, 2018")
        element = driver.find_element_by_name("end_date")
        element.send_keys("August 15th, 2018")
        element = driver.find_element_by_name("description")
        element.send_keys("Really roomy, greate roommates, balcony with a bus stop right nearby")


        driver.find_element_by_xpath("/html/body/center/div/form[@class='post-form']/button[@class='save btn btn-default']").click()

        self.assertTrue("Listing created succesfully" in driver.page_source)
        self.assertEqual("http://web1:8000/", driver.current_url)

        driver.find_element_by_xpath("/html/body/center[1]/div/div[2]/form[1]/input").click()


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
