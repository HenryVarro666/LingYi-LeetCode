def _cap_front(S, B, ret):
    q, p, s, g, i = S.q, S.p, S.s, S.g, S.i
    if p + 1 < len(q):
        a = s[q[p + 1]] + g[q[p + 1]]
        if a <= s[i]:
            return f'`q[p+1]` = {q[p + 1]}：`s+g` = `{a}` ≤ `s[{i}]` = {s[i]} → 后面的更靠后也能转移，==q[p] 被淘汰==，`p` 后移'
        return f'`q[p+1]` = {q[p + 1]}：`s+g` = `{a}` > `s[{i}]` = {s[i]} → 接不上，==q[p] = {q[p]} 就是最靠后的可用 j=='
    return f'`p` 已是队列最后一个，`q[p]` = {q[p]} 就是转移来源'


def _cap_tail(S, B, ret):
    q, p, s, g, i = S.q, S.p, S.s, S.g, S.i
    if len(q) <= p:
        return '队列只剩已淘汰的部分，不再弹出'
    a, b = s[q[-1]] + g[q[-1]], s[i] + g[i]
    if a >= b:
        return f'队尾 `{q[-1]}`：`s+g` = `{a}` ≥ 新的 `{b}` → 又靠前又不小，==以后都不会从它转移==，弹出'
    return f'队尾 `{q[-1]}`：`{a}` < `{b}` → 保留，停止弹出'


def _fml(S):
    i = S.get('i')
    if i is None or S.get('_line', 0) < 14:
        return '`f[i]`：前 i 个数的最长长度；`g[i]`：最后一项的最小值；转移条件 `s[i] ≥ s[j] + g[j]`'
    q, p = S['q'], S['p']
    if p >= len(q):
        return ''
    j = q[p]
    return f'取 `j = {j}`：`s[{i}] − s[{j}] = {S["s"][i] - S["s"][j]}` 作最后一项 → `f[{i}] = f[{j}] + 1`'


CONFIG = dict(
    num=2945, title='找到最大非递减数组的长度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f/g 双数组 + 单调队列', tags=['动态规划', '单调队列优化 DP', '难度分 2943'],
    code='''
class Solution(object):
    def findMaximumLength(self, nums):

        s = [0]
        for v in nums:
            s.append(s[-1] + v)
        
        f = [0]
        g = [0]

        q = [0]
        p = 0

        for i in range(1, len(nums) + 1):
            while p + 1 < len(q) and s[q[p + 1]] + g[q[p + 1]] <= s[i]:
                p += 1
            
            f.append(f[q[p]] + 1)
            g.append(s[i] - s[q[p]])

            while len(q) > p and s[q[-1]] + g[q[-1]] >= s[i] + g[i]:
                q.pop()
            
            q.append(i)
        
        return f[-1]
''',
    call='Solution().findMaximumLength([4, 3, 2, 6])',
    expect=3,
    skip=['s.append(s[-1] + v)', 'for v in nums'],
    views=[
        dict(type='text', fn=_fml, size=24, h=50),
        dict(type='array', var='nums', label='nums', h=120, cell=90,
             color=lambda S, k, v: 'blue' if S.get('i') is not None and k == S['i'] - 1 else None),
        dict(type='array', var='s', label='s 前缀和', h=130, cell=90, pointers={'i': 'blue'}),
        dict(type='array', var='f', label='f', h=130, cell=90, pointers={'i': 'blue'}),
        dict(type='array', var='g', label='g', h=130, cell=90, pointers={'i': 'blue'}),
        dict(type='queue', var='q', h=130, fmt=lambda j: f'{j}'),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p', 'green'), ('q[p]', 'q[p]', 'green')],
    captions={
        's = [0]': '`s` 前缀和，`s[i]` = 前 i 个数之和；先放 0',
        'g = [0]': '`g[i]`：`f[i]` 对应数组里==最后一项的最小值==',
        'q = [0]': '`q` 单调队列放候选的 `j`，`p` 指向队首（用指针代替真正弹出）',
        'while p + 1 < len(q)': _cap_front,
        'p += 1': '`p` → {p}',
        'f.append(f[q[p]] + 1)': '接在 `j = {q[p]}` 后面：`f[{i}] = f[{q[p]}] + 1` = =={f[i]}==',
        'g.append(s[i]': '最后一项 = `s[{i}] − s[{q[p]}]` = =={g[i]}==',
        'while len(q) > p': _cap_tail,
        'q.pop()': '队尾弹出 → `q = {q}`',
        'q.append(i)': '`{i}` 入队 → `q = {q}`',
        'return f[-1]': '前 `{len(nums)}` 个数最多 `{ret}` 项',
    },
    cards=dict(
        one_liner='f 不会减小，g 越小越好：永远选最靠后的可转移位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次可把一个子数组替换为它的和，求能得到的最长非递减数组长度',
                 '示例：`[5,2,2]` → `1`；`[1,2,3,4]` → `4`',
                 '本视频：`[4,3,2,6]` → `3`（`[3,2]` 合并成 5）'],
        quote='遇到逆序时，逆序的数既可以向前合并，也可以向后合并，没有一种方案可以保证当前选择的合并方向是最优的。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心行不通，用 `f[i]`（长度）和 `g[i]`（最后一项）做 DP',
              '条件 `s[i] − s[j] ≥ g[j]` 移项成 `s[i] ≥ s[j] + g[j]`',
              '队首不是因为越界被弹，而是因为后面有更优的 j'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`f` 非降，`j` 越靠前 `f[j]` 越小、`g[i]` 越大，所以取最靠后的 `j`',
                 '作者用指针 `p` 代替队首出队，队尾仍然 `pop`',
                 '原文为 Python 2 风格，本题无需修改即可在 Python 3 运行'],
    ),
)
