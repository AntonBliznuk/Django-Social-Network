from . import models
from posts.models import Post
from django.db.models import Q
from profiles.models import Subscribe
from django.shortcuts import render, redirect
from .SupportPrograms import recomendations
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    """
    This function shows the user's home page, where you can find recommendations based on the viewed posts of the user,
    if the user is not authorized or has not yet seen the posts, random posts are displayed,
    as well as the ability to search by post title and post text.
    """
    # If the user did not send a GET request, we redirect to the home page.
    if request.method != 'GET':
        return redirect('home')
    
    # Initialize the dictionary in which we will put all the necessary data,
    # as well as create a recommender object to create user recommendations.
    data = {}
    recomender = recomendations.Recomender()

    # If the user is not authenticated, we write random recommendations to the dictionary.
    if not request.user.is_authenticated:
        data['posts'] = recomender.random_rec()

    else: # If the user is authenticated, perform the following actions.

        # If we succeeded in personalizing recommendations, we pass them to the dictionary,
        # and if we failed we pass random recommendations.
        if (result := recomender.user_rec(request.user)):
            data['posts'] = result
        else:
            data['posts'] = recomender.random_rec()

    # If the user passed parameters for the search, we search for the necessary posts and pass them to the dictionary,
    # and if the user did not pass None to the dictionary.
    if (search := request.GET.get('search')):
        posts = Post.objects.all()
        search_results = posts.filter(Q(text__icontains=search) | Q(description__icontains=search))
        data['search_results'] = search_results
    else:
        data['search_results'] = None

    # Transfer all data to the template.
    return render(request, 'main/home.html', data)


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

        # Sorting posts by date.
        posts.sort(key=lambda x: x.date)
            
                
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
