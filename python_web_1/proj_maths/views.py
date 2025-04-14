from django.shortcuts import render, redirect
from django.core.cache import cache
from . import terms_work
from . import register_work
from . import login_work


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms, cnt = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        user_password = request.POST.get("password")
        new_term = request.POST.get("new_term", "")
        new_term_tr = request.POST.get("new_term_tr", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        user_check_res = terms_work.check_user(user_name, user_password)
        
        context = {"user": user_name}
        if user_check_res == 1:
            if len(new_definition) == 0:
                context["success"] = False
                context["comment"] = "Перевод не должен быть пустым"
            elif len(new_term) == 0:
                context["success"] = False
                context["comment"] = "Слово не должно быть пустым"
            else:
                context["success"] = True
                context["comment"] = "Ваш перевод принят"
                terms_work.write_term(new_term, new_definition, new_term_tr, user_name)
            if context["success"]:
                context["success-title"] = ""
            return render(request, "term_request.html", context)
        elif user_check_res == 0:
            context["success"] = False
            context["comment"] = "У данного пользователя недостаточно прав"
        elif user_check_res == 2:
            context["success"] = False
            context["comment"] = "Введен неверный пароль"
        elif user_check_res == 3:
            context["success"] = False
            context["comment"] = "Такого пользователя не существует"
        else:
            context["success"] = False
            context["comment"] = "Произошла ошибка"
        if context["success"]:
                context["success-title"] = ""
        return render(request, "term_request.html", context)
    
    else:
        add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)

# register user

def user_registration(request):
    return render(request, "register_user.html")

def user_register(request):

    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        user_email = request.POST.get("email", "")
        user_password_1 = request.POST.get("password_1")
        user_password_2 = request.POST.get("password_2")
        
        user_check_res = register_work.check_user(user_name, user_email)
        
        context = {"user": user_name}
        if user_check_res == 0:
            
            if user_password_1 == user_password_2:
                context["success"] = True
                context["comment"] = ""
                
                register_work.write_user(user_name, user_email, user_password_1)
            else:
                context["success"] = False
                context["comment"] = "Пароли должны совпадать"
            if context["success"]:
                context["success-title"] = ""
            return render(request, "user_add_request.html", context)
        elif user_check_res == 1:
            context["success"] = False
            context["comment"] = "Такой email уже занят"
        elif user_check_res == 2:
            context["success"] = False
            context["comment"] = "Такое имя уже занято"
        else:
            context["success"] = False
            context["comment"] = "Произошла ошибка"
        if context["success"]:
                context["success-title"] = ""
        return render(request, "user_add_request.html", context)
    
    else:
        user_registration(request)


# word translate 

def word_translate_login(request):
    request.session.flush()
    return render(request, "word_translate_login.html")

def login(request):
    user_check_res_prev = request.session.get('user_check_res_prev', 3)
    
    if user_check_res_prev != 0:
        if request.method == "POST":
            cache.clear()

            user_name = request.POST.get("name")
            user_password = request.POST.get("password")
            user_check_res = login_work.check_user(user_name, user_password)
            
            context = {"user": user_name}
            if user_check_res == 0:
                context["success"] = True
                random_word, translation, q_type = terms_work.choose_random()
                if q_type == 1:
                    context["comment"] = "Напишите слово на русском языке означающее: "+random_word
                elif q_type == 2:
                    context["comment"] = "Напишите слово на английском языке означающее: "+random_word
                else:
                    context["comment"] = "Переведите: "+random_word
                
                context["score"] = terms_work.change_user_score(user_name, 0)

                request.session['user'] = user_name
    
                request.session['translation'] = translation
                request.session['user_check_res_prev'] = user_check_res

                return render(request, "word_translate_check_request_start.html", context)
            elif user_check_res == 1:
                context["success"] = False
                context["comment"] = "Неверный пароль"
            elif user_check_res == 2:
                context["success"] = False
                context["comment"] = "Неверное имя пользователя"
            else:
                context["success"] = False
                context["comment"] = "Произошла ошибка"
            if context["success"]:
                    context["success-title"] = ""
            
            return render(request, "word_translate_login_request.html", context)
        else:

            word_translate_login(request)
    else:
        user_name = request.session['user']
        user_check_res = user_check_res_prev

        cache.clear()
        
        context = {"user": user_name}
        if user_check_res == 0:
            context["success"] = True
            random_word, translation, q_type = terms_work.choose_random()
            context["score"] = terms_work.change_user_score(user_name, 0)
            if q_type == 1:
                context["comment"] = "Напишите слово на русском языке означающее: "+random_word
            elif q_type == 2:
                context["comment"] = "Напишите слово на английском языке означающее: "+random_word
            else:
                context["comment"] = "Переведите: "+random_word
            
            request.session['user'] = user_name

            request.session['translation'] = translation
            request.session['user_check_res_prev'] = user_check_res

            return render(request, "word_translate_check_request_start.html", context)
        elif user_check_res == 1:
            context["success"] = False
            context["comment"] = "Неверный пароль"
        elif user_check_res == 2:
            context["success"] = False
            context["comment"] = "Неверное имя пользователя"
        else:
            context["success"] = False
            context["comment"] = "Произошла ошибка"
        if context["success"]:
                context["success-title"] = ""
        
        return render(request, "word_translate_login_request.html", context)
        
            
def check_word(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.session.get('user', 'Anonymous')
        translation = request.session.get('translation', 'Error')
        user_translation = request.POST.get("user_translation")

        context = {"user": user_name}
        if translation == user_translation:
            context["success"] = True
            context["comment"] = "Верный перевод"
            random_word, translation, q_type = terms_work.choose_random()
            user_score = terms_work.change_user_score(user_name, 1)
            context["score_change"] = "+1"
            context["user_score"] = user_score
            request.session['random_word'] = random_word
            request.session['user'] = user_name
            request.session['translation'] = translation
            request.session['user_check_res_prev'] = request.session.get('user_check_res_prev', 3)
        else:
            user_score = terms_work.change_user_score(user_name, -1)
            context["score_change"] = "-1"
            context["user_score"] = user_score
            context["success"] = False
            context["comment"] = "Неверный перевод, верный перевод: "+translation
        return render(request, "word_translate_check_request.html", context)
    else:
            word_translate_login(request)


    