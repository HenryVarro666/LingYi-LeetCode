N, P, BANNED, K = 8, 1, [4, 6], 4


def _win(S, which):
    if S['_line'] is None or 'mn' not in S or 'i' not in S:
        return None
    return max(0, S['mn']) if which == 0 else min(S['mx'], S['n'] - 1)


def _pj(S):
    return S['j'] if S.get('j', 99) < S['n'] else None


def _fa_color(S, i, v):
    if i >= S['n']:
        return 'orange'
    return None


CONFIG = dict(
    num=2612, title='最少翻转操作数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='BFS + 并查集删点',
    tags=['图论算法', '难度分 2824'],
    code='''
class UnionFind:
    def __init__(self, n: int):
        self.fa = list(range(n))

    def find(self, x: int) -> int:
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]

    def merge(self, from_: int, to: int) -> None:
        self.fa[self.find(from_)] = self.find(to)

class Solution:
    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        indices = UnionFind(n + 2)
        indices.merge(p, p + 2)  # 删除 p
        for i in banned:
            indices.merge(i, i + 2)  # 删除 i

        ans = [-1] * n
        ans[p] = 0
        q = deque([p])
        while q:
            i = q.popleft()
            mn = max(i - k + 1, k - i - 1)
            mx = min(i + k - 1, n * 2 - k - i - 1)
            j = indices.find(mn)
            while j <= mx:
                ans[j] = ans[i] + 1
                q.append(j)
                indices.merge(j, mx + 2)  # 删除 j
                j = indices.find(j + 2)  # 快速跳到 >= j+2 的下一个下标
        return ans
''',
    call=f'Solution().minReverseOperations({N}, {P}, {BANNED}, {K})',
    expect=[3, 0, 1, 2, -1, 2, -1, -1],
    views=[
        dict(type='array', var='ans', label='ans（绿 = 已求出最少步数，红 = 被禁止）', cell=84, h=190,
             pointers={'i': 'blue', _pj: 'pink'},
             pointer_labels={_pj: 'j'},
             window=(lambda S: _win(S, 0), lambda S: _win(S, 1)),
             color=lambda S, i, v: 'red' if i in BANNED else ('green' if v >= 0 else None)),
        dict(type='array', var='indices.fa', label='并查集 fa（fa[x] 指向 >= x 的下一个没删除的同奇偶下标；橙 = 哨兵）', cell=70, h=190,
             pointers={'j': 'pink'}, color=_fa_color),
        dict(type='queue', var='q', label='BFS 队列 q', h=110),
        dict(type='text', h=90, size=30, fn=lambda S: (
            f"从 `i={S['i']}` 翻转一次，能到的下标：`{S['mn']}` 到 `{S['mx']}`，公差 2（同奇偶）"
            if 'mx' in S and 'i' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('mn', 'mn', 'cyan'), ('mx', 'mx', 'orange'), ('j', 'j', 'pink')],
    skip=['for i in banned', 'ans = [-1] * n', 'q = deque([p])', 'q.append(j)', 'if self.fa[x] != x', 'self.fa[x] = self.find', 'return self.fa[x]', 'self.fa = list', 'self.fa[self.find(from_)]'],
    max_steps=110,
    captions={
        'indices = UnionFind': '并查集的 `fa[x]=x` 表示 x 还没删；多开两个哨兵 `n`、`n+1`，保证 `mx+2` 一定存在',
        'indices.merge(p, p + 2)': '起点已访问，把 `p={p}` 并到 `p+2`：以后 `find` 会直接跳过它',
        'indices.merge(i, i + 2)': '被禁止的下标 `{i}` 同样并到 `{i}+2`，等于从“未访问集合”里删掉',
        'ans[p] = 0': '起点 `p` 需要 0 次操作',
        'i = q.popleft()': '取出队首 `i = {i}`：它能翻到哪些下标？',
        'mn = max': '最小能到：`max(i-k+1, k-i-1) = {mn}`（后者是子数组贴左边界）',
        'mx = min': '最大能到：`min(i+k-1, 2n-k-i-1) = {mx}`（后者是子数组贴右边界）',
        'j = indices.find(mn)': '`find({mn})`：找 >= `{mn}` 的第一个没访问、没禁止的下标（找不到就落在哨兵 `n`）',
        'while j <= mx': lambda S, B, r: (f'`j = {S.j}` <= `mx = {S.mx}`：还在可达范围内 → 是新下标，访问它' if S.j <= S.mx
                                         else f'`j = {S.j}` > `mx = {S.mx}`：范围内没有未访问的新下标了，处理下一个队首'),
        'ans[j] = ans[i] + 1': '`j={j}` 第一次被到达，BFS 保证最短：`ans[{j}] = ans[{i}] + 1 = {ans[j]}`',
        'q.append(j)': '`j={j}` 入队，下一轮从它出发',
        'indices.merge(j, mx + 2)': '`j={j}` 已访问：并到 `mx+2={mx+2}`，一步到位地跳过 `[j, mx]` 内同奇偶的点',
        'j = indices.find(j + 2)': '`find(j+2)`：快速跳到 >= `j+2` 的下一个没访问的下标',
        'return ans': 'BFS 结束，没被访问到的下标保持 -1：`{ans}`',
    },
    cards=dict(
        one_liner='把翻转看成连边，BFS 最短路；用并查集跳过已访问点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['长为 `n` 的数组只有下标 `p` 处是 1；每次翻转长 `k` 的子数组，1 不能落在 `banned` 上',
                 '求 1 到达每个下标的最少操作次数，到不了为 `-1`',
                 f'本视频：`n={N}, p={P}, banned={BANNED}, k={K}` → `[3,0,1,2,-1,2,-1,-1]`'],
        quote='翻转前后的下标之和恒等于 L+R，所以下标 i 在翻转后的下标是 L+R-i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组每滑动一格，翻转后的下标变 ==2==：能到的下标是公差为 2 的等差数列',
              '范围 `[max(i-k+1,k-i-1), min(i+k-1,2n-k-i-1)]`，同奇偶',
              '边权都是 1 → ==BFS==；用并查集 `find` 跳过已访问下标，每个点只出队入队一次'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '哨兵 `n`、`n+1` 保证 `merge(j, mx+2)` 不越界',
                 '易错：起点 `p` 和 `banned` 要先从集合里删掉；上下界要考虑贴边的 `k-i-1` 和 `2n-k-i-1`',
                 '另一种写法：BFS + 有序集合（SortedList）按奇偶分别维护没访问的下标，思路相同'],
    ),
)
