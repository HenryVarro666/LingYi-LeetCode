CONFIG = dict(
    num=2535, title='数组元素和与数字和的绝对差', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='元素和减数位和，一次遍历', tags=[],
    code='''
class Solution:
    def differenceOfSum(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            ans += x  # 累加元素和
            while x:
                ans -= x % 10  # 减去数位和
                x //= 10
        return ans
''',
    call='Solution().differenceOfSum([1, 15, 6, 3])',
    expect=9,
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=230,
),
        dict(type='text', h=130, size=32, fn=lambda S: (f"正在拆的数 `x = {S['x']}`" if 'x' in S else '')),
        dict(type='text', h=130, size=32, fn=lambda S: (f"目前 `ans`（元素和 − 已减的数位和） = =={S['ans']}==" if 'ans' in S else '')),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 一边加元素和、一边减数位和，最后就是差',
        'for x in nums': lambda S, B, r: (f'取下一个元素 `x = {S.x}`' if S.x else '`nums` 里的元素都处理完了'),
        'ans += x': '先加上元素本身：`ans` = {B.ans} + {x} = =={ans}==',
        'while x': lambda S, B, r: (f'`x = {S.x}` 还有数位，继续拆' if S.x else '`x = 0`：这个数的数位拆完了'),
        'ans -= x % 10': '减去个位 `{x % 10}`：`ans` = {B.ans} − {x % 10} = =={ans}==',
        'x //= 10': '去掉个位：`x` → {x}',
        'return ans': '元素和永远 ≥ 数位和，所以直接返回 `ans = {ans}`，不用取绝对值',
    },
    cards=dict(
        one_liner='元素永远不小于它的数位和，差一定非负，免去绝对值',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['元素和 = 所有元素相加；数字和 = 所有元素的每个数位相加',
                 '返回两者的绝对差',
                 '示例：`[1,15,6,3]` → 元素和 25，数字和 16，答案 `9`'],
        quote='由于元素值一定不小于其数位和，所以答案就是元素和减去数位和，无需取绝对值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`ans += x`：累加元素和',
              '`ans -= x % 10`：每取一个数位就减掉，同一个循环里搞定',
              '全程只用一个变量 `ans`'],
        summary=['时间 `O(n log U)`，`U = max(nums)`，空间 `O(1)`',
                 '`for x in nums` 里改 `x` 不影响 `nums` 本身',
                 '先把 `x` 加进 `ans`，再拆 `x`，顺序不能反',
                 '数位和 ≤ 元素值，所以不必套 `abs`'],
    ),
)
