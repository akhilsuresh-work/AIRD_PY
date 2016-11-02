from django.urls import reverse
from django.template import loader
from .models import Question, Choice, Userdb
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('login/index.html')
    context = {
            'latest_question_list':latest_question_list,
    }
    return render(request,'login/index.html',context)

def airdlogin(request):
        try:
            if request.session.get('logged',True):
                if request.method == "POST" :
                    request_user = request.POST.get("username")
                    request_password = request.POST.get("password")
                    user = Userdb.objects.get(user_name = request_user)
                    if user.user_state == "active":
                        if user.password == request_password :
                            request.session['logged'] = False
                            username = user.user_access
                            return render(request,'login/home.html',{'useraccessed':username,})
                else:
                    return render(request,'login/airdlogin.html')
            else:
                return render(request,'login/home.html',{'error_message':"You have to logout.",})
        except:
            return render(request,'login/airdlogin.html',{'error_message': "Either username or password is incorrect.",})
        else:
            return render(request,'login/airdlogin.html',{'error_message': "Either username or password is incorrect.",})

def airdlogout(request):

    try:
        del request.session['logged']
    except KeyError:
        pass
    return render(request,'login/airdlogin.html')


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,'login/detail.html',{'question':question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'login/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('login:results', args=(question.id,)))