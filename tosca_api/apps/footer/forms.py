from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from tosca_api.apps.core.editorjs import render_content_media_urls
from tosca_api.apps.footer.models import (
    MAX_ACTIVE_DOCUMENTS,
    MAX_ACTIVE_LOGOS,
    FooterDocument,
)
from tosca_api.apps.geocontext.widgets import EditorJsWidget


class ActiveItemLimitFormSet(BaseInlineFormSet):
    active_limit: int
    item_label: str

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        active_count = sum(
            1
            for form in self.forms
            if form.cleaned_data
            and not form.cleaned_data.get("DELETE", False)
            and form.cleaned_data.get("is_active", True)
        )
        if active_count > self.active_limit:
            raise ValidationError(
                f"A footer can have at most {self.active_limit} active {self.item_label}."
            )


class FooterLogoInlineFormSet(ActiveItemLimitFormSet):
    active_limit = MAX_ACTIVE_LOGOS
    item_label = "logos"


class FooterDocumentInlineFormSet(ActiveItemLimitFormSet):
    active_limit = MAX_ACTIVE_DOCUMENTS
    item_label = "documents"

    def clean(self):
        if any(self.errors):
            return

        forms = [
            form
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        ]
        existing_forms = [form for form in forms if form.instance.pk]
        new_forms = [form for form in forms if not form.instance.pk]
        moved_forms = [form for form in existing_forms if "display_order" in form.changed_data]

        if len(moved_forms) == 1:
            moved_form = moved_forms[0]
            ordered_forms = sorted(
                (form for form in existing_forms if form is not moved_form),
                key=lambda form: form.initial.get("display_order", 0),
            )
            requested_order = moved_form.cleaned_data.get("display_order", 0)
            target_order = min(max(requested_order, 0), len(ordered_forms))
            ordered_forms.insert(target_order, moved_form)
        else:
            ordered_forms = sorted(
                existing_forms,
                key=lambda form: (
                    form.cleaned_data.get("display_order", 0),
                    form.initial.get("display_order", 0),
                ),
            )

        # New documents always append, regardless of the cloned inline's initial value.
        ordered_forms.extend(new_forms)
        for display_order, form in enumerate(ordered_forms):
            form.cleaned_data["display_order"] = display_order
            form.instance.display_order = display_order

        # Run model/formset uniqueness and active-item validation after normalization.
        super().clean()


class FooterDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and not self.is_bound:
            self.initial["content"] = render_content_media_urls(self.instance.content)

    class Meta:
        model = FooterDocument
        fields = "__all__"
        widgets = {"content": EditorJsWidget(profile="footer")}
