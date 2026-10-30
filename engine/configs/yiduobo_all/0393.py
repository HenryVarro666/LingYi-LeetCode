def _bits(S):
    return [format(x, '08b') for x in S['data']]


def _color(S, i, v):
    if 'now' not in S:
        return None
    now = S['now']
    cl = S.get('check_len')
    if cl is not None and S.get('_line', 0) >= 14 and now - 1 >= 0 and i == now:
        return 'cyan'
    return None


def _text(S):
    if 'now' not in S:
        return '看每个字节的高位：`0xxxxxxx` 单字节；`110`/`1110`/`11110` 开头是 2/3/4 字节字符；后续字节必须是 `10xxxxxx`'
    now = S['now']
    d = S['data']
    if now >= len(d):
        return '所有字节都检查完，没有出现非法情况'
    cl = S.get('check_len')
    return f"当前字节 `{format(d[now], '08b')}`" + (f'，后面还需要 ==`{cl}`== 个 `10xxxxxx`' if cl and S.get('_line', 0) >= 14 else '')


CONFIG = dict(
    num=393, title='UTF-8 编码验证', difficulty='Medium', category='位运算',
    author='yiduobo', technique='位掩码逐字符检测',
    tags=[],
    code='''
class Solution(object):
    def validUtf8(self, data):

        now = 0
        while now < len(data):
            if data[now] & 128 == 0:
                now += 1
            else:
                if data[now] & 64 == 0:
                    return False
                if data[now] & 32 == 0:
                    check_len = 1
                elif data[now] & 16 == 0:
                    check_len = 2
                elif data[now] & 8 == 0:
                    check_len = 3
                else:
                    return False
                
                now += 1
                while now < len(data) and check_len > 0:
                    if data[now] & 128 != 0 and data[now] & 64 == 0:
                        now += 1
                        check_len -= 1
                    else:
                        return False

                if check_len > 0:
                    return False

        return True
''',
    call='Solution().validUtf8([197, 130, 1, 230, 136, 145])',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var=_bits, label='data 每个字节的二进制', cell=150, pointers={'now': 'blue'},
             color=_color, dim=lambda S, i, v: 'now' in S and i < S['now'] - (1 if S.get('_line', 0) >= 14 else 0) and False, h=240),
        dict(type='text', fn=lambda S: (f"`{S['data'][S['now']]}` & 128 = {S['data'][S['now']] & 128}，& 64 = {S['data'][S['now']] & 64}，& 32 = {S['data'][S['now']] & 32}"
                                         if 'now' in S and S['now'] < len(S['data']) else ''), h=70),
    ],
    watch=[('now', 'now', 'blue'), 'check_len'],
    captions={
        'while now < len(data) and check_len': lambda S, B, r: (f"还要检查 `{S['check_len']}` 个后续字节，且 `now = {S['now']}` 没越界 → 继续" if S['check_len'] > 0 and S['now'] < len(S['data'])
                                                              else ('后续字节检查完了' if S['check_len'] == 0 else '字节不够了，数据提前结束')),
        'while now < len(data)': lambda S, B, r: (f"`now = {S['now']} < {len(S['data'])}`：还有字节没检查，处理下一个 UTF-8 字符" if S['now'] < len(S['data'])
                                                  else f"`now = {S['now']}` 已到末尾：每个字符都合法"),
        'now = 0': '`now` 指向当前要检查的字节，从 0 开始',
        'data[now] & 128 == 0': lambda S, B, r: (f"`{S['data'][S['now']]} & 128 = 0`：最高位是 0，形如 `0xxxxxxx` → 单字节字符" if S['data'][S['now']] & 128 == 0
                                                  else f"`{S['data'][S['now']]} & 128 ≠ 0`：最高位是 1，是多字节字符的开头"),
        7: '单字节字符，只占这一个字节，`now` → {now}',
        20: '开头字节已读，`now` → {now}，接着检查后面的字节',
        23: '后续字节合法，`now` → {now}',
        'if data[now] & 64 == 0': lambda S, B, r: (f"`& 64 = 0`：形如 `10xxxxxx`，它只能做后续字节，不能当开头 → ==非法==" if S['data'][S['now']] & 64 == 0
                                                  else f"`& 64 ≠ 0`：形如 `11xxxxxx`，可以做开头"),
        'if data[now] & 32 == 0': lambda S, B, r: (f"`& 32 = 0`：形如 `110xxxxx` → 共 2 个字节" if S['data'][S['now']] & 32 == 0 else "`& 32 ≠ 0`：至少是 `111xxxxx`，继续看"),
        'elif data[now] & 16 == 0': lambda S, B, r: (f"`& 16 = 0`：形如 `1110xxxx` → 共 3 个字节" if S['data'][S['now']] & 16 == 0 else "`& 16 ≠ 0`：至少是 `1111xxxx`，继续看"),
        'elif data[now] & 8 == 0': lambda S, B, r: (f"`& 8 = 0`：形如 `11110xxx` → 共 4 个字节" if S['data'][S['now']] & 8 == 0 else "`& 8 ≠ 0`：形如 `11111xxx` → ==非法=="),
        'check_len = 1': '共 2 个字节：除开头外还要检查 `check_len = 1` 个后续字节',
        'check_len = 2': '共 3 个字节：除开头外还要检查 `check_len = 2` 个后续字节',
        'check_len = 3': '共 4 个字节：除开头外还要检查 `check_len = 3` 个后续字节',
        'if data[now] & 128 != 0': lambda S, B, r: (f"`{format(S['data'][S['now']], '08b')}`：最高位 1、次高位 0 → 合法的后续字节 `10xxxxxx`" if S['data'][S['now']] & 128 and not S['data'][S['now']] & 64
                                                    else f"`{format(S['data'][S['now']], '08b')}` 不是 `10xxxxxx` → 后续字节不合法"),
        'check_len -= 1': '还差 `check_len = {check_len}` 个后续字节',
        'if check_len > 0': lambda S, B, r: ('`check_len > 0`：数据结束了，后续字节还没凑够 → ==非法==' if S['check_len'] > 0
                                             else '`check_len = 0`：这个字符的所有字节都合法，回到外层检查下一个字符'),
        'return True': '所有字符都合法，返回 `{ret}`',
    },
    cards=dict(
        one_liner='用 128/64/32/16/8 逐级与运算，判断字符占几个字节',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['UTF-8 字符占 1–4 字节：1 字节 `0xxxxxxx`；n 字节则开头 n 个 `1` 再一个 `0`，后续字节都是 `10xxxxxx`',
                 '`data` 是整数数组（只看每个数最低 8 位），判断是否是合法 UTF-8 编码',
                 '示例：`[197,130,1]` → `true`；`[235,140,4]` → `false`',
                 '本视频：`[197,130,1,230,136,145]` → `true`'],
        quote='用data分别与128、64、32、16、8做与运算，判断当前utf8字符属于下列哪一种',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `& 128`：为 0 就是单字节；否则 `& 64` 为 0 说明它是 `10xxxxxx`，不能当开头',
              '再用 `& 32`、`& 16`、`& 8` 分出 2/3/4 字节，得到后续还要检查的字节数 `check_len`',
              '后续字节逐个检查是否 `10xxxxxx`；全部通过再处理下一个字符，非法就直接 `False`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：后续字节要检查最高位是 1 且次高位是 0；数据提前结束也非法',
                 '`11111xxx` 开头非法（UTF-8 最多 4 字节）',
                 '原文本身是 Python 2/3 通用写法，代码一字未改'],
    ),
)
