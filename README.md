# OpenCPC

## Developing
We are currently using the latest version of Ubuntu running in a VirtualBox to do most of development, but if you are already on an Ubuntu environment there shouldn't be any issues.

**This section is incomplete.**

Install the latest version of Ubuntu and VirtualBox and set it up. Install Visual Studio Code and PyLint, as well as enabling PyLint https://code.visualstudio.com/docs/python/linting .

Your settings.json in VSCode should be something like this:

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pycodestyleEnabled": true,
    "python.linting.pycodestyleArgs": ["--max-line-length", "100"],
    "editor.rulers": [
        80
    ],
    "python.pythonPath": "/usr/bin/python3"
}
```
