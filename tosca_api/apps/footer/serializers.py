from __future__ import annotations

from django.core.files.storage import default_storage
from rest_framework import serializers

from tosca_api.apps.core.editorjs import render_content_media_urls
from tosca_api.apps.footer.models import Footer


def _absolute_url(request, path: str) -> str:
    url = default_storage.url(path)
    return request.build_absolute_uri(url) if request is not None else url


def serialize_published_footer(footer: Footer, request=None) -> dict:
    snapshot = footer.published_snapshot or {}
    return {
        "id": str(footer.pk),
        "name": footer.name,
        "version": footer.publication_version,
        "published_at": footer.published_at,
        "logos": [
            {
                **logo,
                "url": _absolute_url(request, logo["image"]),
            }
            for logo in snapshot.get("logos", [])
        ],
        "documents": [
            {
                **document,
                "content": render_content_media_urls(document["content"], request),
            }
            for document in snapshot.get("documents", [])
        ],
    }


class PublishedFooterSerializer(serializers.Serializer):
    """OpenAPI shape for the immutable public footer snapshot."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    version = serializers.IntegerField()
    published_at = serializers.DateTimeField()
    logos = serializers.ListField(child=serializers.DictField())
    documents = serializers.ListField(child=serializers.DictField())
