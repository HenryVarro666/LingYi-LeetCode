def _txt(S):
    if 'ans' not in S or 'i' not in S:
        return ''
    i, x = S['i'], S['x']
    return f"`i = {i}` 是{'奇' if i % 2 else '偶'}数下标 → {'减去' if i % 2 else '加上'} `{x}`，当前和 `{S['ans']}`"


CONFIG = dict(
    num=3701, title='计算交替和', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='奇数下标取反再累加', tags=[],
    code='''
class Solution:
    def alternatingSum(self, nums: List[int]) -> int:
        ans = 0
        for i, x in enumerate(nums):
            ans += -x if i % 2 else x
        return ans
''',
    call='Solution().alternatingSum([1,3,5,7,2,4])',
    expect=-6,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 加，粉 = 减）', pointers={'i': 'blue'}, cell=100, h=220,
             color=lambda S, i, v: 'pink' if i % 2 else 'green'),
        dict(type='text', h=80, size=30, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans = 0`：累加所有（取反后的）元素',
        'for i, x': '取下标 `i = {i}`，元素 `x = {x}`',
        'ans += ': '`i % 2 = {i % 2}`：{"奇数下标，取反" if i % 2 else "偶数下标，保持"}，`ans = {B.ans} {"-" if i % 2 else "+"} {x}` = =={ans}==',
        'return': '累加完毕，交替和为 `{ret}`',
    },
    cards=dict(
        one_liner='奇数下标的元素取反，然后全部加起来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['交替和：`nums[0] - nums[1] + nums[2] - nums[3] ...`',
                 '偶数下标加，奇数下标减',
                 '示例：`[1,3,5,7]` → `-4`；本视频：`[1,3,5,7,2,4]` → `-6`'],
        quote='遍历 nums，如果 i 是奇数，则把 nums[i] 取反。累加元素和，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i % 2` 为 1 就是奇数下标，取 `-x`，否则取 `x`',
              '一遍遍历累加即可，不需要额外数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '视频演示题解里的普通写法；另有一行写法 `sum(nums[::2]) - sum(nums[1::2])`，切片会多开两个数组',
                 '易错：下标从 0 开始，第 0 个元素是「加」'],
    ),
)
