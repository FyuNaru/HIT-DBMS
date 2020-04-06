from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

# Create your models here.

class Department(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=40)
    homepage = models.URLField()
    student_number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id) + str(self.name)

class Laboratory(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=40)
    homepage = models.URLField()
    def __str__(self):
        return str(self.id) + str(self.name)


class Teacher(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    SEX = (
        ('M', 'Man'),
        ('W', 'Woman'),
        ('U', 'Unknown')
    )
    sex = models.CharField(max_length=1, choices=SEX, default='U')
    age = models.PositiveSmallIntegerField()
    phone = models.PositiveIntegerField()
    email = models.EmailField()
    # 一对多关系
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id) + str(self.name)

class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20, db_index=True)
    SEX = (
        ('M', 'Man'),
        ('W', 'Woman'),
        ('U', 'Unknown')
    )
    sex = models.CharField(max_length=1, choices=SEX, default='U')
    age = models.PositiveSmallIntegerField()
    phone = models.PositiveIntegerField()
    # 一对多关系
    tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id) + str(self.name)

# 成绩-学生 多对一
class Score(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    course = models.CharField(max_length=20, db_index=True)
    score = models.IntegerField()

# 奖项-学生 多对一
class Prize(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50)

# 论文-老师 多对多
class Paper(models.Model):
    title = models.CharField(max_length=50)
    author = models.ManyToManyField(Teacher)

# 个人经历-学生 一对一
class Experience(models.Model):
    experience = models.CharField(max_length=50)
    student_id = models.OneToOneField(Student, on_delete=models.CASCADE, null=False)

 # 增加学生数量的触发器
@receiver(pre_save, sender=Student)
def pre_save_student(sender, instance, **kwargs):
    department = instance.department
    department.student_number += 1
    department.save()

 # 减少学生数量的触发器
@receiver(pre_delete, sender=Student)
def pre_delete_student(sender, instance, **kwargs):
    department = instance.department
    department.student_number -= 1
    department.save()

# 增加查看学生奖项的视图
class ViewStudentPrize(models.Model):
    student_id = models.CharField(max_length=10)
    student_name = models.CharField(max_length=20)
    prize_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'view_student_prize'
        managed = False
