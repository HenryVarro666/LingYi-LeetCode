IN4 = '172.16.254.1'
IN6 = '1:G:0:0:0:0:0:0'
CHAR_LINES = (13, 28, 30, 32, 34)
CI = 'part.index(char) if _line in (13, 28, 30, 32, 34) else None'


def _is6(S):
    return (S.get('_line') or 0) >= 21


def _text(S):
    IP = S.get('IP')
    if IP is None:
        return ''
    if isinstance(IP, list) and _is6(S):
        raw = ':'.join(IP)
    elif isinstance(IP, list) and len(IP) > 1:
        raw = '.'.join(IP)
    elif isinstance(IP, list):
        raw = IP[0]
    else:
        raw = IP
    kind = '==IPv6== 分支' if _is6(S) else ('==IPv4== 分支' if isinstance(IP, list) and len(IP) > 1 else '判断类型')
    return f"输入 `{raw}` · {kind}"


def _cur_part(S):
    IP, part = S.get('IP'), S.get('part')
    if not isinstance(IP, list) or part is None or (S.get('_line') or 0) in (3, 21):
        return None
    for k, x in enumerate(IP):
        if x == part:
            return k
    return None


def _char_idx(S):
    if S.get('_line') not in CHAR_LINES or 'char' not in S or 'part' not in S:
        return None
    return S['part'].index(S['char'])


def _cap_part(S, B, ret):
    k = _cur_part(S)
    if k is None or ('part' in B and B.part == S.part):
        return f'{len(S.IP)} 段都检查完，循环结束'
    return f'检查第 {k + 1} 段 `{S.part!r}`'


def _cap_ord4(S, B, ret):
    c = S.char
    o = ord(c)
    if o < 48 or o > 57:
        return f'`{c!r}` 的 ASCII 码 `{o}` 不在 48~57 → 不是数字'
    return f'`{c!r}` 的 ASCII 码 `{o}` 在 48~57 之间 → 是数字'


def _cap_hex(lo, hi, name):
    def f(S, B, ret):
        c = S.char
        o = ord(c)
        if lo <= o <= hi:
            return f'`{c!r}` 的 ASCII 码 `{o}` 在 {lo}~{hi}（{name}）→ 合法，看下一个字符'
        return f'`{c!r}` 的 ASCII 码 `{o}` 不在 {lo}~{hi}（{name}）'
    return f


CONFIG = dict(
    num=468, title='验证IP地址', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按题意模拟 · split + 逐字符检查',
    tags=['热题173'],
    code='''
class Solution(object):
    def validIPAddress(self, IP):
        IP = IP.split('.')
        if len(IP) > 1:
            if len(IP) != 4:
                return 'Neither'
            for part in IP:
                if len(part) == 0:
                    return 'Neither'
                if part[0] == '0' and len(part) > 1:
                    return 'Neither'
                for char in part:
                    if ord(char) < 48 or ord(char) > 57:
                        return 'Neither'
                if int(part) > 255:
                    return 'Neither'

            return 'IPv4'

        else:
            IP = IP[0].split(':')
            if len(IP) != 8:
                return 'Neither'
            for part in IP:
                if len(part) > 4 or len(part) == 0:
                    return 'Neither'
                for char in part:
                    if ord(char) >= 48 and ord(char) <= 57:
                        continue
                    if ord(char) >= 65 and ord(char) <= 70:
                        continue
                    if ord(char) >= 97 and ord(char) <= 102:
                        continue
                    return 'Neither'

            return 'IPv6'
''',
    call=f"s = Solution()\n[s.validIPAddress('{IN4}'), s.validIPAddress('{IN6}')]",
    expect=['IPv4', 'Neither'],
    skip=['for char in part', 'continue'],
    max_steps=70,
    views=[
        dict(type='text', fn=_text, h=56),
        dict(type='array', var=lambda S: S['IP'] if isinstance(S.get('IP'), list) else None,
             label='IP（切分后的各段；黄 = 正在检查）', cell=110,
             color=lambda S, i, v: 'yellow' if i == _cur_part(S) else None),
        dict(type='string', var=lambda S: S['part'] if _cur_part(S) is not None else None,
             label='当前段 part（逐字符检查）', cell=90,
             pointers={CI: 'pink'}, pointer_labels={CI: 'char'}),
        dict(type='text', fn=lambda S: (f"`ord({S['char']!r}) = {ord(S['char'])}`：数字 48~57 · 大写 A~F 65~70 · 小写 a~f 97~102"
                                        if _char_idx(S) is not None else '数字 0~9 = ASCII 48~57 · A~F = 65~70 · a~f = 97~102'),
             size=24, h=56),
    ],
    setup='',
    watch=[('part', 'part', 'yellow'), ('char', lambda S: S['char'] if _char_idx(S) is not None else None, 'pink'),
           ('len(IP)', lambda S: len(S['IP']) if isinstance(S.get('IP'), list) else None)],
    captions={
        "IP = IP.split('.')": lambda S, B, r: (f'先按 `.` 切分：`IP = {S.IP}`' if len(S.IP) > 1
                                               else f'第二个输入 `{S.IP[0]}`：按 `.` 切分只得到 1 段'),
        'if len(IP) > 1': lambda S, B, r: (f'切出了 `{len(S.IP)}` 段 → 含有 `.`，按 ==IPv4== 检查' if len(S.IP) > 1
                                           else '只有 1 段 → 不含 `.`，转去按 ==IPv6== 检查'),
        'if len(IP) != 4': '`len(IP) = {len(IP)}`：IPv4 必须==恰好 4 段==',
        7: _cap_part,
        'if len(part) == 0': '`{part!r}` 非空（`1..2.3` 这种空段不合法）',
        "if part[0] == '0'": lambda S, B, r: (f'`{S.part!r}` 首位是 0 且长度 > 1 → 前导零，不合法' if S.part[0] == '0' and len(S.part) > 1
                                              else f'`{S.part!r}` 没有前导零'),
        'if ord(char) < 48': _cap_ord4,
        'if int(part) > 255': lambda S, B, r: (f'全是数字，再看大小：`int({S.part!r}) = {int(S.part)}` ≤ 255，这段合法'
                                               if int(S.part) <= 255 else f'`{int(S.part)}` > 255 → 不合法'),
        "return 'IPv4'": '4 段都合法 → 返回 =={ret}==',
        "IP = IP[0].split(':')": '改按 `:` 切分：`IP = {IP}`',
        'if len(IP) != 8': '`len(IP) = {len(IP)}`：IPv6 必须==恰好 8 段==',
        24: _cap_part,
        'if len(part) > 4 or': '`{part!r}` 长度为 {len(part)}，在 1~4 之间',
        'if ord(char) >= 48': _cap_hex(48, 57, '数字'),
        'if ord(char) >= 65': _cap_hex(65, 70, '大写 A~F'),
        'if ord(char) >= 97': _cap_hex(97, 102, '小写 a~f'),
        34: '`{char!r}` 不属于任何一种十六进制字符 → 返回 =={ret}==',
        "return 'IPv6'": '8 段都合法 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='先按 . 切分看是不是 IPv4，否则按 : 切分看是不是 IPv6，逐段逐字符检查',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断字符串 `queryIP` 是 `"IPv4"`、`"IPv6"` 还是 `"Neither"`',
                 'IPv4：4 段十进制数 `0~255`，==不能有前导零==，如 `192.168.1.1`',
                 'IPv6：8 段，每段 1~4 位十六进制（大小写均可），==允许前导零==',
                 f'本视频依次验证 `{IN4}` 和 `{IN6}`'],
        quote='首先通过split点或者冒号来确定是ipv4还是ipv6，然后==判断其分割之后的长度是否合法==，接下来对分割之后的每个部分进行判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 `.` 切出多于 1 段 → 只可能是 IPv4，必须恰好 4 段',
              'IPv4 每段：非空、无前导零、全是数字（ASCII 48~57）、不超过 255',
              '否则按 `:` 切分：恰好 8 段，每段长 1~4，字符属于 `0-9 / A-F / a-f`'],
        result='返回 `["IPv4", "Neither"]`：第二个输入的 `G` 超出了十六进制范围',
        summary=['时间 `O(n)`，空间 `O(n)`（切分后的列表）',
                 '易错：IPv4 的 `"0"` 合法，但 `"01"`、`"00"` 不合法；IPv6 允许前导零',
                 '易错：先确认全是数字再 `int(part)`，否则遇到字母会直接报错',
                 '空段（`1..2.3`、`2001::1`）都要拒绝：切分后长度为 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串和行尾空格'],
    ),
)
