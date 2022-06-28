from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpRequest
from todolist.models import TaskList
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save(commit=False).owner= request.user
            form.save()
            messages.success(request, 'New task added successfully')
            
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(owner=request.user)
        paginator = Paginator(all_tasks, 6)
        page= request.GET.get('pgno')
        all_tasks = paginator.get_page(page)
        return render(request,'todolist.html', {'all_tasks': all_tasks})


@login_required
def delete_task(request, task_id):
    task  = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:    
        task.delete()
    else:
        messages.error(request,"Access restricted! You are not the rightful owner")
    
    return redirect('todolist')

@login_required
def complete_task(request, task_id):
    task  = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:    
        task.done=True
        task.save()
    else:
        messages.error(request,"Access restricted! You are not the rightful owner")
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task  = TaskList.objects.get(pk=task_id)
    if task.owner == request.user: 
        task.done = False
        task.save()
    else:
        messages.error(request,"Access restricted! You are not the rightful owner")
    return redirect('todolist')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task  = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task edited successfully')
            
        return redirect('todolist')
    else:
        task_edit = TaskList.objects.get(pk=task_id)
        return render(request,'edit.html', {'task_edit': task_edit})

def index(request):
    context = {
        "welcome_text":  "Home page",   
        }
    return render(request,'index.html', context)

def contact(request):
    context = {
        "welcome_text":  "Contact Us",     
        }
    return render(request,'contact.html', context)

def about(request):
    context = {
        "welcome_text":  "What about me?",   
        }
    return render(request,'about.html', context)
