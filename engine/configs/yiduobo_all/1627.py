_COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _color(S, i, v):
    fa = S.get('fa')
    if not isinstance(fa, list) or i == 0:
        return None
    r = _root(fa, i)
    size = sum(1 for j in range(1, len(fa)) if _root(fa, j) == r)
    if size < 2:
        return None
    return _COLS[r % len(_COLS)]


def _qtxt(S):
    q = S.get('queries')
    if q is None:
        return ''
    res = S.get('res')
    out = []
    for k, (x, y) in enumerate(q):
        mark = ''
        if isinstance(res, list) and k < len(res):
            mark = ' → ' + ('True' if res[k] else 'False')
        out.append(f'`({x},{y})`{mark}')
    return '查询：' + '　'.join(out)


CONFIG = dict(
    num=1627, title='带阈值的图连通性', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='枚举公因数 z 的倍数 + 并查集',
    tags=['常用数据结构', '数学算法'],
    code='''
class Solution(object):
    def areConnected(self, n, threshold, queries):

        fa = list(range(n + 1))
        for z in range(threshold + 1, n):
            fa_z = self.find(fa, z)
            tmp = z + z
            while tmp <= n:
                fa_tmp = self.find(fa, tmp)
                if fa_z != fa_tmp:
                    fa[fa_tmp] = fa_z
                
                tmp += z
        
        res = []
        for x, y in queries:
            res.append(self.find(fa, x) == self.find(fa, y))
        
        return res

    def find(self, fa, now):
        if fa[now] != now:
            fa[now] = self.find(fa, fa[now])
        return fa[now]
''',
    call='Solution().areConnected(6, 1, [[1,4],[2,6],[3,4]])',
    expect=[False, True, True],
    views=[
        dict(type='text', fn=lambda S: (f"公因数 `z = {S['z']}`：它的倍数 `{S['z']}, {2*S['z']}, {3*S['z']}, …` 彼此相连" if 'z' in S and 'res' not in S else _qtxt(S)), size=30),
        dict(type='array', var='fa', label='fa（下标 = 城市编号，值 = 父亲；同色 = 同一连通块）', h=260, cell=84,
             pointers={'z': 'blue', 'tmp': 'pink'}, color=_color,
             dim=lambda S, i, v: i == 0),
        dict(type='text', fn=lambda S: (f"查询 `({S['x']}, {S['y']})`：根相同才连通" if 'x' in S and 'y' in S and 'res' in S else ''), size=30),
    ],
    watch=[('z', 'z', 'blue'), ('tmp', 'tmp', 'pink'), 'fa_z', 'fa_tmp', ('res', 'res', 'green')],
    captions={
        'fa = list': '并查集初始化：每个城市自成一块，`fa = {fa}`',
        'for z in range': '枚举公因数 `z = {z}`（只有 `z > threshold` 才有资格当公因数）',
        'fa_z = self.find': '先找 `z = {z}` 当前所在块的根 `fa_z`',
        'tmp = z + z': '从 `2z = {tmp}` 开始，沿着 `z` 的倍数往上走',
        'while tmp <= n': lambda S, B, r: (f'`tmp = {S.tmp}` ≤ `n = {S.n}`：它是 `{S.z}` 的倍数，要和 `{S.z}` 连起来' if S.tmp <= S.n else f'`tmp = {S.tmp}` > `n = {S.n}`：`{S.z}` 的倍数走完了'),
        'fa_tmp = self.find': '`{tmp}` 所在块的根 `fa_tmp`',
        'if fa_z != fa_tmp': lambda S, B, r: ('两个根不同 → 还不在同一块，要合并' if S.fa_z != S.fa_tmp else f'两个根都是 `{S.fa_z}` → 已经连通，不用动'),
        'fa[fa_tmp] = fa_z': '合并：`fa[{fa_tmp}] = {fa_z}`，`fa = {fa}`',
        'res = []': '开始回答查询：只要两个城市的根相同，就连通',
        'for x, y in queries': '查询 `({x}, {y})`',
        'res.append': '分别找 `{x}`、`{y}` 的根，比较是否相等，把结果加入 `res`',
        'return res': '所有查询回答完，返回 `{ret}`',
        'if fa[now] != now': lambda S, B, r: (f'`fa[{S.now}] = {S.fa[S.now]}` ≠ `{S.now}`：不是根，继续往上找' if S.fa[S.now] != S.now else f'`{S.now}` 的父亲是自己：它就是根'),
        'fa[now] = self.find': '路径压缩：`fa[{now}]` 直接指向根 `{fa[now]}`',
        'return fa[now]': '返回根 `{ret}`',
    },
    skip=['tmp += z', 'return fa[now]', 'res = []'],
    max_steps=110,
    cards=dict(
        one_liner='z 的所有倍数彼此相连：枚举 z，把倍数并到一起',
        complexity='时间 `O(n log n · α(n))`，空间 `O(n)`',
        problem=['`n` 个城市编号 `1..n`；两城市 `x`、`y` 直接相连，当且仅当存在 `z > threshold` 同时整除二者',
                 '给若干查询 `(a, b)`，判断是否连通（可经过中转）',
                 '示例：`n=6, threshold=1, queries=[(1,4),(2,6),(3,4)]` → `[F,T,T]`'],
        quote='对于任意大于threshold的数k而言，点k、2k、...、mk之间都是相连的。由于题目只关心连通性而不管关心具体图的构成，因此在这里可以使用并查集来维护这个连通性。',
        quote_src='—— yiduobo 题解原文',
        idea=['不需要真的建图：`z` 的倍数 `z, 2z, 3z, …` 全在一个连通块里',
              '从 `threshold + 1` 枚举到 `n`，把 `z` 和 `2z、3z、…` 用并查集合并',
              '总共合并 `n/(t+1) + … + n/n` 次，约 `n log n`（调和级数）',
              '查询只要比较两个城市的根'],
        summary=['时间 `O(n log n · α(n))`，空间 `O(n)`',
                 '易错点：`z` 要从 `threshold + 1` 开始；阈值以下的数不能当公因数',
                 '`find` 里做了路径压缩，递归深度不会太深',
                 '原文为 Python 2 写法，`fa = range(n + 1)` 已改为 `fa = list(range(n + 1))`（Python 3 的 range 不能赋值）',
                 '作者说也可以按筛法改进枚举，这里用最直观的写法'],
    ),
)
