from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages
import bcrypt
from datetime import datetime


def index(request):
    if "username" in request.session:
        return redirect("/quotes")
    else:
        return render(request, "index.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                            email=request.POST['email'], birthdate=datetime.strptime(request.POST['birthdate'], '%Y-%m-%d'), password=hash)
        request.session['username'] = request.POST['email']
        User.objects.get(email=request.POST['email'])
        return redirect("/quotes")


def checklogin(request):
    errors = {}
    if "username" not in request.session:
        errors['email'] = "<div class='ohno'>Please log in</div>"
        return False
    return True


def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        request.session['username'] = request.POST['email']
        return redirect("/quotes")


def logout(request):
    if "username" in request.session:
        del request.session["username"]
    if "email" in request.session:
        del request.session["email"]
    if "first_name" in request.session:
        del request.session["first_name"]
    if "last_name" in request.session:
        del request.session["last_name"]
    return redirect("/")


def quotes(request):
    if not checklogin(request):
        return redirect ("/")
    if request.method == "GET":
        context = {
            "user_info": User.objects.get(email=request.session['username']),
            "all_quotes": Quote.objects.all().order_by("-created_at"),
        }
        return render(request, "quotes.html", context)
    if request.method == "POST":
        errors = Quote.objects.quote_validate(request.POST)
        if errors:
            request.session['author'] = request.POST['author']
            request.session['quote'] = request.POST['quote']
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/quotes")
        else:
            uploaded_by = User.objects.get(id=int(request.POST['uploaded_by']))
            new_quote_info = Quote.objects.create(
                author=request.POST['author'], quote=request.POST['quote'], uploaded_by=uploaded_by)
            new_quote_info.users_who_like.add(uploaded_by)
        return redirect("/quotes")


def edit(request, user_id):
    if request.method == "GET":
        context = {
            "user_info": User.objects.get(email=request.session['username'])
        }
        return render(request, "edit.html", context)
    if request.method == "POST":
        errors = User.objects.edit_user_validator(request.POST, request)
        if errors:
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f"/myaccount/{user_id}")
        else:
            user_to_update = User.objects.get(email=request.session['username'])
            user_to_update.first_name = request.POST['first_name']
            user_to_update.last_name = request.POST['last_name']
            user_to_update.email = request.POST['email']
            user_to_update.save()
            request.session['username'] = request.POST['email']
            return redirect("/quotes")


def show(request, user_id):
    if request.method == "GET":
        context = {
            "user_uploader": User.objects.get(id=user_id),
            "all_quotes_uploaded_by_user": User.objects.get(id=user_id).quotes_uploaded.all()
        }
        return render(request, "show.html", context)
    if request.method == "POST":
        return redirect(f"/user/{user_id}")


def delete(request, quote_id):
    Quote.objects.get(id=quote_id).delete()
    return redirect("/quotes")

def likes(request, quote_id):
    user = User.objects.get(email=request.session['username'])
    quote = Quote.objects.get(id=quote_id)
    user.liked_quotes.add(quote)
    return redirect("/quotes")

def unlikes(request, quote_id):
    user = User.objects.get(email=request.session['username'])
    quote = Quote.objects.get(id=quote_id)
    user.liked_quotes.remove(quote)
    return redirect("/quotes")