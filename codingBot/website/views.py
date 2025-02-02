from django.contrib import messages
from django.shortcuts import render, redirect
from  dotenv import load_dotenv
import os
import openai
from .models import Code 
# Authentication imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

def home(request):
    lang_list = ['Objective C', 'R', 'Ruby', 'Swift', 'c++', 'clike', 'css', 'django', 'javascriptc','html', 'markup', 'python', 'rust', 'typesript']
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        # Check to make sure they picked a lang
        if lang == "Select Programming language":
            messages.success(request, "Hey! You Forgot To Pick A Programming Language.....")
            return render(request, 'home.html', {'lang_list':lang_list, 'code':code})
        else:
            #OpenAI key
            load_dotenv()
            client = openai.OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key= os.getenv("OPENAI_API_KEY")
            )

            # Create OpenAI Instance
           # openai.model.list()

            # Make OpenAI request
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": "You are a helpful software developer."},
                        {
                            "role": "user",
                            "content": f"Respond only with code. Fix this {lang} code: {code}"
                        }
                    ]
                )
                
                # Save to database 
                record = Code(question = code, code_answer = response.choices[0].message.content, language =lang, user=request.user )
                record.save()
                return render(request, 'home.html', {'lang_list': lang_list, 'code_response': response.choices[0].message.content, 'lang': lang})
            except Exception as e:
                return render(request, 'home.html', {'lang_list': lang_list, 'error': str(e), 'lang':lang, 'code': code})
    return render(request, 'home.html', {'lang_list': lang_list})




# Suggest View
def suggest(request):
    lang_list = ['Objective C', 'R', 'Ruby', 'Swift', 'c++', 'clike', 'css', 'django', 'javascriptc','html', 'markup', 'python', 'rust', 'typesript']
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        # Check to make sure they picked a lang
        if lang == "Select Programming language":
            messages.success(request, "Hey! You Forgot To Pick A Programming Language.....")
            return render(request, 'suggest.html', {'lang_list':lang_list, 'code':code})
        else:
            #OpenAI key
            load_dotenv()
            client = openai.OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key= os.getenv("OPENAI_API_KEY")
            )

            # Create OpenAI Instance
           # openai.model.list()

            # Make OpenAI request
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": "You are a helpful software developer."},
                        {
                            "role": "user",
                            "content": f"Respond only with code.: {code}"
                        }
                    ]
                )

                # Save to database 
                record = Code(question = code, code_answer = response.choices[0].message.content, language =lang, user=request.user )
                record.save()
                
                
                return render(request, 'suggest.html', {'lang_list': lang_list, 'code_response': response.choices[0].message.content, 'lang': lang})
            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'error': str(e), 'lang':lang, 'code': code})
    return render(request, 'suggest.html', {'lang_list': lang_list})


def login_user(request):
    if request.method == "POST":
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             messages.success(request, "You have been logged In")
             return redirect('home')
         else:
             messages.success(request, "Error loging In")
             return redirect('home')
         
    else:
        return render(request, 'home.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out... Have a good day")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password=password)
            login(request, user)
            messages.success(request, "You Have Registered.....")
            return redirect('home')
        
    else :
        form = SignUpForm

    return render(request, 'register.html', {"form": form})