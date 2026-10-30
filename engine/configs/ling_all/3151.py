CONFIG = dict(
    num=3151, title='特殊数组 I', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='相邻元素奇偶性比较',
    code='''
class Solution:
    def isArraySpecial(self, nums: List[int]) -> bool:
        return all(x % 2 != y % 2 for x, y in pairwise(nums))
''',
    call='Solution().isArraySpecial([2, 1, 4, 6, 5])',
    expect=False,
    views=[
        dict(type='array', var='nums', label='nums（奇偶相同的相邻对 = 不合格）', cell=100, h=200,
             color=lambda S, i, v: 'orange' if v % 2 == 0 else 'blue'),
        dict(type='text', h=90, size=30, fn=lambda S: '蓝 = 奇数，橙 = 偶数；相邻两格必须一蓝一橙'),
    ],
    watch=[('x', 'x'), ('y', 'y')],
    captions={
        'return all': lambda S, B, ret: ('逐对检查 `(x, y)`：`(2,1)` `(1,4)` 都是一奇一偶；到 `(4,6)` 两个都是偶数，`x % 2 == y % 2` ==不满足条件==，`all` 立刻得到 `False`，后面的 `(6,5)` 不用看了'
                                         if ret is False else f'每一对奇偶都不同 → `{ret}`'),
    },
    cards=dict(
        one_liner='只看相邻两个数：奇偶相同就不特殊',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['相邻元素奇偶性都不同的数组叫特殊数组',
                 '判断 `nums` 是不是特殊数组',
                 '示例：`[4,3,1,6]` → `false`，`[2,1,4]` → `true`'],
        quote='遍历数组，如果存在一对相邻元素，它们的奇偶性相同，那么不满足题目要求，返回 false。如果不存在这样的一对元素，返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pairwise(nums)` 依次给出相邻两数 `(x, y)`',
              '`x % 2 != y % 2` 表示这一对奇偶不同',
              '`all(...)`：每一对都满足才是 `True`，遇到第一对不满足就短路返回 `False`'],
        after=[dict(heading='本视频的数据：[2, 1, 4, 6, 5]',
                    lines=['`(2,1)` 偶奇，通过', '`(1,4)` 奇偶，通过', '`(4,6)` 偶偶，==不通过==，直接返回 `False`', '`all` 短路：不会再检查 `(6,5)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只有一个元素时没有相邻对，`all([])` 为 `True`',
                 '易错：比较的是奇偶性 `x % 2 != y % 2`，不是 `x != y`',
                 '`pairwise` 来自 itertools，Python 3.10+ 可用'],
    ),
)
