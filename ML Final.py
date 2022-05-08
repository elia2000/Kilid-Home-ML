from sklearn import tree
import mysql.connector

cnx = mysql.connector.connect(user='home', password='abc123',
                            host='127.0.0.1',
                            database='old_PC')
print('\nConnected To MySQL!\n')
cursor = cnx.cursor()

X = []
Y = []
inp = []
inpp = []
prefix= ['Squer Meter: ','Age: ','Number of Room(s): ','Parking(s): ','Loby: ','Store: ','Sport Room: ','Security: ','Elevator: ','Balkon: ','Pool: ','Sona: ','Air Cond: ','Social Room: ','Roof Garden: ','Remote Door: ','Jacuzzi: ','Centeral Anthena: ']

cursor.execute("SELECT Squer_Meter,Age,Room,Parking,Loby,Store,Sport_Room,Security,Elevator,Balkon,Pool,Sona,Air_Cond,Social_Room,Roof_Garden,Remote_Door,Jacoozy,Centeral_Anthena FROM Home_Data;")
ans_x = cursor.fetchall()

cursor.execute("SELECT Price_Squer FROM Home_Data;")
ans_y = cursor.fetchall()

cursor.execute("SELECT COUNT(*) FROM Home_Data;")
count = cursor.fetchall()
count = count[0][0]

for i in ans_x:
    b = []
    b.append(float(i[0]))
    for j in range(len(i) - 1):
        b.append(j+1)
    X.append(b)

for i in range(len(ans_y)):
    Y.append(int(round(ans_y[i][0])))

clf = tree.DecisionTreeClassifier()
clf.fit(X, Y)

for i in range(18):
    try:
        if i == 1:
            print('--------Age 0 means new bulit apartment--------')
        if i >= 4:
            print('----------Bool Type just enter 0 or 1----------')
        inp.append(int(input(prefix[i])))
    except:
        print('Error!')

inp1 = []
for i in range(18):
    inp1.append(inp)

anss = clf.predict(inp1)
anss = anss[0]

print("--------------------------------------------------------------------------------------------------------------------------------------------------\n\n\tPrice per meter : %i millions\n\tTotal price for %i squer-meter apartment is : %s billions\n\tMachine Learned from %i cases :)\n\n--------------------------------------------------------------------------------------------------------------------------------------------------" %(anss, inp[0], str((float(inp[0]) * float(anss)) / 1000), count))