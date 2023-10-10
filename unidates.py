from datetime import date, timedelta, datetime
from dateutil import parser
class UniDate:
    def __init__(self):        
        self.__current_date = datetime.now()
        self.__weekdays = {
             1: "понедельник",
             2: "вторник",
             3: "среда",
             4: "четверг",
             5: "пятница",
             6: "суббота",
             7: "воскресенье"
        }

        self.__months = {
             1: "Январь",
             2: "Февраль",
             3: "Март",
             4: "Апрель",
             5: "Май",
             6: "Июнь",
             7: "Июль",
             8: "Август",
             9: "Сентябрь",
             10: "Октябрь",
             11: "Ноябрь",
             12: "Декабрь",
        }

    def getMaxDaysCurrentMonth(self):
        self.__month = self.__current_date.month
        self.__year = self.__current_date.year
        
        if self.__month + 1 > 12:
            self.__month = 12

        days_between_months = (date(self.__year, self.__month + 1, 1) - date(self.__year, self.__month, 1)).days
        d1 = date(self.__year, self.__month, 1)
        d2 = date(self.__year, self.__month, days_between_months)
        delta = d2 - d1

        max_days_count = 0

        for i in range(delta.days + 1):
            d = (d1 + timedelta(days=i)).strftime("%d")
            max_days_count = int(d)

        return max_days_count
    
    def getDateByDay(self, day):
        self.__new_date = (date(self.__current_date.year, self.__current_date.month, day)).strftime("%d.%m.%Y")
        return self.__new_date
    
    def getCurrentDay(self, day):
        return day

    def getMonthNameByNum(self, month_number):
        return dict.get(self.__months, month_number)

    def getWeekdayNameByNum(self, day):
        return dict.get(self.__weekdays, day)

    def ConvertStrToDate(self, dateStr):
        string = parser.parse(dateStr)
        string = str(string.year) + "-" + str(string.month) + "-" + str(string.day) + " " + str(string.hour) + ":" + str(string.minute) + ":" + str(string.second)
        converterDate = parser.parse(string)

        return converterDate
