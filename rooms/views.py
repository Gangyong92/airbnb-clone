from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms
from users import mixins as user_mixins


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

    # 이전 페이지 값을 현재 페이지에서 유지하기 위해 사용.
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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["name"].widget.attrs = {
            "class": "form-input",
        }
        form.fields["city"].widget.attrs = {
            "class": "form-input",
        }
        form.fields["price"].widget.attrs = {
            "class": "form-input",
        }
        form.fields["address"].widget.attrs = {
            "class": "form-input",
        }

        form.fields["guests"].widget.attrs = {
            "class": "form-input",
        }
        form.fields["beds"].widget.attrs = {
            "class": "form-input",
        }
        form.fields["bedrooms"].widget.attrs = {
            "class": "form-input",
        }
        form.fields["baths"].widget.attrs = {
            "class": "form-input",
        }

        form.fields["check_in"].widget.attrs = {
            "placeholder": "HH:MM:SS",
            "class": "form-input",
        }
        form.fields["check_out"].widget.attrs = {
            "placeholder": "HH:MM:SS",
            "class": "form-input",
        }

        return form


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photos(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    # urls에서 pk로 안줌.
    # Photo의 field를 띄우고 싶음. 우리가 필요한건 photo_pk임
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["caption"].widget.attrs = {
            "class": "form-input",
        }
        return form

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    # AddPhotoView와 다르게 해봤음. Form 단에서 세팅하는게 아닌
    # View단에서 세팅(view에서 redirect 할 때 room.pk가 필요해서)
    # 물론 form에서 내보낼 수도 있겠지만 그렇게 하지 않음
    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, "Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
