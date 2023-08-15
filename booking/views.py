from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf  import settings
from decouple import config

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


class BookingCheckoutSession(APIView):
    def post(self, request):
        price = int(request.data.get('price')) *100
        task_title = request.data.get('task')
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items = [{
                    'price_data' : {
                        'currency' : 'INR',
                        'product_data' : {
                            'name' : task_title
                        },
                        'unit_amount' : price
                    },
                    'quantity' : 1
                }],
                mode = 'payment',
                success_url = config('BaseUrl'),
                cancel_url = config('BaseUrl')
            )
            return Response(data=checkout_session.url, status=status.HTTP_303_SEE_OTHER)
        except Exception as e:
            print(e)
            return Response(data={'message': 'Oops!Some error occured'})
