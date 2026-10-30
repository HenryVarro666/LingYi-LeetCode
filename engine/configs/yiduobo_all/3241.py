# 示例 3：edges=[[2,4],[0,1],[2,3],[0,2]] -> [4,6,3,5,5]
POS_ = {0: (0.5, 0.10), 1: (0.22, 0.50), 2: (0.78, 0.50), 3: (0.62, 0.90), 4: (0.94, 0.90)}
EDGE_ = [(0, 1), (0, 2), (2, 3), (2, 4)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 150, y1 - y0 - 130
    P = {k: (x0 + 75 + v[0] * W, y0 + 65 + v[1] * H) for k, v in POS_.items()}
    inn = S.get('_inner', {})
    cx, cy = inn.get('now'), inn.get('nxt')
    cv.text((x0 + 18, y0 + 4), '蓝 = 奇数点（进入它要 1），紫 = 偶数点（进入它要 2）；黄框 now，粉框 nxt', 22, T['muted'], bold=True)
    for a, b in EDGE_:
        hot = (cx, cy) in ((a, b), (b, a))
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    f, res = S.get('f'), S.get('res')
    for k, (px, py) in P.items():
        cv.rect((px - 26, py - 26, px + 26, py + 26), fill=T['blue'] if k % 2 else T['purple'], r=26)
        if k == cx:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['yellow'], width=5, r=34)
        if k == cy:
            cv.rect((px - 34, py - 34, px + 34, py + 34), outline=T['pink'], width=5, r=34)
        cv.text((px, py), k, 30, T['bg'], anchor='mm', bold=True)
        lines = []
        if f is not None:
            lines.append((f'f={f[k]}', T['cyan']))
        if res is not None and res[k] != 0:
            lines.append((f'res={res[k]}', T['orange']))
        left = k == 1
        for i, (s, c) in enumerate(lines):
            cv.text((px - 40 if left else px + 40, py - 14 + i * 28), s, 23, c, anchor='rm' if left else 'lm', bold=True, mono=True)


def c_f(S, B, ret):
    now, nxt = S['_inner']['now'], S['_inner']['nxt']
    return (f'`f[{now}] = max(f[{now}], f[{nxt}] + 2 - {nxt}%2)`：孩子 {nxt} 的深度 `{S.f[nxt]}` + 边权 `{2 - nxt % 2}`'
            f' → `f[{now}]` = =={S.f[now]}==')


def c_cost(S, B, ret):
    return f'`cost = f[{S.nxt}] + 2 - {S.nxt} % 2` = {S.f[S.nxt]} + {2 - S.nxt % 2} = =={S.cost}==：从 `{S.now}` 往 `{S.nxt}` 方向走的最长时间'


def c_first(S, B, ret):
    return f'`cost = {S.cost}` 超过最大 `{B.first}` → 最大变成 =={S.first}==，旧最大退居次大 `{S.second}`'


def c_second(S, B, ret):
    return f'没超过最大，但超过次大 → `second = {S.second}`（以后绕开最大那一路时要用它）'


def c_res(S, B, ret):
    return f'`res[{S.now}] = first` = =={S.res[S.now]}==：把==所有方向==（含父亲）里最长的一路当作答案；`f[{S.now}]` 也改成它'


def c_cut(S, B, ret):
    return f'`{S.nxt}` 的这一路正是最大 `{S.first}` → 以 `{S.nxt}` 为根时，`{S.now}` 不能再走回 `{S.nxt}`，先把 `f[{S.now}]` 暂时换成次大 =={S.second}=='


CONFIG = dict(
    num=3241, title='标记所有节点需要的时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='换根 DP · 边做边改 f',
    tags=['灵神题单', '动态规划', '难度分 2522'],
    code='''
class Solution(object):
    def timeTaken(self, edges):

        n = len(edges) + 1

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [0] * n

        def dfs(now, fa):
            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now)
                f[now] = max(f[now], f[nxt] + 2 - nxt % 2)

        dfs(0, -1)
        
        res = [0] * n

        def calc(now, fa):
            first = second = 0
            for nxt in g[now]:
                cost = f[nxt] + 2 - nxt % 2
                if cost > first:
                    first, second = cost, first
                elif cost > second:
                    second = cost

            res[now] = first
            f[now] = first

            for nxt in g[now]:
                if nxt == fa:
                    continue
                cost = f[nxt] + 2 - nxt % 2
                if cost == first:
                    f[now] = second
                    calc(nxt, now)
                    f[now] = first
                else:
                    calc(nxt, now)

        calc(0, -1)
        return res
''',
    call='Solution().timeTaken([[2,4],[0,1],[2,3],[0,2]])',
    expect=[4, 6, 3, 5, 5],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=150),
    ],
    watch=['now', 'nxt', 'cost', 'first', 'second'],
    skip=['n = len(edges)', 'g = [[]', 'g[x].append', 'g[y].append', 'for x, y in edges', 'f = [0] * n', 'res = [0] * n',
          'if nxt == fa', 'continue', 28, 34, 'for nxt in g[now]', 'first = second = 0'],
    captions={
        'f[now] = max(f[now]': c_f,
        'dfs(0, -1)': '第一遍：以 0 为根，`f[i]` = 从 `i` 往下走、标完子树的最短时间（边权 `2 - 孩子%2`）',
        'calc(0, -1)': '第二遍：换根。每个点要把「向上走」也算进去，所以重新求最大 `first`、次大 `second`',
        27: c_cost,
        29: c_first,
        30: lambda S, B, r: f'没超过最大 `{S.first}`，再和次大 `{S.second}` 比：`{S.cost} > {S.second}` → ' + ('==成立==' if S.cost > S.second else '不成立，丢掉'),
        31: c_second,
        33: c_res,
        39: lambda S, B, r: f'再扫一遍孩子（跳过父亲）：`{S.nxt}` 这一路 `cost = {S.cost}`',
        40: lambda S, B, r: (f'`cost = {S.cost}` ' + ('==等于== ' if S.cost == S.first else '不等于 ') + f'最大 `{S.first}`：' +
                              ('最长的一路正好经过 `{0}`'.format(S.nxt) if S.cost == S.first else f'最长的一路不经过 `{S.nxt}`，`f[{S.now}]` 不用改')),
        41: c_cut,
        43: '`calc({nxt}, ...)` 返回，把 `f[{now}]` 恢复成最大 `first` = =={first}==',
        44: '`f[{now}]` 本来就不含 `{nxt}` 的最长路，直接递归求 `{nxt}`',
        'return res': '每个点的 `res` 都算好了',
    },
    cards=dict(
        one_liner='换根时临时把 `f[now]` 改成「不含孩子那一路」的值，递归完再还原',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，0 时刻标记点 `i`：奇数点晚 1 时刻、偶数点晚 2 时刻被相邻点传染',
                 '对每个起点，求整棵树被标记完的时刻',
                 '示例：`edges=[[2,4],[0,1],[2,3],[0,2]]` → `[4,6,3,5,5]`'],
        quote='需要特别注意的是，这里必须边做边算，不能一开始计算first和second，因为一开始计算的f值只包含向下标记的时间，但是first和second应该也包含经过父节点向上标记所需的时间。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i] = max(f[j] + 2 - j%2)`：以 `i` 为根向下标完子树的时间，一遍 DFS 求出',
              '换根：`i` 作为起点，要在所有相邻点（含父亲）里取最长一路 `first`',
              '递归进最长那个孩子 `j` 前，把 `f[i]` 临时改成次大 `second`——否则 `j` 会「绕回自己」'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：必须==边递归边更新== `f[now]`，父亲的 `f` 才包含「向上」那一路',
                 '最长的一路恰好是该孩子时，用次大值；否则最大值不受影响',
                 '代码里 `first` 的循环包含父亲（不跳过 `fa`），因为父亲此时的 `f` 已是修正后的值'],
    ),
)
