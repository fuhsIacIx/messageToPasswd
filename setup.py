from cx_Freeze import setup, Executable

# 定义依赖项，这可能需要根据你的应用程序进行调整
dependencies = [
    "pypinyin",
    "os"

]

# 定义可执行的脚本
executables = [
    Executable("main.py", target_name = "PasswdMaker"),
]

# 调用setup函数来配置打包过程
setup(
    name = "PasswdMaker",
    version="1.0",
    author="sakuya",
    author_email="sakuya_mei@outlook.com",
    description="根据输入信息生成密码",
    options = {
        "build_exe": {
            "packages": dependencies,

        },
    },
    executables = executables
)