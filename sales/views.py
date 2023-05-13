from collections import Counter

from django.db.models import Count, Sum
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from rest_framework.utils import json

from .models import *
from .serializers import SalesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class SalesList(APIView):

    def get(self, request, format=None):
        sale = salesdb.objects.all()
        serializer = SalesSerializer(sale, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesDetail(APIView):
    """

    """
    def get_object(self, id):
        try:
            return salesdb.objects.get(pk=id)
        except salesdb.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        sales = self.get_object(id)
        serializer = SalesSerializer(sales)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        sales = self.get_object(id)
        serializer = SalesSerializer(sales, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        sales = self.get_object(id)
        sales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SalesPdf(APIView):
    def post(self,request,):
        customers_count=salesdb.objects.values().aggregate(Count('customer_id', distinct=True))
        # print(customers_count['customer_id__count'])
        order_years= salesdb.objects.values().annotate(year=ExtractYear('order_date')).values('year').distinct()
        years = [obj['year'] for obj in order_years]
        # print(years)
        per_year_count=[]
        for year in years:
            orders_count = salesdb.objects.annotate(order_year=ExtractYear('order_date')).filter(order_year=year).count()
            # print(year,orders_count)
            per_year_count.append(f"{year}:{orders_count}")

        distinct_customers = salesdb.objects.values('customer_id').distinct()
        # print(distinct_customers.values('customer_id'))
        a=[]
        b=[]
        c=[]
        for c_id in distinct_customers:
            # print(c_id['customer_id'])
            total_sales = salesdb.objects.filter(customer_id=c_id['customer_id']).aggregate(sales_sum=Sum('sales'))['sales_sum']
            a.append(c_id['customer_id'])
            b.append(total_sales)
        test_keys = a
        test_values = b

        tuples = [(key, value)
                  for i, (key, value) in enumerate(zip(test_keys, test_values))]

        # convert list of tuples to dictionary using dict()
        res = dict(tuples)

        print(res)

        my_dict = res

        print("Initial Dictionary:")
        print(my_dict, "\n")

        print("Dictionary with 3 highest values:")
        print("Keys: Values")

        x = list(my_dict.values())
        d = dict()
        e=[]
        x.sort(reverse=True)
        x = x[:3]
        for i in x:
            for j in my_dict.keys():
                if (my_dict[j] == i):
                    print(str(j) + " : " + str(my_dict[j]))
                    e.append(f"{j}:{my_dict[j]}")

        value={
            "Total number of orders count per year":per_year_count,
            "Total count of distinct customers":customers_count['customer_id__count'],
            'Top 3 customers who have ordered the most with their total amount of transactions':e

        }

        return Response(json.dumps(value))





