import pyodbc
from datetime import datetime

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

open_file = open("test.csv",'r').readlines()
print("File is Opened")
data_master_array = []
for line in open_file[1:]:
    current_line = line.strip()
    data_master_array.append(current_line.split("|"))

print("Inserting a record in SQL")

# Temporary solution to generate unique numbers

tem_sql = ("DELETE from dbo.factChargeData")
cursor.execute(tem_sql)

# Inserting new data

valid_data = True

for counter in range(len(data_master_array)):
    current_data = data_master_array[counter]
    fields_string = "(ChargeDataID, AccountID, FacilityID, PostingDate, HCPCSCode, ModifierComboCode, ProvidedRVUCode, PlaceOfServiceID, CarrierNumberCode, RevenueCodeID, PhysicianNPIComboCode, DaysUnits, ChargeAmount, TotalCharges)"
    value_placeholder_string = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = []
    values.append(counter + 1)
    values.append(counter + 1)
    values.append(counter + 1)
    if(current_data[3] is not None and current_data[3] != ""):
        try:
            value_date = datetime.strptime(current_data[3] + " 00:00:00",'%m/%d/%Y %H:%M:%S')
            values.append(value_date)
        except ValueError as ve:
            valid_data = False
            break
    else:
        valid_data = False
        break    
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
if(valid_data):
    connection.commit()
    print("Record Inserted")
else:
    print("Invalid data found, record insert failed")
connection.close()
