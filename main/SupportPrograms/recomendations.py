import random
from posts.models import Category, Category_Of_Post, PostView


class Recomender():
    """
    The class provides the opportunity to receive recommendations in a variety of ways.
    """

    def random_rec(self):
        """
        The method selects random posts. In this way: selects 5 random categories,
        then five random links between a post and a particular category,
        mixes everything up and returns it to the user.
        """

        # Get a list of all categories.
        all_cat = list(Category.objects.all())

        # Choose 5 random categories.
        rand_cat = []
        random.shuffle(all_cat)
        for i in range(0, 5):
            rand_cat.append(all_cat[i])

        # We pick 5 random posts for each selected category.
        posts = []
        for cat in rand_cat:
            category_of_posts = list(Category_Of_Post.objects.filter(category=cat))
            random.shuffle(category_of_posts)

            for p_cat in category_of_posts[:5]:
                posts.append(p_cat.post)

        # We rearrange everything again and return the result.
        random.shuffle(posts)
        return posts 


    def user_rec(self, user):
        """
        The method selects personalized recommendations for the user based on the posts they have viewed.
        Accepts user object. Returns 10 personalized posts.
        """
        
        # Constant for selecting the number of recent posts on which recommendations will be based.
        NUMBER_OF_RECENT_POSTS = 10
        # Constant for selecting the number of posts that will be recommended.
        AMOUNT_OF_RECOMENDED_POSTS = 10


        # Get the 10 most recently viewed posts by a particular user.
        views = PostView.objects.filter(user=user)[:NUMBER_OF_RECENT_POSTS]
        viewed_posts = [i.post for i in views]

        # If no viewed posts could be found, return None.
        if viewed_posts == []:
            return None
        
        # Get objects of post categories viewed by the user.
        categories_of_viewed_posts = []
        for post in viewed_posts:
            cat_of_viewed_posts = list(Category_Of_Post.objects.filter(post=post))

            for cat in cat_of_viewed_posts:
                categories_of_viewed_posts.append(cat.category)

        # Count the number of times a category has been encountered in a user's views.
        count_cat = {}
        for cat in categories_of_viewed_posts:
            if cat in count_cat:
                count_cat[cat] += 1
            else:
                count_cat[cat] = 1

        # We start counting how many places a particular category should rank among the result.
        # To do this, we're going to need:

        # Calculates the total amount of views of all categories.
        whole_sum = 0
        for v in count_cat.values():
            whole_sum += v

        # Calculate what percentage a category will take up as a result.
        percents_cat = {}
        for k, v in count_cat.items():
            percents_cat[k] = (v / whole_sum) * 100

        # Calculate how many posts will be allocated to a category.
        amount_post_for_cat = {}
        for k, v in percents_cat.items():
            amount_post_for_cat[k] = int(AMOUNT_OF_RECOMENDED_POSTS * (v / 100))

        # Initialize the list and add posts with the required categories to it in the required number of posts.
        result = []
        for k, v in amount_post_for_cat.items():
            cat_of_posts = list(Category_Of_Post.objects.filter(category=k))
            random.shuffle(cat_of_posts)

            # Create a list for posts, select posts by specific categories, but only from other users,
            # the user who made the request will not see their posts in the recommendations.
            posts = []
            for i in range(0, len(cat_of_posts)):
                if cat_of_posts[i].post.user != user:
                    if len(posts) < v:
                        posts.append(cat_of_posts[i].post)
                    else:
                        break
                else:
                    i -= 1
                    
            # Add the selected posts to all other posts.
            for p in posts:
                result.append(p)

        # Return the result.
        return result
