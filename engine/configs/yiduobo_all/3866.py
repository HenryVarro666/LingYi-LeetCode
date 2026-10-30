CONFIG = dict(
    num=3866, title='找到第一个唯一偶数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='手写哈希表计数 · 两趟遍历',
    code='''
class Solution(object):
    def firstUniqueEven(self, nums):
        
        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
        
        for v in nums:
            if v % 2 == 0 and cnt[v] == 1:
                return v
        return -1
''',
    call='Solution().firstUniqueEven([3,4,2,5,4,6])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=220, label='nums',
             color=lambda S, k, v: 'blue' if S.get('v') == v and 'cnt' in S and k == S['nums'].index(v) else None),
        dict(type='map', var='cnt', h=300, fmt=lambda k, v: f'{k} : {v}'),
    ],
    watch=[('v', 'v', 'blue')],
    captions={
        'cnt = {}': '用字典 `cnt` 记录每个数出现的次数',
        'cnt[v] = cnt.get': '`cnt[{v}] = {cnt[v]}`：{v} 目前出现 {cnt[v]} 次',
        'if v % 2 == 0': lambda S, B, r: (
            f'`{S.v}` 是奇数 → 不是偶数，跳过' if S.v % 2 else
            (f'`{S.v}` 是偶数，但 `cnt[{S.v}] = {S.cnt[S.v]}` 不是 1 → 跳过' if S.cnt[S.v] != 1
             else f'`{S.v}` 是偶数，且 `cnt[{S.v}] = 1` → ==成立==')),
        'return v': '`v = {v}` 就是第一个恰好出现一次的偶数',
        'return -1': '遍历完也没找到 → 返回 -1',
    },
    cards=dict(
        one_liner='两趟遍历：先统计次数，再找第一个次数为 1 的偶数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，返回恰好出现一次的第一个偶数',
                 '不存在返回 `-1`',
                 '本视频：`[3,4,2,5,4,6]` → `2`'],
        quote='一趟遍历，使用哈希表统计数组中每种元素出现的次数。然后再一趟遍历，对于当前元素v，若其为偶数，则通过哈希表检测其出现次数是否为恰好一次，若是，那么v就是要找的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：`cnt.get(v, 0) + 1` 累加次数，不用 `Counter`',
              '第二趟：对每个 `v` 先判偶数，再查哈希表看是否恰好一次',
              '遍历完没有返回，就是不存在'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '第二趟必须按 `nums` 的顺序走，才能得到“第一个”',
                 '原文为 Python 2 风格，无需改动即可在 Python 3 运行',
                 '对比灵神：灵神用 `Counter` 一行统计，yiduobo 手动 `get` 累加'],
    ),
)
