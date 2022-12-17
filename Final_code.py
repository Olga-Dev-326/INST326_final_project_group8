# Team 8: Olga, Molondo, Viet, Tanna 
# INST326
# Final Project
import pandas as pd
from pprint import pprint
import csv


class UMD_class(object):
    """ Parent class that represents a course taken at UMD

    Args:
        object (UMD_class): class that represents a taken course with grade and credits
    """    
    def __init__(self, classcode, grade, credits):
        """ 

        Args:
            classcode (str): cource name / class code
            grade (str): grade earned for taken course
            credits (int): how many credits course was worth
        """
        self.classcode = classcode
        self.grade = grade
        self.credits = credits
        
    def is_passing_grade(self):
        """ used to check if class was passed with passing grade to earn credits

        Returns:
            bool: true if class is passed
        """        
        if self.grade == "D" or self.grade == "F":
            return False
        elif self.grade == "A" or self.grade == "B" or self.grade =="C":
            return True
        
class BenchMark(UMD_class):
    """ child class of umd_class that represents a benchmark course, inherits common proporties classcode grade and credits

    Args:
        UMD_class (object): parent object
    """   
    def __init__(self,classCode,grade,credits):
        super().__init__(classCode,grade,credits) 
    
    def is_benchmark(self):
        """ returns list of class if it is a benchmark

        Returns:
            list: list of class if it is benchmark class
        """            
        benchmark_list =["CMSC140","MATH115","STAT100","PSYC100"]
        completed_benchmark =[]
        for benchmark_class in benchmark_list:
            if self == benchmark_class:
                completed_benchmark.append(self)
        return completed_benchmark
    
    def __repr__(self):
        """ Returns object is a string format.

        Returns:
            str: returns a description of the Benchmark class properties.
        """
        return f"Classcode: {self.classcode} Grade: {self.grade} Credits: {self.credits}"
    
        
        
class MajorCore(UMD_class):
    """ child class of umd_class that represents a major course, inherits common proporties classcode grade and credits

    Args:
        UMD_class (object): parent object
    """    
    def __init__(self, classCode,grade,credits):
        super().__init__(classCode,grade,credits)
    
    def is_major_core(self):
        """ Return 

        Returns:
            list: list of class if it is major class
        """        
        major_core_list = ["INST301","INST311","INST314","INST326","INST327","INST355","INST346","INST352","INST362","INST490"]
        completed_major_class =[]
        for major_core_class in major_core_list:
            if self == major_core_class:
                completed_major_class.append(self)
        return completed_major_class
    
    def __repr__(self):
        
        """ Returns object is a string format.

        Returns:
            str: returns a description of the driver robot's properties.
        """
        return f"Classcode: {self.classcode} Grade: {self.grade} Credits: {self.credits}"

def main(filename:str):
    """ Read csv file using pandas
        Create two empty lists to hold our objects, one for major classes one for core classes
        We loop through our pandas dataframe that is loaded from csv
        For each loop we parse that row/line and see if the class could be a Major class or Benchmark(core) class
        We initialize a new object for the type of class and prove it the course code, grade and credits worth
        
        Finally we count how many credits were earned for passing courses by looping over our list of objects
        Checking if each class object has a passing grade using the parent class is_passing_grade() function
        If true we add the credits to our major or core credit counter
        
        At the end we print if over 60 credits if user is ready for graduation

    Args:
        filename (str): filename to parse
    """    
    df = pd.read_csv(filename)
    core_classes = []
    major_classes = []
    for index, row in df.iterrows():
        class_code = row["Course"]
        class_grade = row["Grade"]
        class_credits = row["Credits"]
        
        if (class_code.startswith("INST")):
            created_class = MajorCore(class_code,class_grade, class_credits)
            major_classes.append(created_class)
        else: 
            created_class = BenchMark(class_code,class_grade, class_credits)
            core_classes.append(created_class)

    major_credits = 0        
    for x in major_classes:
        if x.is_passing_grade():
            major_credits = major_credits + x.credits
    print("INST Classes",major_credits)

    core_credits = 0        
    for x in core_classes:
        if x.is_passing_grade():
            core_credits = core_credits + x.credits

    total_credits = major_credits + core_credits
    print("Total Credits", total_credits)
    print("Benchmark Classes", core_credits)

    if total_credits < 60:
        print("Not enough total credits to apply for graduation")
    else:
        print("You have earned enough credits to apply for graduation")
    
    # Audited core class list that each core class has a passing grade and how many credits each class is
    # To graduate you need 60 credits GEN Ed
    # For major you need 60 credits and we need to check against the benchmarks if the class exists
 
if __name__ == "__main__":
    filename = "curriculum.csv"
    main(filename)