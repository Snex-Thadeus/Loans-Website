from mpesa.api.serializers import LNMOnlineSerializer
from mpesa.models import LNMLoan
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMLoan.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        # print(request.data, "This is requested data")

        merchant_request_id = request.data['Body']['stkCallback']['MerchantRequestID']
        checkout_request_id = request.data['Body']['stkCallback']['CheckoutRequestID']
        result_code = request.data['Body']['stkCallback']['ResultCode']
        result_desc = request.data['Body']['stkCallback']['ResultDesc']
        amount = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        mpesa_receipt_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        transaction_date = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value']
        phone_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        balance = " "

        from datetime import datetime

        str_transaction_date = str(transaction_date)

        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S") 
        import pytz
        aware_transaction_datetime = pytz.utc.localize(transaction_date)

        from website.models import LNMLoan

        our_model = LNMLoan.objects.create(
            MerchantRequestID = merchant_request_id,
            CheckoutRequestID = checkout_request_id,
            Amount = amount,
            MpesaReceiptNumber = mpesa_receipt_number,
            Balance = balance,
            TransactionDate = aware_transaction_datetime,
            PhoneNumber = phone_number,
        )

        our_model.save()

        from rest_framework.response import Response

        return Response({"OurResultDesc": "YEEY!!"})