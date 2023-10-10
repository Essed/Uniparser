from datetime import date, datetime

from numpy import append, less, nan
from unipars import UniParser
from unidates import UniDate
from db import MODULE_RASP_DB

class UniSystem:    
    def __init__(self):        
        self.__isEnabledParser = False
        self.__ud = UniDate()
        self.__up = UniParser(None)       
        self.__db = MODULE_RASP_DB("dbtimetable.db")

    def setParserStatus(self, isActive: bool):
        self.__isEnabledParser = isActive
    
    def getParserStatus(self):        
        return self.__isEnabledParser

    def startParser(self):
        if self.__isEnabledParser == True:            
            print("Запуск парсера... ")     
            
        else:
            raise ValueError('Необходимо активировать парсер!')
    
    def stopParser(self):
        self.__up.quitBrowser()

    def getMaxCountGroup(self):
        return self.__up.getGroupsCount()
      
    def getMaxDaysCount(self):
        count = self.__ud.getMaxDaysCurrentMonth()
        return count
     
    def fillDataDB(self, month_name, startDay, endDay, groupcount):
        self.__startDay = startDay
        
        allgroups = self.__up.getGroupsCount()
        grabcount = allgroups - (allgroups - groupcount)

        for group in range(0, grabcount):
            
            self.__up.resetDOM()
                       
            current_group = self.__up.getGroupNameByIndex(group)

            groups = self.__up.getAllOptions()

            self.__up.findGroup(current_group)
                
            if(len(current_group) > 2): 
                
                current_group = groups[group].text
                
                print(f"Группа: {current_group}") 

                if not (self.__db.group_exists(current_group)):
                    self.__db.add_group(current_group)
                    print(f"Группа {current_group} успешно добавлена!")


                while startDay <= endDay:                                      
                    result = self.__up.getTimetableByDate(startDay, month_name)                         
                    
                    if(len(result) > 0):

                        classroom = self.__up.getClassroom()
                        teachers = self.__up.getTeacher() 
                        subjects = self.__up.getSubjectName()
                        lesson_types = self.__up.getLessonType()
                        lesson_numbers = self.__up.getLessonNumber()         

                        
                        previous_room = ""

                        for room in classroom:
                            if room != previous_room:
                                print(f"Аудитория: {room}")
                                print("ROOM: ", room)
                                if not(self.__db.auditory_exists(room)):
                                    self.__db.add_auditory(room)                                
                                    print(f"Аудитория {room} успешно добавлена!")

                                previous_room = room

                        previous_teacher = "" 

                        for teacher in teachers:                            
                            if teacher != previous_teacher:
                                    if type(teacher) != float:                                                             
                                        teacher_info = teacher.split()              
                                        print(f"TEACHER INFO: {teacher_info}")
                                        if len(teacher_info) < 4:                      
                                            surname, name, lastname = teacher_info
                                            print(f"ФИО: {surname} {name} {lastname}")                           

                                            if not(self.__db.teacher_existsFromName(te_surname=surname, te_name=name, te_middleName=lastname)):
                                                self.__db.add_teacher(te_surname=surname, te_name=name, te_middleName=lastname)
                                                print(f"Преподаватель {surname} {name} {lastname} успешно добавлен!")

                                                previous_teacher = teacher                                
                                    
                        previous_subject = ""

                        for subject in subjects:
                            if subject != previous_subject:
                                print(f"Предмет: {subject}")

                                if not(self.__db.subject_exists(subject)):
                                    self.__db.add_subject(subject)
                                    print(f"Предмет {subject} успешно добавлен!")

                                previous_subject = subject

                        previous_lesson_type = ""

                        for lesson_type in lesson_types:
                            if lesson_type != previous_lesson_type:
                                print(f"Тип занятия: {lesson_type}")

                                if not(self.__db.lessonType_exists(lesson_type)):
                                    self.__db.add_lessonType(lesson_type)
                                    print(f"Тип занятия {lesson_type} успешно добавлен!")

                                previous_lesson_type = lesson_type

                        previous_number = ""

                        for number in lesson_numbers:
                            if number != previous_number:
                                print(f"Номер пары: {number}")
                                previous_number = number                    

                        
                        weekdaynum= self.__up.getWeekdayByNum(startDay)
                        weekday = self.__ud.getWeekdayNameByNum(weekdaynum + 1)                    

                        lesson_date = date(datetime.now().year, datetime.now().month, startDay)
                        
                        if self.__db.timetableGroupDate_exist(current_group, lesson_date):

                            self.__db.delete_timetable(current_group, lesson_date)

                        cols = self.__up.getMaxColumns() - 1

                        for row in result[2:, :cols]:                                                   
                            row_lesson_number = row[1]
                            row_lesson_type = row[3]
                            row_subject = row[4]
                            row_classroom = row[0]

                            if(row[2] != None):
                                row_teacher = row[2]   
                            else: 
                                row_teacher = "Нет преподавателя"
                           
                            self.__db.add_timetable(
                            current_group, weekday, row_lesson_number, 
                            row_classroom, row_subject, row_lesson_type, 
                            row_teacher, lesson_date)
                                

                        print(f"Текущая дата: {self.__ud.getDateByDay(startDay)}")
                        print(f"День недели: {weekday} \n")

                    startDay+=1 

                startDay = self.__startDay          

    def getParser(self):
        return self.__up
