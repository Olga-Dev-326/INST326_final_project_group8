import pandas as pd

class UMD_Class(object): # All base classes
    def __init__(self,class_name:str, class_code:str, grade:str):
        self.class_name = class_name
        self.class_code = class_code
        self.grade = grade

class Core_Class(UMD_Class):  #Gen Edu
    def __init__(self,class_name:str, class_code:str, grade:str):
        super().__init__(class_name, class_code, grade) 

class Major_Class(UMD_Class):   #INST
    def __init__(self,class_name:str, class_code:str, grade:str, major_name:str, campus:str):
        super().__init__(class_name, class_code, grade)
        self.major_name = major_name
        self.campus = campus
    

def main(filename:str):
    df = pd.read_csv(filename)
    core_classes = []
    major_classes = []
    for index, row in df.iterrows():
        grade = row["Grade"]
        class_name = row["Title"]
        class_code = row["Course"]
        
        if (class_code.startswith("INST")):
            created_class = Major_Class(class_name, class_code, grade, "Information Science", "USG")
            major_classes.append(created_class)
        else: 
            created_class = Core_Class(class_name, class_code, grade)
            core_classes.append(created_class)
            
    print(core_classes)
    print(major_classes)
    
    # Audited core class list that each core class has a passing grade and how many credits each class is
    # To graduate you need 60 credits GEN Ed
    # For major you need 60 credits and we need to check against the benchmarks if the class exists
    
    
if __name__ == "__main__":
    filename = "transcript.csv"
    main(filename)