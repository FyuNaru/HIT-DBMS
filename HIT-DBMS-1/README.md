# 实验要求

实现一个简单的数据库系统。

要求：
实体数量不少于8个，联系数量不少于7个；
实现插入删除修改删除的操作；
实现连接查询、嵌套查询、分组查询（需体现having语句）
为常用属性（非主键建立索引）；
为常用查询建立视图；
完整性检查，包括空值警告，重复值警告，查询时不存在的值警告；

扩展要求：
有图形用户界面；
事务管理；
触发器；

# 文件结构

hit_DBMS/ 为django项目配置文件夹
- settings.py 基本配置
- urls.py 配置url
- 其他文件为默认生成文件

hit_DBMS_app/ 为实际的数据库项目
- templates/ html页面文件夹
- models.py 数据库表的定义
- views.py 对数据库的全部操作
- forms.py html表单的结构
- 其他文件为默认生成文件

db.sqlite3 数据库，可用sqlite的可视化软件打开

manage.py 项目启动程序，在命令行窗口输入`python manage.py runserver`以运行程序

