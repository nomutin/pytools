import subprocess


def copy(text):
    p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=str(text).encode('utf-8'))


def paste():
    p = subprocess.Popen(['pbpaste', 'r'], stdout=subprocess.PIPE, close_fds=True)
    return p.communicate()[0].decode('utf-8')
