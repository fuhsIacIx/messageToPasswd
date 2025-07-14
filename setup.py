from cx_Freeze import setup, Executable

# 定义依赖项，这可能需要根据你的应用程序进行调整
dependencies = [
    "pypinyin",
    "argparse",
    "hashlib",
    "secrets"
]

# 定义可执行的脚本
executables = [
    Executable("main.py", target_name = "PasswdMaker"),
]

# 调用setup函数来配置打包过程
setup(
    name = "PasswdMaker",
    version="2.0.0",
    author="fuhsIacIx",
    author_email="sakuya_mei@outlook.com",
    description="安全密码生成器，支持确定性密码和随机密码生成",
    options = {
        "build_exe": {
            "packages": dependencies,

        },
    },
    executables = executables
)
