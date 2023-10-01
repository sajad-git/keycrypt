from cryptography.fernet import Fernet
import win32con
from win32gui import SendMessage
from winreg import (
    CloseKey, OpenKey, QueryValueEx, SetValueEx,
    HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE,
    KEY_ALL_ACCESS, KEY_READ, REG_EXPAND_SZ, REG_SZ
)

def env_keys(user=True):
    """
    Get the Windows Registry root and subkey for environment variables.

    Args:
        user (bool): If True, retrieves the user's environment key;
                     otherwise, retrieves the system-wide environment key.

    Returns:
        tuple: A tuple containing the Windows Registry root and subkey.
               For user=True, it returns (HKEY_CURRENT_USER, 'Environment').
               For user=False, it returns (HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment').
    """
    if user:
        root = HKEY_CURRENT_USER
        subkey = 'Environment'
    else:
        root = HKEY_LOCAL_MACHINE
        subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    return root, subkey


def get_secret(name, KeyCrypt_key='KeyCrypt_key', user=True):
    """
    Retrieve a secret value from the Windows Registry and decrypt it if necessary.

    Args:
        name (str): The name of the secret to retrieve.
        KeyCrypt_key (str): The name of the encryption key in the registry.
                            Defaults to 'KeyCrypt_key'.
        user (bool): If True, retrieves the user's environment key;
                     otherwise, retrieves the system-wide environment key.

    Returns:
        str: The decrypted secret value, or an empty string if not found or an error occurs.
    """
    if KeyCrypt_key != None:
        name = 'KeyCrypt_'+name
    root, subkey = env_keys(user)
    key = OpenKey(root, subkey, 0, KEY_READ)
    try:
        value, _ = QueryValueEx(key, name)
    except WindowsError:
        return ''
    if KeyCrypt_key==None:
        return value
    f = Fernet(get_secret(KeyCrypt_key, KeyCrypt_key=None))
    return  f.decrypt(value).decode()
    

def set_default_key(KEY):
    """
    Set the default encryption key in the Windows Registry.

    Args:
        KEY (str): The encryption key to set as the default.

    Returns:
        None
    """
    key = OpenKey(HKEY_CURRENT_USER, 'Environment', 0, KEY_ALL_ACCESS)
    SetValueEx(key, 'KeyCrypt_key', 0, REG_EXPAND_SZ, KEY)
    CloseKey(key)
    SendMessage(
        win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')

def set_secret(name, value):
    """
    Encrypt and set a secret value in the Windows Registry.

    Args:
        name (str): The name of the secret to set.
        value (str): The value of the secret to encrypt and store.

    Returns:
        None
    """
    name = 'KeyCrypt_'+name
    KEY = get_secret('KeyCrypt_key', KeyCrypt_key=None)
    if KEY == '':
        KEY = Fernet.generate_key()
        print('new Fernet key generated .')
        set_default_key(KEY.decode())
        
    key = OpenKey(HKEY_CURRENT_USER, 'Environment', 0, KEY_ALL_ACCESS)
    f = Fernet(KEY)
    SetValueEx(key, name, 0, REG_EXPAND_SZ, f.encrypt(value.encode()).decode())
    CloseKey(key)
    SendMessage(
        win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')