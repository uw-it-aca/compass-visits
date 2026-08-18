from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compass_visits", "0002_visit_student_netid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="visit",
            name="program_area",
        ),
        migrations.RemoveField(
            model_name="visit",
            name="tutoring_option",
        ),
        migrations.AddField(
            model_name="visit",
            name="program_area",
            field=models.CharField(
                default="ic-drop-in-tutoring",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="visit",
            name="tutoring_option",
            field=models.CharField(
                default="drop-in",
                max_length=50,
            ),
        ),
        migrations.DeleteModel(
            name="ProgramArea",
        ),
        migrations.DeleteModel(
            name="TutoringOption",
        ),
    ]