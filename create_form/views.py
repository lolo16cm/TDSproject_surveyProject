import json
import random
import string
from django.http import  HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_object_or_404, redirect
from django.urls import reverse
from answers.models import Answer
from results.models import Responses
from create_form.models import Choices, Questions, Form
from user_auth.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def create_form(request):
    """
    Create a blank form for users with the 'creator' role.
    """
    # Check if the user has the "creator" role
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.role != "creator":
            return HttpResponseForbidden("You are not authorized to create a form.")
    except Profile.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to create a form.")

    # Ensure the request method is POST
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            title = data.get("title", "Untitled Form")
            
            # Generate a random code for the form
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            
            # Create initial choices, question, and form
            choices = Choices.objects.create(choice="Option 1")
            question = Questions.objects.create(
                question_type="multiple choice",
                question="Untitled Question",
                required=False
            )
            question.choices.add(choices)
            
            form = Form.objects.create(
                code=code,
                title=title,
                creator=request.user
            )
            form.questions.add(question)
            
            return JsonResponse({"message": "Success", "code": code}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    # Handle invalid HTTP methods
    return JsonResponse({"error": "Invalid request method. Use POST instead."}, status=405)

'''eiditing form'''
@login_required
def edit_form(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    formInfo = Form.objects.filter(code = code)
    profile = get_object_or_404(Profile, user=request.user)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    return render(request, "sub/form.html", {
        "code": code,
        "form": formInfo,        
        "role": profile.role
    })

def edit_title(request, code):
    # Ensure the form exists or return a 404
    form_info = get_object_or_404(Form, code=code)

    # Check if the current user is the form creator
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to edit this form.")
    
    # Ensure the request is a POST request to update the title
    if request.method == "POST":
        data = json.loads(request.body)
        new_title = data.get("title")
        
        if not new_title:
            return JsonResponse({"error": "Title cannot be empty."}, status=400)
        
        # Update the form title
        form_info.title = new_title
        form_info.save()

        return JsonResponse({"message": "Title updated successfully."})
    
    # If not a POST request, return an error
    return JsonResponse({"error": "Invalid request method."}, status=405)

'''eiditing description'''
@login_required
def edit_description(request, code):
    form_info = get_object_or_404
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to edit this form.")
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON body
            description = data.get("description")  # Safely get the description key
            form_info.description = description  # Update the description
            form_info.save()
            return JsonResponse({"message": "Success", "description": form_info.description})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    # Return error for non-POST methods
    return JsonResponse({"error": "Invalid request method."}, status=405)

'''eiditing form setting'''
@login_required
def edit_setting(request, code):
    form_info = get_object_or_404(Form, code=code)
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to edit this form.")
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON body
            form_info.collect_email = data['collect_email']
            form_info.confirmation_message=data['confirmation_message']
            form_info.save()
            return JsonResponse({'message': "Success"})

        except json.JSONDecodeError:    
            return JsonResponse({"error":"Invalid JSON format."}, status=400)    
        
    # Return error for non-POST methods
    return JsonResponse({"error": "Invalid request method."}, status=405)

'''delete form'''
@login_required
def delete_form(request, code):
    """Delete a form and its related data."""
    form_info = get_object_or_404(Form, code=code)

    # Check if the user is the creator of the form
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to delete this form.")

    if request.method == "DELETE":
        # Delete all responses related to the form
        responses = Responses.objects.filter(response_to=form_info)
        for response in responses:
            response.response.clear()  # Clear the ManyToMany relationship
            response.delete()  # Delete the response object

        # Delete all questions and their related choices
        questions = form_info.questions.all()
        for question in questions:
            question.choices.all().delete()  # Delete related choices
            question.delete()  # Delete the question

        # Finally, delete the form itself
        form_info.delete()

        return JsonResponse({'message': "Success"})

    # Return error for invalid request methods
    return JsonResponse({"error": "Invalid request method."}, status=405)

"""Edit a choice in a form."""
@login_required
def edit_choice(request, code):
    
    # Get the form or return a 404 if it doesn't exist
    form_info = get_object_or_404(Form, code=code)

    # Check if the current user is the creator of the form
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to edit this form.")

    # Handle POST request to edit the choice
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Validate choice ID
            choice_id = data.get("id")
            if not choice_id:
                return JsonResponse({"error": "Choice ID is required."}, status=400)

            # Get the choice or return a 404 if not found
            choice = get_object_or_404(Choices, id=choice_id)

            # Update the choice's text
            # If the "choice" key does not exist in data, or if its value is None, the get() method returns the second argument (choice.choice) as a default.
            choice.choice = data.get("choice", choice.choice)  # Retain current value if not provided
            choice.save()

            return JsonResponse({'message': "Success", "choice": choice.choice})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    # Return error for invalid request methods
    return JsonResponse({"error": "Invalid request method."}, status=405)

"""Add a choice to a question in the form."""
@login_required
def add_choice(request, code): 
    # Get the form or return a 404 if it doesn't exist
    form_info = get_object_or_404(Form, code=code)

    # Check if the current user is the creator of the form
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to modify this form.")

    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            if request.method == "POST":
                data = json.loads(request.body)
                choice = Choices(choice="Option")
                choice.save()
                form_info.questions.get(pk = data["question"]).choices.add(choice)
                form_info.save()
                return JsonResponse({"message": "Success", "choice": choice.choice, "id": choice.id})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    # Return error for invalid request methods
    return JsonResponse({"error": "Invalid request method."}, status=405)

"""Remove a choice from a question in the form."""
@login_required
def remove_choice(request, code):
    # Get the form or return a 404 if it doesn't exist
    form_info = get_object_or_404(Form, code=code)
    # Check if the current user is the creator of the form
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to modify this form.")
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            # Validate and retrieve choice ID
            choice_id = data.get("id")
            if not choice_id:
                return JsonResponse({"error": "Choice ID is required."}, status=400)

            # Get the choice or return a 404 if not found
            choice = get_object_or_404(Choices, pk=choice_id)

            # Ensure the choice is associated with a question in the form
            if not form_info.questions.filter(choices=choice).exists():
                return JsonResponse({"error": "The specified choice is not associated with this form."}, status=400)
            # Delete the choice
            choice.delete()
            return JsonResponse({"message": "Success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    # Return error for invalid request methods
    return JsonResponse({"error": "Invalid request method. Use POST instead."}, status=405)

"""Retrieve choices for a specific question in a form."""
@login_required
def get_choice(request, code, question):   
    # Get the form or return a 404 if it doesn't exist
    form_info = get_object_or_404(Form, code=code)
    # Check if the current user is the creator of the form
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to view this form's choices.")
    if request.method == "GET":
        # Get the question or return a 404 if it doesn't exist
        question = get_object_or_404(Questions, id=question)
        # Ensure the question belongs to the form
        if question not in form_info.questions.all():
            return JsonResponse({"error": "The specified question does not belong to this form."}, status=400)
        # Retrieve choices for the question
        choices = question.choices.all()
        choices_data = [
            {"choice": choice.choice,  "id": choice.id} for choice in choices
        ]
        return JsonResponse({
            "choices": choices_data,
            "question": question.question,
            "question_type": question.question_type,
            "question_id": question.id
        }) 
    # Return error for invalid request methods
    return JsonResponse({"error": "Invalid request method. Use GET instead."}, status=405)

"""
    Edit a question in a form. Only the form's creator can edit.
    """
@login_required
def edit_question(request, code):
    # Get the form or return a 404 if it doesn't exist
    form_info = get_object_or_404(Form, code=code)
    # Check if the current user is the creator of the form
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to edit this form.")
    if request.method == "POST":
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            # Validate and retrieve the question
            question_id = data.get("id")
            if not question_id:
                return JsonResponse({"error": "Question ID is required."}, status=400)

            question = get_object_or_404(Questions, id=question_id)

            # Update the question fields
            question.question = data.get("question", question.question)
            question.question_type = data.get("question_type", question.question_type)
            question.required = data.get("required", question.required)
            question.save()

            return JsonResponse({"message": "Success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    # Return an error for invalid HTTP methods
    return JsonResponse({"error": "Invalid request method. Use POST instead."}, status=405)

def add_question(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        choices = Choices(choice = "Option 1")
        choices.save()
        question = Questions(question_type = "multiple choice", question= "Untitled Question", required= False)
        question.save()
        question.choices.add(choices)
        question.save()
        formInfo.questions.add(question)
        formInfo.save()
        return JsonResponse({'question': {'question': "Untitled Question", "question_type": "multiple choice", "required": False, "id": question.id}, 
        "choices": {"choice": "Option 1", "is_answer": False, 'id': choices.id}})

def delete_question(request, code, question):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        question = Questions.objects.filter(id = question)
        if question.count() == 0: return HttpResponseRedirect(reverse("404"))
        else: question = question[0]
        for i in question.choices.all():
            i.delete()
            question.delete()
        return JsonResponse({"message": "Success"})

def view_form(request, code):
    formInfo = get_object_or_404(Form, code=code)
    profile = get_object_or_404(Profile, user=request.user)

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
        # Determine the highest count
        if choice_counts:
            max_count = max(choice["count"] for choice in choice_counts)
            highest_choices = [choice for choice in choice_counts if choice["count"] == max_count]
        else:
            max_count = 0
            highest_choices = []
            
        responsesSummary.append({
            "question": question,
            "answers":answers,
            "responses": Responses.objects.filter(response_to = formInfo),
            "responsesSummary": responsesSummary,
            "choices": choice_counts,  # Pass all choices for the question
            "highestChoice": highest_choices
        })
        
    if formInfo.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "sub/view_form.html", {
        "form": formInfo,
        "role": profile.role,
        "responsesSummary": responsesSummary
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
"""Handle form submission by takers and form creator only."""
def submit_form(request, code):
    # Get the form or return a 404 if it doesn't exist
    form_info = get_object_or_404(Form, code=code)
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # Get the user's profile
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to submit this form.")

    # Check if the user is the creator or has the 'taker' role (allow the creator be able to submit the survey intentionally for testing purpose)
    if user_profile.role != "taker" and form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to submit this form.")

    if request.method == "POST":
        # Generate a unique response code
        response_code = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        # Create the response based on whether authentication or email is required
        response = Responses(
            response_code=response_code,
            response_to=form_info,
            responder_ip=get_client_ip(request),
            responder=request.user
        )
        response.save()
        # Process the answers
        for key, value in request.POST.items():
            # Skip CSRF token and email address fields
            if key in ["csrfmiddlewaretoken", "email-address"]:
                continue
            # Get the associated question
            question = form_info.questions.filter(id=key).first()
            if not question:
                continue
            # Save each answer to the question
            for answer_text in request.POST.getlist(key):
                answer = Answer(answer=answer_text, answer_to=question)
                answer.save()
                response.response.add(answer)

        # Save the response with all associated answers
        response.save()
        # Render the form response page
        return render(request, "sub/form_response.html", {
            "form": form_info,
            "code": response_code,
        })

    # If the request method is not POST, redirect to the form page
    return HttpResponseRedirect(reverse('view_form', args=[code]))

"""
    Retrieve selected checkbox choices for a given response and question.

    Args:
        response (Responses): The response object.
        question (Questions): The question object.

    Returns:
        list: A list of selected choices for the checkbox question.
    """
def retrieve_checkbox_choices(response, question):
    checkbox_answers = []
    # Get answers associated with the question and response
    answers = Answer.objects.filter(answer_to=question, response=response)
    for answer in answers:
        # Ensure the answer is valid before splitting
        if answer.answer:
            selected_choice_ids = answer.answer.split(',')  # Split string into individual choice IDs
            selected_choices = Choices.objects.filter(pk__in=selected_choice_ids)
            checkbox_answers.extend(choice.choice for choice in selected_choices)  # Flatten choices into the list
    return checkbox_answers

def edit_response(request, code, response_code):
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    response = Responses.objects.filter(response_code = response_code, response_to = formInfo)
    if response.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: response = response[0]
    if formInfo.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        if response.responder != request.user:
            return HttpResponseRedirect(reverse('403'))
    if request.method == "POST":
        if formInfo.authenticated_responder and not response.responder:
            response.responder = request.user
            response.save()
        if formInfo.collect_email:
            response.responder_email = request.POST["email-address"]
            response.save()
        #Deleting all existing answers
        for i in response.response.all():
            i.delete()
        for i in request.POST:
            #Excluding csrf token and email address
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = formInfo.questions.get(id = i)
            for j in request.POST.getlist(i):
                answer = Answer(answer=j, answer_to = question)
                answer.save()
                response.response.add(answer)
                response.save()
        if formInfo.is_quiz:
            return HttpResponseRedirect(reverse("response", args = [formInfo.code, response.response_code]))
        else:
            return render(request, "sub/form_response.html", {
                "form": formInfo,
                "code": response.response_code
            })
    return render(request, "sub/edit_response.html", {
        "form": formInfo,
        "response": response
    })

def delete_responses(request, code):
    # Get the form or return a 404 if it doesn't exist
    form_info = get_object_or_404(Form, code=code)
    # Check if the current user is the creator of the form
    if form_info.creator != request.user:
        return HttpResponseForbidden("You are not authorized to delete responses for this form.")
    # Ensure the request method is DELETE
    if request.method == "DELETE":
        # Retrieve all responses associated with the form
        responses = Responses.objects.filter(response_to=form_info)
        # Delete all related answers and responses
        for response in responses:
            response.response.all().delete()  # Delete all answers associated with the response
            response.delete()  # Delete the response itself
        return JsonResponse({"message": "Success"})
    
def publish_form(request, code):    
    form_to_update = get_object_or_404(Form, code=code)

    if request.method == "POST":
        # Update the status to "Publish"
        form_to_update.status = "Publish"
        form_to_update.save()  # Save the changes to the database

        # Return a JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "Form published successfully!"})

        # For regular form submission, redirect to the edit page
        return redirect(f'/{code}/edit')

    # For non-POST requests, render a template or return an error
    return render(request, f'{code}/edit.html', {'form': form_to_update})

def close_form(request, code):    
    form_to_update = get_object_or_404(Form, code=code)
    
    if request.method == "POST":
        # Update the status to "Close"
        form_to_update.status = "Close"
        form_to_update.save()  # Save the changes to the database

        # Return a JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "Form published successfully!"})

        # For regular form submission, redirect to the edit page
        return redirect(f'/{code}/edit')

    # For non-POST requests, render a template or return an error
    return render(request, f'{code}/edit.html', {'form': form_to_update})

def republish_form(request, code):    
    form_to_update = get_object_or_404(Form, code=code)
    
    if request.method == "POST":
        # Update the status to "Republish"
        form_to_update.status = "Republish"
        form_to_update.save()  # Save the changes to the database

        # Return a JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "Form published successfully!"})

        # For regular form submission, redirect to the edit page
        return redirect(f'/{code}/edit')

    # For non-POST requests, render a template or return an error
    return render(request, f'{code}/edit.html', {'form': form_to_update})