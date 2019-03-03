SQL_RESOURCE_GROUP="crowe-demo"
SQL_LOCATION="eastus"
SQL_SERVER_NAME="sql-demo-server"
SQL_USERNAME="crowe"
SQL_PASSWORD="Practicum_2019"
SQL_DATABASE_NAME="sql-db"

az sql server create --location ${SQL_LOCATION} --name ${SQL_SERVER_NAME} --resource-group ${SQL_RESOURCE_GROUP} --admin-user ${SQL_USERNAME} --admin-password ${SQL_PASSWORD}

az sql db create --resource-group ${SQL_RESOURCE_GROUP} --name ${SQL_DATABASE_NAME} --server ${SQL_SERVER_NAME} --service-objective Basic 

