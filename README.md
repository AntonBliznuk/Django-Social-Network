
![Django Social Network Logo](images_readme/logo.jpg)

**Django Social Network** - lightweight and feature-rich social network built with Django. It allows users to register, create and publish posts, explore posts from other users, like and comment on posts, follow other users, view detailed user profiles, and enjoy personalized post recommendations based on their activity.

---
## **Scheme of work**
![scheme](images_readme/scheme.jpg)
### Scheme Description:
1. **Users** - send requests to the application.
2. **Application** - accepts requests and performs actions.
	**Posts** - responsible for post logic(create, view, delete, comments, likes, categories).
	**Main** -  responsible for the recommendation system and search for posts, as well as displaying informative pages.
	**Profiles** - responsible for the logic of user profiles (registration, login, logout, profile view, subscriptions).
3. **Redis** - data caching to reduce load.
4. **PostgeSQL** - storage of all data (users, posts), as well as links to photos in cloudinary.
5. **Cloudinary** - storing all images.

---
## Additional information:
- **Performance** - The whole application is fully deployed on Render using free plans, but because of this the speed of responses is not the best. Any query to the database takes at least 1 second, but if you run the application locally (with a local database) or with at least the cheapest plan everything will work quite fast. 
- **Appearance** - I don't do front-end development and am not very good at HTML and CSS so the look may not be the best, the application mostly shows the back-end. But if you want to improve the appearance, contact me.

---
## **Technology:**
- **Backend**: Django  
- **Database**: PostgreSQL  
- **Caching**: Redis  
- **Image Storage**: Cloudinary  
- **Deployment**: Render, Docker  
- **API integrations**: Cloudinary

---
### **Contacts**
If you have any questions or suggestions, email me:

📧 **Email**: bliznukantonmain@gmail.com
