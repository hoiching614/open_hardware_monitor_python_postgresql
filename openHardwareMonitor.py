import wmi
import time
import psycopg2

# read file for user, password, host
databaseName = ""
username = ""
userpassword = ""
hostIP = ""

file1 = open('login.txt', 'r')
Lines = file1.readlines()
  
count = 0
for line in Lines:
    count += 1
    if(count == 1):
        databaseName = line.strip()
    elif( count == 2):
        username = line.strip()
    elif( count == 3):
        userpassword = line.strip()
    elif( count == 4):
        hostIP = line.strip()
    
    
conn = psycopg2.connect(database = databaseName, user = username, password = userpassword, host = hostIP, port = "5432")

print("Opened database successfully")


cur = conn.cursor()

cur.execute('''Create SCHEMA IF NOT EXISTS usage;''')
cur.execute('''SET SEARCH_PATH TO usage, cpu_usage;''')

cur.execute('''
    create table IF NOT EXISTS info(
        id serial,
        cpu DECIMAL not null,
        cpu1 DECIMAL not null,
        cpu2 DECIMAL not null,
        cpu3 DECIMAL not null
    );
''')
      
print ("Table created successfully")

w = wmi.WMI(namespace="root\OpenHardwareMonitor")
cpu = "CPU"

#print(time.time())

x = 0
for x in range(10):
    temperature_infos = w.Sensor()
    cpuInfo = []
    for sensor in temperature_infos:
        if sensor.SensorType==u'Load' and cpu in sensor.Name:
            cpuInfo.append(round(sensor.Value, 1))

    cur.execute("INSERT INTO info( cpu, cpu1, cpu2, cpu3) \
        values (" + str(cpuInfo[1]) + ", " + str(cpuInfo[0]) + ", " + str(cpuInfo[2]) + ", " + str(cpuInfo[3]) + ");")

    conn.commit()
    time.sleep(2)
    x+=1


#print ("Records created successfully");     
#cur.execute("SELECT id, cpu, cpu1, cpu2, cpu3 from info")
#rows = cur.fetchall()
#for row in rows:
   #print ("id = ", row[0])
   #print ("cpu = ", row[1])
   #print ("cpu1 = ", row[2])
   #print ("cpu2 = ", row[3])
   #print ("cpu3 = ", row[4])

conn.close()

