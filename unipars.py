from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
from datetime import date, datetime


class UniParser:
    def __init__(self, time_period):
        self.__chrome_options = Options()
        self.__chrome_options.add_argument('--headless')
        self.__webdriver = webdriver
        self.__driver = self.__webdriver.Chrome(executable_path=r'F:\Программы\ChromeDriver\chromedriver.exe', chrome_options=self.__chrome_options)
        self.__driver.get("https://www.tolgas.ru/services/raspisanie/") 
        self.__groupname = None       
        self.__time_period_near = time_period
        self.__dropdown = Select(self.__driver.find_element(By.XPATH, '//*[@id="vr"]')) 
        self.__menu_options = self.__dropdown.options        
        self.__showbutton = self.__driver.find_element(By.XPATH, '//*[@id="submit_button"]')
        self.__from_date = self.__driver.find_element(By.XPATH, '//*[@id="from"]')
        self.__to_date = self.__driver.find_element(By.XPATH, '//*[@id="to"]')        
        self.__timeTable = []  
    
    def setGroupName(self, groupname):
        self.__groupname = groupname
    
    def getGroupNameByIndex(self, index):        
        return self.__menu_options[index].text

    def getAllOptions(self):
        return self.__menu_options

    def getGroupsCount(self):        
        return len(self.__menu_options) 

    def getAllDates(self):
        return self.__alldates

    def findGroup(self, groupname):

        for option in range(0, len(self.__menu_options)):            
            optionName = self.__menu_options[option].text

            if groupname.lower() == optionName.lower():
                self.__groupname = optionName

        return self.__groupname
    
    def resetDOM(self):
        self.__driver.get("https://www.tolgas.ru/services/raspisanie/")         
        self.__dropdown = Select(self.__driver.find_element(By.XPATH, '//*[@id="vr"]'))
        self.__menu_options = self.__dropdown.options
        self.__showbutton = self.__driver.find_element(By.XPATH, '//*[@id="submit_button"]')
        self.__from_date = self.__driver.find_element(By.XPATH, '//*[@id="from"]')       
        self.__to_date = self.__driver.find_element(By.XPATH, '//*[@id="to"]')  

    def getTimetableByDate(self, day, month_name):
        
        self.resetDOM()
       
        try:            
            if self.__groupname != "":               
                
                self.__dropdown.select_by_visible_text(self.__groupname)

                self.__from_date.click()                  
                
                self.__month_selector_from = Select(self.__driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/div/div/select[1]')) 

                self.__month_selector_from.select_by_visible_text(month_name)

                self.__driver.find_element(By.XPATH, f'//a[text()="{day}"]').click()     

                self.__to_date.click()    

                self.__month_selector_to = Select(self.__driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/div/div/select[1]')) 

                self.__month_selector_to.select_by_visible_text(month_name)

                self.__driver.find_element(By.XPATH, f'//a[text()="{day}"]').click()
               
                self.__showbutton.click()

                self.__html = self.__driver.page_source                

                self.__dataframe = pd.read_html(self.__html)
        
                self.__ScheduleTable = self.__dataframe[1].to_numpy()

                self.__sizeTable = self.__ScheduleTable.shape

                self.__maxRows, self.__maxColumns = self.__sizeTable     

                if self.__ScheduleTable[0][0] != "По данному запросу ничего не найдено!":
                    for i in self.__ScheduleTable[:1, :self.__maxColumns - 1]:
                        for j in i:   
                            pass
                        print(i)                    

                    for i in self.__ScheduleTable[1:self.__maxRows, :self.__maxColumns - 1]:
                        for j in i:
                            print("", j, end=' ')                                                          
                        print()
                else:
                    print(f"У группы {self.__groupname} на {day} число нет пар")

                    self.__ScheduleTable = []

                    return self.__ScheduleTable
      
            self.__timeTable = self.__ScheduleTable
        except:
            pass
        
        return self.__timeTable

    def getTimetableNear(self):
        try:
            if self.__groupname != "":        
                self.__dropdown.select_by_visible_text(self.__groupname)
                self.__driver.find_element_by_xpath(f'//*[@id="{self.__time_period_near}"]').click()

                self.__html = self.__driver.page_source                

                self.__dataframe = pd.read_html(self.__html)
        
                self.__ScheduleTable = self.__dataframe[1].to_numpy()

                self.__sizeTable = self.__ScheduleTable.shape

                self.__maxRows, self.__maxColumns = self.__sizeTable     

                if self.__ScheduleTable[0][0] != "По данному запросу ничего не найдено!":
                    for i in self.__ScheduleTable[:1, :self.__maxColumns - 1]:
                        for j in i:   
                            pass
                        print(i)                    

                    for i in self.__ScheduleTable[2:self.__maxRows, :self.__maxColumns - 1]:
                        for j in i:
                            print("", j, end=' ')                                                          
                        print() 
                    
                else:   
                    return (f"У группы {self.__groupname} на сегодня нет расписания... ")
        except:
            pass
       
        return self.__ScheduleTable

    def getHeader(self):
        self.__headerTable = []

        for i in self.__ScheduleTable[0]:
            self.__headerTable.append(i)
       
        return self.__headerTable

    def getDate(self):        
        try:
            if len(self.__timeTable) > 0:
                return self.__timeTable[1, 0]
        except:
            pass

    def getWeekdayByNum(self, day_num):
        self.__month = datetime.now().month
        self.__year = datetime.now().year
        
        self.__weekday_date = date(self.__year, self.__month, day_num)

        return int(self.__weekday_date.weekday())

    def getTeacher(self):
        if len(self.__timeTable) > 0:
            timetable = self.__timeTable[2:self.__maxRows, 2]
            return timetable
        else:
            self.__driver.quit()
            raise ValueError
   
    def getClassroom(self):
        if len(self.__timeTable) > 0:
            return self.__timeTable[2:self.__maxRows, 0]
        else:
            print(self.__timeTable)
            self.__driver.quit()
            raise ValueError

    def getLessonType(self):
        if len(self.__timeTable) > 0:
            return self.__timeTable[2:self.__maxRows, 3]
        else:
            self.__driver.quit()
            raise ValueError

    def getSubjectName(self):
        if len(self.__timeTable) > 0:
            return self.__timeTable[2:self.__maxRows, 4]
        else:
            self.__driver.quit()
            raise ValueError

    def getLessonNumber(self):
         if len(self.__timeTable) > 0:
            return self.__timeTable[2:self.__maxRows, 1]
         else:
            self.__driver.quit()
            raise ValueError

    def getGroupName(self):
        return self.__groupname

    def getMaxRows(self):
        return self.__maxRows
    
    def getMaxColumns(self):
        return self.__maxColumns

    def quitBrowser(self):
        self.__driver.quit()
