## KeyCrypt

Have you ever found yourself needing to include sensitive information like passwords or cookies in your code? Often, as you're about to type out these confidential words, your programming instincts kick in and raise a red flag.
You start to wonder, "Is it really safe to embed the password directly into the code?"

A quick search usually confirms your suspicion – it's not a recommended practice. So, what's the solution?

The solution is actually quite straightforward. Instead of hardcoding the sensitive word directly into your script, you can define it once as an environment variable with a unique name. Then, whenever you need to use it in your code, simply call the variable by its name.

After doing this for a project, I thought it could be helpful to simplify this process for both myself and others. So, I developed a simple package that does this automatically. I'll encode the sensitive word exclusively for you and securely store it. When you need to use the secret word, it will be decoded with your private key, allowing you to seamlessly integrate it into your code.

This approach adds an extra layer of security, making it more challenging for anyone, even if they have access to your environment variables, to discern your secret word easily. While your secret word isn't entirely invulnerable, this method certainly makes it more time-consuming and complex for unauthorized access.

<p align="center">
  <img src="https://github.com/sajad-git/keycrypt/blob/crawler/readme/lugu.jpg?raw=true" alt="Sublime's custom image"/>
</p>
<br>

## Installation

KeyCrypt requires the following packages:

- cryptography == 41.0.1

  
```python
pip install cryptography == 41.0.1
```

# Usage
```python
from keycrypt import get_secret, set_secret
```

***
***
### set_secret:
at the first time you should set your secret in environment variables. so :
```python
set_secret(name='gmail_pass' , value='your_password')
```

### get_secret:
all the next time you can just call your password with it's name. so :
+ Create a connection
```python
set_secret(name='gmail_pass') # --> returns 'your_password'
```
## usage sample:
<p align="center">
  <img src="https://github.com/sajad-git/keycrypt/blob/crawler/readme/sample_code.jpg?raw=true" alt="Sublime's custom image"/>
</p>

<p align="center">
  <img src="https://github.com/sajad-git/keycrypt/blob/crawler/readme/env.jpg?raw=true" alt="Sublime's custom image"/>
</p>
