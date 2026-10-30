def _starts(s):
    b, seen = [0], set()
    for i, ch in enumerate(s):
        if ch in seen:
            b.append(i)
            seen = set()
        seen.add(ch)
    return b


def _pos(S):
    """当前正在处理的字符下标"""
    if 'used' not in S or 'char' not in S:
        return None
    b = _starts(S['s'])
    res, ln, u = S.get('res', 0), S['_line'], len(S['used'])
    if ln == 8:      # res += 1：used 还是旧的
        return b[res - 1] + u if res - 1 < len(b) else None
    if ln == 9:      # used = set()
        return b[res] if res < len(b) else None
    if ln == 10:     # used.add(char)
        return b[res] + u - 1
    return b[res] + u


def _color(S, i, v):
    p = _pos(S)
    if p is None:
        return None
    if i == p:
        return 'blue'
    b = _starts(S['s'])
    g = max(k for k in range(len(b)) if b[k] <= i)
    done = i < p
    if not done:
        return None
    return 'green' if g % 2 == 0 else 'cyan'


def _txt(S):
    if 'used' not in S:
        return '一趟遍历：字符不重复就并入当前划分，重复了就另起一段'
    return f"当前划分已含 {{{', '.join(sorted(S['used'])) or '空'}}}，已封口 ==`{S.get('res', 0)}`== 段，最后还要补上未封口的 1 段"


def _chk(S, B, ret):
    ch, used = S.char, S.used
    if ch in used:
        return f"`'{ch}'` 已在 `used` 里 → 再并入就重复了，==当前划分到此为止=="
    return f"`'{ch}'` 不在 `used` 里 → 可以并入当前划分"


CONFIG = dict(
    num=2405, title='子字符串的最优划分', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · set 记录当前划分',
    tags=['贪心算法', '划分型贪心', '难度分 1355'],
    code='''
class Solution(object):
    def partitionString(self, s):

        used = set()
        res = 0
        for char in s:
            if char in used:
                res += 1
                used = set()
            used.add(char)
        
        return res + 1
''',
    call='Solution().partitionString("abacaba")',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿/青 = 已划好的各段）', cell=90, color=_color, h=260),
        dict(type='set', var='used', fmt=lambda x: str(x), h=240),
    ],
    watch=[('char', 'char', 'blue'), ('res', 'res', 'green')],
    captions={
        'used = set()': lambda S, B, r: ('`used` 记录当前这一段已经出现的字符' if 'char' not in S
                                         else '当前划分封口，`used` 清空：这个字符是==新一段的第一个字符=='),
        'res = 0': '`res` 记录已经封口的段数',
        'for char in s': lambda S, B, r: f"从左到右取下一个字符 `'{S.char}'`",
        'if char in used': _chk,
        'res += 1': '`res` → =={res}==：把前一段封口',
        'used.add': "`'{char}'` 加入当前划分，`used` = {sorted(used)}",
        'return res + 1': '最后一段还没封口，所以答案是 `{res} + 1` = =={res + 1}==',
    },
    cards=dict(
        one_liner='第一段尽量长，剩下的后缀才可能更好划分',
        complexity='时间 `O(n)`，空间 `O(1)`（字符集大小）',
        problem=['把字符串切成若干段，每段内字符==互不重复==，求最少段数',
                 '示例：`"abacaba"` → `4`，如 `ab | ac | ab | a`'],
        quote='对于划分出去的第一个字符串而言，应该尽可能地划分得长一些，这样一来后面剩余的字符串就可能有更好的划分方案。',
        quote_src='—— yiduobo 题解原文',
        idea=['后缀的最优划分段数不会比原串多 → 第一段越长越好',
              '一趟遍历：字符不在 `used` 里就并入，==遇到重复就封口==，清空 `used`',
              '重复的那个字符正好成为下一段的开头'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：循环结束后==最后一段没被计数==，要返回 `res + 1`',
                 '封口后要先清空 `used` 再 `add(char)`，让重复字符进入新一段',
                 '原文本身是 Python 3 可运行的写法，未改动'],
    ),
)
