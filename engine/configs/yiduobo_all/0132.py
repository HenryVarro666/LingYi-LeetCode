S0 = 'aabc'


def _tcolor(S, i, j, v):
    ln = S.get('_line', 0)
    if ln >= 19 and S.get('left') is not None and S.get('right') is not None:
        if (i, j) == (S['left'], S['right']):
            return 'yellow'
        return None
    if ln in (7, 8) and S.get('index') is not None and (i, j) == (0, S['index']):
        return 'yellow'
    if ln in (12, 13, 14) and S.get('cut_pos') is not None and (i, j) == (S['cut_pos'], S['index']):
        return 'yellow'
    return None


def _scolor(S, k, v):
    ln = S.get('_line', 0)
    idx, cp = S.get('index'), S.get('cut_pos')
    if ln >= 19 and S.get('left') is not None:
        return 'yellow' if S['left'] <= k <= S['right'] else None
    if idx is None:
        return None
    if ln in (7, 8):
        return 'cyan' if k <= idx else None
    if ln in (11, 12, 13, 14) and cp is not None:
        if k >= cp and k <= idx:
            return 'pink'
        return 'cyan' if k < cp else None
    if 6 <= ln <= 15:
        return 'cyan' if k <= idx else None
    return None


def _cap_eq(S, B, ret):
    s, l, r = B.s, B.left, B.right
    return f'`s[{l}] = {s[l]}`，`s[{r}] = {s[r]}`：两端相同 → 看里层 `check({l + 1}, {r - 1})`，它的结果就是答案'


CONFIG = dict(
    num=132, title='分割回文串 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='划分型 DP · 记忆化判回文',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minCut(self, s):

        f = [0]
        g = [[None] * len(s) for _ in range(len(s))]
        for index in range(1, len(s)):
            if self.check(s, 0, index, g):
                f.append(0)
            else:
                min_step = None
                for cut_pos in range(1, index + 1):
                    if self.check(s, cut_pos, index, g):
                        if min_step is None or min_step > f[cut_pos - 1] + 1:
                            min_step = f[cut_pos - 1] + 1
                f.append(min_step)

        return f[len(s) - 1]

    def check(self, s, left, right, g):
        if g[left][right] is None:
            if left >= right:
                g[left][right] = True
            else:
                if s[left] == s[right]:
                    g[left][right] = self.check(s, left + 1, right - 1, g)
                else:
                    g[left][right] = False

        return g[left][right]
''',
    call=f'Solution().minCut({S0!r})',
    expect=2,
    skip=['def check', 'if g[left][right] is None', 'if left >= right', 'if s[left] == s[right]', 'f = [0]',
          'for cut_pos in range', 'for index in range'],
    max_steps=110,
    views=[
        dict(type='string', var='s', label='s（青 = s[0..index]，粉 = 最后一段 s[cut_pos..index]）', h=150, cell=76,
             color=_scolor),
        dict(type='table', var='g', label='g[left][right]：· = 还没判断，T/F = 是否回文（记忆化）', h=290, cell=50,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_tcolor),
        dict(type='array', var='f', label='f[i]：s[0..i] 的最少切割次数（逐个追加）', h=140, cell=84),
        dict(type='calls', h=120, hide=('s', 'g')),
    ],
    watch=[('index', 'index', 'blue'), ('cut_pos', 'cut_pos', 'pink'), ('min_step', 'min_step', 'orange'), ('left', 'left', 'yellow'), ('right', 'right', 'yellow')],
    captions={
        'g = [[None]': '`g[l][r]` 缓存 `s[l..r]` 是否回文，`None` 表示还没算过（记忆化）',
        'if self.check(s, 0, index, g)': '`s[0..{index}] = {s[:index+1]}`：先问 `check(0, {index})`，整段是回文吗？是的话不用切',
        'f.append(0)': '`f[{index}] = 0`：整个前缀就是回文 → {f}',
        'min_step = None': '`min_step` 记最小切割次数，先设为 `None`',
        'if self.check(s, cut_pos': '最后一段 `s[{cut_pos}..{index}] = {s[cut_pos:index+1]}`：问 `check({cut_pos}, {index})`，是回文才能在 `{cut_pos - 1}|{cut_pos}` 切一刀',
        'if min_step is None or': lambda S, B, r: (f'`min_step` 还是 `None` → 先接受 `f[{S.cut_pos-1}] + 1 = {S.f[S.cut_pos-1] + 1}`' if S.min_step is None
                                                   else f'比较 `{S.min_step}` 和 `f[{S.cut_pos-1}] + 1 = {S.f[S.cut_pos-1] + 1}`，更小才更新'),
        'min_step = f[cut_pos - 1] + 1': '`min_step = f[{cut_pos-1}] + 1` = =={min_step}==（前面 `f[{cut_pos-1}]` 刀，再加这一刀）',
        'f.append(min_step)': '`f[{index}] = {min_step}`：前缀 `{s[:index+1]}` 最少切 {min_step} 刀 → {f}',
        'g[left][right] = True': '`left >= right`：单个字符或空串 → ==是回文== `True`',
        'g[left][right] = self.check': _cap_eq,
        'g[left][right] = False': '`s[{left}] = {s[left]}` ≠ `s[{right}] = {s[right]}`：两端不同 → ==不是回文== `False`',
        'return g[left][right]': lambda S, B, r: f'`check({S.left}, {S.right})`：`s[{S.left}..{S.right}]{(" = " + S.s[S.left:S.right+1]) if S.left <= S.right else "（空串）"}` ' + ('==是回文==' if r else '==不是回文==') + '（结果记进 `g`，下次直接用）',
        'return f[len(s) - 1]': '整个字符串的最少切割次数 `f[{len(s)-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] 枚举最后一段回文的切点，回文判断用记忆化搜索',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['把字符串 `s` 切成若干回文子串，求==最少切几刀==',
                 '示例：`"aab"` → `1`（`aa | b`）',
                 '本视频：`"aabc"` → `2`（`aa | b | c`）'],
        quote='若s[:i]本身就是回文串，那么不需要进行切分，于是有f[i] = 0。若s[:i]不是回文串，则需要从1到i之间枚举分割点cut_pos，若s[cut_pos : index]是回文串，那么有f[i] = min(f[i], f[cut_pos - 1] + 1)。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：前 `i+1` 个字符切成回文的最少次数',
              '整段是回文 → `0`；否则枚举切点 `cut_pos`，最后一段是回文就用 `f[cut_pos-1] + 1`',
              '判断回文用 `check`：两端相同再看里层，结果记在 `g` 里，不重复算',
              '和上一题（131）判断回文的写法完全一样'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`（`g` 表）',
                 '易错：`g` 缓存的 `None` / `True` / `False` 要区分，不能用 `if g[l][r]` 判缓存',
                 '`min_step` 初值用 `None`，第一次直接接受',
                 '原文已是 Python 3 可运行写法，只删去了类型说明',
                 '对比灵神：灵神先把回文表整张预处理好，yiduobo 用记忆化按需计算'],
    ),
)
