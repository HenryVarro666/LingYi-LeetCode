CONFIG = dict(
    num=1133, title='最大唯一数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='计数数组 + 从大到小找',
    code='''
class Solution(object):
    def largestUniqueNumber(self, nums):

        cnt = [0] * 1001
        for num in nums:
            cnt[num] += 1
        
        for num in range(1000, -1, -1):
            if cnt[num] == 1:
                return num
        
        return -1
''',
    call='Solution().largestUniqueNumber([993,997,999,997,999,990,8])',
    expect=993,
    setup='',
    views=[
        dict(type='array', var='nums', h=170, label='nums', color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None),
        dict(type='map', var=lambda S: {k: c for k, c in enumerate(S['cnt']) if c} if 'cnt' in S else {}, h=260,
             fmt=lambda k, v: f'{k} 出现 {v} 次'),
    ],
    watch=['num'],
    captions={
        'cnt = [0]': '`cnt[x]` 统计数字 x 出现几次，值域 0~1000 开 1001 格',
        'cnt[num] += 1': '`cnt[{num}]` → {cnt[num]}',
        'for num in range': '从 1000 往下查：第一个只出现一次的就是最大的唯一数',
        'if cnt[num] == 1': lambda S, B, r: (f'`cnt[{S.num}] = {S.cnt[S.num]}` 恰好为 1 → 找到了' if S.cnt[S.num] == 1
                                              else f'`cnt[{S.num}] = {S.cnt[S.num]}`：{"没出现过" if S.cnt[S.num] == 0 else "出现多次，不是唯一数"}，继续往小找'),
        'return num': '最大的唯一数是 `{num}`',
        'return -1': '没有唯一数，返回 -1',
    },
    cards=dict(
        one_liner='计数后从大到小扫，第一个次数为 1 的数就是答案',
        complexity='时间 `O(n + 值域)`，空间 `O(值域)`',
        problem=['给一个整数数组 `nums`，返回只出现过一次的整数中最大的那个',
                 '不存在这样的整数则返回 `-1`',
                 '示例：`[5,7,3,9,4,9,8,3,1]` → `8`；本视频用大数 `[993,997,999,997,999,990,8]` → `993`'],
        quote='一趟遍历，使用哈希表统计每个数出现的次数，然后从大到小遍历这些数，找到第一个出现次数为1的数即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['值域只有 0~1000，用长度 1001 的数组代替哈希表',
              '从 1000 往下找，第一个 `cnt == 1` 的数必然最大'],
        summary=['时间 `O(n + 1001)`，空间 `O(1001)`',
                 '`range(1000, -1, -1)` 要包含 0',
                 '次数为 0 或大于 1 都要跳过',
                 '没有唯一数时返回 -1'],
    ),
)
