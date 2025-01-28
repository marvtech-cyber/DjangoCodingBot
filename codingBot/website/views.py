from django.contrib import messages
from django.shortcuts import render
from  dotenv import load_dotenv
import os
import openai

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
                
                
                return render(request, 'suggest.html', {'lang_list': lang_list, 'code_response': response.choices[0].message.content, 'lang': lang})
            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'error': str(e), 'lang':lang, 'code': code})
    return render(request, 'suggets.html', {'lang_list': lang_list})
