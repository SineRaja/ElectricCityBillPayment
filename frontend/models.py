from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    usercontactnumber = models.CharField(max_length=15, null=True)
    useraddress = models.CharField(max_length=200, null=True)
    usercity = models.CharField(max_length=100,null=True)
    userstate = models.CharField(max_length=100, null=True) 
    userregdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Connection(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    customerconnectionid = models.CharField(max_length=10, null=True)
    customerconnectiontype = models.CharField(max_length=100, null=True)
    customerconnectionstartdate = models.DateField(null=True)
    customeroccupation = models.CharField(max_length=100, null=True)
    customerconnectionload = models.CharField(max_length=100, null=True)
    customerplotno = models.CharField(max_length=50, null=True)
    customercity = models.CharField(max_length=100, null=True)
    customerpincode = models.CharField(max_length=10, null=True)
    customeraddress = models.CharField(max_length=200, null=True)
    customerstate = models.CharField(max_length=100, null=True)
    customerdescription = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.customerconnectionid

class Bill(models.Model):
    connection = models.ForeignKey(Connection,on_delete=models.CASCADE)
    billformonth = models.CharField(max_length=50, null=True)
    dayelectricitycurrentreading = models.CharField(max_length=50, null=True)
    dayelectricitypreviousreading = models.CharField(max_length=50, null=True)
    dayelectricitytotalunit = models.CharField(max_length=100, null=True)
    dayelectricitychargeperunit = models.CharField(max_length=100, null=True)
    nightelectricitycurrentreading = models.CharField(max_length=50, null=True)
    nightelectricitypreviousreading = models.CharField(max_length=50, null=True)
    nightelectricitytotalunit = models.CharField(max_length=100, null=True)
    nightelectricitychargeperunit = models.CharField(max_length=100, null=True)
    gascurrentreading = models.CharField(max_length=50, null=True)
    gaspreviousreading = models.CharField(max_length=50, null=True)
    gastotalunit = models.CharField(max_length=100, null=True)
    gaschargeperunit = models.CharField(max_length=100, null=True)
    standingcharge = models.CharField(max_length=50, null=True)
    finalamount = models.CharField(max_length=100, null=True)
    duedate = models.DateField(null=True)
    status = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.billformonth
