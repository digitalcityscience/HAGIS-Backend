import uuid

import django.core.validators
import django.db.models.deletion
import tosca_api.apps.core.editorjs
import tosca_api.apps.footer.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Footer",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid7, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=120, unique=True)),
                ("is_published", models.BooleanField(db_index=True, default=False, editable=False)),
                ("publication_version", models.PositiveBigIntegerField(default=0, editable=False)),
                ("published_snapshot", models.JSONField(blank=True, default=dict, editable=False)),
                ("published_at", models.DateTimeField(blank=True, editable=False, null=True)),
                (
                    "published_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="published_footers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="FooterLogo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        upload_to=tosca_api.apps.footer.models.footer_logo_upload_to,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["png", "jpg", "jpeg", "webp"]
                            )
                        ],
                    ),
                ),
                ("alt_text", models.CharField(max_length=255)),
                ("destination_url", models.URLField(blank=True, max_length=500)),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "footer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logos",
                        to="footer.footer",
                    ),
                ),
            ],
            options={"ordering": ["display_order", "created_at"]},
        ),
        migrations.CreateModel(
            name="FooterDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=120)),
                (
                    "slug",
                    models.SlugField(
                        help_text="Reserved frontend path without a leading slash, for example privacy.",
                        max_length=80,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Use lowercase letters, numbers, and single hyphens only.",
                                regex="^[a-z0-9]+(?:-[a-z0-9]+)*$",
                            )
                        ],
                    ),
                ),
                (
                    "content",
                    models.JSONField(
                        blank=True,
                        default=tosca_api.apps.core.editorjs.empty_document,
                    ),
                ),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "footer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="footer.footer",
                    ),
                ),
            ],
            options={"ordering": ["display_order", "created_at"]},
        ),
        migrations.AddConstraint(
            model_name="footer",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_published", True)),
                fields=("is_published",),
                name="one_published_footer",
            ),
        ),
        migrations.AddConstraint(
            model_name="footerlogo",
            constraint=models.UniqueConstraint(
                fields=("footer", "display_order"),
                name="unique_footer_logo_order",
            ),
        ),
        migrations.AddConstraint(
            model_name="footerdocument",
            constraint=models.UniqueConstraint(
                fields=("footer", "slug"),
                name="unique_footer_document_slug",
            ),
        ),
        migrations.AddConstraint(
            model_name="footerdocument",
            constraint=models.UniqueConstraint(
                fields=("footer", "display_order"),
                name="unique_footer_document_order",
            ),
        ),
    ]
