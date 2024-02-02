from django.shortcuts import render, redirect
from .models import admin_user,regular_user, Category, BlogPost, Search, Item, Review
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import ReviewForm
from actions.models import Action

#home page view is used to render the home page
def home_page(request):
    return render(request, 'tripobeatApp/travel/index.html')

#alternate page view is used to render the home page after user is logged in
def alternate_page(request):
    searches = Search.objects.all()
    actions = Action.objects.all().order_by('-created')
    print(actions)
    return render(request, 'tripobeatApp/travel/alternate.html', {"searches": searches, "actions": actions})

#blog page view is used to render the blog page.
def blog_page(request):
    return render(request, 'tripobeatApp/travel/blog.html')

def get_other_blogs(request):
    blogs = BlogPost.objects.all()
    blog_data = [{'title': blog.title, 'description': blog.description} for blog in blogs]
    print(blog_data)
    return JsonResponse({'blogs': blog_data})

#category page view is used to render the list view of itineraries
def category_page(request):
    categories = Category.objects.all().order_by("id")
    return render(request, 'tripobeatApp/travel/category.html', {"categories": categories})

#item page view displays a single selected itineraries from a list of itineraries
def item_page(request, itinerary_id):
    itinerary = get_object_or_404(Category, id=itinerary_id)
    reviews = list(Review.objects.filter(item=itinerary_id).order_by('-date_posted'))
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        review = Review.objects.create(name=user, title=title, description=description, item=itinerary)
        review_title = review.title
        try:
            reviews.append(review)
            action = Action(
                user=user,
                verb="has created a review named " + review_title + " for the product",
                target=itinerary
            )
            action.save()
        except Category.DoesNotExist:
            pass
    reviews = Review.objects.filter(item = itinerary_id).order_by('-date_posted')
    return render(request, 'tripobeatApp/travel/item.html', {"items": itinerary, "reviews": reviews})

def edit_review(request, review_id, itinerary_id):
    review = get_object_or_404(Review, id=review_id)
    itinerary_name = Category.objects.get(id=itinerary_id)
    user = User.objects.get(username=request.session.get('username'))
    review_title = review.title
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            action = Action(
                user=user,
                verb="has edited review with title: " + review.title + " for product:",
                target=review
            )
            action.save()
            return redirect('tripobeatApp:item_page', itinerary_id=review.item.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, "tripobeatApp/travel/edit_review.html", {"form": form, "review": review})


def delete_review(request, review_id, itinerary_id):
    review = get_object_or_404(Review, id=review_id)
    itinerary_name = Category.objects.get(id=itinerary_id)
    review_title = review.title
    print(review_title)
    user = User.objects.get(username=request.session.get('username'))
    if request.session.get('username') == review.name.username or request.session.get('access') == 'admin':
        print(review_title)
        action = Action(
            user=user,
            verb="has deleted review: " + review_title,
            target=review
        )
        action.save()
        review.delete()
    number_of_objects = Review.objects.count()
    if number_of_objects == 0:
        return JsonResponse({'success': True, 'deleted_review_id': review_id, 'no_reviews': 0})
    return JsonResponse({'success': True, 'deleted_review_id': review_id})


#search result view is to display the simulated search feature
def search_result(request):
    text_input = request.GET.get('text-input', '').lower()
    if text_input == 'blacksburg':
        return render(request, 'tripobeatApp/travel/category.html', {"categories": categories})
    else:
        return render(request, 'tripobeatApp/travel/search_result.html', {"title": text_input})

#add category view is to demonstrate add view functionality
def add_category(request):
    if request.method == 'POST':
        place_name = request.POST['place_name']
        description = request.POST['description']
        days_price = request.POST['days_price']
        image_url = request.FILES['image_url'] if 'image_url' in request.FILES else None
        departure_details = request.POST['departure_details']
        exclusions_string = request.POST['exclusion']
        return_details = request.POST['return_details']
        #exclusions_string = "Lunch & Dinner, Anything not mentioned in the Inclusions"
        inclusions_string = request.POST['inclusion']
        access_string = request.POST['access']
        cancel_string = request.POST['cancel']
        user = User.objects.get(username=request.session.get('username'))
        new_category = Category(
            title=place_name,
            description=description,
            cost=days_price,
            image_url=image_url,
            author = request.session.get('username'),
            departure_details = departure_details,
            return_details = return_details,
            inclusions = inclusions_string,
            exclusions = exclusions_string,
            access = access_string,
            cancel = cancel_string,
        )
        title_save = new_category.title
        if image_url:
            new_category.image_url = image_url

        new_category.save()
        action = Action(
            user=user,
            verb=f"has created a new Itinerary named- '{title_save}': Link- ",
            target=new_category
        )
        action.save()
        messages.add_message(request, messages.SUCCESS, "You have added new itinerary successfully: %s" % new_category.title)
        return redirect('tripobeatApp:item_page', itinerary_id = new_category.id)
    categories= Category.objects.all()
    print(place_name, description, days_price, image_url, departure_details, return_details, inclusion, exclusion,
          access, cancel)
    return render(request, 'tripobeatApp/travel/category.html', {'categories': categories})

#edit category view is to demonstrate edit view functionality
def edit_category(request, itinerary_id):
    user = User.objects.get(username=request.session.get('username'))
    category = Category.objects.get(id=itinerary_id)
    if request.method == 'POST':
        old_name = category.title
        old_description = category.description
        category.title = request.POST.get('title')
        category.description = request.POST.get('description');
        category.cost = request.POST.get('cost');
        category.departure_details = request.POST['departure_details']
        category.exclusions = request.POST['exclusion']
        category.return_details = request.POST['return_details']
        # exclusions_string = "Lunch & Dinner, Anything not mentioned in the Inclusions"
        category.inclusions = request.POST['inclusion']
        category.access = request.POST['access']
        category.cancel = request.POST['cancel']
        if old_name != category.title:
            action_name = f"has edited the title from '{old_name}' to '{category.title}'- Link: "
        else:
            action_name = None
        if old_description != category.description:
            action_description = f"has edited the description from '{old_description}' to '{category.description}'- Link:"
        else:
            action_description = None
        category.save()
        if action_name:
            action_title_instance = Action(
                user=user,
                verb=action_name,
                target=category
            )
            action_title_instance.save()
        if action_description:
            action_price_instance = Action(
                user=user,
                verb=action_description,
                target=category
            )
            action_price_instance.save()
        messages.add_message(request, messages.INFO, "You have edited an itinerary: %s" % old_name)
        redirect_url = reverse('tripobeatApp:item_page', kwargs={'itinerary_id': itinerary_id})
        return HttpResponseRedirect(redirect_url)
    return render(request, 'tripobeatApp/travel/edit_item.html', {'category': category})

#delete category view is to demonstrate delete view functionality
def delete_category(request, itinerary_id):
    user = User.objects.get(username=request.session.get('username'))
    place = Category.objects.get(id = itinerary_id)
    action = Action(
        user=user,
        verb="has deleted the Itinerary:" + place.title,
        target=place
    )
    action.save()
    place.delete()
    messages.add_message(request, messages.WARNING, "You have deleted the itinerary: %s" % place.title)
    return redirect('tripobeatApp:category_page')

def add_item_page(request):
    return render(request, 'tripobeatApp/travel/add_item.html')


