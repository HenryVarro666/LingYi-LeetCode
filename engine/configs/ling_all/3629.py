SETUP = '''
from itertools import count
# 预处理每个数的质因子列表，思路同埃氏筛（本视频的小例子只需要 MX 很小；原题 MX = 1_000_001）
MX = 20
prime_factors = [[] for _ in range(MX)]
for i in range(2, MX):
    if not prime_factors[i]:  # i 是质数
        for j in range(i, MX, i):  # i 的倍数有质因子 i
            prime_factors[j].append(i)
'''


def _txt(S):
    ln = S.get('_line', 0)
    if ln < 9:
        return '预处理：质数 p → 所有含质因子 p 的下标（传送目标）'
    if ln < 13:
        return '准备 bfs：`vis` 标记已访问，`q` 是当前层'
    i = S['i']
    v = S['nums'][i]
    return f"当前下标 `i = {i}`，`nums[i] = {v}`，已走 ==`{S['ans']}`== 步；终点是 `{len(S['nums']) - 1}`"


CONFIG = dict(
    num=3629, title='通过质数传送到达终点的最少跳跃次数', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='图论建模 + bfs · 质因子分组',
    tags=['图论算法', '数学算法', '难度分 2139'],
    code='''
class Solution:
    def minJumps(self, nums: List[int]) -> int:
        n = len(nums)
        groups = defaultdict(list)
        for i, x in enumerate(nums):
            for p in prime_factors[x]:
                groups[p].append(i)  # 对于质数 p，可以跳到下标 i

        vis = [False] * n
        vis[0] = True
        q = [0]

        for ans in count(0):
            tmp = q
            q = []
            for i in tmp:
                if i == n - 1:
                    return ans
                idx = groups[nums[i]]
                idx.append(i + 1)
                if i:
                    idx.append(i - 1)
                for j in idx:  # 可以从 i 跳到 j
                    if not vis[j]:
                        vis[j] = True
                        q.append(j)
                idx.clear()  # 避免重复访问下标列表
''',
    setup=SETUP,
    call='Solution().minJumps([2,3,4,7,9])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='nums', label='nums（蓝 = 当前下标，绿 = 已访问）', h=150,
             color=lambda S, i, v: ('blue' if S.get('i') == i and S.get('_line', 0) >= 16 else 'green' if 'vis' in S and S['vis'][i] else None)),
        dict(type='map', var='groups', fmt=lambda k, v: f'{k}: {v}', label='groups：质数 → 可传送到的下标', h=230),
        dict(type='array', var='q', label='下一层 q（本层 bfs 新发现的下标）', h=130),
    ],
    watch=[('ans', 'ans', 'yellow'), 'i', 'idx', 'vis'],
    max_steps=62,
    skip=['for p in prime_factors[x]:', 'tmp = q'],
    captions={
        'n = len': '`n = {n}`，终点是下标 `{n - 1}`',
        'groups = defaultdict': '`groups`：key 是质数，value 是下标列表',
        'groups[p].append(i)': '`nums[{i}] = {x}` 含质因子 `{p}` → 质数 `{p}` 的传送目标里加入下标 `{i}`',
        'vis = [False]': '`vis[i]` 表示下标 `i` 已经入过队，不会重复访问',
        'vis[0] = True': '起点 0 先标记访问',
        'q = [0]': 'bfs 从 0 出发，`q` 是当前层',
        'for ans in count(0)': '开始第 ==`{ans}`== 层：从起点走 `{ans}` 步能到的下标',
        'q = []': '`tmp` 是这一层，`q` 清空来装下一层（双列表 bfs）',
        'if i:': lambda S, B, r: ('`i > 0`，左边还有格子' if S.i else '`i = 0` 没有左邻居'),
        'for i in tmp': lambda S, B, r: (f'取出下标 `i = {S.i}`，`nums[i] = {S.nums[S.i]}`' if B.get('i') != S.get('i') or 'i' not in B or B.get('ans') != S.get('ans') else '这一层处理完，进入下一层'),
        'if i == n - 1': lambda S, B, r: (f'`i = {S.i}` 是终点 → 最少跳 ==`{S.ans}`== 次' if S.i == S.n - 1 else f'`i = {S.i}` 不是终点 `{S.n - 1}`，继续扩展'),
        'idx = groups[nums[i]]': '`nums[{i}] = {nums[i]}`：若它是质数，`groups` 里就是它所有倍数的下标；不是质数则是空列表',
        'idx.append(i + 1)': '相邻右移：下标 `{i + 1}` 加入候选',
        'idx.append(i - 1)': '相邻左移：下标 `{i - 1}` 加入候选',
        'for j in idx': lambda S, B, r: f'逐个看候选 `j = {S.j}`（候选 `{S.idx}`）' if B.get('j') != S.get('j') or 'j' not in B else '候选都看完了',
        'if not vis[j]': lambda S, B, r: (f'`vis[{S.j}] = False` → 第一次到达，最短路就是 `ans + 1`' if not S.vis[S.j] else f'下标 `{S.j}` 已经访问过，跳过'),
        'vis[j] = True': '标记 `vis[{j}] = True`',
        'q.append(j)': '`{j}` 进入下一层',
        'idx.clear()': '清空这个质数的下标列表：下次再遇到同一质数不用重复遍历，每个下标最多被传送一次',
    },
    cards=dict(
        one_liner='bfs 最短路，质数的倍数下标用哈希表一次性分组',
        complexity='时间 `O(n log U)`，空间 `O(n log U)`',
        problem=['从下标 0 出发到 `n-1`，每步可以走到相邻格子',
                 '若 `nums[i]` 是质数 `p`，还能传送到任意满足 `nums[j] % p == 0` 的下标',
                 '示例：`nums=[2,3,4,7,9]` → `2`（0 → 1，再传送到 4）'],
        quote='预处理。在执行 BFS 之前，对于 nums 中的每个数 x=nums[i]，把 x 的的质因子 p 和下标 i 插入哈希表。哈希表的 key 是质数，value 是下标列表。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一个下标 = 图中一个点，一步 = 一条边，求 0 到 `n-1` 最短路',
              '`groups[p]` 存所有含质因子 `p` 的下标；当前值是质数 `p`，就能传送到 `groups[p]`',
              '遍历完立刻 `clear`：同一个质数的列表只展开一次，避免退化'],
        summary=['时间 `O(n log U)`：下标列表总长度是 `O(n log U)`，每个下标最多入队一次',
                 '易错点：`idx.clear()` 不能漏，否则很多个质数 2 会重复遍历列表而超时',
                 '`groups[nums[i]]` 只在 `nums[i]` 是质数时才非空（合数不是任何 key）',
                 '预处理 `prime_factors` 用埃氏筛思想；视频里 `MX` 缩小到 20，原题是 `1_000_001`',
                 '灵神方法二是逆向 bfs：从终点倒着走，只对质数建表'],
    ),
)
