def _frm(S):
    fr = S.get('frm')
    if fr is None:
        return ''
    items = [f'`{j}` ← {v}' for j, v in enumerate(fr) if v]
    return '新增边的起点（frm[终点] = 起点列表）：' + ('；'.join(items) if items else '暂无')


_flag = {}


def _entry(S):
    _flag['entry'] = True
    return f'终点 `{S.r}` 的最短路缩短为 `{S.f[S.r]}`'


def _for_i(S, B, ret):
    if _flag.pop('entry', False):
        return ('`r` 变近了，==后面的点都可能受影响==：从 `r+1` 往后按顺序重算' if S.r < len(S.f) - 1
                else '`r` 就是终点，后面没有点要重算')
    if B.get('i') == S.get('i'):
        return '`r` 之后的点都重算完了'
    return f'继续重算下一个点 `{S.i}`'


CONFIG = dict(
    num=3243, title='新增道路查询后的最短距离 I', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='DP 维护 0 到各点的最短路',
    tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 1568'],
    code='''
class Solution:
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        frm = [[] for _ in range(n)]
        f = list(range(n))
        ans = []
        for l, r in queries:
            frm[r].append(l)
            if f[l] + 1 < f[r]:
                f[r] = f[l] + 1
                for i in range(r + 1, n):
                    f[i] = min(f[i], f[i - 1] + 1, min((f[j] for j in frm[i]), default=inf) + 1)
            ans.append(f[-1])
        return ans
''',
    call='Solution().shortestDistanceAfterQueries(6, [[2,4],[0,2],[0,5]])',
    expect=[4, 3, 1],
    views=[
        dict(type='text', fn=lambda S: f"新增道路 `{S['l']} → {S['r']}`" if 'l' in S and 'r' in S else '', size=28, h=60),
        dict(type='text', fn=_frm, size=24, h=80),
        dict(type='array', var='f', label='f[i]：从 0 到 i 的最短路（蓝=边起点 l，粉=边终点 r，黄=正在重算）', cell=100, h=230,
             pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: 'yellow' if S.get('_line') in (11,) and i == S.get('i') else None),
        dict(type='array', var='ans', label='ans（每次查询后的答案）', cell=100, h=170, color=lambda S, i, v: 'green'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'i', ('f[-1]', 'f[-1]', 'green')],
    captions={
        'frm = [[]': '`frm[i]`：额外边里，终点是 `i` 的那些起点',
        'f = list(range(n))': '初始只有 `i → i+1` 的路，所以 `f[i] = i`：`f = {f}`',
        'ans = []': '`ans` 存每次查询后的答案',
        'for l, r in queries': lambda S, B, ret: (f'处理新道路 `{S.l} → {S.r}`' if (B.get('l'), B.get('r')) != (S.l, S.r)
                                                  else '所有查询都处理完了'),
        'frm[r].append(l)': '记下：`{r}` 多了一个来源 `{l}`，`frm[{r}] = {frm[r]}`',
        'if f[l] + 1 < f[r]': lambda S, B, ret: (f'走新路到 `{S.r}`：`f[{S.l}] + 1 = {S.f[S.l] + 1}`，现有 `f[{S.r}] = {S.f[S.r]}` → ==更短，要更新=='
                                                 if S.f[S.l] + 1 < S.f[S.r] else
                                                 f'走新路到 `{S.r}`：`f[{S.l}] + 1 = {S.f[S.l] + 1}` 不比 `f[{S.r}] = {S.f[S.r]}` 小 → ==不更新，后面都不变=='),
        'f[r] = f[l] + 1': lambda S, B, ret: _entry(S),
        'for i in range(r + 1, n)': _for_i,
        'f[i] = min(': '重算 `f[{i}]`：取「从 {i-1} 走一步 = {f[i-1]+1}」「从各来源 `{frm[i]}` 走一步」「原值」的最小值 → ==`{f[i]}`==',
        'ans.append(f[-1])': '本次查询后，0 到 `n-1` 的最短路是 `{f[-1]}`，记入 `ans`',
        'return ans': '全部查询处理完：`{ans}`',
    },
    cards=dict(
        one_liner='把「从 0 到 i 的最短路」存下来，加边后只往后更新',
        complexity='时间 `O(q(n+q))`，空间 `O(n+q)`',
        problem=['`n` 个城市，`i → i+1` 有单向路；每次查询新增一条单向路 `u → v`',
                 '每次加边后，求 `0 → n-1` 的最短路长度',
                 '示例：`n=5, queries=[[2,4],[0,2],[0,4]]` → `[3,2,1]`',
                 '本视频：`n=6, [[2,4],[0,2],[0,5]]` → `[4,3,1]`'],
        quote='定义 f[i] 为从 0 到 i 的最短路。我们可以从 i-1 到 i，也可以从 from[i][j] 到 i，这些位置作为转移来源，用其 f 值 +1 更新 f[i] 的最小值。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['所有边都从小编号指向大编号 → 图是 DAG，`f` 按下标顺序就能递推',
              '新边 `l → r`：只有 `f[l]+1 < f[r]` 才有用，否则什么都不用改',
              '有用时，`r` 之后的 `f[i]` 按顺序重新取最小值'],
        summary=['时间 `O(q(n+q))`，空间 `O(n+q)`',
                 '易错：加边 `l → r` 后必须先判断 `f[l]+1 < f[r]`，不然白白重算',
                 '易错：重算 `f[i]` 要同时考虑 `i-1 → i` 和所有额外边的起点',
                 '方法一是每次加边后重跑 BFS，更直观但更慢；本视频演示的是方法二'],
    ),
)
