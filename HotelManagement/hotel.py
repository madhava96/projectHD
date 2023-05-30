#create table rooms(room_no int auto_increment primary key,type varchar(10), no_of_bed int, status varchar(10));
import MySQLdb as sql
import random as r
con = sql.connect(user='root',passwd='admin',db='hotel')
#con = sql.connect(host=' 192.168.30.80',user='root',passwd='admin',db='hotel')
cur = con.cursor()

l=[1,2,3,4]

for i in range(1,51):
    #print(r.choice(l))
    add = "insert into availibilty_rooms values({},'{}',{},'NOT BOOKED')".format(i,r.choice(["AC","NON-AC"]),(r.choice(l)))
    cur.execute(add)
con.commit()
