# -*- coding: utf-8 -*-
# @Time    : 2024/8/20 20:35
# @Author  : Imens zhang
# @File    : main.py
# @Software: PyCharm

from pypinyin import pinyin, Style
from password_generator import PasswordGenerator
from key_manager import generate_key, get_available_keys, load_key
import os
import sys
import argparse
from typing import Optional

VERSION = "2.0.0"

def show_version():
    print(f"密码生成器 v{VERSION}")
    sys.exit(0)

def show_help():
    print(f"""密码生成器 v{VERSION}
使用方法:
  交互模式: python main.py
  命令行模式: python main.py [选项]

选项:
  -V, --version       显示版本信息
  -h, --help          显示帮助信息
  -a, --account TEXT  账户名称(支持ASCII或中文)
  -l, --length INT    密码长度(8-64)
  -k, --key NAME      指定使用的密钥
  --new-key           生成新密钥
  --key-name NAME     新密钥名称
  --key-length INT    新密钥长度(16-256)
  --ant               生成随机密码

交互模式支持:
- 密钥管理
- 带选项的密码生成
- 配置设置
- 确定性/随机密码选择""")
    sys.exit(0)

def parse_arguments():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-V', '--version', action='store_true', help='Show version')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    parser.add_argument('-a', '--account', type=str, help='Account name')
    parser.add_argument('-l', '--length', type=int, default=12, help='Password length')
    parser.add_argument('-k', '--key', type=str, help='Key to use')
    parser.add_argument('--new-key', action='store_true', help='Generate new key')
    parser.add_argument('--key-name', type=str, help='Name for new key')
    parser.add_argument('--key-length', type=int, default=32, help='Length for new key')
    parser.add_argument('--ant', action='store_true', help='交互模式生成随机密码或快速模式生成确定性密码')
    return parser.parse_known_args()

def convert_to_pinyin(target_text: str) -> str:
    """Convert Chinese characters to pinyin (optional enhancement)"""
    pinyin_str = ""
    for char in target_text:
        if '\u4e00' <= char <= '\u9fff':
            pinyin_list = pinyin(char, style=Style.NORMAL)
            pinyin_str += pinyin_list[0][0] if isinstance(pinyin_list[0], list) else pinyin_list[0]
        else:
            pinyin_str += char
    return pinyin_str

def select_key_interactive() -> str:
    """显示密钥选择菜单"""
    keys = get_available_keys()
    print("\n可用密钥:")
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key['name']} ({key['length']} 字符, {key['strength']})")
    
    while True:
        try:
            choice = int(input("选择密钥 (1-{}): ".format(len(keys))))
            if 1 <= choice <= len(keys):
                return keys[choice-1]['name']
            print("无效选择")
        except ValueError:
            print("请输入数字")

def generate_password_interactive():
    """交互式密码生成"""
    try:
        # 密钥选择
        keys = get_available_keys()
        if not keys:
            print("未找到密钥，正在生成默认密钥...")
            generate_key()
            keys = get_available_keys()
        
        key_name = select_key_interactive()
        key = load_key(key_name)
        
        # 获取账户名称
        account = input("\n输入账户/软件名称: ").strip()
        if not account:
            raise ValueError("账户名称不能为空")
        
        # 密码选项
        use_pinyin = '\u4e00' <= account[0] <= '\u9fff'
        length = int(input("密码长度 (8-64) [12]: ") or "12")
        use_symbols = input("包含符号? (y/n) [y]: ").lower() != "n"
        use_numbers = input("包含数字? (y/n) [y]: ").lower() != "n"
        use_mixed_case = input("混合大小写? (y/n) [y]: ").lower() != "n"
        deterministic = not args.ant if hasattr(args, 'ant') else input("生成确定性密码? (y/n) [y]: ").lower() != "n"
        
        # 处理输入
        processed_input = convert_to_pinyin(account) if use_pinyin else account
        processed_input += key  # 使用密钥增强
        
        # 生成密码
        generator = PasswordGenerator(
            length=length,
            use_symbols=use_symbols,
            use_numbers=use_numbers,
            use_mixed_case=use_mixed_case
        )
        password = generator.generate_password(processed_input, deterministic=deterministic)
        
        print(f"\n生成的密码: {password}")
    except Exception as e:
        print(f"\n错误: {e}")
    finally:
        input("\n按回车键继续...")

def handle_cli_mode(args):
    """处理命令行模式"""
    if args.new_key:
        generate_key(args.key_name, args.key_length)
        print(f"已生成新密钥: {args.key_name or 'default'}")
        return
    
    if not args.account:
        raise ValueError("命令行模式需要提供账户名称")
    
    # 加载或生成密钥
    keys = get_available_keys()
    if not keys:
        generate_key()
        keys = get_available_keys()
    
    key_name = args.key or keys[0]['name']
    key = load_key(key_name)
    
    # 生成密码
    generator = PasswordGenerator(length=args.length)
    deterministic = not args.ant  # 快速模式默认随机，加--ant则确定
    password = generator.generate_password(args.account + key, deterministic=deterministic)
    
    print(password)

if __name__ == '__main__':
    args, _ = parse_arguments()
    if args.version:
        show_version()
    elif args.help:
        show_help()
    elif args.account or args.new_key:
        handle_cli_mode(args)
    else:
        while True:
            print("\n密码生成器 - 主菜单")
            print("1. 生成密码")
            print("2. 退出")
            choice = input("请选择操作 (1-2): ")
            
            if choice == "1":
                generate_password_interactive()
            elif choice == "2":
                print("感谢使用，再见！")
                sys.exit(0)
            else:
                print("无效选择，请重新输入")
