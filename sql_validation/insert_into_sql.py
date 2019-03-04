import pyodbc
from datetime import datetime

# Connection details

server = 'sql-demo-server.database.windows.net'
database = 'sql-db'
username = 'crowe'
password = 'Practicum_2019'
driver= '{ODBC Driver 17 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
    print (row[0]) 
    row = cursor.fetchone()

# Read file

open_file = open("test.csv",'r').readlines()
print("File is Opened")
data_master_array = []
for line in open_file[1:]:
    current_line = line.strip()
    data_master_array.append(current_line.split("|"))

print("Inserting records in SQL")

# Temporary solution to generate unique numbers

tem_sql = ("DELETE from dbo.factChargeData")
cursor.execute(tem_sql)

# Inserting new data

valid_data = True
fields_string = "(ChargeDataID, AccountID, FacilityID, PostingDate, HCPCSCode, ModifierComboCode, ProvidedRVUCode, PlaceOfServiceID, CarrierNumberCode, RevenueCodeID, PhysicianNPIComboCode, DaysUnits, ChargeAmount, TotalCharges)"
value_placeholder_string = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Function to insert a record

def insert_record(current_data, counter):
    isvalid = True
    values = []
    values.append(counter + 1)
    values.append(counter + 1)
    values.append(counter + 1)
    if(current_data[3] is not None and current_data[3] != ""):
        try:
            value_date = datetime.strptime(current_data[3] + " 00:00:00",'%m/%d/%Y %H:%M:%S')
            values.append(value_date)
        except ValueError as ve:
            isvalid = False
            return(isvalid)
    else:
        isvalid = False
        return(isvalid)
    values.append(int(current_data[4]))
    values.append(str(current_data[5]) + "," + str(current_data[6]) + "," + str(current_data[7]) + "," + str(current_data[8]))
    values.append(str(current_data[9]))
    values.append(str(current_data[10]))
    values.append(str(current_data[11]))
    values.append(str(current_data[13]))
    values.append(str(current_data[14]) + "," + str(current_data[15]) + "," + str(current_data[16]) + "," + str(current_data[17]))
    values.append(float(current_data[18]))
    values.append(str(current_data[19]))
    values.append(str(current_data[20]))
    sql_command = "INSERT INTO dbo.factChargeData " + fields_string + " VALUES " +  value_placeholder_string
    print(sql_command)
    print(values)
    cursor.execute(sql_command,values)
    return(isvalid)

# Function to insert data from file

total_count = len(data_master_array)

def insert_file(data_master_array):
    isvalid = True
    for counter in range(len(data_master_array)):
        current_data = data_master_array[counter]
        if(isvalid):
            isvalid = insert_record(current_data, counter)
            if(not isvalid):
                return(isvalid)
    return(isvalid)

# Function call to insert data

valid_data = insert_file(data_master_array)

# Validate data and commit only if all records executed successfully

if(valid_data):
    connection.commit()
    print("{} Records Inserted".format((total_count)))
else:
    print("Invalid data found, record insert failed")
connection.close()
