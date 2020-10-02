from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q
from django_countries import countries
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    # request에서 가져오는 것
    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    # DB에서 가져오는 것
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    # city filter
    if city != "Anywhere":
        # startswith 옵셥
        filter_args["city__startswith"] = city

    # country filter
    filter_args["country"] = country

    # room_type filter
    if room_type != 0:
        # room_type는 RoomType의 pk를 받고 있고 Room에서 room_type은 fk를 통해 접근하고 있음
        filter_args["room_type__pk"] = room_type

    # price filter
    if price != 0:
        filter_args["price__lte"] = price

    # guests, bedrooms, beds, baths filter
    if guests != 0:
        filter_args["guests__gte"] = guests
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    if beds != 0:
        filter_args["beds__gte"] = beds
    if baths != 0:
        filter_args["baths__gte"] = baths

    # instant, superhost filter
    if instant is True:
        filter_args["instant_book"] = True
    if superhost is True:
        filter_args["host__superhost"] = True

    rooms = models.Room.objects.filter(**filter_args)

    if len(s_amenities) > 0:
        s_amenities_query = Q(amenities__pk=int(s_amenities[0]))
        for s_amenity in s_amenities[1:]:
            s_amenities_query |= Q(amenities__pk=int(s_amenity))
        rooms = rooms.filter(s_amenities_query).distinct()

    if len(s_facilities) > 0:
        s_facilities_query = Q(facilities__pk=int(s_facilities[0]))
        for s_facility in s_facilities[1:]:
            s_facilities_query |= Q(facilities__pk=int(s_facility))
        rooms = rooms.filter(s_facilities_query).distinct()

    return render(
        request,
        "rooms/search.html",
        context={
            **form,
            **choices,
            "rooms": rooms,
        },
    )
