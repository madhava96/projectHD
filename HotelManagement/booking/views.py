from django.shortcuts import render,HttpResponse
import MySQLdb as sql
from login.views import userdata

check = 0 #its storing data data coming from check function 


def check(request):
    global check
    user = userdata()
    print(user)
    try:
        if request.method=='GET':
            if user=='none':
                return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
        elif request.method == "POST":
            if user=='none':
                return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
            #conn = sql.connect(host='192.168.30.75',user='user',passwd='pass',db='hotel') #connection done
            conn = sql.connect(user='root',passwd='admin',db='hotel')
            cur = conn.cursor()
            data = request.POST
            #print(len(data))
            val = list(data.values())[1:] #storing values
            #print(val)
            x = 1    #validating if no data is coming
            for i in val:
                #print(i)
                if i == '':
                    x = 0
            #print(x)
            if x == 0:
                return render(request,"booking.html",{'data':x,'u':user}) #pass data is none so its validate in html
            else:
                #print(val)
                check = val
                q="select * from  availibilty_rooms where no_of_bed = {} and type='{}' and status = 'NOT BOOKED'".format(int(val[2]),val[3])#according to customers requirement we searching availbles rooms from db
                cur.execute(q)
                l = list(cur.fetchall())
                if len(l) !=0:
                    return render(request,"booking.html",{'d':l,'s':'flex','u':user}) #if data found next field will apear
                else:
                    return render(request,"booking.html",{'data':1,'u':user}) #if data not found it will disaplay no rooms availbale
    except Exception as e:
        return HttpResponse('something went wrong check:'+str(e)) #if any error came it will throw error as httpresponce
'''this function used for booking the room'''
def book(request):
    user = userdata()
    print(user)
    try:
        if request.method=='GET':
            if user=='none':
                return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
        elif request.method == "POST":
            if user=='none':
                return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
            #conn = sql.connect(host='192.168.30.75',user='user',passwd='pass',db='hotel')
            conn = sql.connect(user='root',passwd='admin',db='hotel')
            cur = conn.cursor()
            data = request.POST
            x=list(data.values())[1:]
            #print(x)
            if len(x) !=0:
                x = x + check[:2] #merging data booking details and avaibility details
                print(x)
                q = "insert into booking_booking(name,mobile_no,email,checkin,checkout,a_room_id) values('{}',{},'{}','{}','{}',{})".format(x[0],x[1],x[2],x[4],x[5],x[3]) #customer data inserted into booking table in db
                cur.execute(q)
                cur.execute("update availibilty_rooms set status='BOOKED' where room_no = {}".format(x[3])) #its updating status of rooms available
            conn.commit()
        return render(request,"booking.html",{'s':'none','u':user}) #its now gonna display booking field
    except Exception as e:
        return HttpResponse('something went wrong check:'+str(e)) #if any error came it will throw error as httpresponce
    
