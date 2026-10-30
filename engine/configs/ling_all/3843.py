CONFIG = dict(
    num=3843, title='频率唯一的第一个元素', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 次数的次数',
    tags=[],
    code='''
class Solution:
    def firstUniqueFreq(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        cc = Counter(cnt.values())

        for x in nums:
            if cc[cnt[x]] == 1:
                return x
        return -1
''',
    call='Solution().firstUniqueFreq([20,20,10,30,30,30,40,40])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums（从左到右找第一个）', pointers={'x': 'blue'}, cell=90, h=200),
        dict(type='map', var='cnt', label='cnt（数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=210, font=30),
        dict(type='map', var='cc', label='cc（出现次数 → 有几个数是这个次数）', fmt=lambda k, v: f'次数 {k}: {v} 个数', h=210, font=30),
    ],
    watch=['x', ('cnt[x]', "cnt[x] if 'x' in S else ''", 'cyan'), ('cc[cnt[x]]', "cc[cnt[x]] if 'x' in S else ''", 'orange')],
    captions={
        'cnt = Counter': '先数每个数出现几次：`cnt = {dict(cnt)}`',
        'cc = Counter': '再数「出现次数」的出现次数：`cc = {dict(cc)}`',
        'for x in nums': '从左到右看 `x = {x}`',
        'if cc[cnt[x]] == 1': '`x = {x}` 出现 `{cnt[x]}` 次，而恰好出现 `{cnt[x]}` 次的数有 `{cc[cnt[x]]}` 个 → ' + '{"==频率唯一=="if cc[cnt[x]] == 1 else "不唯一，看下一个"}',
        'return x': '第一个频率唯一的数是 ==`{ret}`==',
        'return -1': '没有任何数的频率唯一 → `-1`',
    },
    cards=dict(
        one_liner='用第二个哈希表数「次数的次数」，等于 1 就是唯一',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['返回 `nums` 中从左到右第一个「出现频率与众不同」的元素',
                 '即没有其他数和它出现次数相同；不存在返回 `-1`',
                 '示例：`[20,20,10,30,30,30]` → `20`；`[10,10,20,20]` → `-1`'],
        quote='用哈希表统计 nums 每个数的出现次数，然后再用一个哈希表（或者数组）统计出现次数的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cnt[x]` 是 x 的出现次数，`cc[c]` 是「出现 c 次的数有几个」',
              '`cc[cnt[x]] == 1` 说明没有别的数和 x 次数相同',
              '最后按 nums 的顺序扫，遇到的第一个满足条件的就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`cc` 统计的是「次数」的个数，不是数的个数',
                 '必须按 `nums` 原顺序找第一个，不能遍历哈希表',
                 '原文说 `cc` 也可以用数组，次数不超过 n'],
    ),
)
