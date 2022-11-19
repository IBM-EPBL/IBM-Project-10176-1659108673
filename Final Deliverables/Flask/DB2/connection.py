import ibm_db

def insertvalues(USERNAME,EMAIL,MOBILE,MESSAGE):

    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=bzf32027;PWD=70dj8j0I3SAosWRH;", '', '')
    print("Connected to DB")
    sql = "INSERT INTO contact VALUES('{}', '{}', '{}', '{}')".format(USERNAME,EMAIL,MOBILE,MESSAGE)
    stmt = ibm_db.exec_immediate(conn, sql)
    print("Number Of Rows Added : 1")

def listall():
    sql = "SELECT * FROM contact"
    stmt = ibm_db.exec_immediate(conn, sql)
    result = ibm_db.fetch_both(stmt)
    while result != False:
        print ("UserID is : ",  result['USERNAME'])
        print ("Email is : ", result['EMAIL'])
        print ("Mobile Number is : ", result['MOBILE'])
        print ("Message is : ", result['MESSAGE'])
        result = ibm_db.fetch_both(stmt)

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=bzf32027;PWD=70dj8j0I3SAosWRH;", '', '')
    print("Connected to DB")
    #listall()
    #insertvalues(USERNAME,EMAIL,MOBILE,MESSAGE)
    
except:
    print("Not Connected")
