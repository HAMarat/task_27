import json

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, Selection
from ads.permissions import IsOwner, IsStaff
from ads.serializers import AdSerializer, SelectionSerializer, SelectionDetailSerializer, \
    SelectionListSerializer, SelectionCreateUpdateSerializer, AdCreateSerializer


class StartPageView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "ok"})


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()

    default_serializer = AdSerializer
    serializers = {
        "create": AdCreateSerializer,
    }

    default_permission = [AllowAny]
    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsStaff],
        "partial_update": [IsAuthenticated, IsOwner | IsStaff],
        "destroy": [IsAuthenticated, IsOwner | IsStaff]
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        cat = request.GET.get("cat", None)
        if cat:
            self.queryset = self.queryset.filter(category__in=cat)

        text = request.GET.get("text", None)
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location", None)
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from", None)
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to", None)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'address': self.object.address,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image.url else None,
            'category': self.object.category.name
        }, safe=False)


class CategoriesListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        response = []
        for cat in self.object_list:
            response.append({
                'id': cat.id,
                'name': cat.name,
            })

        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
            'id': cat.id,
            'name': cat.name
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Category.objects.create(name=category_data["name"])

        return JsonResponse({
            'id': category.id,
            'name': category.name,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"]

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = 'cat/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()

    default_serializer = SelectionSerializer
    serializers = {
        "list": SelectionListSerializer,
        "retrieve": SelectionDetailSerializer,
        "create": SelectionCreateUpdateSerializer,
        "update": SelectionCreateUpdateSerializer,
        "partial_update": SelectionCreateUpdateSerializer,
    }

    default_permission = [AllowAny]
    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner],
        "partial_update": [IsAuthenticated, IsOwner],
        "destroy": [IsAuthenticated, IsOwner],
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)
