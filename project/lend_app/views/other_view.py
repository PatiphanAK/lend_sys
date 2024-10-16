from rest_framework.views import APIView
from lend_app.serializers import CategorySerializer
from rest_framework.permissions import AllowAny
from lend_app.models import Category
from rest_framework.response import Response
# Category List View
class CategoriesView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)