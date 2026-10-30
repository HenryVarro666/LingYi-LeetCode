CONFIG = dict(
    num=3712, title='出现次数能被 K 整除的元素总和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表 freq 两趟遍历',
    tags=[],
    code='''
class Solution(object):
    def sumDivisibleByK(self, nums, k):
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        res = 0
        for v in freq:
            if freq[v] % k == 0:
                res += v * freq[v]
        
        return res
''',
    call='Solution().sumDivisibleByK([4,4,4,1,2,3], 3)',
    expect=12,
    views=[
        dict(type='array', var='nums', label='nums', cell=80, h=170,
             pointers={}, color=lambda S, i, v: 'blue' if S.get('v') == v and 'res' not in S else None),
        dict(type='map', var='freq', label='freq（元素 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=190, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"`freq[{S['v']}] = {S['freq'][S['v']]}`，`{S['freq'][S['v']]} % {S['k']} = {S['freq'][S['v']] % S['k']}`" if 'res' in S and 'v' in S and S['v'] in S['freq'] else '')),
    ],
    watch=['k', 'v', ('res', 'res', 'green')],
    captions={
        'freq = {}': '`freq` 记录每种元素出现的次数',
        'for v in nums': '第一趟：取出 `v = {v}`',
        'freq[v] = freq.get': '`freq[{v}]` 加一 → {freq[v]}',
        'res = 0': '第二趟之前，`res` 清零',
        'for v in freq': '第二趟遍历 `freq`：元素 `v = {v}`',
        'if freq[v] % k': '`{freq[v]} % {k} = {freq[v] % k}` → ' + '{"次数是 k 的倍数" if freq[v] % k == 0 else "不是倍数，跳过"}',
        'res += v * freq[v]': '把 `v * freq[v] = {v} × {freq[v]}` 累加 → `res` = =={res}==',
        'return res': '没有满足条件的元素时 `res` 仍为 0；这里返回 `{res}`',
    },
    cards=dict(
        one_liner='两趟遍历：先用 freq 数次数，再把次数合格的 v*freq[v] 累加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `nums` 与整数 `k`',
                 '求所有出现次数能被 `k` 整除的元素之和（重复出现的都要算）',
                 '本视频：`[4,4,4,1,2,3]`，`k=3` → `12`'],
        quote='一趟遍历，使用哈希表freq记录每种元素出现的次数，然后再对freq进行一趟遍历，对于其中的元素v，若v出现次数freq[v]为k的倍数，那么就将v * freq[v]累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟用 `freq.get(v, 0) + 1` 计数',
              '第二趟遍历 `freq` 的键，检查 `freq[v] % k == 0`',
              '合格就累加 `v * freq[v]`，一个都没有则答案保持 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '累加的是 `v * freq[v]`，不是 `v`',
                 '没有合格元素时返回初值 0',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改'],
    ),
)
