from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from lend_app.models import Borrower, Approver, User
from lend_app.serializers import BorrowerListSerializer, BorrowerSerializer, ApproverSerializer, ApproverListSerializer, UserSerializer, BorrowerUpdateSerializer, ApproverUpdateSerializer

# Borrower Create List View
class BorrowerListCreateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        borrowers = Borrower.objects.all()
        serializer = BorrowerListSerializer(borrowers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BorrowerSerializer(data=request.data)
        if serializer.is_valid():
            borrower = serializer.save()
            return Response({
                'message': 'Borrower created successfully',
                'borrower': BorrowerSerializer(borrower).data
            })
        return Response(serializer.errors)


# Approver Registration List View
class ApproverListCreateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        approvers = Approver.objects.all()
        serializer = ApproverListSerializer(approvers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ApproverSerializer(data=request.data)
        if serializer.is_valid():
            approver = serializer.save()
            return Response({
                'message': 'Approver created successfully',
                'approver': ApproverSerializer(approver).data
            })
        return Response(serializer.errors)

#UserDeatialView
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # บังคับให้ต้องล็อกอิน
    """ Retrieve, update or delete a user instance. """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User updated successfully',
                'user': serializer.data})
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({'message': 'User deleted successfully'})

class BorrowerDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Borrower.objects.get(pk=pk)
        except Borrower.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        borrower = self.get_object(pk)
        serializer = BorrowerUpdateSerializer(borrower)
        return Response(serializer.data)
    
    def put(self, request, pk):
        borrower = self.get_object(pk)
        serializer = BorrowerUpdateSerializer(borrower, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Borrower updated successfully',
                'borrower': serializer.data})
        return Response(serializer.errors)
    
class ApproverDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Approver.objects.get(pk=pk)
        except Approver.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        approver = self.get_object(pk)
        serializer = ApproverUpdateSerializer(approver)
        return Response(serializer.data)
    
    def put(self, request, pk):
        approver = self.get_object(pk)
        serializer = ApproverUpdateSerializer(approver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Approver updated successfully',
                'approver': serializer.data})
        return Response(serializer.errors)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request):
        user = self.get_object(request.user.id)
        approver = Approver.objects.filter(user=user).first()
        borrower = Borrower.objects.filter(user=user).first()

        if approver:
            serializer = ApproverUpdateSerializer(approver)
        elif borrower:
            serializer = BorrowerUpdateSerializer(borrower)
        else:
            return Response({'message': 'User not found both Approver and Borrower'}, status=404)
        return Response(serializer.data)