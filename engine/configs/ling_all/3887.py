EDGES = [[0, 1, 1], [1, 2, 1], [0, 2, 1], [2, 3, 0], [1, 3, 0]]


def _uf(S, k):
    I = S.get('_inner', S)
    u = I.get('self') if hasattr(I, 'get') else None
    return getattr(u, k, None) if u is not None else None


def _fa(S):
    u = S.get('uf') or S.get('self')
    return getattr(u, 'fa', None) if u is not None and hasattr(u, 'fa') else None


def _dis(S):
    u = S.get('uf') or S.get('self')
    return getattr(u, 'dis', None) if u is not None and hasattr(u, 'dis') else None


def _edge(S):
    if 'x' in S and 'y' in S and 'w' in S and 'uf' in S:
        return f"当前边 `({S['x']}, {S['y']}, 权 {S['w']})`　已加入 ==`{S.get('ans', 0)}`== 条"
    return ''


CONFIG = dict(
    num=3887, title='增量偶权环查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='带权并查集 · 路径异或和',
    tags=['灵神题单', '常用数据结构', '难度分 2128'],
    code='''
class UnionFind:
    def __init__(self, n: int):
        self.fa = list(range(n))  # fa[x] 是 x 的代表元
        self.dis = [0] * n  # dis[x] = 从 x 到 fa[x] 的路径异或和

    def find(self, x: int) -> int:
        fa = self.fa
        if fa[x] != x:
            root = self.find(fa[x])
            self.dis[x] ^= self.dis[fa[x]]
            fa[x] = root
        return fa[x]

    def merge(self, from_: int, to: int, value: int) -> bool:
        x, y = self.find(from_), self.find(to)
        dis = self.dis
        if x == y:
            return dis[from_] ^ dis[to] == value
        dis[x] = value ^ dis[to] ^ dis[from_]
        self.fa[x] = y
        return True

class Solution:
    def numberOfEdgesAdded(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFind(n)
        ans = 0
        for x, y, w in edges:
            if uf.merge(x, y, w):
                ans += 1
        return ans
''',
    call=f'Solution().numberOfEdgesAdded(4, {EDGES})',
    expect=3,
    views=[
        dict(type='text', h=70, size=30, fn=_edge),
        dict(type='array', var=_fa, label='fa（代表元）', h=190, pointers={'from_': 'blue', 'to': 'pink'}),
        dict(type='array', var=_dis, label='dis（到 fa[x] 的路径异或和）', h=190,
             color=lambda S, i, v: 'orange' if v else None),
        dict(type='calls', h=220),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'w', ('ans', 'ans', 'green')],
    captions={
        'self.fa = list': '`fa[x] = x`：每个点自成一个连通块，代表元是自己',
        'self.dis = [0]': '`dis[x]`：x 到代表元的路径==异或和==，自己到自己为 0',
        'uf = UnionFind': '建好带权并查集',
        'ans = 0': '`ans` 统计成功加入的边数',
        'for x, y, w in edges': '取下一条边 `({x}, {y}, {w})`',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] != {S.x}`：不是代表元，要先找到根并压缩路径' if S.fa[S.x] != S.x
                                          else f'`fa[{S.x}] = {S.x}`：已经是代表元，直接返回'),
        'root = self.find': '递归找 `fa[x]` 的代表元 `root`',
        'self.dis[x] ^= ': '路径压缩：x 直连 root，所以 `dis[x]` 要再异或上父亲到根的 `dis`：`dis[{x}] = {self.dis[x]}`',
        'fa[x] = root': '`fa[{x}]` 直接指向根 `{root}`',
        'return fa[x]': '返回 `x` 的代表元 `{ret}`',
        'x, y = self.find': '分别对两端点 `find`：找代表元，同时把 `dis` 更新为到根的异或和',
        'if x == y': lambda S, B, r: (f'代表元相同 `{S.x} == {S.y}`：两点已连通，加这条边会成环' if S.x == S.y
                                      else f'代表元不同 `{S.x} != {S.y}`：连接两个连通块，不会形成新环，直接连'),
        'return dis[from_] ^': '环偶数 ⇔ 已有路径异或和 == 边权：`{dis[from_]} ^ {dis[to]} = {dis[from_] ^ dis[to]}` vs `{value}` → ==`{ret}`==',
        'dis[x] = value': '根 x 挂到根 y 下：`dis[x] = value ^ dis[to] ^ dis[from_]` = =={dis[x]}==（x→from→to→y 三段异或）',
        'self.fa[x] = y': '`fa[{x}] = {y}`：合并两个连通块',
        'return True': '合并成功，返回 True',
        'ans += 1': '这条边被加入，`ans` = =={ans}==',
        'return ans': '一共加入 `{ans}` 条边',
    },
    skip=['fa = self.fa', 'dis = self.dis', 'return True', 'return fa[x]'],
    max_steps=110,
    cards=dict(
        one_liner='环的边权和为偶数 ⇔ 两点间路径异或和唯一，用带权并查集维护',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['无向图 `n` 个点、初始无边，边权只有 `0` 或 `1`',
                 '按顺序处理每条边：加入后若==每个环的边权和仍是偶数==才加入',
                 '返回成功加入的边数。示例：`n=3, [[0,1,1],[1,2,1],[0,2,1]]` → `2`',
                 '本视频：`n=4`，5 条边 → `3`'],
        quote='当且仅当两条路径的异或和相同，环的边权和是偶数。……可以维护节点到其代表元 root 的路径异或和。从 x 到 y 的路径，可以拆分成先从 x 到 root，再从 root 到 y（重复走的边权会被异或抵消掉）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['权为 0/1，环权和是偶数 ⇔ 环上异或和为 0 ⇔ ==两条 x→y 路径异或和相同==',
              '加边 `(x,y,w)`：不同连通块直接连；同一连通块则要求 `dis[x] ^ dis[y] == w`',
              '`dis[x]` 记录到代表元的异或和，路径压缩时同步异或，重复边自动抵消'],
        summary=['时间 `O(n log n)`（只有路径压缩），空间 `O(n)`',
                 '合并时 `dis[x] = value ^ dis[to] ^ dis[from_]`：被挂靠的根 x 到新根 y 的权',
                 '`find` 里先递归再更新 `dis[x]`，顺序不能反',
                 '同一连通块内的边只判断、不合并；相似题：399. 除法求值'],
    ),
)
