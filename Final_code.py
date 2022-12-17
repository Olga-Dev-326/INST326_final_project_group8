# Team 8: Olga, Molondo, Viet, Tanna 
# INST326
# Final Project
import pandas as pd
from collections import defaultdict
import xml.etree.ElementTree as ET
import numpy


#reprequisite is a list of Course that need to be taken before taking the current class
class Course(object):
    def __init__(self, code, credit, description):
        self.code = code
        self.credit = credit
        self.description = description
        self.reprequisite = numpy.empty((10, 0)).tolist()
   
    def isSatisfy(self, completedClasses):
        for i in range (len(self.reprequisite) -1, -1, -1):
            for j in range(len(self.reprequisite[i])-1, -1, -1):
                if self.reprequisite[i][j] in completedClasses:
                    del self.reprequisite[i]
                    break
        if len(self.reprequisite):
            print("Not complete one or more reprequisite courses", self.reprequisite)
            return False
        else:
            return True

    def addEdge(self, courses):
        self.reprequisite.append(courses) 
    def set_reprequisite(self, reprequisite):
        self.reprequisite = reprequisite                                                                                                                           


class Benmark(object):
    def __init__(self, benchMark1, benchMark2):
        self.benchMark1 = benchMark1
        self.benchMark2 = benchMark2

    def isSatisfy(self, year, completedClass):
        if year == 1:
            for i in range (len(self.benchMark1) -1, -1, -1):
                if self.benchMark1[i] in completedClass:
                    del self.benchMark1[i]
            if len(self.benchMark1):
                print("Not complete class ", self.benchMark1)
                return False
            else:
                return True
        if year == 2:
            if self.isSatisfy(1, completedClass):
                for i in range (len(self.benchMark2) -1, -1, -1):
                    if self.benchMark2[i] in completedClass:
                        del self.benchMark2[i]
                if len(self.benchMark2):
                    print("Not complete class ", self.benchMark1)
                    return False
                else:
                    return True
            else:
                return False

class MajorRequirement(object):
    def __init__(self, requirementCourses):
        self.requirementCourses = requirementCourses

    def isCompleted(self, completedCources):
        for i in range (len(self.requirementCourses) - 1, -1, -1):
            if (self.requirementCourses[i] in completedCources):
                del self.requirementCourses[i]
        if (len(self.requirementCourses)):
            print("One or more major requirements not meet", self.requirementCourses)
            return False
        else:
            return True

class PlanValidation(object):
    def __init__(self, coursesDatabase):
        self.courseDatabase = coursesDatabase
        self.finishedCourse = []
    def validateCourses(self, plan):
        for semester in range (1,9):
            currentSemester = plan[semester]
            for courseItr in currentSemester:
                if (courseItr in self.courseDatabase.keys()):
                    currCourseObj = self.courseDatabase[courseItr]
                    if len(currCourseObj.reprequisite):
                        if currCourseObj.isSatisfy(self.finishedCourse):
                            self.finishedCourse.append(currCourseObj.code)
                        else:
                            print("Failed one or more reprequisite courses ", currCourseObj.code)
                            return False
                    else:
                        self.finishedCourse.append(currCourseObj.code)
            benMark = Benmark(["MATH115", "PSYC100"], ["INST126", "INST201", "STAT100"])
            if semester == 2:
                if benMark.isSatisfy(1, self.finishedCourse):
                    print("Satisfy first year benchMark")
                else:
                    print("Failed to meet first year benchMark")
                    return False
            elif semester == 4:
                if benMark.isSatisfy(2, self.finishedCourse):
                    print("Satisfy second year benchMark")
                else:
                    print("Failed to meet second year benchMark")
                    return False
        majorReq = MajorRequirement(["INST311", "INST314", "INST326", "INST327", "INST335", "INST352", "INST346", "INST362", "INST490"])
        if majorReq.isCompleted(self.finishedCourse):
            print("Congratulation. You completed all requirements")
        else:
            print("Failed to complete the major requirements", self.finishedCourse)
            return False
        return True

def main(filename:str):
    tree = ET.parse(filename)
    root = tree.getroot()

    courseDataFromFile = {}
    for coursesItr in root.findall("courses"):
        course = coursesItr.findall("course")
        for courseItr in course:
            attr = courseItr.attrib
            code = attr["name"]
            credit = attr["credit"]
            description = attr["description"]
            courseObj = Course(code, credit, description)
            courseDataFromFile[code] = courseObj
            for prerequisiteItr in courseItr.findall("prerequisite"):
                prerequisiteName = prerequisiteItr.findall("name")
                prerequisiteCurrList = []
                for prerequisiteNameItr in prerequisiteName:
                    prerequisiteCurrList.append(courseDataFromFile[prerequisiteNameItr.text].code)
                courseObj.addEdge(prerequisiteCurrList)
            new_list = []
            for ele in courseObj.reprequisite:
                if ele:
                    new_list.append(ele)
            courseObj.set_reprequisite(new_list)

    validPlan = {1: ["MATH115","STAT100", "ENGL101", "ELECTIVE", "DSHU"],
            2: ["INST126", "PSYC100", "DSSP", "FSOC", "ELECTIVE"],
            3: ["INST201", "INST326", "INST311", "DSNL", "ELECTIVE"],
            4: ["INST327", "INST335", "DSHU", "DSHS", "ELECTIVE"],
            5: ["INST314", "INST_UP", "ENGL391", "ELECTIVE", "ELECTIVE"],
            6: ["INST352", "INST_UP", "ELECTIVE", "ELECTIVE", "ELECTIVE"],
            7: ["INST346", "INST362", "INST_UP", "ELECTIVE", "ELECTIVE"],
            8: ["INST490", "INST_UP", "INST_UP", "INST_UP", "ELECTIVE"]
            }

    errorPlan = {1: ["INST335", "STAT100", "ENGL101", "ELECTIVE", "DSHU"],
            2: ["INST126", "PSYC100", "DSSP", "FSOC", "ELECTIVE"],
            3: ["INST201", "INST326", "INST311", "DSNL", "ELECTIVE"],
            4: ["INST327", "MATH115", "DSHU", "DSHS", "ELECTIVE"],
            5: ["INST314", "INST_UP", "ENGL391", "ELECTIVE", "ELECTIVE"],
            6: ["INST352", "INST_UP", "ELECTIVE", "ELECTIVE", "ELECTIVE"],
            7: ["INST346", "INST362", "INST_UP", "ELECTIVE", "ELECTIVE"],
            8: ["INST490", "INST_UP", "INST_UP", "INST_UP", "ELECTIVE"]
            }
    validator = PlanValidation(courseDataFromFile)
    validator.finishedCourse.append("MATH113")
    validator.validateCourses(validPlan)

if __name__ == "__main__":
    filename = "planner.xml"
    main(filename)

