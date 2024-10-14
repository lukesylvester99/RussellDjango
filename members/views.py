from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST['username'] #get username/password from form on login.html
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) #verify its correct

        if user is not None:
            login(request, user) #if it is, log them in
            return redirect('home') #and return them to the homepage
        else:
            messages.error(request, "Login unsuccessful. Please check your username and password.")
            return redirect('login') #and return them to the login pg
    
    else:
        return render(request,'authenticate/login.html', {}) 
    
def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('home')