from django.db import migrations, models
from django.utils.text import slugify


PROGRAM_AREA_SLUGS = {
    "Writing Assistance": "ic-writing-assistance",
}

TUTORING_OPTION_SLUGS = {
    "Drop In": "drop-in",
    "Workshop": "workshop",
    "Other": "other",
}


def copy_visit_catalog_values(apps, schema_editor):
    Visit = apps.get_model("compass_visits", "Visit")

    for visit in Visit.objects.select_related(
            "legacy_program_area", "legacy_tutoring_option").iterator():
        program_area_name = visit.legacy_program_area.name
        tutoring_option_name = visit.legacy_tutoring_option.name
        visit.program_area = PROGRAM_AREA_SLUGS.get(
            program_area_name,
            f"legacy-{slugify(program_area_name)}"[:50],
        )
        visit.tutoring_option = TUTORING_OPTION_SLUGS.get(
            tutoring_option_name,
            f"legacy-{slugify(tutoring_option_name)}"[:50],
        )
        visit.save(update_fields=("program_area", "tutoring_option"))


def noop_reverse_copy_visit_catalog_values(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("compass_visits", "0002_visit_student_netid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="visit",
            old_name="program_area",
            new_name="legacy_program_area",
        ),
        migrations.RenameField(
            model_name="visit",
            old_name="tutoring_option",
            new_name="legacy_tutoring_option",
        ),
        migrations.AddField(
            model_name="visit",
            name="program_area",
            field=models.CharField(
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="visit",
            name="tutoring_option",
            field=models.CharField(
                max_length=50,
                null=True,
            ),
        ),
        migrations.RunPython(
            copy_visit_catalog_values,
            noop_reverse_copy_visit_catalog_values,
        ),
        migrations.AlterField(
            model_name="visit",
            name="program_area",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="visit",
            name="tutoring_option",
            field=models.CharField(max_length=50),
        ),
        migrations.RemoveField(
            model_name="visit",
            name="legacy_program_area",
        ),
        migrations.RemoveField(
            model_name="visit",
            name="legacy_tutoring_option",
        ),
        migrations.DeleteModel(
            name="ProgramArea",
        ),
        migrations.DeleteModel(
            name="TutoringOption",
        ),
    ]