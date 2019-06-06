from django.http import QueryDict
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas_datareader.data as web
import datetime
import time
from . import port_fin
import datetime
from . import models
from . import serializers

# Create your views here.


# return a list of stocks
class ListStock(generics.ListCreateAPIView):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer


# return a list of stock the current user own
class ListUserInvest(generics.ListCreateAPIView):
    serializer_class = serializers.InvestSerializer

    def get_queryset(self):
        return models.Invest.objects.filter(user=self.request.user)


# create a new invest record
class CreateInvest(generics.CreateAPIView):
    queryset = models.Invest.objects.all()
    serializer_class = serializers.InvestSerializerCreate

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data.update({'user': self.request.user.pk})
        # create the stock if it is not in our stock Model
        if not models.Stock.objects.filter(ticker=request.data['ticker']).exists():
            models.Stock.objects.create(ticker=request.data['ticker'], name="", price=10.0)
        print(request.data)
        return super(CreateInvest, self).create(request, *args, **kwargs)


# delete the previous portfolio
class RemoveUserInvest(generics.DestroyAPIView):
    serializer_class = serializers.InvestSerializer

    def get_queryset(self):
        return models.Invest.objects.filter(user=self.request.user)

    def delete(self, request):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# handle the user input and run MPT.
class ReceiveStock(APIView):

    def post(self, request):
        print(request.data)
        request.data._mutable = True
        count = 0
        stocks = []
        # Filter the user input
        for key, val in request.data.items():
            if key == 'val':
                continue
            if not val:
                request.data[key] = 'null'
                continue
            if self._check_stock(val):
                stocks.append(val)
            else:
                count += 1
        # not enough valid input
        if len(stocks) < 2:
            error_qdict = QueryDict('', mutable=True)
            error_dict = {}
            error_dict["input error"] = "not enough valid tickers"
            error_qdict.update(error_dict)
            print(error_qdict)
            return Response(error_qdict, status=status.HTTP_406_NOT_ACCEPTABLE)
        # data used for MPT
        start = '2018-01-01'
        end = '2019-01-01'
        # default risk preference
        risk_a = 5.5
        # multi-thread
        processer = 4
        user_port = port_fin.Portfolio(stocks, start, end, risk_a, processer, self.request.user.pk)
        user_port.get_data()
        result = user_port.plo(1, 4000)
        print(result)
        print(count)
        request.data['user'] = self.request.user.pk
        serializer = serializers.ReceiveSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            print(serializer.data)
            ans_qdict = QueryDict('', mutable=True)
            ans_dict = {}
            for i, stock in enumerate(stocks):
                ans_dict[stock] = result[0][i]
            ans_dict['user'] = self.request.user.pk
            ans_qdict.update(ans_dict)
            return Response(ans_qdict, status=status.HTTP_202_ACCEPTED)

    # check the sticker is valid or not
    @staticmethod
    def _check_stock(ticker):
        req = None
        num = 0
        end= datetime.date.today()
        start = end - datetime.timedelta(days=7)
        while req is None:
            try:
                stock_data = web.DataReader(
                    ticker, 'yahoo', start=start, end=end)
                print(stock_data)
                return True
            except :
                # It automatically
                print('Data request failed, trying again..')
                time.sleep(3)
                num += 1
                if num == 5:
                    return False
