from . import models
from posts.models import Post
from profiles.models import Subscribe
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    """
    Function for displaying the home page.
    """
    return render(request, 'main/home.html')


def about(request):
    """
    Function for displaying the “about us” page.
    """
    return render(request, 'main/about.html', {'workers': models.Worker.objects.all()})


def contact(request):
    """
    Function for displaying the “contacts” page.
    """
    return render(request, 'main/contact.html')


def subscriptions(request, page_number):
    """
    Function that allows users to view the posts of users they are subscribed to,
    all posts will be divided into pages, takes page_number(page number).
    """

    # If the user is authenticated and sends a GET request, perform the following actions.
    if request.user.is_authenticated and request.method == 'GET':


        # Constant for storing the number of posts on one page.
        POSTS_ON_PAGE = 15

        # Find out all of the user's subscriptions.
        user_subs = Subscribe.objects.filter(user_from=request.user)

        # Find out all users this user is subscribed to and add them to the list.
        followed_users = []
        for sub in user_subs:
            followed_users.append(sub.user_to)

        # We take the last 10 posts of all users this user is subscribed to and add them to the list.
        posts = []
        for user in followed_users:
            for post in Post.objects.filter(user=user).order_by('-date')[:10]:
                posts.append(post)
                

        # Create a paginator object and pass to it all posts and the number of posts on one page.
        paginator = Paginator(posts, POSTS_ON_PAGE)

        # Trying to get data on the page specified by the user.
        try:
            paginated_posts = paginator.page(page_number)

        # If the entered page number is not an integer, redirect to the first page.
        except PageNotAnInteger:
            paginated_posts = paginator.page(1)

        # If the entered page number is too large, return the last page.
        except EmptyPage:
            paginated_posts = paginator.page(paginator.num_pages)


        # Initialize the dictionary with all data and pass it to the template.
        data = {
            'posts': paginated_posts,
        }
        return render(request, 'main/subscriptions.html', data)
    
    # If the user is not authenticated or sends a non-GET request, we redirect him to the login page.
    return redirect('login')
