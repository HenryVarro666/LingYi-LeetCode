S0, T0 = 'goddi', 'gd'


def _ch(v):
    return chr(97 + v)


def _kl(i, l, n):
    return n - l + i if l > i else i - l


def _kr(i, r, n):
    return n - i + r if r < i else r - i


def _cell(S, jj, ii, v):
    if 'x' not in S or 'j' not in S or 'i' not in S:
        return None
    i, j, n = S['i'], S['j'], len(S['s'])
    c = S['t'][j]
    if (jj, ii) == (j, i):
        return 'yellow'
    if S['s'][i] == c:
        return 'green' if (jj, ii) == (j + 1, i) else None
    l, r = S['left'][i][c], S['right'][i][c]
    return 'blue' if (jj, ii) in ((j + 1, l), (j + 1, r)) else None


def _formula(S):
    if 'x' not in S or 'j' not in S or 'i' not in S:
        return '`f[j][i]` = 拼写 `t[j..]`、12:00 对着 `s[i]` 时的最小旋转次数；`j` 从大到小'
    i, j, n = S['i'], S['j'], len(S['s'])
    c = S['t'][j]
    if S['s'][i] == c:
        return f'`s[{i}] = {_ch(c)}` 已对齐：`f[{j}][{i}] = f[{j + 1}][{i}]`'
    l, r = S['left'][i][c], S['right'][i][c]
    return f'`min(f[{j + 1}][{l}] + {_kl(i, l, n)}, f[{j + 1}][{r}] + {_kr(i, r, n)})`（左 {l} / 右 {r}）'


def _cap_if(S, B, ret):
    i, j = S.i, S.j
    c = S.t[j]
    if S.x == c:
        return f'`s[{i}] = {_ch(c)}` 就是要拼的字母 → ==无需旋转==，直接继承 `f[{j + 1}][{i}]`'
    return f'`s[{i}] = {_ch(S.x)} ≠ {_ch(c)}` → 要转：==左边最近 or 右边最近=='


def _cap_min(S, B, ret):
    i, j, n = S.i, S.j, len(S.s)
    c = S.t[j]
    l, r = S.l, S.r
    if S.f[j][i] == 0:
        return (f'`s[{i}]` 要转到字母 `{_ch(c)}`：向左最近在 `{l}`（{_kl(i, l, n)} 步），向右最近在 `{r}`（{_kr(i, r, n)} 步）')
    return (f'左转到 `{l}` 要 {_kl(i, l, n)} 步，右转到 `{r}` 要 {_kr(i, r, n)} 步：'
            f'`f[{j}][{i}] = min({S.f[j + 1][l]}+{_kl(i, l, n)}, {S.f[j + 1][r]}+{_kr(i, r, n)})` = =={S.f[j][i]}==')


CONFIG = dict(
    num=514, title='自由之路', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='枚举选哪个 · 记忆化搜索翻译成递推',
    tags=['动态规划', '其他线性 DP', '难度分 2400'],
    code='''
class Solution:
    def findRotateSteps(self, s: str, t: str) -> int:
        s = [ord(c) - ord('a') for c in s]
        t = [ord(c) - ord('a') for c in t]
        n, m = len(s), len(t)

        # 先算出每个字母的最后一次出现的下标
        # 由于 s 是环形的，循环结束后的 pos 就刚好是 left[0]
        pos = [0] * 26  # 初始值不重要
        for i, c in enumerate(s):
            pos[c] = i
        # 计算每个 s[i] 左边 a-z 的最近下标（左边没有就从 n-1 往左找）
        left = [None] * n
        for i, c in enumerate(s):
            left[i] = pos[:]
            pos[c] = i  # 更新下标

        # 先算出每个字母的首次出现的下标
        # 由于 s 是环形的，循环结束后的 pos 就刚好是 right[n-1]
        for i in range(n - 1, -1, -1):
            pos[s[i]] = i
        # 计算每个 s[i] 右边 a-z 的最近下标（左边没有就从 0 往右找）
        right = [None] * n
        for i in range(n - 1, -1, -1):
            right[i] = pos[:]
            pos[s[i]] = i  # 更新下标

        f = [[0] * n for _ in range(m + 1)]
        for j in range(m - 1, -1, -1):
            c = t[j]
            for i, x in enumerate(s):
                if x == c:  # 无需旋转
                    f[j][i] = f[j + 1][i]
                else:  # 左边最近 or 右边最近，取最小值
                    l, r = left[i][c], right[i][c]
                    f[j][i] = min(f[j + 1][l] + (n - l + i if l > i else i - l),
                                  f[j + 1][r] + (n - i + r if r < i else r - i))
        return f[0][0] + m
''',
    call=f'Solution().findRotateSteps({S0!r}, {T0!r})',
    expect=4,
    skip=['pos = [0] * 26', 'pos[c] = i', 'left[i] = pos[:]', 'pos[s[i]] = i', 'right[i] = pos[:]', 'for i, c in enumerate(s)',
          'for i in range(n - 1, -1, -1)', 'left = [None]', 'right = [None]', 'for i, x in enumerate(s)', 'c = t[j]', 'f[j + 1][r] + (n - i + r', 'l, r = left[i][c]'],
    max_steps=90,
    views=[
        dict(type='array', var=lambda S: [_ch(v) for v in S['s']], label='ring（s，环形：0 号左边是 n−1 号）', h=170, cell=84,
             pointers={'i': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('i') and 'x' in S else None)),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[j][i]：行 = 还剩 t[j..]，列 = 对着 s[i]（黄=在算，蓝/绿=依赖）', h=300, cell=84,
             rows=lambda S: [f'{k}' + (_ch(S["t"][k]) if k < len(S['t']) else '-') for k in range(len(S['t']) + 1)],
             cols=lambda S: [f'{k}{_ch(v)}' for k, v in enumerate(S['s'])],
             color=_cell),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i', 'pink'), ('l', 'l', 'cyan'), ('r', 'r', 'orange')],
    captions={
        's = [ord': '把 `ring` 转成数字 0~25，方便当下标',
        't = [ord': '把 `key` 也转成数字',
        'n, m = len(s)': '`n = {n}`（环长），`m = {m}`（要拼的字母数）。只算旋转次数，最后再加 `m` 次按钮',
        'f = [[0] * n': '预处理完：`left[i][c]` / `right[i][c]` = ==s[i] 左边/右边最近的字母 c==（环形，所以首尾相连）。`f[m][·] = 0` 是边界',
        'for j in range': lambda S, B, r: (f'`j = {S.j}`：算 `f[j]` 要先有 `f[j+1]` → ==j 从大到小==' if 'j' in S and S.get('j') != B.get('j') else '所有状态算完，答案在 `f[0][0]`'),
        'if x == c': _cap_if,
        'f[j][i] = f[j + 1][i]': '`f[{j}][{i}] = f[{j + 1}][{i}]` = =={f[j][i]}==',
        'f[j][i] = min(': _cap_min,
        'return f[0][0] + m': '一开始 12:00 对着 `s[0]`：旋转 `f[0][0] = {f[0][0]}` 次，再加按钮 `{m}` 次 = =={ret}==',
    },
    cards=dict(
        one_liner='枚举「转到左边最近 / 右边最近的目标字母」，旋转次数最小',
        complexity='时间 `O(n(|Σ|+m))`，空间 `O(n(|Σ|+m))`',
        problem=['`ring` 是环形表盘，12:00 方向最初对着 `ring[0]`',
                 '每转一格 1 步，对齐 `key[i]` 后按按钮也算 1 步，求拼出整个 `key` 的最少步数',
                 '示例：`ring="godding"`，`key="gd"` → `4`；本视频用 `goddi` / `gd`'],
        quote='我们可以只计算最小旋转次数，最后加上 m，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(j, i)`：拼 `t[j..]`、此时 12:00 对着 `s[i]` 的最小旋转次数',
              '`s[i]` 就是目标字母 → 不转；否则只可能转到左边最近或右边最近的那个，取小',
              '先预处理 `left` / `right`，再把记忆化搜索 1:1 翻译成递推，`j` 从大到小'],
        summary=['时间 `O(n(|Σ|+m))`，预处理 left/right 要 `O(n·26)`，DP 要 `O(nm)`',
                 '`s` 是环形：左边没有就从 `n-1` 往左找，旋转次数是 `n-l+i` 或 `i-l`',
                 '不要漏掉按按钮的 `m` 步；`f[m][·]=0` 是边界',
                 '递推会算到无效状态（`t` 里没有的字母），记忆化搜索更省；原文还给了 BFS 写法（状态 `(i,j)`，每步代价 1）'],
    ),
)
