def _loop(S):
    return 'p' in S and 'query' in S


def _qcol(S, i, v):
    if not _loop(S):
        return None
    qi = S['queries_with_index']
    cur = [S['query'], S['index']]
    k = qi.index(cur) if cur in qi else -1
    if i == k:
        return 'yellow'
    if i < k:
        return 'green'
    return None


def _top(S):
    if _loop(S):
        p, s, q = S['p'], S['s'], S['query']
        if S['_line'] == 15:
            return f"`query = {q}`：选入 `nums[{p}] = {S['nums'][p]}`，和变成 `{s}`"
        if p < S['n'] and s + S['nums'][p] <= q:
            return f"`query = {q}`：已选 `{p}` 个，和 `{s}`；下一个 `{S['nums'][p]}` 还放得下"
        return f"`query = {q}`：已选 `{p}` 个，和 `{s}`" + (f"；再加 `{S['nums'][p]}` 就超了" if p < S['n'] else '；全部选完')
    return '小的数优先选；query 越大，选的数==只增不减== → 两边都排序，一趟扫完'


def _while(S, B, ret):
    p, s, q, n = S.p, S.s, S.query, S.n
    if p < n and s + S.nums[p] <= q:
        return f'`{s} + nums[{p}] = {s + S.nums[p]} ≤ {q}`：放得下 → 选它'
    if p == n:
        return f'`p = {n}`：nums 已经全选了'
    return f'`{s} + {S.nums[p]} = {s + S.nums[p]} > {q}`：放不下，停 → 更大的数更放不下'


CONFIG = dict(
    num=2389, title='和有限的最长子序列', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='排序 + 离线询问 + 双指针',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def answerQueries(self, nums, queries):

        nums.sort()
        queries_with_index = [[query, index] for index, query in enumerate(queries)]
        queries_with_index.sort(key = lambda d:d[0])

        n = len(nums)
        m = len(queries_with_index)
        res = [0] * m
        p = 0
        s = 0
        for query, index in queries_with_index:
            while p < n and s + nums[p] <= query:
                s += nums[p]
                p += 1
            res[index] = p

        return res
''',
    call='Solution().answerQueries([4,5,2,1,6], [3,10,21,1])',
    expect=[2, 3, 5, 1],
    skip=['m = len', 'res = [0]', 'p = 0'],
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='array', var='nums', label='nums 排序后（绿 = 已选进子序列）', cell=96,
             color=lambda S, i, v: 'green' if 'p' in S and (i < S['p'] or i == S['p'] and S['_line'] == 15) else None,
             pointers={'p': 'blue'}, h=230),
        dict(type='array', var=lambda S: [q for q, _ in S['queries_with_index']] if 'queries_with_index' in S else None,
             label='按大小排序的 query（黄 = 当前，绿 = 已回答）', color=_qcol, cell=96, h=170),
        dict(type='array', var='res', label='res（按原下标写回）', cell=96,
             color=lambda S, i, v: 'yellow' if _loop(S) and S['_line'] == 17 and i == S['index'] else None, h=170),
    ],
    watch=[('query', 'query', 'yellow'), ('index', 'index', 'purple'), ('p', 'p', 'blue'), ('s', 's', 'green')],
    captions={
        'nums.sort()': '`nums` 从小到大：`{nums}`，==优先选小的数==',
        'queries_with_index = [': '给每个 query 记下原下标：`{queries_with_index}`',
        'queries_with_index.sort': '按 query 从小到大排序：`{queries_with_index}`',
        'n = len': '`n = {n}`，`m = {len(queries)}`',
        's = 0': '`res` 全 0；`p = 0` 是已选个数，`s = 0` 是已选数字之和',
        'for query, index in': lambda S, B, r: ('所有 query 处理完毕' if 'index' in B and B.index == S.index
                                                else f'处理 `query = {S.query}`（原下标 `{S.index}`）：==接着上一个 query 的结果==继续选'),
        'while p < n': _while,
        's += nums[p]': '`s` → {s}',
        'p += 1': '`p` → {p}',
        'res[index] = p': '`res[{index}] = {p}`：和 `≤ {query}` 时最多选 =={p}== 个',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='把 query 从小到大处理，已选的数只增不减，一个指针一趟扫完',
        complexity='时间 `O(n log n + m log m)`，空间 `O(m)`',
        problem=['对每个 `queries[i]`，求 nums 中元素和 `≤ queries[i]` 的==子序列的最大长度==',
                 '示例：`nums = [4,5,2,1], queries = [3,10,21]` → `[2,3,4]`',
                 '本视频：`[4,5,2,1,6], [3,10,21,1]` → `[2,3,5,1]`'],
        quote='对于较大的query而言，其对应的子序列必然是在较小的query对应的子序列基础上==再添加一些没使用过的较小的数==。',
        quote_src='—— yiduobo 题解原文',
        idea=['为了子序列尽量长，应该优先选较小的数 → nums 排序',
              'query 也排序（记住原下标），大 query 的选择包含小 query 的选择',
              '指针 `p` 和累加和 `s` 不回退，一趟遍历回答所有 query'],
        summary=['时间 `O(n log n + m log m)`：两次排序；双指针本身 `O(n + m)`',
                 '排序前要带上==原下标==，答案按 `res[index]` 写回',
                 '`while` 条件是 `s + nums[p] <= query`，等于也能选',
                 '对比灵神：灵神不排序 queries，而是对前缀和做 `bisect_right` 二分'],
    ),
)
