import os
import sys

def main():
    # 设置项目路径
    project_path = r"F:\002 Web_Project\yalhardware\backend"
    
    # 确保路径存在
    if not os.path.exists(project_path):
        print(f"路径不存在: {project_path}")
        return
    
    print(f"正在导出项目结构: {project_path}")
    
    # 要排除的目录
    exclude_dirs = {
        '.git', '__pycache__', 'node_modules', 'venv', 
        '.idea', '.vscode', 'dist', 'build', 'target',
        '.next', 'out', 'coverage', '.nuxt'
    }
    
    # 要排除的文件
    exclude_files = {'.DS_Store', 'Thumbs.db'}
    
    with open('项目结构.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(f"项目目录: {project_path}\n")
        f.write(f"导出时间: {sys.argv[0]}\n")
        f.write("=" * 70 + "\n\n")
        
        # 统计信息
        dir_count = 0
        file_count = 0
        
        # 遍历目录
        for root, dirs, files in os.walk(project_path):
            # 计算层级（从项目根目录开始）
            rel_path = os.path.relpath(root, project_path)
            if rel_path == '.':
                level = 0
            else:
                level = rel_path.count(os.sep) + 1
            
            # 只显示3层
            if level > 3:
                continue
            
            # 排除目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # 排除文件
            files = [fi for fi in files if fi not in exclude_files and not fi.startswith('.')]
            
            # 排序
            dirs.sort(key=lambda x: x.lower())
            files.sort(key=lambda x: x.lower())
            
            # 构建缩进
            if level == 0:
                indent = ''
                f.write(f"📁 {os.path.basename(project_path) or '项目根目录'}/\n")
            else:
                indent = '│   ' * (level - 1)
                f.write(f"{indent}├── 📁 {os.path.basename(root)}/\n")
            
            # 当前层级的缩进
            current_indent = '│   ' * level
            
            # 统计
            dir_count += len(dirs)
            file_count += len(files)
            
            # 显示文件
            for i, file in enumerate(files):
                is_last_file = (i == len(files) - 1) and (len(dirs) == 0)
                connector = '└── ' if is_last_file else '├── '
                f.write(f"{current_indent}{connector}📄 {file}\n")
            
            # 显示子目录（如果未超过3层）
            if level < 3:
                for i, dir_name in enumerate(dirs):
                    is_last_dir = (i == len(dirs) - 1)
                    connector = '└── ' if is_last_dir else '├── '
                    f.write(f"{current_indent}{connector}📁 {dir_name}/\n")
            
            # 如果这是第3层，添加提示
            if level == 3:
                f.write(f"{current_indent}│   └── ... (更深层级已折叠)\n")
        
        # 添加统计信息
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"统计信息:\n")
        f.write(f"  • 目录数: {dir_count}\n")
        f.write(f"  • 文件数: {file_count}\n")
        f.write(f"  • 最大显示深度: 3层\n")
        f.write("=" * 70 + "\n")
    
    print(f"✓ 导出完成！")
    print(f"✓ 文件已保存为: 项目结构.txt")
    print(f"✓ 共 {dir_count} 个目录, {file_count} 个文件")

if __name__ == '__main__':
    main()