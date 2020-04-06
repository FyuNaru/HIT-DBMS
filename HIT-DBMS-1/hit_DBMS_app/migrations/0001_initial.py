# Generated by Django 3.0.4 on 2020-04-03 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ViewStudentPrize',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.CharField(max_length=10)),
                ('student_name', models.CharField(max_length=20)),
                ('prize_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'view_student_prize',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('homepage', models.URLField()),
                ('student_number', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('homepage', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('sex', models.CharField(choices=[('M', 'Man'), ('W', 'Woman'), ('U', 'Unknown')], default='U', max_length=1)),
                ('age', models.PositiveSmallIntegerField()),
                ('phone', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Department')),
                ('lab', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Laboratory')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=20)),
                ('sex', models.CharField(choices=[('M', 'Man'), ('W', 'Woman'), ('U', 'Unknown')], default='U', max_length=1)),
                ('age', models.PositiveSmallIntegerField()),
                ('phone', models.PositiveIntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Department')),
                ('lab', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Laboratory')),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(db_index=True, max_length=20)),
                ('score', models.IntegerField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author', models.ManyToManyField(to='hit_DBMS_app.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(max_length=50)),
                ('student_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hit_DBMS_app.Student')),
            ],
        ),
    ]