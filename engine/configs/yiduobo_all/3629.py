def _txt(S):
    if 'index_list' not in S:
        return '把每个下标看成图中的点：相邻有边，质数还连到它的所有倍数'
    if 'index' not in S or 'head' not in S:
        return '准备 bfs：`vis_index` 记下标，`vis_num` 记已展开过的数值'
    return f"当前下标 `index = {S['index']}`，`nums[index] = {S['nums'][S['index']]}`，已跳 ==`{S['res']}`== 步；终点是 `{S['n'] - 1}`"


CONFIG = dict(
    num=3629, title='通过质数传送到达终点的最少跳跃次数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='bfs · 下标去重 + 数值去重',
    tags=['图论算法', '数学算法', '难度分 2139'],
    code='''
class Solution(object):
    def minJumps(self, nums):

        ma = max(nums)
        n = len(nums)
        vis_num = [False] * (ma + 1)
        vis_index = [False] * n
        index_list = [[] for _ in range(ma + 1)]
        for index, v in enumerate(nums):
            index_list[v].append(index)

        prime = [True] * (ma + 1)
        prime[0] = False
        prime[1] = False
        v = 2
        while v <= ma:
            if prime[v]:
                for x in range(v + v, ma + 1, v):
                    prime[x] = False
            v += 1

        q = [0]
        head, tail = 0, 1
        vis_index[0] = True
        res = 0
        while head < tail:
            if vis_index[n - 1]:
                return res
            res += 1
            for index in q[head : tail]:
                v = nums[index]
                if prime[v]:
                    for x in range(v, ma + 1, v):
                        if not vis_num[x]:
                            for nxt_index in index_list[x]:
                                if not vis_index[nxt_index]:
                                    q.append(nxt_index)
                                    vis_index[nxt_index] = True
                            vis_num[x] = True

                if index > 0 and not vis_index[index - 1] and not vis_num[nums[index - 1]]:
                    q.append(index - 1)
                    vis_index[index - 1] = True
                if index < n - 1 and not vis_index[index + 1] and not vis_num[nums[index + 1]]:
                    q.append(index + 1)
                    vis_index[index + 1] = True

            head, tail = tail, len(q)

        return res
''',
    call='Solution().minJumps([2,3,4,7,9])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='nums', label='nums（蓝 = 当前下标，绿 = 已访问）', h=150,
             color=lambda S, i, v: ('blue' if S.get('index') == i and S.get('_line', 0) >= 28 else 'green' if S.get('head') is not None and S['vis_index'][i] else None)),
        dict(type='array', var=lambda S: ['T' if b else '·' for b in S['vis_num']] if 'vis_num' in S else None, label='vis_num[值]：这个数值的倍数下标已展开过', h=150,
             color=lambda S, i, v: 'orange' if v == 'T' else None),
        dict(type='array', var=lambda S: S.get('q') if 'q' in S else None, label='队列 q', h=130),
    ],
    watch=[('res', 'res', 'yellow'), 'head', 'tail', 'index', 'v', 'x'],
    max_steps=66,
    skip=['ma = max', 'prime = [True]', 'prime[0] = False', 'prime[1] = False', 'v = 2', 'while v <= ma', 'if prime[v]:',
          'for x in range(v + v', 'prime[x] = False', 'v += 1', 'for index, v in enumerate', 'index_list = ', 'index_list[v].append'],
    captions={
        'n = len': '`n = {n}`，终点是下标 `{n - 1}`；`ma = {ma}` 是最大值',
        'vis_num = ': '`vis_num[x]`：数值 `x` 的所有下标是否已被传送展开过（数值去重）',
        'vis_index = ': '`vis_index[i]`：下标 `i` 是否已访问（下标去重）',
        'q = [0]': 'bfs 队列从下标 0 开始',
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一层',
        'vis_index[0] = True': '起点已访问',
        'res = 0': '`res` 是已经跳的步数（层数）',
        'while head < tail': '`head < tail`：这一层还有点',
        'if vis_index[n - 1]': lambda S, B, r: (f'终点 `{S.n - 1}` 已访问 → 答案 ==`res = {S.res}`==' if S.vis_index[S.n - 1] else f'终点还没到，继续下一层'),
        'res += 1': '再跳一步，下面是第 ==`{res}`== 步能到的点',
        'for index in q': lambda S, B, r: (f'处理 `q[{S.head}:{S.tail}]` 里的 `index = {S.index}`' if B.get('index') != S.get('index') else '这一层的下标都处理完了'),
        'v = nums[index]': '`v = nums[{index}] = {nums[index]}`',
        'if prime[v]': lambda S, B, r: (f'`{S.v}` 是质数 → 可以传送到 `{S.v}` 的所有倍数所在的下标' if S.prime[S.v] else f'`{S.v}` 不是质数，不能传送，只能走相邻格子'),
        'for x in range(v, ma + 1, v)': lambda S, B, r: (f'枚举 `v` 的倍数 `x = {S.x}`（`v`, `2v`, `3v`, ...）' if B.get('x') != S.get('x') else '`v` 的倍数枚举完了'),
        'if not vis_num[x]': lambda S, B, r: (f'数值 `{S.x}` 还没展开过 → 把值为 `{S.x}` 的所有下标加入队列' if not S.vis_num[S.x] else f'数值 `{S.x}` 的下标已经全入队过，不用再看（数值去重）'),
        'for nxt_index in index_list[x]': lambda S, B, r: (f'值为 `{S.x}` 的下标有 `{S.index_list[S.x]}`，看 `{S.nxt_index}`' if S.index_list[S.x] and B.get('nxt_index') != S.get('nxt_index') else ('值为 %d 的下标看完了' % S.x if S.index_list[S.x] else f'没有值为 `{S.x}` 的下标')),
        'if not vis_index[nxt_index]': lambda S, B, r: (f'下标 `{S.nxt_index}` 没访问过 → 传送到这里' if not S.vis_index[S.nxt_index] else f'下标 `{S.nxt_index}` 已访问，跳过'),
        'vis_num[x] = True': '数值 `{x}` 标记为已展开',
        'if index > 0 and not': lambda S, B, r: (f'左邻居 `{S.index - 1}` 可走（没访问过）' if S.index > 0 and not S.vis_index[S.index - 1] and not S.vis_num[S.nums[S.index - 1]] else '左边没有可走的邻居（越界、已访问，或它的数值已展开过）'),
        'if index < n - 1 and not': lambda S, B, r: (f'右邻居 `{S.index + 1}` 可走（没访问过）' if S.index < S.n - 1 and not S.vis_index[S.index + 1] and not S.vis_num[S.nums[S.index + 1]] else '右边没有可走的邻居（越界、已访问，或它的数值已展开过）'),
        'q.append(index - 1)': '左邻居 `{index - 1}` 入队',
        'q.append(index + 1)': '右邻居 `{index + 1}` 入队',
        'vis_index[nxt_index] = True': '标记下标 `{nxt_index}` 已访问',
        'vis_index[index - 1] = True': '标记下标 `{index - 1}` 已访问',
        'vis_index[index + 1] = True': '标记下标 `{index + 1}` 已访问',
        'q.append(nxt_index)': '传送目标 `{nxt_index}` 入队',
        'head, tail = tail, len(q)': '这一层结束，新一层是 `q[{head}:{tail}]`',
        'return res': '返回 ==`{res}`==',
    },
    cards=dict(
        one_liner='下标是点，bfs 求最短路；数值也要去重，避免重复传送',
        complexity='时间 `O(n + U log log U)`，空间 `O(n + U)`',
        problem=['从下标 0 出发走到 `n-1`，每步可走相邻格子',
                 '若 `nums[i]` 是质数 `p`，可传送到所有满足 `nums[j] % p == 0` 的下标 `j`',
                 '本视频：`nums = [2,3,4,7,9]` → `2`'],
        quote='再具体实现时，不需要真的建立有向边，而是可以使用哈希表记录每种数值对应的所有下标。在bfs的过程中，如果碰到了质数p，那么就可以从p开始，以p为步长循环',
        quote_src='—— yiduobo 题解原文',
        idea=['`index_list[v]` 记录值为 `v` 的所有下标，不真的建边',
              '碰到质数 `v`，枚举 `v, 2v, 3v…` 这些数值，把对应下标全部入队',
              '数值也加 `vis_num` 去重：一个数值的下标只会被展开一次'],
        summary=['时间：筛质数 `O(U log log U)`，bfs 里每个数值只展开一次',
                 '易错点：传送时 `x` 要从 `v` 开始（包含 `v` 自己的其他下标）',
                 '易错点：除下标去重外，还要数值去重，否则重复枚举会超时',
                 '视频里为突出 bfs，把埃氏筛、建 `index_list` 的几行快进了，代码是完整执行的',
                 '对比灵神：灵神预处理质因子表、按质数分组；yiduobo 用质数的倍数反查数值'],
    ),
)
