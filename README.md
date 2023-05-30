# projectsHD

Hotel Management:
*****************
This is our cicily hotel home page. In this page we have to login using username and password. Here we have 3 users hotel manager, hotel admin,receptionist. Based on designation we can access particular users pages,If we enter wrong user name and password details its shows invalid details. After that we enter manager details like username and password it goes to managerhomepage . Afer that manager page displays, in this page we have Home,Employee form,Employee Details,Room Availability,Room Booking. when we open Employee Form Page  Hotel Employee details form will be displayed were we need enter to employee details and submit. Next is Employee Details page where the submitted employee details will be shown.In this page we can do sorting according to our requirements like employee id ,gender,mobile number etc. Next is  Room Availability page in this page we have unbooked and booked rooms list. Next is Room Booking page where we can book a room by giving checkin and checkout dates and no.of beds and room type when we submit the details it asks details like name ,mbl no , email and displays available rooms. From available rooms we have to select a room andclick on book now button then a dialogue appears shows booked succesfully then click ok. when go back to room availability page the selected room by us will be shown on booked rooms side .Also in this page we have a option to cancel our booked room on booked room side and a dialogue box appers saying do u want to cancel thr room 201?then click ok to cancel booking. if we click on cancel the booked room will be cancelled. when we logout from the page and click back button and enter room booking detalis and submit then it will shows session over plaese login again>..... Logout from manager page and now we login with receptionist credentials.  In this page we will have room availabilty and room booking accessibility to recepionist the functionalities are same as the admin functionalities..

commands:1.python manage.py makemigrations 2.python manage.py migrate 3.python manage.py runserver



DigitalMarketing:
*****************
I am gonna give overview of digital marketing project.This is the DigitalMarketing project folder.This is the source code of our project..
lets talk about the overview of our project
Inside the DigitalMarketing project we have 3 users
1.SuperAdmin
2.User
3.Client

In DigitalMarketing project we have different access for each user.Here for 
SUPERADMIN having (all privalages) like clientForm,ClientDetails,CampaignData,CampaignDetails,ReportForm,ReportDetails 

For USER we have (Campaign Data & Report Form) ,

And CLIENT having(Client Pages) access

lets look at the previlages
we need to enter python manage.py runserver command for running our project


And each user have different privileges of web pages.Like the superadmin have ---- these privilages and client have -- access and user have --- access.

Now we need to run our project by using python manage.py runserver command.By clicking on the following link the project home page will open.These are the username and password for each user.

using superadmin credentials now we login then logout.if we enter wrong udername and Password it shows invalid details.

Next we login into super admin page.Here we have so many pages like client form , client details------.

In client form we enter new client detalis like client name, username, Password etc..and choose a image for the particular client.click on submit then a dialogue box appers saying form submitted successfully then click on ok.
click on back button and then click client details here it show all client details that are entered previously and we have extra functionality of deteting and editing the client details.
Now click on campain data where we have to enter client campain requirements.To do that first we have select the client name from the drop down button.Then enter campain name,start and end date,planned impressions.....when clicked on submit button it shows submoitted successfully.

now open campaign details its shows the previously entered data from campaign data and we  can delete and edit data.
IN report page we should select client and campaign name
and based on the our requiremetn we have select a date.
enter no.of impressions and --------- of that patricualr date tthen it will calculate the total no.of imp....... click on submit button a dialoge box appears saying form submitted successfully. 
  
* coming to report details 
it will show all the data regarding to client name and campaign details, date of report,no of impressions, no of clicks,cost per impression, cost per click,
cost per day, status(showing whether the campaign is running are closed or pending) actions (edit or delete).
here we can search the particular campaign in search bar or we can filter the data by the client name and campaign name
* log out from super admin

USER page:
*********
login with user details in login page
if we enter wrong creditionals then invalied details msg is shown
* comming to client requirements
the client name we have created in client form it should be displayed in client name dropdown
based on that we create campaign name
then we will give starting date and ending date
here we will fill only required fields
* comming to report form
here we will enter daily reports regarding to no of impressions, no of clicks,cost per impression, cost per click
it defaultly take total cost per impressions, total cost per clicks, cost per day
then click on submit button a dialoge box appears saying form submitted successfully. 
* the report form data is shown in super admin page
 
* log out from User page


Client page:
*************
login with Client Details in the login page
there is one dropdown in the clientpage to select campaign name 
based on the selected campaign name it will take all the data from reportpage and the mix-chart type (consists of bar and line chart)
and the secound graph is donut type it will show all the data regarding to the report of campagin like (total cost,total impressions,total clicks)
it will show all the statics of the campaign

* logout form client page

Forget Password field:
**********************
if we forget password regarding to client login we should click on forget password field
we have to give the details like username and mail id while we gave at the time of creating client
and submit the data
the otp is send to regestered mailid 
after entering the otp we have to click on submit
then enter new password and reset password 
and click on submit button 
then the msg is displayed the password is changed sucessfully
after changing the password we try to login with old password it will show the msg invalid details
the password is changed sucessfully
