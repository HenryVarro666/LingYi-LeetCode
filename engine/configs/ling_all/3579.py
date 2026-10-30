CODE_ROWS = None

def _pre(S):
    """True while still building rev_op (before f is created)"""
    return 'f' not in S


def _op_txt(S):
    if _pre(S):
        if 'l' not in S or 'r' not in S or 'op' not in S:
            return '`rev_op[l][r]` = 先反转 `s[l..r]`（1 次）再配对的最少操作数'
        l, r = S['l'], S['r']
        if l < 0 or r >= len(S['s']):
            return '这个中心扩展完了'
        return f'中心扩展：`s[{l}..{r}]` 反转后 `s[{l}]`→`t[{r}]`，`s[{r}]`→`t[{l}]`，当前 `op = {S["op"]}`（含反转 1 次）'
    if 'j' not in S or 'i' not in S:
        return ''
    i, j = S['i'], S['j']
    if j < 0:
        return f'`f[{i + 1}] = {S["f"][i + 1]}`'
    return f'最后一段 `[{j}..{i}]`：不反转 `op = {S["op"]}`，反转 `rev_op = {S["rev_op"][j][i]}`'


def _cnt_fmt(k, v):
    return f'({k[0]},{k[1]})' if isinstance(k, tuple) else str(k)


CONFIG = dict(
    num=3579, title='字符串转换需要的最小操作数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 中心扩展预处理 rev_op + 配对贪心',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2493'],
    code='''
class Solution:
    def minOperations(self, s: str, t: str) -> int:
        def update(x: str, y: str) -> None:
            if x == y:
                return
            if cnt[(y, x)] > 0:
                cnt[(y, x)] -= 1
            else:
                cnt[(x, y)] += 1
                nonlocal op
                op += 1

        n = len(s)
        # 预处理 rev_op
        rev_op = [[0] * n for _ in range(n)]
        # 中心扩展法
        # i 为偶数表示奇长度子串，i 为奇数表示偶长度子串
        for i in range(2 * n - 1):
            cnt = defaultdict(int)
            op = 1
            # 从闭区间 [l, r] 开始向左右扩展
            l, r = i // 2, (i + 1) // 2
            while l >= 0 and r < n:
                update(s[l], t[r])
                if l != r:
                    update(s[r], t[l])
                rev_op[l][r] = op
                l -= 1
                r += 1

        f = [0] * (n + 1)
        for i in range(n):
            res = inf
            cnt = defaultdict(int)
            op = 0  # 不反转时的最小操作次数
            for j in range(i, -1, -1):
                update(s[j], t[j])
                res = min(res, f[j] + min(op, rev_op[j][i]))
            f[i + 1] = res
        return f[n]
''',
    call='Solution().minOperations("abc", "bad")',
    expect=2,
    max_steps=95,
    skip=['n = len(s)', 'rev_op = [[0]', 'cnt = defaultdict(int)', 'f = [0] * (n + 1)', 'res = inf', 'nonlocal op', 'l, r = i // 2', 'r += 1', 'op = 1', 'l -= 1', 'while l >= 0', 'op = 0', 4, 5, 6, 7, 9, 11],
    views=[
        dict(type='string', var='s', label='s = word1', h=170, cell=60,
             pointers={'l if (_line < 28 and l >= 0) else None': 'blue', 'r if (_line < 28 and r < n) else None': 'pink', 'j if (_line >= 28 and j >= 0) else None': 'blue'},
             pointer_labels={'l if (_line < 28 and l >= 0) else None': 'l', 'r if (_line < 28 and r < n) else None': 'r', 'j if (_line >= 28 and j >= 0) else None': 'j'}),
        dict(type='string', var='t', label='t = word2', h=130, cell=60, index=False),
        dict(type='text', fn=_op_txt, size=24, h=60),
        dict(type='table', var='rev_op', label='rev_op[l][r]（中心扩展，黄 = 刚算出）', h=200, cell=50,
             rows=lambda S: list(range(len(S['s']))), cols=lambda S: list(range(len(S['s']))),
             color=lambda S, a, b, v: ('yellow' if _pre(S) and S.get('l') == a and S.get('r') == b else
                                       'green' if (not _pre(S)) and S.get('j') == a and S.get('i') == b else None)),
        dict(type='array', var='f', label='f[i] = 前 i 个字符的最少操作数', h=130, cell=60,
             color=lambda S, k, v: 'yellow' if (not _pre(S)) and S.get('i') is not None and k == S['i'] + 1 and S.get('_line', 0) >= 33 else None),
        dict(type='map', var='cnt', label='cnt：还没配上的字母对 (x→y)', h=130, fmt=lambda k, v: f'{k[0]}→{k[1]}：{v}' if isinstance(k, tuple) else f'{k}：{v}'),
    ],
    watch=[('i', 'i', 'blue'), ('op', 'op', 'green'), ('res', 'res', 'orange')],
    captions={
        'def update': '`update(x, y)`：处理一对 `(s[p], t[q])`，`op` 记录需要的操作数',
        'rev_op = [[0]': '`rev_op[l][r]`：子串 `s[l..r]` 先反转（1 次）后的最少操作数',
        'for i in range(2 * n - 1)': lambda S, B, r: (f'中心 `i = {S.i}`：从 `[{S.i // 2}, {(S.i + 1) // 2}]` 向两边扩展（保证中心不变）' if S.get('f') is None and S.i != B.get('i') else '`rev_op` 全部算完'),
        'op = 1': '新的中心：已经用了 1 次反转，`op = 1`，`cnt` 清空',
        'update(s[l], t[r])': lambda S, B, r: f'反转后 `s[{S.l}]` 对到 `t[{S.r}]`：`({S.s[S.l]}, {S.t[S.r]})`' + ('，相同不用操作' if S.s[S.l] == S.t[S.r] else (f'，反向对 ({S.t[S.r]},{S.s[S.l]}) 有人在等 → ==一次交换抵两次替换==，`op` 不增' if B.cnt.get((S.t[S.r], S.s[S.l]), 0) > 0 else '，没有可配对的 → 先记一次替换，`op` 加一')),
        'update(s[r], t[l])': lambda S, B, r: f'反转后 `s[{S.r}]` 对到 `t[{S.l}]`：`({S.s[S.r]}, {S.t[S.l]})`' + ('，相同不用操作' if S.s[S.r] == S.t[S.l] else (f'，反向对 ({S.t[S.l]},{S.s[S.r]}) 有人在等 → ==配成交换==，`op` 不增' if B.cnt.get((S.t[S.l], S.s[S.r]), 0) > 0 else '，没有可配对的 → 记一次替换，`op` 加一')),
        'if l != r': lambda S, B, r: ('奇长度子串的中心 `l == r`，只处理一次' if S.l == S.r else '`l != r`：还要处理对称的另一端'),
        'rev_op[l][r] = op': '`rev_op[{l}][{r}] = {op}`：`s[{l}..{r}]` 反转+配对的操作数；接着 `l, r` 各向外扩一格',
        'for i in range(n)': lambda S, B, r: (f'`f[{S.i + 1}]`：前缀 `[0..{S.i}]`，枚举最后一段的左端点 `j`' if S.i != B.get('i') else '所有前缀算完'),
        'op = 0': '不反转的操作数从 0 开始，随 `j` 左移增量计算',
        'for j in range': lambda S, B, r: (f'`j = {S.j}`：最后一段是 `[{S.j}..{S.i}]`' if S.j != B.get('j') else '`j` 枚举完毕'),
        'update(s[j], t[j])': lambda S, B, r: f'不反转：`s[{S.j}]={S.s[S.j]}` 对 `t[{S.j}]={S.t[S.j]}`' + ('，相同不用操作' if S.s[S.j] == S.t[S.j] else (f'，与之前的 ({S.t[S.j]},{S.s[S.j]}) 互补 → ==换一次抵两次==，`op` 不增' if B.cnt.get((S.t[S.j], S.s[S.j]), 0) > 0 else '，没有互补对 → 记一次替换，`op` 加一')),
        'res = min(res, f[j] + min(op, rev_op[j][i]))': '`f[{j}] + min(op={op}, rev_op={rev_op[j][i]})` → `res` = =={res}==',
        'f[i + 1] = res': '`f[{i+1}] = {f[i+1]}`：前 `{i+1}` 个字符最少 `{f[i+1]}` 次',
        'return f[n]': '整串 `f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='划分型 DP：每段的代价 = min(不反转配对, 反转后配对)',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['把 `word1` 切成若干连续子串，每段可以替换、交换、反转（每个下标每种操作最多一次）',
                 '求变成 `word2` 的==最少操作数==',
                 '示例：`"abcdf" → "dacbe"` = `4`；本视频：`"abc" → "bad"` = `2`'],
        quote='操作 2 等价两次操作 1，所以应该最大化操作 2 的次数……字母对 (s_p, t_p) 等于字母对 (t_q, s_q) 就可以执行一次操作 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i+1] = min(f[j] + op(j, i))`，枚举最后一段的左端点 `j`',
              '每段不反转：配对 `(x,y)` 与 `(y,x)` 换一次，剩下的替换，用 `cnt` 计数',
              '反转的代价 `rev_op[j][i]` 用==中心扩展==增量预处理（中心不变）'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错：反转本身要算 1 次，`rev_op` 的 `op` 从 1 开始',
                 '易错：偶数长度子串中心是 `[i//2, (i+1)//2]`，`l != r` 时要处理对称两对',
                 '题解还给了 `O(n^3)` 的优化前写法：每个 `[j,i]` 现场统计反转；这里选的是预处理 rev_op 并重构 update 的版本'],
    ),
)
