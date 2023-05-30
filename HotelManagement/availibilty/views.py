from django.shortcuts import render,HttpResponse
import MySQLdb as sql
from login.views import userdata

def show(request):
    #print(request)
    try:
        user = userdata()
        if user=='none':
            return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
        #conn = sql.connect(host='192.168.30.75',user='user',passwd='pass',db='hotel') #connection done
        conn = sql.connect(user='root',passwd='admin',db='hotel')
        cur = conn.cursor()
        data = request.POST #storing data in data variable
        #print(len(data))
        if len(data) != 0:  #after clicking cancle data will came here we are validating and updating
            d = int(list(data.keys())[1])
            #print(d)
            cur.execute('delete from booking_booking where a_room_id ={}'.format(d))
            cur.execute("update availibilty_rooms set status='NOT BOOKED' where room_no = {}".format(d))
            conn.commit()
        cur.execute("select * from availibilty_rooms where status='NOT BOOKED'")
        l = list(cur.fetchall())
        #print(l)
        cur.execute("select room_no,name,mobile_no,checkin,checkout,status from availibilty_rooms inner join booking_booking on room_no =  a_room_id order by room_no;")
        l1 = list(cur.fetchall())
        return render(request,"check.html",{'data':l,'d1':l1,'d':user}) #sending available and not available rooms data to the web page
    except Exception as e:
        return HttpResponse('something went wrong check:'+str(e)) #if any error came it will throw error as httpresponce