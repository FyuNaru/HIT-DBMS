from django import forms

class DepartmentForm(forms.Form):
    id = forms.CharField(max_length=10, label="学院编号")
    name = forms.CharField(max_length=40, label="学院名")
    homepage = forms.URLField(label="主页地址")
    student_number = forms.IntegerField(label="学生数量")

class DeleteDepartmentForm(forms.Form):
    id = forms.CharField(max_length=10, label="请输入学院编号")

class UpdateDepartmentForm(forms.Form):
    id = forms.CharField(max_length=10, label="请输入要更改的学院编号")
    name = forms.CharField(max_length=40, label="请输出更改后的学院名", required=False)
    homepage = forms.URLField(label="请输入更改后的主页地址", required=False)


class StudentForm(forms.Form):
    id = forms.CharField(max_length=10)
    name = forms.CharField(max_length=20)
    sex = forms.ChoiceField(choices=[('M', 'Man'), ('W', 'Woman'), ('U', 'Unknown')])
    age = forms.IntegerField(min_value=0, max_value=100)
    phone = forms.IntegerField()
    tutor = forms.CharField(max_length=10, required=False)
    lab = forms.CharField(max_length=10, required=False)
    department = forms.CharField(max_length=10)

class DeleteStudentForm(forms.Form):
    id = forms.CharField(max_length=10, label="请输入学生编号")

class QueryScoreForm(forms.Form):
    name = forms.CharField(max_length=20, label="请输入要查询成绩的学生姓名")

class QueryPrizeForm(forms.Form):
    name = forms.CharField(max_length=20, label="请输入要查询奖项的学生姓名")

class LabForm(forms.Form):
    id = forms.CharField(max_length=10)
    name = forms.CharField(max_length=40)
    homepage = forms.URLField()

class PaperForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.CharField(max_length=50)

class TeacherForm(forms.Form):
    # lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, null=True)

    id = forms.CharField(max_length=10)
    name = forms.CharField(max_length=20)
    sex = forms.ChoiceField(choices=[('M', 'Man'), ('W', 'Woman'), ('U', 'Unknown')])
    age = forms.IntegerField(min_value=0, max_value=100)
    phone = forms.IntegerField()
    email = forms.EmailField()
    department = forms.CharField(max_length=10)
    lab = forms.CharField(max_length=10, required=False)

class ScoreForm(forms.Form):
    student_id = forms.CharField(max_length=10)
    course = forms.CharField(max_length=20)
    score = forms.IntegerField(min_value=0, max_value=100)

class PrizeForm(forms.Form):
    student_id = forms.CharField(max_length=10)
    name = forms.CharField(max_length=50)

class ExperienceForm(forms.Form):
    student_id = forms.CharField(max_length=10)
    experience = forms.CharField(max_length=50)




