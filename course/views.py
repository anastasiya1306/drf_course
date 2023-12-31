from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import stripe
from course.tasks import send_email
from config import settings
from course.models import Course, Lesson, Payments
from course.paginators import Pagination
from course.permissions import IsModerator, IsOwner
from course.serializers import CourseSerializer, LessonSerializer, PaymentsSerializers, SubscriptionSerializer, \
    PaymentCreateSerializer
from course.services import checkout_session, create_payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = Pagination
    queryset = Course.objects.all()
    permission_classes = [IsModerator | IsOwner]

    def update(self, request, *args, **kwargs):
        send_email.delay(kwargs['pk'])
        return super().update(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = Pagination
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]


class PaymentsListView(generics.ListAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']


class PaymentsCreateView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    queryset = Payments.objects.all()

    def post(self, request, *args, **kwargs):
        """Создание платежа"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = checkout_session(
            course=serializer.validated_data['course'],
            user=self.request.user
        )
        create_payment(course=serializer.validated_data['course'],
                       user=self.request.user)
        return Response(session['id'], status=status.HTTP_201_CREATED)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Lesson.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Lesson.objects.all()
