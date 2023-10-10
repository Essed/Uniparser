from unicontrolsystem import UniSystem
from datetime import date, datetime
from unidates import UniDate
import time 

ud = UniDate()

ucs = UniSystem() 

ucs.setParserStatus(True)

ucs.startParser()

is_updated = False
is_adding = False

while True:

    current_day = datetime.now().day
    current_month = datetime.now().month
    current_hour = datetime.now().hour

    month_name = ud.getMonthNameByNum(current_month)

    next_day = current_day

    last_month_day = ud.getMaxDaysCurrentMonth()

    time.sleep(1)

    if current_day == next_day and is_adding == False:
        ucs.fillDataDB(month_name , current_day, current_day + 7, 30)      
        print("Расписание успешно добавлено!")
        print(f"Текующий месяц {current_month}")
        print(f"Следующее заполнение расписание произойдет в {current_month + 1} месяце")        
        is_adding = True

    elif current_day == last_month_day - 1 and current_hour > 18 and current_hour < 22:
        ucs.fillDataDB(current_month + 1, current_day, current_day, 1)
        print("Расписание на следующую неделю успешно добавлено!")
    
    else:
        
        if current_hour > 18 and current_hour <= 22 and is_updated == False:
            print("Начато обновление расписания!")
            ucs.fillDataDB(current_month, current_day, current_day, 1)
            print("Расписание успешно обновлено!")
            is_updated = True

        elif current_hour > 16 and current_hour < 18:
             is_updated = False
             print("Обновление расписания скоро начнется...")
         

        else:
            print("Еще рано для обновления раписания!")                        
            print(f"Месяц: {current_month} день: {current_day} час: {current_hour}")
