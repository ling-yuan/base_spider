import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # 表示当前路径
FATHER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 表示上一级目录
GRANDFATHER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 表示上两级目录
sys.path.insert(0, FATHER_DIR)  # 将上一级目录添加到环境变量中
sys.path.insert(0, GRANDFATHER_DIR)  # 将上两级目录添加到环境变量中
