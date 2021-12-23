from django.urls import path, include
from poll.views import *
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register('poll', PollViewSet)

urlpatterns = [
  # path('poll/', poll),
  path('poll/', include(router.urls)),
  # path('poll/', PollAPIView.as_view()),
  path('poll/<int:id>/', poll_details),
  path('generics/poll/<int:id>', PollListView.as_view()),
  # path('generics/poll/', PollListView.as_view()),
]