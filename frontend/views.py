from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.db.models import Q
from datetime import date
# Create your views here.
from django.contrib import messages



def index(request):
    error = ""
    if request.method == 'POST':
        sd = request.POST['customernumber']
        pwd = request.POST['password']
        connection = Connection.objects.filter(customerconnectionid=sd).first()
        if connection is not None and connection.customeroccupation == pwd:
            viewbill = Bill.objects.filter(connection=connection, status='Not Paid')
            return render(request, 'viewmybill.html', locals())
        else:
            messages.info(request, 'There is no user found, Can you please use below link to create account!')
            return redirect('index')

    return render(request, 'index.html', locals())


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['userfullname']
        p = request.POST['userpassword']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())


def admin_home(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    cus = Customer.objects.all().count()
    conn = Connection.objects.all().count()
    b = Bill.objects.all().count()

    d = {'cus': cus, 'conn': conn, 'b': b}
    return render(request, 'admin_home.html', d)


def add_Customer(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        c = request.POST['usercontactnumber']
        e = request.POST['nickname']
        a = request.POST['address']
        city = request.POST['city']
        s = request.POST['state']
        try:
            user = User.objects.create_user(
                first_name=fn, last_name=ln, username=e)
            Customer.objects.create(
                user=user, usercontactnumber=c, useraddress=a, usercity=city, userstate=s)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Customer.html', locals())


def view_Customer(request):
    if not request.user.is_authenticated:
        return redirect('index')
    customer = Customer.objects.all()
    return render(request, 'view_Customer.html', locals())


def edit_Customer(request, pid):
    if not request.user.is_authenticated:
        return redirect('index')
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(id=pid)
    error = False
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        c = request.POST['contact']
        a = request.POST['address']
        city = request.POST['city']
        s = request.POST['state']

        user.first_name = fn
        user.last_name = ln
        customer.usercontactnumber = c
        customer.useraddress = a
        customer.usercity = city
        customer.userstate = s
        user.save()
        customer.save()
        error = True

    d = {'customer': customer, 'user': user, 'error': error}
    return render(request, 'edit_Customer.html', locals())


def delete_Customer(request, pid):
    customer = Customer.objects.get(id=pid)
    customer.delete()
    return redirect('view_Customer')


def add_Connection(request):
    if not request.user.is_authenticated:
        return redirect(index)
    error = ""
    customer1 = Customer.objects.all()
    if request.method == "POST":
        cid = request.POST['connectionid']
        customerid = request.POST['customerid']
        ctype = request.POST['connectiontype']
        cdate = request.POST['connectionstartdate']
        o = request.POST['occupation']
        cload = request.POST['connectionload']
        pno = request.POST['plotno']
        c = request.POST['city']
        p = request.POST['pincode']
        a = request.POST['address']
        s = request.POST['state']
        d = request.POST['description']

        customer = Customer.objects.get(id=customerid)
        try:
            Connection.objects.create(customer=customer, customerconnectionid=cid, customerconnectiontype=ctype, customerconnectionstartdate=cdate, customeroccupation=o,
                                      customerconnectionload=cload, customerplotno=pno, customercity=c, customerpincode=p, customeraddress=a, customerstate=s, customerdescription=d)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Connection.html', locals())


def view_Connection(request):
    if not request.user.is_authenticated:
        return redirect('index')
    connection = Connection.objects.all()
    return render(request, 'view_Connection.html', locals())


def edit_Connection(request, pid):
    if not request.user.is_authenticated:
        return redirect('index')
    customer = Customer.objects.all()
    connection = Connection.objects.get(id=pid)
    error = False
    if request.method == 'POST':
        cid = request.POST['connectionid']
        customerid = request.POST['customerid']
        ctype = request.POST['connectiontype']
        cdate = request.POST['connectionstartdate']
        o = request.POST['occupation']
        cload = request.POST['connectionload']
        pno = request.POST['plotno']
        c = request.POST['city']
        p = request.POST['pincode']
        a = request.POST['address']
        s = request.POST['state']
        d = request.POST['description']

        customer1 = Customer.objects.get(id=customerid)

        connection.customer = customer1
        connection.customerconnectiontype = ctype
        connection.customeroccupation = o
        connection.customerconnectionload = cload
        connection.customerplotno = pno
        connection.customercity = c
        connection.customerpincode = p
        connection.customeraddress = a
        connection.customeraddress = s
        connection.customerdescription = d
        if cdate:
            connection.customerconnectionstartdate = cdate
        connection.save()
        error = True

    d = {'connection': connection, 'customer': customer, 'error': error}
    return render(request, 'edit_Connection.html', locals())

def delete_Connection(request, pid):
    connection = Connection.objects.get(id=pid)
    connection.delete()
    return redirect('view_Connection')

def add_Bill(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    error = ""
    connection1 = Connection.objects.all()
    if request.method == "POST":
        customerconnectionid = request.POST['connectionid']
        b = request.POST['newbilldate']
        cdreading = request.POST['currentdayreading']
        cpdreading = request.POST['previousdayreading']
        cnreading = request.POST['currentnightreading']
        cnpreading = request.POST['previousnightreading']
        cgreading = request.POST['currentgasreading']
        cgpreading = request.POST['previousgasreading']
        # t = request.POST['totalunit']
        cpud = request.POST['chargeperunitforday']
        cpun = request.POST['chargeperunitfornight']
        cpug = request.POST['chargeperunitforgas']
        cpuv = request.POST['stadingchargeper']
        fa = request.POST['finalamount']
        dd = request.POST['duedate']

        connection = Connection.objects.get(id=customerconnectionid)
        try:
            Bill.objects.create(connection=connection, billformonth=b, dayelectricitycurrentreading=cdreading, dayelectricitypreviousreading=cpdreading,
                                dayelectricitychargeperunit=cpud, nightelectricitycurrentreading=cnreading, nightelectricitypreviousreading=cnpreading,
                                nightelectricitychargeperunit=cpun, gascurrentreading=cgreading, gaspreviousreading=cgpreading, gaschargeperunit=cpug, standingcharge=cpuv,  finalamount=fa, duedate=dd, status='Not Paid')
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Bill.html', locals())


def add_BillUser(request):
    # if not request.user.is_authenticated:
    #     return redirect(index)
    error = ""
    connection1 = Connection.objects.all()
    if request.method == "POST":
        customerconnectionid = request.POST['connectionid']
        b = request.POST['newbilldate']
        cdreading = request.POST['currentdayreading']
        cpdreading = request.POST['previousdayreading']
        cnreading = request.POST['currentnightreading']
        cnpreading = request.POST['previousnightreading']
        cgreading = request.POST['currentgasreading']
        cgpreading = request.POST['previousgasreading']
        # t = request.POST['totalunit']
        cpud = request.POST['chargeperunitforday']
        cpun = request.POST['chargeperunitfornight']
        cpug = request.POST['chargeperunitforgas']
        cpuv = request.POST['stadingchargeper']
        fa = request.POST['finalamount']
        dd = request.POST['duedate']

        connection = Connection.objects.get(id=customerconnectionid)
        try:
            Bill.objects.create(connection=connection, billformonth=b, dayelectricitycurrentreading=cdreading, dayelectricitypreviousreading=cpdreading,
                                dayelectricitychargeperunit=cpud, nightelectricitycurrentreading=cnreading, nightelectricitypreviousreading=cnpreading,
                                nightelectricitychargeperunit=cpun, gascurrentreading=cgreading, gaspreviousreading=cgpreading, gaschargeperunit=cpug, standingcharge=cpuv,  finalamount=fa, duedate=dd, status='Not Paid')
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_BillUser.html', locals())



def view_Bill(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    bill = Bill.objects.all()
    return render(request, 'view_Bill.html', locals())


def delete_Bill(request, pid):
    bill = Bill.objects.get(id=pid)
    bill.delete()
    return redirect('view_Bill')


def Logout(request):
    logout(request)
    return redirect('index')


def payment(request, pid):
    error = ""
    bill = Bill.objects.get(id=pid)
    if request.method == "POST":
        bill.status = "paid"
        try:
            bill.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'payment.html', locals())


def viewmybill(request, pid):
    error = ""
    bill = Bill.objects.get(id=pid)
    if request.method == "POST":
        bill.status = "paid"
        try:
            bill.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'viewmybill.html', locals())

def billpayment(request, pid):
    error= ""
    bill = Bill.objects.get(id = pid)
    if request.method == "POST":
        bill.status = "paid"
        try:
            bill.save()
            error = "no"
        except:
            error = "yes"
    return render(request, "billpayment.html", locals())
    