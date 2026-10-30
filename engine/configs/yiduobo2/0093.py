S0 = '1010'
SEG_COLORS = ['blue', 'pink', 'purple', 'cyan']


def _draw(cv, S, B, box, T):
    """原串 S0：已经截好的部分按段上色，剩余部分（当前层的 s）用框标出"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '原串（颜色 = 已截取的段，框 = 剩余的 s）', 24, T['muted'], bold=True)
    rest = S.get('s')
    now = S.get('now') or []
    if rest is None:
        return
    off = len(S0) - len(rest)
    seg = {}
    p = 0
    for k, part in enumerate(now):
        for _ in part:
            if p < off:
                seg[p] = k
            p += 1
    cw = 92
    sx = x0 + (x1 - x0 - cw * len(S0)) / 2
    y = y0 + 52
    if off < len(S0):
        cv.rect((sx + off * cw - 6, y - 8, sx + len(S0) * cw + 2, y + 86), outline=T['yellow'], width=3, r=12)
        cv.text((sx + len(S0) * cw + 12, y + 40), f's = "{rest}"', 22, T['yellow'], anchor='lm', mono=True, bold=True)
    else:
        cv.text((sx + len(S0) * cw + 12, y + 40), 's = ""', 22, T['yellow'], anchor='lm', mono=True, bold=True)
    for k, ch in enumerate(S0):
        X = sx + k * cw
        c = T[SEG_COLORS[seg[k]]] if k in seg else T['panel2']
        cv.rect((X + 4, y, X + cw - 4, y + 78), fill=c, r=10, outline=T['border'], width=1)
        cv.text((X + cw / 2, y + 39), ch, 38, T['bg'] if k in seg else T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, y + 94), k, 18, T['dim'], anchor='mt', mono=True)


def _cap_level(S, B, ret):
    if S.level == 0:
        return '`level == 0`：四段都截好了'
    return f'`level = {S.level}`：还要截 {S.level} 段，剩下 `"{S.s}"`'


def _cap_long(S, B, ret):
    L = len(S.s)
    if 3 * S.level < L:
        return f'`3×{S.level} = {3 * S.level} < {L}`：剩下的太长，每段最多 3 位也分不完 → ==提前 return=='
    return f'`3×{S.level} ≥ {L}`：不会太长'


def _cap_short(S, B, ret):
    L = len(S.s)
    if S.level > L:
        return f'`{S.level}` 段 > 剩下 `{L}` 位：长度不足，每段至少 1 位 → ==提前 return=='
    return f'`{S.level} ≤ {L}`：长度也够 → 开始尝试截 1～3 位'


def _cap_two(S, B, ret):
    if S.s[0] == '0':
        return "`s[0] = '0'`：截两位或三位都会==以 0 开头== → 不行"
    if len(S.s) < 2:
        return '只剩 1 位，截不了两位'
    return "`s[0]` 不是 `'0'` 且至少 2 位 → 试试截两位"


def _cap_three(S, B, ret):
    if len(S.s) < 3:
        return f'剩 {len(S.s)} 位，截不了三位'
    v = int(S.s[:3])
    if v > 255:
        return f'`{v} > 255` → 不能截三位'
    return f'`{v} ≤ 255` → 试试截三位'


def _pop(S, B, ret):
    return f"回溯：弹出 `'{B.now[-1]}'`，换一种截法"


CONFIG = dict(
    num=93, title='复原 IP 地址', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯 · 每次截 1～3 位',
    tags=['热题173'],
    code='''
class Solution(object):
    def restoreIpAddresses(self, s):
        res = []
        self.dfs(4, s, [], res)
        return ['.'.join(x) for x in res]

    def dfs(self, level, s, now, res):
        if level == 0:
            if len(s) == 0:
                res.append(now[:])
            return
        if 3 * level < len(s):
            return
        if level > len(s):
            return

        now.append(s[0])
        self.dfs(level - 1, s[1:], now, res)
        now.pop()
        if s[0] != '0' and len(s) >= 2:
            now.append(s[0 : 2])
            self.dfs(level - 1, s[2:], now, res)
            now.pop()
            if len(s) >= 3 and int(s[0 : 3]) <= 255:
                now.append(s[0 : 3])
                self.dfs(level - 1, s[3:], now, res)
                now.pop()
''',
    call=f"Solution().restoreIpAddresses('{S0}')",
    expect=['1.0.1.0'],
    views=[
        dict(type='custom', draw=_draw, h=160),
        dict(type='stack', var='now', label='now（已截取的段）', h=100),
        dict(type='calls', h=210, hide=('now', 'res')),
        dict(type='stack', var='res', label='res', fmt=lambda x: '.'.join(x), h=100),
    ],
    watch=[('level', 'level', 'yellow'), ('s', 's', 'cyan')],
    captions={
        'res = []': '`res` 收集所有方案',
        'self.dfs(4, s, [], res)': '`level = 4`：==还要截出几段==；从完整的 `s` 开始',
        'if level == 0': _cap_level,
        'if len(s) == 0': lambda S, B, r: ('剩余为空 → ==找到一种分割方案==' if len(S.s) == 0
                                           else f'还剩 `"{S.s}"` 没用完 → 不合法'),
        'res.append(now[:])': '复制 `now` 加入 res：`{res[-1]}`',
        11: '返回上一层',
        'if 3 * level < len(s)': _cap_long,
        13: '剪枝：返回',
        'if level > len(s)': _cap_short,
        15: '剪枝：返回',
        'now.append(s[0])': "截取 1 位 `'{s[0]}'`",
        'self.dfs(level - 1, s[1:]': '处理剩下的 `"{B.s[1:]}"`，还要 `{B.level - 1}` 段',
        "if s[0] != '0' and len(s) >= 2": _cap_two,
        'now.append(s[0 : 2])': "截取 2 位 `'{s[0:2]}'`",
        'self.dfs(level - 1, s[2:]': '处理剩下的 `"{B.s[2:]}"`，还要 `{B.level - 1}` 段',
        'if len(s) >= 3 and int(s[0 : 3]) <= 255': _cap_three,
        'now.append(s[0 : 3])': "截取 3 位 `'{s[0:3]}'`",
        'self.dfs(level - 1, s[3:]': '处理剩下的 `"{B.s[3:]}"`，还要 `{B.level - 1}` 段',
        'now.pop()': _pop,
        "return ['.'.join(x)": '每个方案用 `.` 连起来：`{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='每次截 1～3 位作为一段，剩余太长或太短就提前 return',
        complexity='时间 `O(3^4 · n)`，空间 `O(n)`（不计返回值）',
        problem=['有效 IP：恰好 4 个 `0`–`255` 的整数，用 `.` 分隔，==不能有前导 0==',
                 '给只含数字的字符串 `s`，返回所有能通过插入 `.` 得到的有效 IP（不能重排或删除数字）',
                 '示例：`"101023"` → `["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]`',
                 '本视频：`"1010"` → `["1.0.1.0"]`'],
        quote='每次尝试截取1至3位作为这个部分的值，然后继续考虑剩余的s。截取时需要判断==位数为两位或三位时不能以0开头==，以及位数为三位时是否小于等于255。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(level, s, now, res)`：还要截 `level` 段，剩余字符串是 `s`',
              '处理完四轮（`level == 0`）且 `s` 正好为空 → 找到一种方案',
              '剩余太长（`> 3·level`）或太短（`< level`）都可以==提前 return=='],
        result='`["1.0.1.0"]` ✓：`"01"`、`"010"` 这种前导 0 都被排除',
        summary=['每层至多 3 个分支、共 4 层，再算上切片和拼接 → `O(3^4 · n)`',
                 '两位、三位都要求 `s[0] != \'0\'`；只有三位才需要和 255 比较',
                 '`now` 是共享列表：`append` → 递归 → `pop` 恢复现场；存答案要复制 `now[:]`',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
