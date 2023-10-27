"""
Author: Zella King (zella.king@ucl.ac.uk)

File: patient_class.py
Description: Class definition for a single instance of a patient

Inputs: Attributes about a patient
Outputs: An instance of a class Patient, with a medical condition generated by ChatGPT

Requires:
- Custom Libraries: pick_medical_condition

"""


# Import required modules
from functions.pick_medical_condition import pick_medical_condition


# Define Patient class
class Patient:
    # Initialize instance
    def __init__(
        self,
        id,
        IMD_Decile_From_LSOA,
        Age_Band,
        Sex,
        AE_Arrive_Date,
        AE_Arrive_HourOfDay,
        AE_Time_Mins,
        AE_HRG,
        AE_Num_Diagnoses,
        AE_Num_Investigations,
        AE_Num_Treatments,
        AE_Arrival_Mode,
        Provider_Patient_Distance_Miles,
        ProvID,
        Admitted_Flag,
        Admission_Method,
        ICD10_Chapter_Code,
        Treatment_Function_Code,
        Length_Of_Stay_Days,
        Chapter,
        Block,
        Title,
        Treatment_Function_Title,
    ):
        # Assign attributes
        self.id = id
        self.IMD_Decile_From_LSOA = IMD_Decile_From_LSOA
        self.Age_Band = Age_Band
        self.Sex = Sex
        self.AE_Arrive_Date = AE_Arrive_Date
        self.AE_Arrive_HourOfDay = AE_Arrive_HourOfDay
        self.AE_Time_Mins = AE_Time_Mins
        self.AE_HRG = AE_HRG
        self.AE_Num_Diagnoses = AE_Num_Diagnoses
        self.AE_Num_Investigations = AE_Num_Investigations
        self.AE_Num_Treatments = AE_Num_Treatments
        self.AE_Arrival_Mode = AE_Arrival_Mode
        self.Provider_Patient_Distance_Miles = Provider_Patient_Distance_Miles
        self.ProvID = ProvID
        self.Admitted_Flag = Admitted_Flag
        self.Admission_Method = Admission_Method
        self.ICD10_Chapter_Code = ICD10_Chapter_Code
        self.Treatment_Function_Code = Treatment_Function_Code
        self.Length_Of_Stay_Days = Length_Of_Stay_Days
        self.Chapter = Chapter
        self.Block = Block
        self.Title = Title
        self.Treatment_Function_Title = Treatment_Function_Title

        # Get medical condition and notes
        # self.Medical_Condition = self._pick_medical_condition()
        (
            self.Medical_Condition,
            self.Admission_Note,
            self.Latest_Note,
        ) = self._pick_medical_condition()

    # Private method to pick medical condition
    def _pick_medical_condition(self):
        # Get medical condition from external function
        return pick_medical_condition(self)
