def _seg_text(S):
    if 'fa' not in S:
        return ''
    n = len(S['w'])
    q = S['q']
    i = S.get('i')
    if i is None:
        return '倒着看：删除变成添加；添加一个货物，可能把左右两段合并'
    present = [q[j] - 1 for j in range(i, n)]
    segs, cur = [], []
    for k in range(n):
        if k in present:
            cur.append(k)
        elif cur:
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    return '当前已放回的子段：' + '　'.join(f"`{[S['w'][k] for k in s]}` = =={sum(S['w'][k] for k in s)}==" for s in segs) if segs else '当前没有货物'


def _color(S, k, v):
    if 'q' not in S or 'i' not in S:
        return None
    n = len(S['w'])
    if k == S.get('x'):
        return 'yellow'
    return 'green' if k in [S['q'][j] - 1 for j in range(S['i'], n)] else None


def _dim(S, k, v):
    if 'q' not in S or 'i' not in S:
        return False
    n = len(S['w'])
    return k not in [S['q'][j] - 1 for j in range(S['i'], n)]


def _cap_loop(S, B, ret):
    if 'i' in B and S.i == B.i:
        return '循环结束'
    return f'倒序处理：第 `{S.i + 1}` 次取出的是货物 `{S.q[S.i]}`（下标 `{S.q[S.i] - 1}`），倒着看 = ==把它放回去=='


CONFIG = dict(
    num='meituan-002', title='小美的仓库整理', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='倒序 + 并查集',
    tags=[],
    code='''
def main():
    n = int(input())
    w = list(map(int, input().split()))
    q = list(map(int, input().split()))
    fa = list(range(n + 1))
    sum = [0] * (n + 1)
    def find(x: int) -> int:
        if fa[x] != x:
            fa[x] = find(fa[x])
        return fa[x]

    ans = [0] * n
    for i in range(n - 1, 0, -1):
        x = q[i] - 1
        to = find(x + 1)
        fa[x] = to  # 合并 x 和 x+1
        sum[to] += sum[x] + w[x]
        ans[i - 1] = max(ans[i], sum[to])
    print(*ans, sep='\\n')
''',
    setup='''
_in = iter(['5', '3 2 4 4 5', '4 3 5 2 1'])
input = lambda: next(_in)
OUT = []
def print(*a, sep=' ', **k):
    OUT.append(sep.join(map(str, a)))
''',
    call='''main()
OUT[0]''',
    expect='9\n5\n5\n3\n0',
    views=[
        dict(type='text', fn=_seg_text, size=26, h=60),
        dict(type='array', var='w', label='w（绿 = 已放回的货物，黄 = 这一步放回的）', pointers={'x': 'yellow'},
             color=_color, dim=_dim, cell=90),
        dict(type='array', var='fa', label='fa（并查集：fa[x] 指向 x 所在链的最右端，下标 n 是「幽灵火车头」）', pointers={'x': 'yellow'}, cell=80),
        dict(type='array', var=lambda S: S.get('sum'), label='sum（链尾下标上记录该子段的元素和）', cell=80),
        dict(type='array', var='ans', label='ans（每次取出后的最大一堆；ans[n-1] = 0）',
             color=lambda S, k, v: 'green' if 'i' in S and k >= S['i'] - 1 else None, cell=80),
    ],
    watch=[('i', 'i', 'blue'), 'x', 'to', ('ans', 'ans', 'green')],
    captions={
        'n = int': '读入货物数量 `n = {n}`',
        'w = list': '重量 `w = {w}`',
        'q = list': '取出顺序 `q = {q}`（货物编号 1~n）',
        'fa = list': '并查集 `fa`：下标 `0..n`，初始每个下标是自己的根；多开一个 `n` 当哨兵',
        'sum = [0]': '`sum[to]` 记录以 `to` 为链尾的子段元素和',
        'ans = [0]': '`ans[i]` = 第 `i+1` 次取出后的答案；最后一次取完什么都不剩，==`ans[n-1] = 0`==',
        'for i in range': _cap_loop,
        'x = q[i] - 1': '货物编号 `{q[i]}` → 下标 `x = {x}`',
        'to = find(x + 1)': '找右边相邻货物（下标 `x + 1`）所在链的链尾 `to`；右边没放回时，它就是 `x + 1` 自己',
        'fa[x] = to': '把 `x` 接到右边那条链上：`fa[{x}] = {to}`（只合并 x 和 x+1，不管 x−1）',
        'sum[to] +=': '子段和：`sum[{to}] += sum[{x}] + w[{x}]`（左边那段的和 + 新货物）= =={sum[to]}==',
        'ans[i - 1] = max': '`ans[{i - 1}] = max(ans[{i}], sum[{to}])` = `max({B.ans[i]}, {sum[to]})` = =={ans[i - 1]}==：最大堆要么是之前的，要么是刚合并出的',
        'fa[x] != x': lambda S, B, ret: (f'`fa[{S.x}] != {S.x}`：不是根，继续往上找' if S.fa[S.x] != S.x else f'`{S.x}` 就是根，直接返回'),
        'fa[x] = find(fa[x])': '路径压缩：`fa[{x}] = {fa[x]}`',
        'return fa[x]': '返回根 `{ret}`',
        'print(*ans': '按行输出 `ans`',
    },
    max_steps=70,
    cards=dict(
        one_liner='删除不好做，倒过来就是添加；添加时用并查集合并相邻子段',
        complexity='时间 `O(n α(n))`，空间 `O(n)`',
        problem=['货物 `1~n` 排成一堆，按顺序取出，取走一件就把所在堆一分为二',
                 '每次取出后，求==重量和最大的一堆==的重量',
                 '示例：`w = [3,2,4,4,5]`，取出 `[4,3,5,2,1]` → 输出 `9 5 5 3 0`',
                 '需要自己写输入输出（视频里用固定输入代替 `input()`）'],
        quote='删除不好做，添加比较好做。不妨倒着思考，删除变成了添加。添加时可能会合并两个子段。',
        quote_src='—— 灵茶山艾府题解（提示 1、2）',
        idea=['==倒着看==：最后什么都不剩（0），一件件把货物放回去',
              '放回下标 `x`：与右边相邻段合并，`fa[x] = find(x+1)`，段和累加到链尾',
              '链尾是「幽灵火车头」：每条链去掉最右的元素才是真实子段，所以只合并 `x` 和 `x+1`',
              '`ans[i-1] = max(ans[i], 合并后子段和)`'],
        summary=['时间 `O(n α(n))`，空间 `O(n)`；`w[i] <= 100`、`n <= 50000`',
                 '倒序从 `i = n-1` 到 `1`；`ans[n-1] = 0`，`ans[n-2]` 是最后一个放回的货物自己的重量',
                 '为了能逐行动画，视频把原脚本的顶层代码包进了 `def main():`，输入输出用固定数据和收集列表代替，逻辑一字未改',
                 '相似题：2334、1562（同样是倒序 + 并查集合并子段）'],
    ),
)
