import os
import json
import pandas as pd
import uuid
from logger import logger


class StudentModel:

    def __init__(self, path, filename) -> None:
        self.path, self.filename = path, filename
        self.filepath = os.path.join(self.path, self.filename)
        # check if file does not exist, if true create it
        try:
            if not os.path.isfile(self.filepath):
                with open(self.filepath, 'w') as f:
                    f.write("[]")
            # read file and store it globally
            with open(self.filepath, 'r') as f:
                fileContent = json.load(f)
                self.df = pd.DataFrame(fileContent)
                logger.info('content read')
        except Exception as e:
            logger.critical(e)
            return

    def writeFile(self):
        # write file whenever necessary using the below function
        try:
            with open(self.filepath, 'w') as f:
                jsonContent = self.df.to_dict('records')
                json.dump(jsonContent, f, indent=2)
                logger.info('Operation Successful')
        except Exception as e:
            logger.critical(e)

    def addStudent(self, data):
        # concat new records to the dataframe
        data["id"] = str(uuid.uuid4())
        self.df = pd.concat([self.df, pd.DataFrame([data])], ignore_index=True)
        logger.info('Adding Student to Database')
        self.writeFile()

    def viewAllStudents(self):
        print(self.df)

    def viewStudent(self, key, val):
        # load the identified row into frame and print it
        frame = self.df[self.df[key] == val]
        print(frame)

    def updateStudent(self, filtObj, updateObj):
        # identify index of the row we need to find using filtObj parameter
        m = (self.df[list(filtObj)] == pd.Series(filtObj)).all(axis=1)
        # update the existing df using update method at index m
        self.df.update(pd.DataFrame(updateObj, index=self.df.index[m]))
        logger.info('Updating Students')
        self.writeFile()

    def deleteStudent(self, key, val):
        # drop a value by identifying the index of the given paramenters
        self.df.drop(self.df.index[self.df[key] == val], inplace=True)
        logger.info('Deleting Student')
        self.writeFile()

    def export(self, path):
        # use this method to copy your records to a new file by simply providing the path for the file
        try:
            with open(path, 'w') as f:
                jsonContent = self.df.to_dict('records')
                json.dump(jsonContent, f, indent=2)
                logger.info('Records tranfered Successfully')
        except Exception as e:
            logger.critical(e)


c = StudentModel('E:\FILES', 'studentInfo2.json')
# data1 = {"name": "Ojas", "roll": "20102A0025"}
# data2 = {"name": "Tanisha", "roll": "20102A004"}
# c.addStudent(data1)
# c.addStudent(data2)
# c.viewAllStudents()
# c.viewStudent("name","Ojas")
# filtObj = {"name": "Ojas"}
# new_values = {"name": "Ojas Taskar","roll":"20102A0026"}
# c.updateStudent(filtObj,new_values)
# c.deleteStudent("name", "Tanisha")
# c.export('E:\FILES\mydata.json')
c.viewAllStudents()
k = {"name": "Sonal", "roll": "20102A0040"}
c.addStudent(k)
