''''''
'''管理员视图'''
from interface import admin_interface
from interface import common_interface
from lib import common

admin_info = {
    'user': None
}

# 管理员注册
def register():
    while True:
        username = input('请输入用户名: ').strip()
        password = input('请输入密码: ').strip()
        re_password = input('请确认密码: ').strip()

        # 小的逻辑判断
        if password == re_password:
            # 调用接口层，管理员注册接口
            flag, msg = admin_interface.admin_register_interface(
                username, password
            )

            if flag:
                print(msg)
                break

            else:
                print(msg)

        else:
            print('两次密码不一致，请重新输入')


# 管理员登录
def login():
    while True:
        username = input('请输入用户名: ').strip()
        password = input('请输入密码: ').strip()

        # 1.调用管理员登录接口
        flag, msg = admin_interface.admin_login_interface(
            username, password
        )
        if flag:
            print(msg)
            # 记录当前用户登录状态
            # 可变类型不需要global
            admin_info['user'] = username
            break

        else:
            print(msg)


# 管理员创建学校
@common.auth('admin')
def create_school():
    while True:
        # 1.让用户输入学校的名称与地址
        school_name = input('请输入学校名称: ').strip()
        school_addr = input('请输入学校地址: ').strip()

        # 2.调用接口，保存学校
        flag, msg = admin_interface.create_school_interface(
            # 学校名、学校地址、创建学校的管理员
            school_name, school_addr, admin_info.get('user')
        )

        if flag:
            print(msg)
            break

        else:
            print(msg)


# 管理员创建课程
@common.auth('admin')
def create_course():
    while True:
 
        flag, school_list_or_msg = common_interface.get_all_school_interface()
        if not flag:
            print(school_list_or_msg)
            break

        for index, school_name in enumerate(school_list_or_msg):
            print(f'编号: {index}    学校名: {school_name}')

        choice = input('请输入学校编号: ').strip()

        if not choice.isdigit():
            print('请输入数字')
            continue

        choice = int(choice)

        if choice not in range(len(school_list_or_msg)):
            print('请输入正确编号!')
            continue

        # 获取选择后的学校名字
        school_name = school_list_or_msg[choice]

        # 2.选择学校后，再输入课程名称
        course_name = input('请输入需要创建的课程名称： ').strip()

        # 3.调用创建课程接口，让管理员去创建课程
        flag, msg = admin_interface.create_course_interface(
            # 传递学校的目的，是为了关联课程
            school_name, course_name, admin_info.get('user')
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)



# 管理员创建老师
@common.auth('admin')
def create_teacher():
    while True:
        # 1.让管理员输入创建的老师名字
        teacher_name = input('请输入老师的名字: ').strip()
        # 2.调用接口创建老师
        flag, msg = admin_interface.create_teacher_interface(
            teacher_name, admin_info.get('user'))

        if flag:
            print(msg)
            break

        else:
            print(msg)


func_dict = {
    '1': register,
    '2': login,
    '3': create_school,
    '4': create_course,
    '5': create_teacher,
}


# 管理员视图函数
def admin_view():
    while True:
        print('''
        - 1.注册
        - 2.登录
        - 3.创建学校
        - 4.创建课程
        - 5.创建讲师
        ''')

        choice = input('请输入功能编号: ').strip()

        if choice == 'q':
            admin_info['user'] = None
            break

        if choice not in func_dict:
            print('输入有误，请重新输入!')
            continue

        func_dict.get(choice)()