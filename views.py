
# Importing the required modules

# The render module is used to render the html pages, 
# the get_object_or_404 module is used to get the object or return 404 error if the object is not found 
from django.shortcuts import render, get_object_or_404,redirect

# The HttpResponseRedirect module is used to redirect to a particular page
from django.http import HttpResponseRedirect

# The RegistrationForm module is used to create the registration form
from .forms import RegistrationForm

# The messages module is used to display the messages in the html pages
from django.contrib import messages

# The login,logout,authenticate, update_session_auth_hash modules are used to login, logout, authenticate and update the session auth hash
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash

# The PasswordChangeForm module is used to create the change password form
from django.contrib.auth.forms import PasswordChangeForm

# The login_required module is used to restrict the access to the page
from django.contrib.auth.decorators import login_required

# The Candidate,ControlVote,Position models are used to create the candidate, control_vote and position tables
from .models import Candidate,ControlVote,Position

# The ChangeForm module is used to create the change password form
from .forms import ChangeForm


# ------------------ Online Voting System - Views ------------------ #

# The homeView function is used to render the home page when the user visits the home page
def homeView(request):
    return render(request, "poll/home.html")

# The registrationView function is used to render the registration page when the user visits the registration page
def registrationView(request):

    # The if statement is used to check if the request method is POST
    if request.method == "POST":

        # The form variable is used to store the RegistrationForm
        form = RegistrationForm(request.POST)

        # The if statement is used to check if the form is valid
        if form.is_valid():

            # The cd variable is used to store the cleaned data of the form
            cd = form.cleaned_data

            # The if statement is used to check if the password and confirm password are same
            if cd['password'] == cd['confirm_password']:

                # The obj variable is used to store the form data
                obj = form.save(commit=False)
                obj.set_password(obj.password)
                obj.save()

                # The messages.success function is used to display the success message
                messages.success(request, 'You have been registered.')

                # The redirect function is used to redirect to the home page
                return redirect('home')
            else:

                # The messages.success function is used to display the error message if the password and confirm password are not same
                return render(request, "poll/registration.html", {'form':form,'note':'password must match'})
    else:

        # The form variable is used to store the RegistrationForm if the request method is not POST
        form = RegistrationForm()

    # The render function is used to render the registration page
    return render(request, "poll/registration.html", {'form':form})

# The loginView function is used to render the login page when the user visits the login page
def loginView(request):
    # The if statement is used to check if the request method is POST
    if request.method == "POST":

        # The usern variable is used to store the username entered by the user
        # The passw variable is used to store the password entered by the user
        usern = request.POST.get('username')
        passw = request.POST.get('password')

        # The user variable is used to store the user object if the user is authenticated
        user = authenticate(request, username=usern, password=passw)
        if user is not None:

            # The login function is used to login the user if the user is authenticated
            # and the user is redirected to the dashboard page
            login(request,user)
            return redirect('dashboard')
        else:

            # The messages.success function is used to display the error message if the user is not authenticated
            # and the user is redirected to the login page
            messages.success(request, 'Invalid username or password!')
            return render(request, "poll/login.html")
    else:

        # The render function is used to render the login page if the request method is not POST
        # and the user is redirected to the login page
        return render(request, "poll/login.html")


# The logoutView function is used to logout the user when the user visits the logout page
@login_required
def logoutView(request):
    logout(request)
    return redirect('home')

# The dashboardView function is used to render the dashboard page when the user visits the dashboard page
@login_required
def dashboardView(request):
    return render(request, "poll/dashboard.html")

# The passwordView function is used to render the position page when the user visits the position page
@login_required
def positionView(request):

    # The obj variable is used to store the list of positions
    obj = Position.objects.all()

    # The render function is used to render the position page
    # obj is passed to the position page to display the list of positions
    return render(request, "poll/position.html", {'obj':obj})

# The candidateView function is used to render the candidate page when the user visits the candidate page
@login_required
def candidateView(request, pos):

    # The obj variable is used to store the position object
    obj = get_object_or_404(Position, pk = pos)

    # if statement is used to check if the request method is POST
    if request.method == "POST":

        # The temp variable is used to store the ControlVote object 
        # it is used to check if the user has already voted for the position
        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]

        # if statement is used to check if the user has already voted for the position
        if temp.status == False:

            # The temp2 variable is used to store the Candidate object
            # The total_vote of the candidate is incremented by 1
            # The status of the ControlVote object is changed to True
            # The user is redirected to the position page
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/position/')
        else:

            # if the user has already voted for the position then the user is redirected to the position page
            # and the error message is displayed
            messages.success(request, 'you have already been voted this position.')
            return render(request, 'poll/candidate.html', {'obj':obj})
    else:

        # if the request method is not POST then the render function is used to render the candidate page
        return render(request, 'poll/candidate.html', {'obj':obj})

# The resultView function is used to render the result page when the user visits the result page
@login_required
def resultView(request):

    # The obj variable is used to store the list of Candidate objects
    obj = Candidate.objects.all().order_by('position','-total_vote')

    # The render function is used to render the result page
    return render(request, "poll/result.html", {'obj':obj})

# The candidateDetailView function is used to render the candidate detail page when the user visits the candidate detail page
@login_required
def candidateDetailView(request, id):

    # The obj variable is used to store the Candidate object
    obj = get_object_or_404(Candidate, pk=id)

    # The render function is used to render the candidate detail page
    # obj is passed to the candidate detail page to display the details of the candidate
    return render(request, "poll/candidate_detail.html", {'obj':obj})

# The changePasswordView function is used to render the password page when the user visits the password page
@login_required
def changePasswordView(request):

    # if statement is used to check if the request method is POST
    if request.method == "POST":

        # The form variable is used to store the PasswordChangeForm
        form = PasswordChangeForm(user=request.user, data=request.POST)

        # check if the form is valid
        if form.is_valid():

            # User is saved and the session is updated
            form.save()
            update_session_auth_hash(request,form.user)

            # The user is redirected to the dashboard page
            return redirect('dashboard')
    else:

        # if the request method is not POST then the render function is used to render the password page
        form = PasswordChangeForm(user=request.user)

    # The render function is used to render the password page
    return render(request, "poll/password.html", {'form':form})

# The editProfileView function is used to render the edit profile page when the user visits the edit profile page
@login_required
def editProfileView(request):

    # Check if the request method is POST
    if request.method == "POST":

        # The form variable is used to store the ChangeForm
        form = ChangeForm(request.POST, instance=request.user)

        # Check if the form is valid
        if form.is_valid():

            # The user is saved and the user is redirected to the dashboard page
            form.save()
            return redirect('dashboard')
    else:

        # if the request method is not POST then the render function is used to render the edit profile page
        form = ChangeForm(instance=request.user)

    # The render function is used to render the edit profile page
    return render(request, "poll/edit_profile.html", {'form':form})
