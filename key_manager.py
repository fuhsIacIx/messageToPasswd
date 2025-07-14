import os
import secrets
import string
from typing import Optional, List
from datetime import datetime
import json

KEY_DIR = "keys"
DEFAULT_KEY_LENGTH = 32
MIN_KEY_LENGTH = 16
MAX_KEY_LENGTH = 256

class KeyMetadata:
    """Class to store key metadata"""
    def __init__(self, created: str, length: int, strength: str):
        self.created = created
        self.length = length
        self.strength = strength

def ensure_key_dir() -> None:
    """Ensure keys directory exists"""
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

def generate_key(key_name: Optional[str] = None, 
                key_length: int = DEFAULT_KEY_LENGTH,
                encrypt: bool = False) -> str:
    """
    Generate new key file with enhanced security
    
    Args:
        key_name: Custom name for key file (optional)
        key_length: Desired key length (16-256 chars)
        encrypt: Whether to encrypt the key file (TODO)
    
    Returns:
        Path to generated key file
    """
    ensure_key_dir()
    
    # Validate key length
    key_length = max(MIN_KEY_LENGTH, min(key_length, MAX_KEY_LENGTH))
    
    # Generate secure random key
    key_content = ''.join(secrets.choice(
        string.ascii_letters + string.digits + string.punctuation
    ) for _ in range(key_length))
    
    # Generate metadata
    metadata = KeyMetadata(
        created=datetime.now().isoformat(),
        length=key_length,
        strength="strong" if key_length >= 64 else "medium"
    )
    
    # Set default name if not provided
    if key_name is None:
        key_name = f"key_{len(os.listdir(KEY_DIR)) + 1:03d}.key"
    elif not key_name.endswith('.key'):
        key_name += '.key'
    
    key_path = os.path.join(KEY_DIR, key_name)
    
    # Write key and metadata
    with open(key_path, 'w') as f:
        json.dump({
            'key': key_content,
            'metadata': vars(metadata)
        }, f, indent=2)
    
    return key_path

def get_available_keys() -> List[dict]:
    """Get list of available keys with metadata
    
    Returns:
        List of dicts containing key info: 
        {'name': str, 'created': str, 'length': int, 'strength': str}
    """
    ensure_key_dir()
    keys = []
    for fname in os.listdir(KEY_DIR):
        if fname.endswith('.key'):
            try:
                with open(os.path.join(KEY_DIR, fname), 'r') as f:
                    data = json.load(f)
                    keys.append({
                        'name': fname,
                        **data['metadata']
                    })
            except (json.JSONDecodeError, KeyError):
                # Fallback for old format keys
                keys.append({
                    'name': fname,
                    'created': 'unknown',
                    'length': DEFAULT_KEY_LENGTH,
                    'strength': 'legacy'
                })
    return keys

def load_key(key_name: str) -> str:
    """Load key content from file
    
    Args:
        key_name: Name of key file to load
    
    Returns:
        The key content as string
    """
    key_path = os.path.join(KEY_DIR, key_name)
    with open(key_path, 'r') as f:
        try:
            data = json.load(f)
            return data['key']
        except (json.JSONDecodeError, KeyError):
            # Fallback for old format keys
            return f.read().strip()
