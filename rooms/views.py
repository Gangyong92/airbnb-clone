from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")

        if country:
            # 어떤 데이터를 가지고 있음. 무슨 데이터인지는 아직 모름
            form = forms.SearchForm(request.GET)

            # is_valid()에서 데이터를 확인하는 일들이 일어남.
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                # cleaned_data가 알아서 잘 정리해줘서 pk 필요 없음.
                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                # 앞서 했던 필터와 다르게 cleaned_data가 알아서 데이터를 정리해줘서 pk를 안씀
                if len(amenities) > 0:
                    amenities_query = Q(amenities=amenities[0])
                    for amenity in amenities[1:]:
                        amenities_query |= Q(amenities=amenity)
                    qs = qs.filter(amenities_query).distinct()

                if len(facilities) > 0:
                    facilities_query = Q(facilities=facilities[0])
                    for facility in facilities[1:]:
                        facilities_query |= Q(facilities=facility)
                    qs = qs.filter(facilities_query).distinct()

                page = request.GET.get("page")

                paginator = Paginator(qs, 1)

                rooms = paginator.get_page(page)

                # 삭제 필요한 page query 문자열 생성
                remove_page_url = f"&page={page}"
                query_url = request.get_full_path()[len("/rooms/search/?") :]
                query_url = query_url.replace(remove_page_url, "")

                return render(
                    request,
                    "rooms/search.html",
                    context={
                        "form": form,
                        "rooms": rooms,
                        "query_url": query_url,
                    },
                )
        else:
            form = forms.SearchForm()

        return render(
            request,
            "rooms/search.html",
            context={"form": form},
        )
