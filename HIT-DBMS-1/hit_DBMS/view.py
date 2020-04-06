from django.http import HttpResponse  # 需要导入HttpResponse模块

def hello(request):   # request参数必须有，名字类似self的默认规则，可以修改，它封装了用户请求的所有内容
    return HttpResponse("Hello world ! ")  # 不能直接字符串，必须是由这个类封装，此为Django规则