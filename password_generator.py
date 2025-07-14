from typing import Tuple, Optional
import hashlib
import secrets
import string

class PasswordGenerator:
    def __init__(self, 
                 length: int = 12,
                 use_symbols: bool = True,
                 use_numbers: bool = True,
                 use_mixed_case: bool = True):
        """
        Initialize password generator with configurable options
        
        Args:
            length: Desired password length (8-64)
            use_symbols: Include special characters
            use_numbers: Include digits
            use_mixed_case: Include both upper/lowercase
        """
        self.length = max(8, min(length, 64))
        self.use_symbols = use_symbols
        self.use_numbers = use_numbers
        self.use_mixed_case = use_mixed_case

    def generate_password(self, input_str: str, salt: Optional[str] = None, deterministic: bool = True) -> str:
        """
        从输入字符串生成安全密码
        
        参数:
            input_str: 基础输入字符串
            salt: 可选的salt增加熵值
            deterministic: 是否生成确定性密码
            
        返回:
            生成的密码字符串
        """
        # 根据选项构建字符集
        chars = string.ascii_lowercase
        if self.use_mixed_case:
            chars += string.ascii_uppercase
        if self.use_numbers:
            chars += string.digits
        if self.use_symbols:
            chars += string.punctuation

        # 生成安全哈希(带salt)
        if salt is None:
            if deterministic:
                # 使用输入字符串的哈希作为确定性salt
                salt = hashlib.sha256(input_str.encode()).hexdigest()[:16]
            else:
                salt = secrets.token_hex(8)
        salted_input = f"{input_str}:{salt}"
        
        # Use PBKDF2 for key derivation
        dk = hashlib.pbkdf2_hmac(
            'sha256',
            salted_input.encode(),
            salt.encode(),
            100000,
            dklen=64
        )
        
        # Convert to password using selected character set
        password = []
        for i in range(self.length):
            index = int.from_bytes(dk[i:i+1], 'big') % len(chars)
            password.append(chars[index])
        
        return ''.join(password)

    def generate_random_password(self) -> str:
        """
        Generate completely random password
        
        Returns:
            Random password using configured options
        """
        chars = string.ascii_lowercase
        if self.use_mixed_case:
            chars += string.ascii_uppercase
        if self.use_numbers:
            chars += string.digits
        if self.use_symbols:
            chars += string.punctuation
            
        return ''.join(secrets.choice(chars) for _ in range(self.length))
