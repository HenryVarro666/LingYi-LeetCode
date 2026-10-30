_in = lambda k: (lambda S: S['_inner'].get(k))
_L, _R, _CUT = _in('l'), _in('r'), _in('cut_pos')
SS = 'DID'


def _state(S):
    s = S['_inner']
    if 'l' not in s:
        return '`f[l][r]`：把 `S[l..r-1]` 当作 DI 序列时，合法排列的个数（只看相对大小）'
    l, r = s['l'], s['r']
    if l == r:
        return f'`f[{l}][{r}]`：只有 1 个数，没有 D / I 要求'
    return f'`f[{l}][{r}]`：约束 `{SS[l:r]}`，共 `{r - l + 1}` 个数的合法排列数'


def _color(S, i, j, v):
    l, r = S['_inner'].get('l'), S['_inner'].get('r')
    if l is None:
        return None
    if (i, j) == (l, r):
        return 'yellow'
    if v is not None and i >= l and j <= r and i <= j:
        return 'green' if (i, j) in ((l + 1, r), (l, r - 1)) else None
    return None


def _cut_cap(S, B, ret):
    l, r, c, s = B.l, B.r, B.cut_pos, B.S
    if s[c] == 'I':
        if c == l:
            return f'`S[{c}] = I` 且在最前：最小值放最前面 → 转成子问题 `f[{l + 1}][{r}]`'
        if s[c - 1] == 'D':
            return f'`S[{c - 1}..{c}] = DI`：最小值放在第 {c} 位的「谷底」，左 `[{l},{c - 1}]` 右 `[{c + 1},{r}]` 各是子问题'
        return f'`S[{c}] = I`，前一个也是 `I`：最小值放这里不成谷底 → 跳过'
    if c == r - 1:
        return f'`S[{c}] = D` 且在最后：最小值放最后面 → 转成子问题 `f[{l}][{r - 1}]`'
    return f'`S[{c}] = D` 不在末尾：最小值不能放这里 → 跳过'


CONFIG = dict(
    num=903, title='DI 序列的有效排列', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 把最小值放进谷底',
    tags=[],
    code='''
class Solution(object):
    def numPermsDISequence(self, S):

        n = len(S)
        mod = 10 ** 9 + 7

        C = [[1, 0]]
        for i in range(n):
            C.append([])
            for j in range(i + 2):
                C[-1].append((C[-2][j] + C[-2][j - 1]) % mod)
            C[-1].append(0)

        f = [[None] * (n + 1) for _ in range(n + 1)]
        return self.dfs(0, n, S, f, C, mod)

    def dfs(self, l, r, S, f, C, mod):
        if f[l][r] is None:
            if l == r:
                f[l][r] = 1
            else:
                f[l][r] = 0
                for cut_pos in range(l, r):
                    if S[cut_pos] == 'I':
                        if cut_pos == l:
                            f[l][r] += self.dfs(l + 1, r, S, f, C, mod)
                            f[l][r] %= mod
                        elif S[cut_pos - 1] == 'D':
                            f[l][r] += C[r - l][cut_pos - l] * self.dfs(l, cut_pos - 1, S, f, C, mod) * self.dfs(cut_pos + 1, r, S, f, C, mod)
                            f[l][r] %= mod
                    elif cut_pos == r - 1 and S[cut_pos] == 'D':
                        f[l][r] += self.dfs(l, r - 1, S, f, C, mod)
                        f[l][r] %= mod

        return f[l][r]
''',
    call=f'Solution().numPermsDISequence({SS!r})',
    expect=5,
    skip=['n = len(S)', 'mod = 10', 'C = [[1, 0]]', 'C.append', 'for j in range(i + 2)', 'C[-1].append', 'for i in range(n)',
          'f[l][r] %= mod', 'else:'],
    max_steps=90,
    views=[
        dict(type='string', var='S', label='S（粉 = 当前尝试放最小值的位置 cut_pos）', cell=90, h=190,
             pointers={_CUT: 'pink'}, pointer_labels={_CUT: 'cut_pos'},
             color=lambda S, i, v: 'pink' if i == S['_inner'].get('cut_pos') else None,
             dim=lambda S, i, v: S['_inner'].get('l') is not None and not (S['_inner']['l'] <= i < S['_inner']['r'])),
        dict(type='text', fn=_state, size=24, h=80),
        dict(type='table', var='f', label='f[l][r]（None = 还没算；黄 = 正在算，绿 = 刚用到的子问题）', cell=80, h=250,
             rows=lambda S: [str(k) for k in range(len(SS) + 1)], cols=lambda S: [str(k) for k in range(len(SS) + 1)],
             color=_color),
        dict(type='calls', h=200, hide=('S', 'f', 'C', 'mod')),
    ],
    watch=[('l', "_inner.get('l')", 'blue'), ('r', "_inner.get('r')", 'pink'), ('cut_pos', "_inner.get('cut_pos')", 'orange')],
    captions={
        'f = [[None]': '`f[l][r]` 做记忆化：`None` 表示还没算过',
        'return self.dfs(0, n': '入口：整串 `S = {S}`，`f[0][{n}]`',
        'if f[l][r] is None': lambda S, B, r: (f'`f[{B.l}][{B.r}]` 没算过 → 开始计算' if B.f[B.l][B.r] is None
                                              else f'`f[{B.l}][{B.r}] = {B.f[B.l][B.r]}` 算过了 → 直接返回'),
        'if l == r': lambda S, B, r: (f'`l == r`：没有字符，只有 1 个数 → 记为 ==1== 种' if B.l == B.r
                                      else f'`l = {B.l} < r = {B.r}`：枚举最小值放在哪个位置 `cut_pos`'),
        'f[l][r] = 1': '没有约束，1 个数只有 1 种排列',
        'f[l][r] = 0': '`f[{l}][{r}]` 从 0 开始累加',
        'for cut_pos in range': '枚举最小值所在位置 `cut_pos`（只有 `I` 的左边或最后的 `D` 才行）',
        "if S[cut_pos] == 'I'": lambda S, B, r: _cut_cap(S, B, r),
        'if cut_pos == l': lambda S, B, r: ('最小值在最前面' if B.cut_pos == B.l else '最小值不在最前面 → 看它前一个字符'),
        "elif S[cut_pos - 1] == 'D'": lambda S, B, r: (f'`S[{B.cut_pos - 1}] = D` → 前一个是下降，这里 `I` 上升 → ==是谷底，最小值可以放这=='
                                                      if B.S[B.cut_pos - 1] == 'D' else f'`S[{B.cut_pos - 1}] = I` → 不是谷底，跳过'),
        'f[l][r] += self.dfs(l + 1, r': '`f[{B.l}][{B.r}] += f[{B.l + 1}][{B.r}]`：去掉最前面的最小值，剩下的是子问题',
        'f[l][r] += C[r - l]': '`f[{B.l}][{B.r}] += C({B.r - B.l}, {B.cut_pos - B.l}) × f[{B.l}][{B.cut_pos - 1}] × f[{B.cut_pos + 1}][{B.r}]`：其余 `{B.r - B.l}` 个数里选 `{B.cut_pos - B.l}` 个放左边，`C` = {B.C[B.r - B.l][B.cut_pos - B.l]}',
        "elif cut_pos == r - 1": lambda S, B, r: (f'`cut_pos = r-1` 且 `S[{B.cut_pos}] = D`：最小值放最后' if (B.cut_pos == B.r - 1 and B.S[B.cut_pos] == 'D')
                                                 else f'`S[{B.cut_pos}] = D` 但不在最后 → 跳过'),
        'f[l][r] += self.dfs(l, r - 1': '`f[{B.l}][{B.r}] += f[{B.l}][{B.r - 1}]`：去掉最后面的最小值，剩下的是子问题',
        'return f[l][r]': '`f[{B.l}][{B.r}] = {ret}`，返回',
    },
    cards=dict(
        one_liner='把最小值放进序列，只有「谷底」位置可放，剩下的拆成两个子问题',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['字符串 `S` 只含 `D`（下降）和 `I`（上升），长度为 `n`',
                 '统计 `0..n` 的排列 `P` 有多少个满足：`S[i]=D` 时 `P[i]>P[i+1]`，`S[i]=I` 时 `P[i]<P[i+1]`',
                 '答案对 `10^9+7` 取模。本视频：`S = "DID"` → `5`'],
        quote='D和I只涉及到相对大小，……对于一个规模为k的子问题，我们无需关心这k + 1个数到底是什么，因为其答案都是一样的。……先把当前最小的数给安排上，然后再进行分析。',
        quote_src='—— yiduobo 题解原文',
        idea=['只看相对大小：`f[l][r]` = `S[l..r-1]` 对应的 `r-l+1` 个数的合法排列数',
              '最小值只能放在「谷底」：最前面（`S[l]=I`）、最后面（`S[r-1]=D`）、或 `DI` 之间',
              '放中间时分成左右两段，从其余 `r-l` 个数里选 `cut_pos-l` 个给左边：`C(r-l, cut_pos-l) × 左 × 右`',
              '组合数 `C` 先用递推预处理，`f` 用记忆化搜索'],
        summary=['时间 `O(n^3)`：`O(n^2)` 个状态 × 枚举 `cut_pos` `O(n)`',
                 '易错：最小值放中间时，必须是 `D` 后面接 `I`，否则它不是局部最小',
                 '易错：乘法后别忘了取模；`f[l][r]` 用 `None` 区分「没算过」和「算出 0」',
                 '原文已是可在 Python 3 运行的写法，无需改动'],
    ),
)
