import os
import shutil

def classify_files(directory):
    # 获取目录下的所有文件
    files = os.listdir(directory)
    
    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            # 获取文件的扩展名
            file_extension = os.path.splitext(file)[1]
            
            # 创建分类文件夹（如果不存在）
            folder_path = os.path.join(directory, file_extension[1:])
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            # 移动文件到分类文件夹
            source_path = os.path.join(directory, file)
            destination_path = os.path.join(folder_path, file)
            shutil.move(source_path, destination_path)
            
            print(f"Moved '{file}' to '{folder_path}'")

# 运行目录
directory = os.getcwd()

# 分类和移动文件
classify_files(directory)
