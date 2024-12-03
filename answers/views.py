from django.http import HttpResponseRedirect
from django.shortcuts import render
from create_form.models import Form
from results.models import Responses
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

def response(request, code, response_code):
    # Retrieve the form or return 404 if not found
    form_info = get_object_or_404(Form, code=code)

    # Retrieve the response or return 404 if not found
    response_info = get_object_or_404(Responses, response_code=response_code)

    # Render the response page with the retrieved data
    return render(request, "sub/response.html", {
        "form": form_info,
        "response": response_info,
    })
