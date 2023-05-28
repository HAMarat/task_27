import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location
from task_27 import settings


class UserListView(ListView):
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("first_name")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        response = []

        for user in page_obj:
            response.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "location": [loc.name for loc in user.location.all()],
                "total_ads": user.total_ads
            })

        result = {
            "items": response,
            "num_page": page_number,
            "total": paginator.count
        }

        return JsonResponse(result, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "location": [loc.name for loc in user.location.all()]
        },
            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        locations = user_data.pop("location")

        user = User.objects.create(**user_data)
        for loc_name in locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.location.add(loc)
        user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "location": [loc.name for loc in user.location.all()]
        },
            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        if "first_name" in user_data:
            self.object.first_name = user_data["first_name"]
        if "last_name" in user_data:
            self.object.last_name = user_data["last_name"]
        if "username" in user_data:
            self.object.username = user_data["username"]
        if "password" in user_data:
            self.object.password = user_data["password"]
        if "role" in user_data:
            self.object.role = user_data["role"]
        if "age" in user_data:
            self.object.age = user_data["age"]
        if "location" in user_data:
            self.object.location.clear()
            for loc_name in user_data["location"]:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "location": [loc.name for loc in self.object.location.all()]
        },
            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = 'users/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})
