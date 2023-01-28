''''''

'''用于存放类的
学校类、学员类、课程类、讲师类、管理员类
'''
from db import db_handler


# 父类,让所有子类都继承 select 与 save方法
class Base:
    # 查看数据  ----> 登录、查看数据库
    @classmethod
    def select(cls, username):  # School, school_name
        # obj： 对象   or   None
        obj = db_handler.select_data(cls, username)
        return obj

    # 保存数据 ---> 注册、保存、更新数据
    def save(self):
        # 让db_handler中的save_data帮我保存对象数据
        db_handler.save_data(self)


# 管理员类
class Admin(Base):
    # 调用类的时候触发
    # username, password
    def __init__(self, user, pwd):
        # 给当前对象赋值
        self.user = user
        self.pwd = pwd

    # 创建学校
    def create_school(self, school_name, school_addr):
        '''该方法内部来调用学校类实例化的得到对象，并保存'''
        school_obj = School(school_name, school_addr)
        school_obj.save()

    # 创建课程
    def create_course(self, school_obj, course_name):
        # 1.调用课程类，实例化创建课程
        course_obj = Course(course_name)
        course_obj.save()
        # 2.获取当前学校对象，并将课程添加到课程列表中
        school_obj.course_list.append(course_name)
        # 3.更新学校数据
        school_obj.save()

    # 创建讲师
    def create_teacher(self, teacher_name, teacher_pwd):
        # 1.调用老师类，实例化的到老师对象，并保存
        teacher_obj = Teacher(teacher_name, teacher_pwd)
        teacher_obj.save()


# 学校类
class School(Base):
    def __init__(self, name, addr):
        # 必须写: self.user,
        # 因为db_handler里面的select_data统一规范
        self.user = name
        self.addr = addr
        # 课程列表: 每所学校都应该有相应的课程
        self.course_list = []


# 学生类
class Student(Base):
    pass


# 课程类
class Course(Base):
    def __init__(self, course_name):
        self.user = course_name
        self.student_list = []


# 老师类
class Teacher(Base):
    def __init__(self, teacher_name, teacher_pwd):
        self.user = teacher_name
        # self.pwd需要统一
        self.pwd = teacher_pwd
        self.course_list_from_tea = []



