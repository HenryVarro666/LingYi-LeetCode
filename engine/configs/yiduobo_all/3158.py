CONFIG = dict(
    num=3158, title='求出出现两次数字的 XOR 值', difficulty='Easy', category='位运算',
    author='yiduobo', technique='哈希表计数 · 次数为 2 才异或',
    code='''
class Solution(object):
    def duplicateNumbersXOR(self, nums):

        freq = Counter(nums)
        res = 0
        for v, f in freq.items():
            if f == 2:
                res ^= v
        
        return res
''',
    call='Solution().duplicateNumbersXOR([3, 1, 2, 3, 5, 1])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', cell=96, h=170,
             color=lambda S, i, v: 'yellow' if 'v' in S and v == S['v'] else None),
        dict(type='map', var='freq', label='freq（数字 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', h=80, size=30, fn=lambda S: f"异或累计 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=[('v', 'v', 'yellow'), ('f', 'f', 'pink'), ('res', 'res', 'green')],
    captions={
        'freq = Counter': '先用哈希表统计每个数出现的次数：`freq = {dict(freq)}`',
        'res = 0': '`res` 累计异或值，从 0 开始（0 异或任何数都不变）',
        'for v, f in freq.items()': lambda S, B, ret: ('哈希表遍历完了，循环结束' if B.get('v') == S.v else f'遍历哈希表：数字 `{S.v}` 出现了 `{S.f}` 次'),
        'if f == 2': lambda S, B, ret: (f'`f = 2`：`{S.v}` 出现了两次，需要异或' if S.f == 2 else f'`f = {S.f}`：`{S.v}` 只出现一次，跳过'),
        'res ^= v': '`res = {B.res} ^ {v} = {res}`',
        'return res': '哈希表遍历完，答案 ==`{res}`==',
    },
    cards=dict(
        one_liner='先数一遍次数，再把次数为 2 的数全部异或起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 中每个数要么出现一次要么出现两次',
                 '求出现两次的数的异或值，没有则为 `0`',
                 '示例：`[1,2,2,1]` → `3`；本视频 `[3,1,2,3,5,1]` → `2`'],
        quote='使用哈希表统计每种数字出现的次数，接下来遍历哈希表中的元素，若当前元素出现了两次，就将其异或到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`Counter(nums)` 一步得到每个数的出现次数',
              '遍历哈希表的键值对 `(v, f)`，只有 `f == 2` 才让 `v` 参与异或',
              '`res` 从 0 开始，没有重复数时直接返回 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：遍历的是 `freq`（每个数字一次），不是 `nums`，否则会把重复数异或两次抵消成 0',
                 '对比灵神：灵神一趟遍历用位集合省掉哈希表，空间 `O(1)`',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
