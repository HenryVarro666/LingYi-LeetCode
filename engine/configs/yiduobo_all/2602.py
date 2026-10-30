def _col(S, i, v):
    if 'p' in S and 'k' in S:
        return 'blue' if i < S['p'] else 'green'
    return None


def _txt(S):
    if 'k' not in S or 'p' not in S or 'prefix' not in S:
        return '把询问也排好序：`k` 越来越大，已加入前缀的小数只增不减'
    k, p, pre, s, n = S['k'], S['p'], S['prefix'], S['s'], len(S['nums'])
    return (f'`k={k}`：{p} 个数 < k，和 `{pre}`；涨 `{k}×{p} − {pre}` = =={k * p - pre}==，'
            f'降 `({s} − {pre}) − {n - p}×{k}` = =={(s - pre) - (n - p) * k}==')


CONFIG = dict(
    num=2602, title='使数组元素全部相等的最少操作次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序询问 + 双指针前缀和',
    tags=['前缀和', '难度分 1903'],
    code='''
class Solution(object):
    def minOperations(self, nums, queries):

        nums.sort()
        res = [0] * len(queries)
        p = 0
        s = sum(nums)
        prefix = 0
        for index, k in sorted(enumerate(queries), key=lambda d:d[1]):
            while p < len(nums) and nums[p] < k:
                prefix += nums[p]
                p += 1
            
            res[index] = k * p - prefix + s - prefix - (len(nums) - p) * k
        
        return res
''',
    call='Solution().minOperations([3,1,6,8], [5,1])',
    expect=[10, 14],
    views=[
        dict(type='array', var='nums', label='nums（排序后；蓝 = 已计入前缀，绿 = 还没轮到）', h=170,
             color=lambda S, i, v: _col(S, i, v), pointers={'p': 'pink'}),
        dict(type='array', var='queries', label='queries（按值从小到大处理）', h=130,
             color=lambda S, i, v: 'yellow' if S.get('index') == i and 'k' in S else None),
        dict(type='array', var='res', label='res（按原下标存放）', h=130,
             color=lambda S, i, v: 'yellow' if S.get('index') == i and 'k' in S and S.get('_line', 0) >= 14 else None),
        dict(type='text', fn=_txt, h=60),
    ],
    watch=['index', 'k', ('p', 'p', 'pink'), ('prefix', 'prefix', 'cyan'), ('s', 's', 'orange'), ('res', 'res', 'green')],
    captions={
        'nums.sort()': '先给数组排序：`nums = {nums}`，比 k 小的数就是一段前缀',
        's = sum(nums)': '`s` = 全部数之和 = {s}；`prefix` 记「比 k 小的数」之和，初始为 0',
        'for index, k in sorted': lambda S, B, r: ('询问都处理完了' if 'k' in B and B.k == S.k and B.p == S.p and S.res[S.index] != 0 and S.k == max(S.queries)
                                                  else f'按 k 从小到大处理：这是第 `{S.index}` 个询问，`k = {S.k}`'),
        'while p < len(nums) and nums[p] < k': lambda S, B, r: (
            f'`nums[{S.p}] = {S.nums[S.p]} < {S.k}`：它要涨到 k，计入前缀' if S.p < len(S.nums) and S.nums[S.p] < S.k
            else f'`p = {S.p}`：{"数组用完了" if S.p >= len(S.nums) else f"nums[{S.p}] = {S.nums[S.p]} ≥ {S.k}"}，前缀不再增加'),
        'prefix += nums[p]': '`prefix` += {nums[p]} → {prefix}',
        'p += 1': '`p` → {p}：前 `{p}` 个数都小于 k',
        'res[index] =': '涨：`{k}×{p} − {prefix}` = {k * p - prefix}；降：`({s} − {prefix}) − {len(nums) - p}×{k}` = {(s - prefix) - (len(nums) - p) * k} → `res[{index}]` = =={res[index]}==',
        'return res': '按原询问顺序的答案：`{res}`',
    },
    cards=dict(
        one_liner='把询问也排序，指针只往右走，前缀和随之累加',
        complexity='时间 `O(n log n + q log q)`，空间 `O(n)`',
        problem=['每次查询把 `nums` 全变成 `queries[i]`，每次操作 ±1，求最少次数',
                 '查询之间互不影响',
                 '示例：`[3,1,6,8]`，`queries=[1,5]` → `[14,10]`；视频里询问顺序换成 `[5,1]`'],
        quote='接下来对于每个q，都可以二分这个q在数组中的位置……也可以将询问数组同样从小到大进行排序，然后利用单调性一边遍历q一边计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['代价 = `q×cnt1 − s1 + s2 − q×cnt2`：小于 q 的涨、大的降',
              '`s1 + s2` 是数组总和，`cnt1 + cnt2` 是长度，只需求 `s1` 和 `cnt1`',
              '询问从小到大，小于 k 的数只增不减，用指针 `p` 代替二分'],
        summary=['时间 `O(n log n + q log q)`，空间 `O(n)`',
                 '`sorted(enumerate(queries), key=...)` 保留原下标，答案写回 `res[index]`',
                 '`nums[p] < k` 用严格小于：等于 k 的数不用动',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：灵神每次二分，yiduobo 排序询问后一次扫描'],
    ),
)
