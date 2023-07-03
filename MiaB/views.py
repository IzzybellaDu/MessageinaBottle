from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import memory
from random import randint

def index(request):
    return render(request, 'MiaB/index.html')

def register(request):
    if request.method == 'POST':
        # Retrieving the form posted by the user
        form = UserRegisterForm(request.POST)

        # Checking if the form is valid and filled correctly
        if form.is_valid():
            # Saves the object (here, a user) related to the form
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')

    else: 
        # A new form is generated for the user accessing the register function
        form = UserRegisterForm()
    
    return render(request, 'MiaB/register.html', {
        'form': form
    })

def user_login(request):
    if request.method == "POST":
        # Retrieving the form posted by the user
        form = AuthenticationForm(request, data=request.POST)
        
        # Checking if the form is valid and filled correctly
        if form.is_valid():
            # Retrieving specific fields of the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Checking if the data matches a row in the database
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Login successful. You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.warning(request,'Invalid username or password.')
        
        else:
            messages.warning(request,'Invalid username or password.')
    
    form = AuthenticationForm()
    
    return render(request, 'MiaB/login.html', {
        "form" : form })

def user_logout(request):
    logout(request)
    return render(request, 'MiaB/logout.html')

@login_required
def newMemory(request):

    # Checking if the form is requested or has been submitted
    if request.method == 'POST':

        # Retrieve the information from the form
        title = request.POST.get('title')
        bodyText = request.POST.get('bodyText')
        date = request.POST.get('date')
        user = request.user
        
        # Add memory to the database
        newmemory = memory(title = title, bodyText=bodyText, date=date, user=user)
        newmemory.save()
        messages.success(request, 'Memory saved!')  
        return redirect('memoryList')

    return render(request, 'MiaB/newmemory.html')

@login_required
def memoryList(request):
    currentuser = request.user
    
    # Finding all the memories that belong to the specific user
    memories = memory.objects.filter(user=currentuser)

    return render(request, 'MiaB/memorylist.html', {
        'memories' : memories
    })

@login_required
def memoryFullscreen(request, id):
    # Finding the memory that the user wants to access
    desiredmemory = memory.objects.get(id=id)
    
    return render(request, 'MiaB/memoryfullscr.html', {
        'memory': desiredmemory
    })

@login_required
def deleteMemory(request):
    if request.method == 'POST':
        MemoryID = request.POST.get('MemoryID')

        # Checking if the memory exists before deleting it
        if memory.objects.filter(id=MemoryID).exists():
            memory.objects.filter(id=MemoryID).delete()
            messages.success(request, 'Memory deleted.')
            return redirect('memoryList')

        # In the case that the user tries to delete a memory that does not exist or has been deleted.
        messages.warning(request, 'An error occurred. Memory was not deleted.')
        return redirect('memoryList')

@login_required
def random(request):
    # Finding all the user's memories
    memories = memory.objects.filter(user=request.user)
    
    # Checking that the user has memories
    if len(memories) == 0:
        messages.warning(request, 'User must have at least 1 memory to use this function.')
        return redirect('memoryList')
    
    itemnum = randint(0, len(memories) - 1)
    id = memories[itemnum].id
    
    return redirect('fullscreen', id=id)