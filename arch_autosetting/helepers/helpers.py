import subprocess
import re
import os
import time
import Quartz

COMMANDS = {'arch': ['clip', 'clip --no_enter', 'type', 'type --no_enter', 'press', 'press --no_enter', 'wait']}

keyboardMapping = ({
    'a': 0x00, 's': 0x01, 'd': 0x02, 'f': 0x03, 'h': 0x04, 'g': 0x05, 'z': 0x06, 'x': 0x07, 'c': 0x08,
    'v': 0x09, 'b': 0x0b, 'q': 0x0c, 'w': 0x0d, 'e': 0x0e, 'r': 0x0f, 'y': 0x10, 't': 0x11, '1': 0x12,
    '!': 0x12, '2': 0x13, '@': 0x13, '3': 0x14, '#': 0x14, '4': 0x15, '$': 0x15, '6': 0x16, '^': 0x16,
    '5': 0x17, '%': 0x17, '=': 0x18, '+': 0x18, '9': 0x19, '(': 0x19, '7': 0x1a, '&': 0x1a, '-': 0x1b,
    '_': 0x1b, '8': 0x1c, '*': 0x1c, '0': 0x1d, ')': 0x1d, ']': 0x1e, '}': 0x1e, 'o': 0x1f, 'u': 0x20,
    '[': 0x21, '{': 0x21, 'i': 0x22, 'p': 0x23, 'l': 0x25, 'j': 0x26, "'": 0x27, '"': 0x27, 'k': 0x28,
    ';': 0x29, ':': 0x29, '\\': 0x2a, '|': 0x2a, ',': 0x2b, '<': 0x2b, '/': 0x2c, '?': 0x2c, 'n': 0x2d,
    'm': 0x2e, '.': 0x2f,  '>': 0x2f, '`': 0x32, '~': 0x32, ' ': 0x31, 'space': 0x31, '\r': 0x24,
    '\n': 0x24, 'enter': 0x24, 'return': 0x24, '\t': 0x30, 'tab': 0x30, 'backspace': 0x33, '\b': 0x33,
    'esc': 0x35, 'escape': 0x35, 'command': 0x37, 'shift': 0x38, 'shiftleft': 0x38, 'capslock': 0x39,
    'option': 0x3a, 'optionleft': 0x3a, 'alt': 0x3a, 'altleft': 0x3a, 'ctrl': 0x3b, 'ctrlleft': 0x3b,
    'shiftright': 0x3c, 'optionright': 0x3d, 'ctrlright': 0x3e, 'fn': 0x3f, 'f17': 0x40,
    'volumeup': 0x48, 'volumedown': 0x49, 'volumemute': 0x4a,
    'help': 0x72, 'pageup': 0x74, 'pgup': 0x74, 'del': 0x75, 'delete': 0x75, 'f4': 0x76, 'end': 0x77, 'f2': 0x78,
    'pagedown': 0x79, 'pgdn': 0x79, 'f1': 0x7a, 'left': 0x7b, 'right': 0x7c, 'down': 0x7d, 'up': 0x7e,
    'yen': 0x5d, 'underscore': 0x5e, 'comma': 0x5f, 'eisu': 0x66, 'kana': 0x68,
})

for c in 'abcdefghijklmnopqrstuvwxyz':
    keyboardMapping[c.upper()] = keyboardMapping[c]


def _isShiftCharacter(character):
    return character.isupper() or character in '~!@#$%^&*()_+{}|:"<>?'


def _autoPause(_pause):
    if _pause:
        time.sleep(0.1)


def keyUpDown(upDown, key, _pause=True):
    assert upDown in ('up', 'down'), "upDown argument must be 'up' or 'down'"

    key = key.lower() if len(key) > 1 else key
    if key not in keyboardMapping or keyboardMapping[key] is None:
        return

    try:
        if _isShiftCharacter(key):
            key_code = keyboardMapping[key.lower()]

            event = Quartz.CGEventCreateKeyboardEvent(None, keyboardMapping['shift'], upDown == 'down')
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            time.sleep(0.01)

        else:
            key_code = keyboardMapping[key]

        event = Quartz.CGEventCreateKeyboardEvent(None, key_code, upDown == 'down')
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
        time.sleep(0.01)

    except KeyError:
        raise RuntimeError("Key %s not implemented." % key)

    _autoPause(_pause)


def press(keys, _pause=True):
    keys = [keys] if type(keys) == str else keys

    for k in keys:
        keyUpDown('down', k, _pause=False)
        keyUpDown('up', k, _pause=False)

    _autoPause(_pause)


def typewrite(message, _pause=True):
    for s in message:
        press(s, _pause=False)

    _autoPause(_pause)


def hotkey(*args, **kwargs):
    for _c in args:
        keyUpDown('down', _c, _pause=False)

    for _c in reversed(args):
        keyUpDown('up', _c, _pause=False)

    _autoPause(kwargs.get('_pause', True))


def copy(text):
    p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=str(text).encode('utf-8'))


def read_code_from_md(_md, code_start='~~~code', code_end='~~~', command_letter='|', default_command=''):
    """read_code_from_md()
    markdownファイルからコード部分及び特殊操作を抜き出す

    Args:
        _md (str): markdown file
        code_start: _md内から抽出するコードの開始文字列、デフォルトは'~~~code'
        code_end: _md内から抽出するコードの終了文字列、デフォルトは'~~~'
        command_letter: 各行のコード部とコマンド部を分割する文字列
        default_command: コマンドが存在しない場合のデフォルトコマンド

    Return:
        dict: {章の番号:[[コード,コマンド],[コード,コマンド]...],章の番号:[[コード,コマンド],...]]...}

    """
    assert code_start != code_end, '_code_startと_code_endは異なる文字列を指定してください'

    with open(_md, 'r') as file:
        sectors = re.findall(r'(?<=### )\d+.*?(?=###)', repr(file.read()))

        all_codes = {}

        for sector_str in sectors:
            sector_number = int(sector_str[0])

            if code_start not in sector_str:
                all_codes[sector_number] = []

            else:
                sector_code_all = re.findall(f'(?<={code_start}).*?(?={code_end})', sector_str)
                code_lines = [line for pg in sector_code_all for line in pg.split('\\n') if line != '']

                separated_codes = []

                for code_line in code_lines:

                    if command_letter not in code_line:
                        separated_codes.append([code_line, default_command])

                    else:
                        _code = code_line[:code_line.find(command_letter)-1]
                        _command = code_line[code_line.find(command_letter)+1+len(command_letter):]
                        separated_codes.append([_code, _command])

                all_codes[sector_number] = separated_codes

        return all_codes


def generate_code_and_command(_code_dict, sections):
    if len(sections) == 1:
        sections = [sections]

    code_part = []
    for section in sections:
        if _code_dict[section] is None:
            pass
        else:
            code_part.extend(_code_dict[section])

    for line in code_part:
        yield line[0], line[1]


def is_valid_command(_section_code_list: list, section_number, _environment='arch'):
    """ _section_code_list must be two dimension"""

    assert _environment in COMMANDS, f'{_environment} is not in {os.path.basename(__file__)}/COMMANDS'

    for line_number, line in enumerate(_section_code_list):
        _, _command = line

        if _command not in COMMANDS[_environment]:
            assert False, f'invalid : section {section_number+1}, line {line_number+1}, command {_command} is not in ' \
                          f'{os.path.basename(__file__)}/COMMANDS'
        else:
            pass


def run_command_arch(cmd_line):
    code, command = cmd_line

    if 'clip' in command:
        copy(code)
        keyUpDown('down', 'command')
        press('v')
        keyUpDown('up', 'command')
        if '--no_enter' not in command:
            press('enter')

    elif 'type' in command:
        typewrite(code)
        if '--no_enter' not in command:
            press('enter')

    elif 'press' in command:
        press(code)
        if '--no_enter' not in command:
            press('enter')

    elif command == 'wait':
        time.sleep(float(code))



