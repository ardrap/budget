from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,ExpenseCreateForm,DateSearchForm,ReviewExpenseForm
from django.contrib.auth import authenticate,login,logout
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Create your views here.

#reg
#login
#logout
def signin(request):
    if request.method=="POST":
        uname=request.POST.get("uname")
        pwrd=request.POST.get("password")
        #authenticate user with this username&pwd
        user=authenticate(username=uname,password=pwrd)
        if user is not None:
            login(request,user)
            return render(request,"budget/home.html")
        else:
            return render(request, "budget/login.html",{"message":"invalid credentials"})

    return render(request,"budget/login.html")

def registration(request):
    form=UserRegistrationForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("user creates")
            return redirect("signin")
        else:
            context["form"]=form
            return render(request, 'budget/registration.html', context)


    return render(request,'budget/registration.html',context)

def signout(request):
    logout(request)
    return redirect("signin")

@login_required
def expense_create(request):
    form=ExpenseCreateForm(initial={'user':request.user})
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ExpenseCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addexpense")
    return render(request,"budget/addexpenses.html",context)

@login_required
def view_expenses(request):
    form=DateSearchForm()
    context={}
    expenses=Expense.objects.filter(user=request.user)
    context["form"]=form
    context["expenses"]=expenses
    if request.method == "POST":
        form = DateSearchForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data.get("date")
            expenses=Expense.objects.filter(data=date,user=request.user)
            context["expenses"] = expenses
            return render(request, "budget/viewexpenses.html", context)
    return render(request,"budget/viewexpenses.html",context)

@login_required
def edit_expense(request, id):
    expenses=Expense.objects.get(id=id)
    form=ExpenseCreateForm(instance=expenses)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ExpenseCreateForm(request.POST,instance=expenses)
        if form.is_valid():
            form.save()
            return redirect("viewexpenses")
        else:
            form = ExpenseCreateForm(request.POST, instance=expenses)
            context["form"]=form
            return render(request, "budget/expenseedit.html", context)
    return render(request,"budget/expenseedit.html",context)

@login_required
def delete_expense(request,id):
    expenses = Expense.objects.get(id=id)
    expenses.delete()
    return redirect("viewexpenses")

def review_expense(request):
    form=ReviewExpenseForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ReviewExpenseForm(request.POST)
        if form.is_valid():
            frm_date=form.cleaned_data.get("from_date")
            to_date=form.cleaned_data.get("to_date")
            total = Expense.objects.filter(date__gte=frm_date, date__lte=to_date, user =request.user).aggregate(Sum('amount'))
            total=total["amount__sum"]
            context["total"]=total
            return render(request, "budget/review.html", context)
    return render(request,"budget/review.html",context)



