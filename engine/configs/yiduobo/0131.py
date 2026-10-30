def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S.get('s')
    if s is None:
        return
    n = len(s)
    # ---- 左边：字符串 s，框出当前判断/分割的子串
    cv.text((x0 + 18, y0 + 4), 's（框 = 正在看的子串）', 24, T['muted'], bold=True)
    if 'right' in S:
        a, b, wc = S['left'], S['right'], T['yellow']
    elif 'index' in S and 'left' in S:
        a, b, wc = S['left'], S['index'], T['cyan']
    else:
        a = b = wc = None
    cs, sx, sy = 72, x0 + 40, y0 + 52
    if a is not None and a <= b:
        cv.rect((sx + a * cs - 5, sy - 6, sx + b * cs + cs - 3, sy + cs + 2), fill=wc, alpha=40, r=10)
        cv.rect((sx + a * cs - 5, sy - 6, sx + b * cs + cs - 3, sy + cs + 2), outline=wc, width=3, r=10)
    for k, ch in enumerate(s):
        X = sx + k * cs
        cv.rect((X + 3, sy, X + cs - 7, sy + cs - 4), fill=T['panel2'], outline=T['border'], width=1, r=8)
        cv.text((X + cs / 2 - 2, sy + cs / 2 - 2), ch, 30, T['text'], anchor='mm', bold=True)
        cv.text((X + cs / 2 - 2, sy + cs + 6), k, 18, T['dim'], anchor='mt', mono=True)
    # ---- 右边：记忆化表 f[left][right]
    f = S.get('f')
    if f is None:
        return
    bf = B.get('f')
    fx = x0 + 520
    cv.text((fx, y0 + 4), 'f[left][right]：s[left..right] 是否回文', 24, T['muted'], bold=True)
    c2, gx, gy = 52, fx + 40, y0 + 64
    for k in range(n):
        cv.text((gx + k * c2 + c2 / 2, gy - 6), k, 18, T['muted'], anchor='mb', mono=True)
        cv.text((gx - 10, gy + k * c2 + c2 / 2), k, 18, T['muted'], anchor='rm', mono=True)
    for r in range(n):
        for c in range(n):
            v = f[r][c]
            fill = T['green'] if v is True else (T['red'] if v is False else T['panel2'])
            changed = bf is not None and bf[r][c] != v
            X, Y = gx + c * c2, gy + r * c2
            cv.rect((X + 2, Y + 2, X + c2 - 2, Y + c2 - 2), fill=fill, r=6,
                    outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
            cv.text((X + c2 / 2, Y + c2 / 2), {True: 'T', False: 'F'}.get(v, '·'), 22,
                    T['bg'] if v is not None else T['dim'], anchor='mm', bold=True)
    if 'right' in S and 0 <= S['left'] < n and 0 <= S['right'] < n:
        X, Y = gx + S['right'] * c2, gy + S['left'] * c2
        cv.rect((X - 1, Y - 1, X + c2 + 1, Y + c2 + 1), outline=T['yellow'], width=4, r=8)
    cv.text((gx + n * c2 + 20, gy + 10), 'T 回文', 20, T['green'], bold=True)
    cv.text((gx + n * c2 + 20, gy + 40), 'F 不是', 20, T['red'], bold=True)
    cv.text((gx + n * c2 + 20, gy + 70), '· 没算过', 20, T['dim'], bold=True)


def _for(S, B, ret):
    if 'index' in S and S.index != B.get('index'):
        return f"枚举分割点：这一段取 `s[{S.left}..{S.index}] = '{S.s[S.left:S.index + 1]}'`"
    return f'`left = {S.left}` 开头的所有分割点都试过了 → 返回'


def _memo(S, B, ret):
    v = S.f[S.left][S.right]
    if B.f[S.left][S.right] is None:
        return f'`f[{S.left}][{S.right}]` 是 `None`：还没算过 → 现在算'
    return f'`f[{S.left}][{S.right}] = {v}` 已经算过 → ==记忆化，直接返回=='


CONFIG = dict(
    num=131, title='分割回文串', difficulty='Medium', category='回溯',
    author='yiduobo', technique='枚举分割点回溯 + 记忆化搜索判回文',
    code='''
class Solution(object):
    def partition(self, s):
        res = []
        f = [[None] * len(s) for _ in range(len(s))]
        self.dfs(s, 0, f, [], res)
        return res

    def dfs(self, s, left, f, now, res):
        if len(s) == left:
            res.append(now[:])
            return

        for index in range(left, len(s)):
            if self.check(s, left, index, f):
                now.append(s[left : index + 1])
                self.dfs(s, index + 1, f, now, res)
                now.pop()

    def check(self, s, left, right, f):
        if f[left][right] is None:
            if left >= right:
                f[left][right] = True
            else:
                if s[left] == s[right]:
                    f[left][right] = self.check(s, left + 1, right - 1, f)
                else:
                    f[left][right] = False

        return f[left][right]
''',
    call="Solution().partition('aab')",
    expect=[['a', 'a', 'b'], ['aa', 'b']],
    views=[
        dict(type='custom', draw=_draw, h=230),
        dict(type='stack', var='now', label='now', h=96),
        dict(type='calls', h=214),
        dict(type='stack', var='res', label='res', h=96),
    ],
    watch=[('left', 'left', 'cyan'), ('index', 'index', 'cyan'), ('right', 'right', 'yellow')],
    skip=['f = [[None] * len(s)'],
    captions={
        'self.dfs(s, 0, f, [], res)': '`f` 是 `n×n` 的记忆表（`None` = 还没算）；从 `left = 0` 开始枚举分割点',
        'if len(s) == left': lambda S, B, ret: (
            '`left == len(s)`：==整个 s 都分割完了==' if S.left == len(S.s) else
            f'`left = {S.left}`：剩下 `s[{S.left}:]` 还要分割'),
        'res.append(now[:])': '复制 now 加入 res：`{res[-1]}`',
        '            return': '返回上一层',
        'for index in range(left, len(s))': _for,
        'if self.check(s, left, index, f)': '调用 `check` 检测 `s[{left}..{right}]` 是不是回文',
        'now.append(s[left : index + 1])': "`check` 返回 `True` → `'{now[-1]}'` 是回文，加入 now",
        'self.dfs(s, index + 1, f, now, res)': '继续分割剩下的部分：`dfs(left = {left})`',
        'now.pop()': "回溯：弹出 `'{B.now[-1]}'`，换下一个分割点",
        'if f[left][right] is None': _memo,
        'if left >= right': lambda S, B, ret: (
            '`left == right`：只有一个字符 → 一定是回文' if S.left == S.right else
            '`left > right`：空串 → 算作回文' if S.left > S.right else
            f'`left < right`：要比较两端字符'),
        'f[left][right] = True': '记下 `f[{left}][{right}] = True`',
        'if s[left] == s[right]': lambda S, B, ret: (
            f"`s[{S.left}] == s[{S.right}]`（'{S.s[S.left]}'）→ 回文与否取决于里面的 `f[{S.left + 1}][{S.right - 1}]`"
            if S.s[S.left] == S.s[S.right] else
            f"`s[{S.left}] = '{S.s[S.left]}' ≠ s[{S.right}] = '{S.s[S.right]}'` → ==不是回文=="),
        'f[left][right] = self.check(': '两端相等 → 先递归计算 `f[{left}][{right}]`',
        'f[left][right] = False': '记下 `f[{left}][{right}] = False`',
        'return f[left][right]': '返回 `f[{left}][{right}] = {ret}`',
        'return res': '搜索结束，共 `{len(ret)}` 种分割方案',
    },
    max_steps=80,
    cards=dict(
        one_liner='枚举分割点，回文判断用记忆化只算一次',
        complexity='时间 `O(n·2^n)`，记忆表 `O(n^2)`',
        problem=['把字符串 `s` 分割成若干子串，使==每个子串都是回文串==，返回所有分割方案',
                 "示例：`\"aab\"` → `[[\"a\",\"a\",\"b\"],[\"aa\",\"b\"]]`"],
        quote='每次枚举分割点，然后检测分割出的部分是否是回文串……==所有子串是否是回文串从一开始就确定下来了==，因此可以先进行预处理，或者使用==记忆化搜索==的方式将是否回文记录下来。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(left)`：`s[left:]` 还没分，枚举这一段的结尾 `index`',
              '`f[l][r]`：`l ≥ r` 为 `True`；两端不等为 `False`；相等则等于 `f[l+1][r-1]`',
              '同一个子串可能被问很多次，算过一次就存进 `f`'],
        summary=['回溯部分和普通的「枚举选哪个」一样：`append` → `dfs` → `pop`',
                 '记忆化让每个 `f[l][r]` 只算一次（共 `O(n²)`），回溯总时间 `O(n·2^n)`',
                 '`left > right` 是空串，也要当作回文（如 `"aa"` 递归到 `f[1][0]`）',
                 '原文为 Python 2 风格，仅删去 docstring，其余代码未改'],
    ),
)
