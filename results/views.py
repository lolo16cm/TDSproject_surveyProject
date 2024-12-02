from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from create_form.models import Form
from answers.models import Answer
from results.models import Responses
from user_auth.models import Profile

# Create your views here.
def responses(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    formInfo = Form.objects.filter(code = code)
    profile = get_object_or_404(Profile, user=request.user)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    formInfo = formInfo[0]

    responsesSummary = []
    for question in formInfo.questions.all():
        answers = Answer.objects.filter(answer_to = question.id)
        choices = question.choices.all()

        choice_counts = [
            {
                "choice": choice.choice,
                "count": answers.filter(answer=choice.id).count()
            }
            for choice in choices
        ]
        
        responsesSummary.append({
            "question": question,
            "answers":answers,
            "choices": choice_counts  # Pass all choices for the question
        })
        
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    
    return render(request, "sub/responses.html", {
        "form": formInfo,
        "responses": Responses.objects.filter(response_to = formInfo),
        "responsesSummary": responsesSummary,
        "role": profile.role
    })

# Error handler
def FourZeroThree(request):
    return render(request, "error/403.html")

def FourZeroFour(request):
    return render(request, "error/404.html")
