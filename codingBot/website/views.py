from django.contrib import messages
from django.shortcuts import render



def home(request):
    lang_list = ['Objective C', 'R', 'Ruby', 'Swift', 'c++', 'clike', 'css', 'django', 'javascriptc','html', 'markup', 'python', 'rust', 'typesript']
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        # Check to make sure they picked a lang
        if lang == "Select Programming language":
            messages.success(request, "Hey! You Forgot To Pick A Programming Language.....")
            return render(request, 'home.html', {'lang_list':lang_list, 'code':code})
       # return render(request, 'home.html', {'lang_list':lang_list, 'code':code, 'lang':lang})


    return render(request, 'home.html', {'lang_list': lang_list})
