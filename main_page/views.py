import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from main_page.models import Ad, Category


@method_decorator(csrf_exempt, name='dispatch')
class StartPageView(View):
    def get(self, response):
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        ads = Ad.objects.all()
        response = []
        for ad in ads:
            response.append({
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'address': ad.address,
                'is_published': ad.is_published,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(**data)

        return JsonResponse({
                'id': new_ad.id,
                'name': new_ad.name,
                'author': new_ad.author,
                'price': new_ad.price,
                'description': new_ad.description,
                'address': new_ad.address,
                'is_published': new_ad.is_published,
            }, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'address': ad.address,
                'is_published': ad.is_published,
            }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(View):
    def get(self, request):
        cats = Category.objects.all()
        response = []
        for cat in cats:
            response.append({
                'name': cat.name,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_cat = Category.objects.create(
                name=data.get('name')
            )

        return JsonResponse({
                'id': new_cat.id,
                'name': new_cat.name
            }, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
                'id': cat.id,
                'name': cat.name
            }, safe=False)
