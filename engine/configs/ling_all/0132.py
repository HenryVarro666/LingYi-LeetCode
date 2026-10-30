S0 = 'aabbc'
N0 = len(S0)
HID = (24, 28, 36)


def _ij(S):
    """phase 1 的 (l, r)，只在 7~8 行有效"""
    return S.get('l'), S.get('r')


def _tcolor(S, i, j, v):
    if j < i:
        return HID                      # 下三角没有意义，涂成背景色
    ln = S.get('_line', 0)
    l, r = S.get('l'), S.get('r')
    if ln in (7, 8) and l is not None and r is not None:
        if (i, j) == (l, r):
            return 'yellow'
        if (i, j) == (l + 1, r - 1) and s_ok(l, r):
            return 'blue'
    if ln in (11, 12, 13) and S.get('r') is not None and (i, j) == (0, S['r']):
        return 'yellow'
    if ln in (15, 16, 17) and l is not None and r is not None and (i, j) == (l, r):
        return 'yellow'
    return None


def s_ok(l, r):
    return l + 1 <= r - 1


def _scolor(S, k, v):
    ln = S.get('_line', 0)
    l, r = S.get('l'), S.get('r')
    if ln in (7, 8) or ln in (15, 16, 17):
        if l is not None and r is not None:
            if k in (l, r):
                return 'blue' if k == l else 'pink'
            if l < k < r:
                return 'cyan'
    if ln in (11, 12, 13) and S.get('r') is not None and k <= S['r']:
        return 'cyan'
    return None


def _formula(S):
    ln = S.get('_line', 0)
    l, r = S.get('l'), S.get('r')
    s = S['s']
    if ln in (7, 8) and l is not None and r is not None:
        return f'`s[{l}..{r}]` = =={s[l:r+1]}=={"，" + "两端相同才看里面" if s[l] == s[r] else "，两端不同 → 不是回文"}'
    if ln in (15, 16, 17) and l is not None and r is not None:
        return f'最后一段 `s[{l}..{r}]` = =={s[l:r+1]}==，切在 `{l-1}|{l}`：`f[{l-1}] + 1`'
    if ln in (11, 12, 13) and S.get('r') is not None:
        return f'`s[0..{S["r"]}]` = =={s[:S["r"]+1]}==，整段是回文吗？'
    return '`f[r]` = 把 `s[0..r]` 分成回文段的最少切割次数'


CONFIG = dict(
    num=132, title='分割回文串 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP · 回文表预处理（递推）',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    def minCut(self, s: str) -> int:
        n = len(s)
        # is_palindrome[l][r] 表示 s[l:r+1] 是否为回文串
        is_palindrome = [[True] * n for _ in range(n)]
        for l in range(n - 2, -1, -1):
            for r in range(l + 1, n):
                is_palindrome[l][r] = s[l] == s[r] and is_palindrome[l + 1][r - 1]

        f = [0] * n
        for r, is_pal in enumerate(is_palindrome[0]):
            if is_pal:  # 已是回文串，无需分割
                continue
            res = inf
            for l in range(1, r + 1):  # 枚举分割位置
                if is_palindrome[l][r]:
                    res = min(res, f[l - 1] + 1)  # 在 l-1 和 l 之间切一刀
            f[r] = res
        return f[-1]
''',
    call=f'Solution().minCut({S0!r})',
    expect=2,
    skip=['for r in range(l + 1', 'for l in range(1, r + 1)', 'n = len(s)', 'f = [0] * n'],
    max_steps=100,
    views=[
        dict(type='string', var='s', label='s（蓝 = l，粉 = r，青 = 之间）', h=140, cell=76,
             pointers={'l if _line in (7, 8, 15, 16, 17) else None': 'blue', 'r if _line >= 7 else None': 'pink'},
             pointer_labels={'l if _line in (7, 8, 15, 16, 17) else None': 'l', 'r if _line >= 7 else None': 'r'},
             color=_scolor),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='is_palindrome', label='is_palindrome[l][r]（T = 回文；黄 = 正在算，蓝 = 它依赖的里层）', h=330, cell=52,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_tcolor),
        dict(type='array', var='f', label='f[r]：s[0..r] 的最少切割次数', h=170, cell=84,
             pointers={'r if _line >= 11 else None': 'pink'}, pointer_labels={'r if _line >= 11 else None': 'r'},
             color=lambda S, k, v: 'yellow' if S.get('_line') == 18 and k == S.get('r') else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'orange'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'is_palindrome = [[True]': '先预处理回文表：`is_palindrome[l][r]` = `s[l..r]` 是否回文；长度 ≤ 1 的区间默认就是 True',
        'for l in range(n - 2': lambda S, B, r: (f'`l = {S.l}`：算 `[l][r]` 要用 `[l+1][r-1]`，所以 ==l 从大到小==' if S.get('l') != B.get('l')
                                                 else '回文表算完了'),
        'is_palindrome[l][r] = ': lambda S, B, r: (f'`s[{S.l}] = {S.s[S.l]}`，`s[{S.r}] = {S.s[S.r]}`：两端不同 → ==不是回文== `F`' if S.s[S.l] != S.s[S.r]
                                                   else (f'两端都是 `{S.s[S.l]}`，里面是空的（长度 ≤ 0）→ ==是回文== `T`' if S.l + 1 > S.r - 1
                                                         else f'两端都是 `{S.s[S.l]}` → 结果就是里层 `[{S.l+1}][{S.r-1}]` 的值 =={S.is_palindrome[S.l][S.r]}==')),
        'f = [0] * n': '`f[r]` 的定义和 `dfs(r)` 一样：前缀 `s[0..r]` 的最少切割次数',
        'for r, is_pal in enumerate': lambda S, B, r: (f'`r = {S.r}`：前缀 `{S.s[:S.r+1]}`' if S.get('r') != B.get('r')
                                                       else '所有前缀都算完了，答案是 `f[-1]`'),
        'if is_pal:': lambda S, B, r: (f'`s[0..{S.r}]` 本身就是回文 → 一刀都不用切，`f[{S.r}] = 0`' if S.is_pal
                                      else f'`s[0..{S.r}]` 不是回文 → 要枚举最后一段 `s[l..{S.r}]` 的起点 `l`'),
        'continue': '`f[{r}]` 保持初值 0，直接看下一个 `r`',
        'res = inf': '`res` 记录最小切割数，先设为 ∞',
        'if is_palindrome[l][r]': lambda S, B, r: (f'最后一段 `s[{S.l}..{S.r}] = {S.s[S.l:S.r+1]}` 是回文 → ==可以切==' if S.is_palindrome[S.l][S.r]
                                                   else f'最后一段 `s[{S.l}..{S.r}] = {S.s[S.l:S.r+1]}` 不是回文 → 跳过'),
        'res = min(res': '切在 `{l-1}|{l}`：前面 `f[{l-1}] = {f[l-1]}`，再切这一刀 `+1` → `res = {res}`',
        'f[r] = res': '`f[{r}] = {res}`：前缀 `{s[:r+1]}` 最少切 {res} 刀',
        'return f[-1]': '整个字符串的最少切割次数 `f[{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一段回文的起点，前缀答案 + 1 刀',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['把字符串 `s` 分割成若干子串，==每个子串都是回文串==',
                 '返回最少需要切几刀',
                 '示例：`"aab"` → `1`（`aa | b`）；`"a"` → `0`',
                 '本视频：`"aabbc"` → `2`（`aa | bb | c`）'],
        quote='枚举分割出的最右边那段子串的左端点 l：如果 s[l] 到 s[r] 是回文串，那么在 l-1 和 l 之间切一刀，接下来需要解决的子问题为 dfs(l-1)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[r]` = 前缀 `s[0..r]` 的最少切割次数；整段是回文就是 `0`',
              '否则枚举最后一段 `s[l..r]`：是回文就 `f[l-1] + 1`，取最小',
              '回文判断也预处理成表：两端相同 ∧ 里层是回文，`l` ==从大到小==算',
              '递归边界翻译成初值：前缀本身是回文 → `f[r] = 0`'],
        summary=['时间 `O(n^2)`：回文表 `O(n^2)`，`f` 每个状态枚举 `O(n)`',
                 '易错：回文表 `l` 倒序、`r` 正序；前缀是回文要 `continue`，保持 `f[r] = 0`',
                 '灵神前面还有记忆化搜索（`@cache`）版本，和这份递推 1:1 对应',
                 '补充：这类问题叫 palindromic length，另有 `O(n)` 做法',
                 '同类划分型 DP：131 分割回文串、1278、2707'],
    ),
)
