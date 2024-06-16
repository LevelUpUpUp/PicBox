import os
import shutil
from collections import defaultdict

def move_nonunique_files(directory_path):
    # 确保输入的是一个绝对路径
    if not os.path.isabs(directory_path):
        raise ValueError("请输入一个绝对路径")

    # 创建存放移动文件的新文件夹
    pic_remove_path = os.path.join(directory_path, "pic_remove")
    os.makedirs(pic_remove_path, exist_ok=True)

    # 使用defaultdict存储文件名（不包括后缀）及其完整路径
    files_dict = defaultdict(set)

    # 遍历文件夹
    for root, dirs, files in os.walk(directory_path):
        # 仅处理位于顶层目录的文件
        if root == directory_path:
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                file_name_lower = file_name.lower()  # 文件名忽略大小写
                full_path = os.path.join(root, file)
                files_dict[file_name_lower].add(full_path)

    # 找到需要移动的文件并将其移动到新文件夹中
    for file_paths in files_dict.values():
        if len(file_paths) > 1:  # 如果有同名但不同后缀的文件
            continue  # 保留这些文件，不移动
        else:
            for file_path in file_paths:
                shutil.move(file_path, pic_remove_path)

# 示例使用
move_nonunique_files('/Users/zhuojianfei/Pictures/奉贤乐隐谷')