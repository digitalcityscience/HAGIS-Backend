from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("footer", "0001_initial")]

    operations = [
        migrations.RemoveConstraint(
            model_name="footerdocument",
            name="unique_footer_document_order",
        ),
        migrations.AddConstraint(
            model_name="footerdocument",
            constraint=models.UniqueConstraint(
                fields=("footer", "display_order"),
                name="unique_footer_document_order",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ),
    ]
