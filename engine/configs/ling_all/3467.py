CONFIG = dict(
    num=3467, title='将数组按照奇偶性转化', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='只数奇数个数', tags=['灵神题单'],
    code='''
class Solution:
    def transformArray(self, nums: List[int]) -> List[int]:
        cnt1 = sum(x % 2 for x in nums)
        cnt0 = len(nums) - cnt1
        return [0] * cnt0 + [1] * cnt1
''',
    call='Solution().transformArray([4,3,2,1,7,8,5,6,9])',
    expect=[0, 0, 0, 0, 1, 1, 1, 1, 1],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 偶数 → 0，粉 = 奇数 → 1）', h=200,
             color=lambda S, i, v: 'pink' if v % 2 else 'blue'),
        dict(type='array', var=lambda S: [x % 2 for x in S['nums']], label='替换成 0 / 1 之后', h=200,
             color=lambda S, i, v: 'pink' if v else 'blue'),
        dict(type='text', size=30, fn=lambda S: (f"答案 = `{S['cnt0']}` 个 0 + `{S['cnt1']}` 个 1" if 'cnt0' in S
                                                 else (f"奇数个数 `cnt1 = {S['cnt1']}`" if 'cnt1' in S else '先数一数有几个奇数'))),
    ],
    watch=[('cnt1', 'cnt1', 'pink'), ('cnt0', 'cnt0', 'blue')],
    captions={
        'cnt1 = sum': '`x % 2` 奇数得 1、偶数得 0，加起来就是奇数个数：`cnt1` = =={cnt1}==',
        'cnt0 = len': '偶数个数 = 总数 − 奇数个数：`cnt0 = {len(nums)} − {cnt1}` = =={cnt0}==',
        'return': '排序后一定是 `{cnt0}` 个 0 在前、`{cnt1}` 个 1 在后：`{ret}`',
    },
    cards=dict(
        after=[dict(heading='另一种写法', lines=['写法一：`Counter(x % 2 for x in nums)` 一次数出两种',
                                                 '`[0] * cnt[0] + [1] * cnt[1]` 直接拼出答案',
                                                 '本视频演示写法二：少一个计数器，==偶数 = n − 奇数==',
                                                 '两种写法都是 `O(n)` 时间、`O(1)` 额外空间'])],
        one_liner='替换后只有 0 和 1，排序就是先放 0 再放 1',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['偶数换成 `0`，奇数换成 `1`，再按非递减排序',
                 '返回处理后的数组',
                 '示例：`[4,3,2,1]` → `[0,0,1,1]`'],
        quote='统计 nums 中的偶数个数 cnt0 和奇数个数 cnt1，那么答案就是 cnt0 个 0，后跟 cnt1 个 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['值只有 0 和 1，排序后必然是 ==0 在左、1 在右==',
              '不用真的排序，数出个数直接拼接',
              '写法二更省：只数 `cnt1`，`cnt0 = n - cnt1`'],
        summary=['时间 `O(n)`，空间 `O(1)`，返回值不计入',
                 '`x % 2` 本身就是 0/1，求和即奇数个数',
                 '写法一用 `Counter(x % 2 for x in nums)` 同时统计两种，思路一样',
                 '易错：别把偶数个数和奇数个数拼反了'],
    ),
)
