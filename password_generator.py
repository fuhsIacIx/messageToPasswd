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

    def generate_password(self, input_str: str, salt: Optional[str] = None) -> str:
        """
        Generate secure password from input string
        
        Args:
            input_str: Input string to base password on
            salt: Optional salt for additional entropy
            
        Returns:
            Generated password string
        """
        # Build character set based on options
        chars = string.ascii_lowercase
        if self.use_mixed_case:
            chars += string.ascii_uppercase
        if self.use_numbers:
            chars += string.digits
        if self.use_symbols:
            chars += string.punctuation

        # Generate secure hash with salt
        if salt is None:
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
