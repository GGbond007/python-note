# -*- coding:utf-8 -*-
import os

# print("����1~20�ڵ�����֮�ͣ�����1��20")

def add(x, y):
    return int(x) + int(y)

while True:
    try:
        num1 = input('������һ��ֵ������ q �˳�: ').strip()
        if num1.upper() == 'Q':
            break
        num2 = input('�ٴ�����һ��ֵ: ').strip()
        os.system('cls')
        print('{} + {} = {}'.format(num1, num2, add(num1, num2)))
    except Exception as e:
        print(e)