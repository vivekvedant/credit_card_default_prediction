from fastapi import Query
from enum import Enum

class Gender(str,Enum):
    male = "male"
    female = "female"

class Education(str,Enum):
    graduage_school = "graduage_school (1)"
    university = "university (2)"
    high_school = "high_school (3)"
    others = "others (4)"
    unkown_1_education = "unkown_1_education (6)"
    unkown_2_education = "unkown_2_education (0)"

class MARRIAGE(str, Enum):
    married = "married (1)"
    single = "single (2)"
    others= "others (3)"
    unkown_1_marraige = "unkown_1_marraige (0)"

class PredictionParams:
    def __init__(self,education: Education,marriage: MARRIAGE,
                 age: int,sex: Gender,bill_amt1: int,bill_amt2: int,
                 bill_amt3: int,bill_amt4: int,bill_amt5: int,
                 bill_amt6:int, limit_balance: int, pay_0: int, pay_2: int,
                 pay_3: int, pay_4: int , pay_5: int, pay_6:int,
                 pay_amt1:int, pay_amt2: int, pay_amt3:int,
                 pay_amt4: int, pay_amt5:int, pay_amt6:int,
                
                 ):
        self.EDUCATION = education
        self.MARRIAGE = marriage
        self.SEX = sex
        self.AGE = age
        self.BILL_AMT1 = bill_amt1
        self.BILL_AMT2 = bill_amt2
        self.BILL_AMT3 = bill_amt3
        self.BILL_AMT4 = bill_amt4
        self.BILL_AMT5 = bill_amt5
        self.BILL_AMT6 = bill_amt6
        self.LIMIT_BAL = limit_balance
        self.PAY_0 = pay_0
        self.PAY_2 = pay_2
        self.PAY_3 = pay_3
        self.PAY_4 = pay_4
        self.PAY_5 = pay_5
        self.PAY_6 = pay_6
        self.PAY_AMT1 = pay_amt1
        self.PAY_AMT2 = pay_amt2
        self.PAY_AMT3 = pay_amt3
        self.PAY_AMT4 = pay_amt4
        self.PAY_AMT5 = pay_amt5
        self.PAY_AMT6 = pay_amt6
        
    def to_dict(self):
        return self.__dict__