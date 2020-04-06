from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.

from hit_DBMS_app import models
from hit_DBMS_app import forms
from django.views import generic
from django.shortcuts import HttpResponse
from django.db.models import Avg, Count
from django.db import transaction, IntegrityError


def db_handle(request):
    models.Department.objects.create(id='127',name='123',homepage='fyunaru.cn')
    models.Student.objects.create(id='1', name='test',age=11,phone=1234,department=models.Department.objects.get(id='1'))
    return HttpResponse("OK")

# 主页
class IndexView(generic.TemplateView):
    template_name = 'index.html'

# 系
def listDepartment(request):
    list_obj = models.Department.objects.all()
    return render(request, 'Department/listDepartment.html', {'li': list_obj})

def createDepartment(request):
    if request.method == 'POST':
        form = forms.DepartmentForm(request.POST)
        if form.is_valid():
            try:
                models.Department.objects.create(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    homepage=request.POST['homepage'],
                    student_number=request.POST['student_number'],
                )
            except IntegrityError:
                error_message = "输出了重复的主键，请返回检查"
                return render(request, 'error.html', {'message':error_message})
        return render(request, 'success.html')
    form = forms.DepartmentForm()
    return render(request, 'Department/createDepartment.html', {'form': form})

def deleteDepartment(request):
    if request.method == 'POST':
        form = forms.DeleteDepartmentForm(request.POST)
        if form.is_valid():
            models.Department.objects.filter(id=request.POST['id']).delete()
        return render(request, 'success.html')
    form = forms.DeleteDepartmentForm()
    return render(request, 'Department/deleteDepartment.html', {'form': form})

# 当要更新的id不存在时，不会产生任何影响
def updateDepartment(request):
    if request.method == 'POST':
        form = forms.UpdateDepartmentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    if request.POST['name']:
                        models.Department.objects.filter(id=request.POST['id']).update(name=request.POST['name'])
                    #手动抛出一个错误
                    #raise Exception("异常")
                    if request.POST['homepage']:
                        models.Department.objects.filter(id=request.POST['id']).update(homepage=request.POST['homepage'])
            except Exception:
                error_message = "检测到手动抛出的异常，数据更新失败"
                return render(request, 'error.html', {'message': error_message})
        return render(request, 'success.html')

    form = forms.UpdateDepartmentForm()
    return render(request, 'Department/updateDepartment.html', {'form': form})

# 学生
def listStudent(request):
    list_obj = models.Student.objects.all()
    return render(request, 'Student/listStudent.html', {'li': list_obj})

@transaction.atomic
def createStudent(request):
    if request.method == 'POST':
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            try:
                student = models.Student(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    sex=request.POST['sex'],
                    age=request.POST['age'],
                    phone=request.POST['phone'],
                    department=models.Department.objects.get(id=request.POST['department'])
                )
                if request.POST['tutor']:
                    student.tutor = models.Teacher.objects.get(id=request.POST['tutor'])
                if request.POST['lab']:
                    student.lab = models.Laboratory.objects.get(id=request.POST['lab'])
                student.save()
            except ObjectDoesNotExist:
                error_message = "输入数据中某外键值不存在，请返回检查"
                return render(request, 'error.html', {'message': error_message})
            except IntegrityError:
                error_message = "输出了重复的主键，请返回检查"
                return render(request, 'error.html', {'message':error_message})
        return render(request, 'success.html')
    form = forms.StudentForm()
    return render(request, 'Student/createStudent.html', {'form': form})

def deleteStudent(request):
    if request.method == 'POST':
        form = forms.DeleteStudentForm(request.POST)
        if form.is_valid():
            models.Student.objects.filter(id=request.POST['id']).delete()
        return render(request, 'success.html')
    form = forms.DeleteStudentForm()
    return render(request, 'Student/deleteStudent.html', {'form': form})

# 查询某一学生的全部成绩（连接查询）(可查询姓名重复的学生）
def queryScore(request):
    if request.method == 'POST':
        form = forms.QueryScoreForm(request.POST)
        if form.is_valid():
            result = models.Student.objects.none()
            for student in models.Student.objects.filter(name=request.POST['name']):
                result = result | models.Score.objects.filter(student_id=student.id)
            return render(request, 'Student/scoreResult.html', {'result': result})
    form = forms.QueryScoreForm()
    return render(request, 'Student/queryScore.html', {'form': form})

# 查询某一学生的奖项（view视图实例应用）
def queryPrize(request):
    if request.method == 'POST':
        form = forms.QueryPrizeForm(request.POST)
        if form.is_valid():
            result = models.ViewStudentPrize.objects.filter(student_name=request.POST['name'])
            return render(request, 'Student/prizeResult.html', {'result': result})
    form = forms.QueryPrizeForm()
    return render(request, 'Student/queryPrize.html', {'form': form})

# 实验室
def listLab(request):
    list_obj = models.Laboratory.objects.all()
    return render(request, 'Lab/listLab.html', {'li': list_obj})

def createLab(request):
    if request.method == 'POST':
        form = forms.LabForm(request.POST)
        if form.is_valid():
            models.Laboratory.objects.create(
                id=request.POST['id'],
                name=request.POST['name'],
                homepage=request.POST['homepage']
            )
        return render(request, 'success.html')
    form = forms.LabForm()
    return render(request, 'Lab/createLab.html', {'form': form})

# 论文
def listPaper(request):
    list_obj = models.Paper.objects.all()
    return render(request, 'Paper/listPaper.html', {'li': list_obj})

def createPaper(request):
    if request.method == 'POST':
        form = forms.PaperForm(request.POST)
        if form.is_valid():
            paper = models.Paper(title=request.POST['title'])
            paper.save()
            for teacher_name in request.POST['author'].split(' '):
                paper.author.add(models.Teacher.objects.get(name=teacher_name))
            paper.save()
        return render(request, 'success.html')
    form = forms.PaperForm()
    return render(request, 'Paper/createPaper.html', {'form': form})

# 老师
def listTeacher(request):
    list_obj = models.Teacher.objects.all()
    return render(request, 'Teacher/listTeacher.html', {'li': list_obj})

def createTeacher(request):
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST)
        if form.is_valid():
            teacher = models.Teacher(
                id=request.POST['id'],
                name=request.POST['name'],
                sex=request.POST['sex'],
                age=request.POST['age'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                department=models.Department.objects.get(id=request.POST['department'])
            )
            if request.POST['lab']:
                teacher.lab = models.Laboratory.objects.get(id=request.POST['lab'])
            teacher.save()
        return render(request, 'success.html')
    form = forms.TeacherForm()
    return render(request, 'Teacher/createTeacher.html', {'form': form})

# 分数
def listScore(request):
    list_obj = models.Score.objects.all()
    return render(request, 'Score/listScore.html', {'li': list_obj})

def createScore(request):
    if request.method == 'POST':
        form = forms.ScoreForm(request.POST)
        if form.is_valid():
            models.Score.objects.create(
                course=request.POST['course'],
                score=request.POST['score'],
                student_id=models.Student.objects.get(id=request.POST['student_id'])
            )
        return render(request, 'success.html')
    form = forms.ScoreForm()
    return render(request, 'Score/createScore.html', {'form': form})

# 查询平均成绩group,having，要求成绩至少为两门
def averageScore(request):
    result = models.Score.objects.values('student_id').annotate(avg=Avg('score'), c=Count('course')).values('student_id', 'avg').filter(c__gt=2)
    return render(request, 'Score/averageScore.html', {'result':result})

# 奖项
def listPrize(request):
    list_obj = models.Prize.objects.all()
    return render(request, 'Prize/listPrize.html', {'li': list_obj})

def createPrize(request):
    if request.method == 'POST':
        form = forms.PrizeForm(request.POST)
        if form.is_valid():
            models.Prize.objects.create(
                name=request.POST['name'],
                student_id=models.Student.objects.get(id=request.POST['student_id'])
            )
        return render(request, 'success.html')
    form = forms.PrizeForm()
    return render(request, 'Prize/createPrize.html', {'form': form})

# 经历
def listExperience(request):
    list_obj = models.Experience.objects.all()
    return render(request, 'Experience/listExperience.html', {'li': list_obj})

def createExperience(request):
    if request.method == 'POST':
        form = forms.ExperienceForm(request.POST)
        if form.is_valid():
            models.Experience.objects.create(
                experience=request.POST['experience'],
                student_id=models.Student.objects.get(id=request.POST['student_id'])
            )
        return render(request, 'success.html')
    form = forms.ExperienceForm()
    return render(request, 'Experience/createExperience.html', {'form': form})


