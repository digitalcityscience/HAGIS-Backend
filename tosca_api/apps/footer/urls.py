from django.urls import path

from tosca_api.apps.footer.views import (
    PublishedFooterDocumentView,
    PublishedFooterView,
)


app_name = "footer"

urlpatterns = [
    path("footer/", PublishedFooterView.as_view(), name="published-footer"),
    path(
        "footer/documents/<slug:slug>/",
        PublishedFooterDocumentView.as_view(),
        name="published-footer-document",
    ),
]
