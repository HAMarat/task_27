import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView

from ads.models import Ad, Category, User
from ads.serializers import AdSerializer


class StartPageView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "ok"})


class AdsListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
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

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, username=ad_data.pop('author'))
        category = get_object_or_404(Category, name=ad_data.pop('category'))

        ad = Ad.objects.create(author=author, category=category, **ad_data)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.username,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published,
            'category': ad.category.name
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        if "name" in ad_data:
            self.object.name = ad_data["name"]
        if "author" in ad_data:
            self.object.author = get_object_or_404(User, username=ad_data.pop('author'))
        if "price" in ad_data:
            self.object.price = ad_data["price"]
        if "description" in ad_data:
            self.object.description = ad_data["description"]
        if "address" in ad_data:
            self.object.address = ad_data["address"]
        if "is_published" in ad_data:
            self.object.is_published = ad_data["is_published"]
        if "image" in ad_data:
            self.object.image = ad_data["image"]
        if "category" in ad_data:
            self.object.category = get_object_or_404(Category, name=ad_data.pop('category'))

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


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


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
