from django.shortcuts import render, redirect
from . import forms, models
from django.core.cache import cache 

def create_post(request):
    """
    Function that allows the user to publish posts.
    """
    # If a non-authenticated user tries to enter the page, redirect him to the login page.
    if not request.user.is_authenticated:
        return redirect('login')
    
    # If the request method is POST, fill in the forms.
    if request.method == 'POST':
        post_form = forms.CreatePostForm(request.POST, request.FILES)
        category_form = forms.CategoryForm(request.POST)

        # If the forms are valid, create a new post and bind to it the categories specified by the user.
        if post_form.is_valid() and category_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()

            # Binding categories to a post.
            for cat in category_form.cleaned_data['categories']:
                new_cat = models.Category_Of_Post(post=new_post, category=models.Category.objects.filter(name=cat).first())
                new_cat.save()

            # Redirect to the page of viewing all posts of the user.
            return redirect(f'/profile/{request.user.id}/posts/')

    # In a GET request, we initialize the dictionary with the required forms and pass it to the template.
    data = {
        'form': forms.CreatePostForm,
        'category_form': forms.CategoryForm
    }
    return render(request, 'posts/create_post.html', data)



def view_post(request, post_id):
    """
    Function that allows to view posts, takes post_id (unique post number),
    as well as allow you to write comments, put likes, and the owner of the post to delete comments.
    """
    # Looking for a post with this post_id.
    post = models.Post.objects.filter(id=post_id).first()

    # If such a post exists, proceed as follows.
    if post:

        # We create cache key.
        cache_key = f'post_view_{request.session.session_key}'

        # Register post view by user.
        # If this user has already viewed this post, delete the past entry.
        if request.user.is_authenticated:
            if (old_view := models.PostView.objects.filter(user=request.user, post=post)):
                old_view.delete()

            # Add a post page view record.
            new_view = models.PostView(user=request.user, post=post)
            new_view.save()

        # We don't know yet if this user liked this post or owns it.
        is_liked = False
        is_owner = False

        # If the request method is POST and the user is authenticated, perform the following actions.
        if request.method == 'POST' and request.user.is_authenticated:

            # If the user sent a POST request, we delete its cache, so that it will immediately see the changes, other users will see them only when they receive a new one. 
            cache.delete(cache_key)

            # Fill out the comment form, if it is valid, create a new comment and redirect the user to the page of the same post.
            comment_form = forms.CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = post
                new_comment.save()
                return redirect(f'/post/{post_id}/')

            # Fill out the likes form, if it turns out to be valid, check if this user has likes for this post, if it exists, delete it,
            # and if not, add it and forward it to the page of this post.
            like_form = forms.LikeForm(data=request.POST)
            if like_form.is_valid():
                if (likes := models.Like.objects.filter(user=request.user, post=post)):
                    likes.delete()
                    return redirect(f'/post/{post_id}/')
                new_like = like_form.save(commit=False)
                new_like.user = request.user
                new_like.post = post
                new_like.save()
                return redirect(f'/post/{post_id}/')
            
        # Search for information by this key, if information was found, we put it in the dictionary.
        cached_data = cache.get(cache_key)
        if cached_data:
            return render(request, 'posts/post.html', cached_data)
                
        # If the request method is GET and the user is authenticated, perform the following actions.
        if request.method == 'GET' and request.user.is_authenticated:

            # find out if this post has been liked by a user.
            if models.Like.objects.filter(user=request.user, post=post).exists():
                is_liked = True

            # find out if this user owns this post.
            if post.user.id == request.user.id:
                is_owner = True

        # Initialize the dictionary with all the necessary data and forms, and then pass it to the template.
        data = {
            'post': post,
            'is_liked': is_liked,
            'is_owner': is_owner,
            'comment_form': forms.CommentForm,
            'comments': models.Comment.objects.filter(post=post).order_by('-date'),
            'like_amount': models.Like.objects.filter(post=post).count(),
        }
        # if information wasn't found, we cache the result.
        cache.set(cache_key, data, timeout=600)

        return render(request, 'posts/post.html', data)
    
    # If no such post was found, we redirect to the home page.
    return redirect('home')



def delete_comment(request, post_id):
    """
    The function that allows you to delete comments accepts post_id (unique comment number),
    also checks whether the user who wants to delete a comment is the owner of the post under which the comment is written.
    """
    # If the user is authenticated and has sent a POST request, perform the following actions.
    if request.user.is_authenticated and request.method == 'POST':

        # If such a comment exists, and the user who wants to delete it has the right to do so, delete the comment and redirect it to the post page.
        comment = models.Comment.objects.filter(id=request.POST.get("comment_id")).first()
        if comment:
            if comment.post.user.id == request.user.id:
                comment.delete()

                # If a user deleted a comment under his/her post, we clear the cache so that the user can immediately see the changes.
                cache.delete(f'post_view_{request.session.session_key}')

                return redirect(f'/post/{post_id}/')
    
    # If something went wrong in the process, for example, the comment does not exist or the user does not have permission to delete it,
    # we redirect it to the home page.
    return redirect('home')



def delete_post(request, user_id):
    """
    The function that allows you to delete posts accepts user_id (unique user number),
    also checks whether the user who wants to delete a posts is the owner of the post.
    """
    # If the user is authenticated and has sent a POST request, perform the following actions.
    if request.user.is_authenticated and request.method == 'POST':

        # If such a post exists, and the user who wants to delete it has the right to do so, delete the post and redirect it to the posts page.
        post = models.Post.objects.filter(id=request.POST.get("post_id")).first()
        if post:
            if post.user.id == request.user.id:
                post.delete()
                return redirect(f'/profile/{user_id}/posts/')
    
    # If something went wrong in the process, for example, the post does not exist or the user does not have permission to delete it,
    # we redirect it to the home page.
    return redirect('home')