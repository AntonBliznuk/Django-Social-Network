from . import forms
from . import models
from posts.models import Like, Post, PostView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache 


def profile_page(request, user_id):
    """
    Function for displaying user profiles If a user views his/her profile, he/her has the right to edit it.
    It accepts user_id argument (unique user number).
    """
    user = models.CustomUser.objects.filter(id=user_id).first() # Get user object (page owner).
    if user: # If such a user exists.

        # Counting all of the user's likes.
        all_user_posts = Post.objects.all()
        likes_amount = 0
        for post in all_user_posts:
            likes_amount += Like.objects.filter(post=post).count()

        # Counting all of the user's follows.
        follow_amount = models.Subscribe.objects.filter(user_to=user).count()

        # Initialize the dictionary that will be passed to the template.
        data = {
            'user': user,
            'likes_amount': likes_amount,
            'follow_amount': follow_amount,
        }

        # Find out if the user is subscribed to this user, pass the data to the dictionary.
        if (sub_obj := models.Subscribe.objects.filter(user_to=user, user_from=request.user).first()):
            data['is_sub'] = True
            data['sub_obj'] = sub_obj


        if request.user.is_authenticated: # If the user is authenticated.

            # If the request method is POST and the user accesses his page, change his/her data to the data from the request.
            if request.method == "POST" and request.user.id == user_id:
                form_image = forms.UploadUserImage(request.POST, request.FILES, instance=user)
                if form_image.is_valid():
                    form_image.save()

                form_user_name = forms.UploadUserName(request.POST, instance=user)
                if form_user_name.is_valid():
                    form_user_name.save()
                
                return redirect(f'/profile/{user_id}/')
            

            # If the query method is POST and the user is accessing someone else's page, then the user has clicked the “Subscribe” button.
            elif request.method == 'POST':
                cache.delete(f'user_subscriptions_{request.user.id}')

                this_user_subs = models.Subscribe.objects.filter(user_from=request.user, user_to=user)
                if this_user_subs:
                    this_user_subs.delete()
                    return redirect(f'/profile/{user_id}/')
                new_sub = models.Subscribe(user_from=request.user, user_to=user)
                new_sub.save()
                return redirect(f'/profile/{user_id}/')


            # If the request method is GET and the user accesses his/her page, add new values to the dictionary.
            elif request.method == "GET" and request.user.id == user_id:
                data['is_owner'] = True
                data['image_form'] = forms.UploadUserImage
                data['user_name_form'] = forms.UploadUserName


        # Display a page with all the data from the dictionary.
        return render(request, 'profiles/profile.html', data)
    
    # If no such user exists, redirect to the home page
    return redirect('home')



def user_subscriptions(request, user_id):
    """
    The function passes all user subscriptions to the template, accepts user_id(unique user number),
    if there is no such user, redirects to the home page.
    """
    # Looking for a user with this user_id.

    cache_key = f'user_subscriptions_{request.user.id}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return render(request, 'profiles/subscriptions.html', cached_data)

    user = models.CustomUser.objects.filter(id=user_id).first()
    if user:

        # Find out if a user is viewing his/her subscription page.
        is_owner = False
        if request.user.id == user.id:
            is_owner = True

        # Initialize the dictionary that we pass to the template.
        data = {
            'subscriptions': models.Subscribe.objects.filter(user_from=user).order_by('-date'),
            'is_owner': is_owner,
        }

        cache.set(cache_key, data, timeout=1000)
        return render(request, 'profiles/subscriptions.html', data)
    
    # If the user with this user_id does not exist, redirect to the home page.
    return redirect('home')



def delete_user_subscriptions(request, user_id):
    """
    A feature that allows users to unsubscribe from other users. Accepts user_id(unique user number),
    if no such user or subscription exists, redirects to the home page.
    """
    # Search for such a user and check the necessary information.
    user = models.CustomUser.objects.filter(id=user_id).first()
    if user and request.user.is_authenticated and request.method == 'POST':

        # Search for the user's subscription, delete the subscription, redirect to the specified link.
        sub = models.Subscribe.objects.filter(id=request.POST.get("sub_id")).first()
        if sub:
            if sub.user_from == request.user:
                sub.delete()
                cache.delete(f'user_subscriptions_{request.user.id}')
                return redirect(request.POST.get('redirect_link'))

    # If errors occur during the process, redirect to the home page.
    return redirect('home')




def user_posts(request, user_id):
    """
    The function passes all user posts to the template, accepts user_id(unique user number),
    if there is no such user, redirects to the home page.
    """
    # Looking for a user with this user_id.
    user = models.CustomUser.objects.filter(id=user_id).first()
    if user:

        # Find out if a user is viewing his/her posts page.
        is_owner = False
        if request.user.id == user.id:
            is_owner = True

        # Initialize the dictionary that we pass to the template.
        data = {
            'posts': Post.objects.filter(user=user).order_by('-date'),
            'is_owner': is_owner
        }
        return render(request, 'profiles/posts.html', data)
    
    # If the user with this user_id does not exist, redirect to the home page.
    return redirect('home')



def register(request):
    """
    Function for user registration, depending on the request method either shows the form or registers the user.
    """
    # If an authenticated user tries to register, he/her is redirected to the home page.
    if request.user.is_authenticated:
        return redirect('home')
    
    # If the user is not logged in and sends a POST request, we register him/her and log him/her in.
    elif request.method == 'POST':
        form = forms.RegisterForm(data=request.POST)
        if form.is_valid(): # Form verification.

            # register.
            new_user = models.CustomUser(username=form.cleaned_data['username'])
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            # log in.
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            # redirect to the home page.
            return redirect('home')
        
        else: # If the user has entered incorrect data, we output the form with errors.
            return render(request, 'profiles/register.html', {'form': form})

    # If the user is not logged in and has sent a GET request, the registration form is returned.
    return render(request, 'profiles/register.html', {'form': forms.RegisterForm})



def login_page(request):
    """
    Function for user login, depending on the request method either shows the form or allows the user to log in.
    """
    # If an authenticated user tries to log in, he/her is redirected to the home page.
    if request.user.is_authenticated:
        return redirect('home')
    
    # If the user is not logged in and sends a POST request, we log him/her in.
    elif request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid(): # Form verification.
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password']) # Authentication.

            if user: # log in and redirect to the home page.
                login(request, user)
                return redirect('home')
            
            else: # If the user with this data does not exist, add an error to the form.
                form.add_error('username','Wrong username or password!')

        # If errors occurred while processing the form, return the form with errors.
        return render(request, 'profiles/login.html', {'form': form})
        
    # If the user is not logged in and has sent a GET request, the log in form is returned.
    return render(request, 'profiles/login.html', {'form': forms.LoginForm})



def logout_page(request):
    """
    Function for logging users out of the account.
    """
    logout(request) # logout.
    return redirect('home') # redirect to the home page.



def user_subscribers(request, user_id):
    """
    Function for viewing the user's subscribers.
    """
    # Looking for a user with this user_id.
    user = models.CustomUser.objects.filter(id=user_id).first()
    if user:

        # Initialize the dictionary that we pass to the template.
        data = {
            'subscriptions': models.Subscribe.objects.filter(user_to=user).order_by('-date'),
        }
        return render(request, 'profiles/subscribers.html', data)
    
    # If the user with this user_id does not exist, redirect to the home page.
    return redirect('home')



def user_history(request, user_id, page_number):
    """
    A function that shows the history of the user's viewed posts and breaks the viewed posts into pages.
    Accepts: user_id(Unique user number), page_number(page number).
    """
    # Looking for a user with this user_id.
    user = models.CustomUser.objects.filter(id=user_id).first()

    # If such a user exists and accesses his/her page and the request method is GET, perform the following action.
    if user and request.user.id == user.id and request.method == 'GET':

        # Constant for selecting the number of posts on one page.
        VIEWS_ON_PAGE = 10

        # We take all the user's views and sort them by date.
        viewed_posts = PostView.objects.filter(user=user).order_by('-date')

        # Create a paginator object.
        paginator = Paginator(viewed_posts, VIEWS_ON_PAGE)

        # Trying to get data on the page specified by the user.
        try:
            paginated_views = paginator.page(page_number)

        # If the entered page number is not an integer, redirect to the first page.
        except PageNotAnInteger:
            paginated_views = paginator.page(1)

        # If the entered page number is too large, return the last page.
        except EmptyPage:
            paginated_views = paginator.page(paginator.num_pages)


        # Initialize the dictionary that we pass to the template.
        data = {
            'viewed_posts': paginated_views 
        }
        return render(request, 'profiles/history.html', data)
    
    # If such a user exists and accesses his/her page and the request method is POST, perform the following action.
    elif user and request.user.id == user.id and request.method == 'POST':

        # Delete all the user's views and redirect the user to the first page.
        history = PostView.objects.filter(user=request.user)
        history.delete()
        return redirect(f'/profile/{user_id}/history/page/1/')

    
    # If the user with this user_id does not exist, redirect to the home page.
    return redirect('home')



def delete_user_view(request, user_id):
    """
    A feature that allows you to delete a specific view of a specific post from a specific user.
    Accepts: user_id(Unique user number).
    """
    # Looking for a user with this user_id.
    user = models.CustomUser.objects.filter(id=user_id).first()

    # If such a user exists and tries to delete his/her view and POST request method, perform the following actions.
    if user and user.id == request.user.id and request.method == 'POST':
        
        # Find user's view using view_id(unique view number) from POST request, if such view exists,
        # delete it and redirect user to the page that was specified in POST request.
        view = PostView.objects.filter(id=request.POST.get('view_id')).first()
        if view:
            view.delete()
            return redirect(request.POST.get('redirect_link'))
        
    # If something goes wrong in the process, redirect the user to the home page. 
    return redirect('home')
