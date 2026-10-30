CONFIG = dict(
    num=2169, title='得到 0 的操作数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='辗转相除累加商',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution:
    def countOperations(self, x: int, y: int) -> int:
        ans = 0
        while y > 0:
            ans += x // y  # x 变成 x%y
            x, y = y, x % y
        return ans
''',
    call='Solution().countOperations(10, 4)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"`x = {S['x']}`，`y = {S['y']}`，累计操作数 `ans = {S['ans']}`" if 'ans' in S else ''), size=36),
        dict(type='text', fn=lambda S: (f"`x` 不断减 `y`，减到小于 `y`：一共减 `{S['x']} // {S['y']}` = =={S['x']//S['y']}== 次" if 'y' in S and S['y'] > 0 and S.get('_line') == 6 else ''), size=30),
    ],
    watch=[('x', 'x', 'orange'), ('y', 'y', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计操作数',
        'while y > 0': lambda S, B, r: (f'`y = {S.y}` > 0：还没减到 0，继续' if S.y > 0 else '`y = 0`：有一个数变成 0，结束'),
        'ans += x // y': '`x` 不断减 `y` 直到小于 `y`，要减 `{x} // {y}` = =={x//y}== 次 → `ans = {ans}`',
        'x, y = y, x % y': '`x` 减完剩 `x % y`；==交换==后就不用再写 `x < y` 的分支：`x = {x}`，`y = {y}`',
        'return ans': '总操作数 `{ans}`',
    },
    cards=dict(
        one_liner='连续减法就是除法：每轮累加商，余数继续',
        complexity='时间 `O(log max(x,y))`，空间 `O(1)`',
        problem=['每步用大的减小的，直到其中一个为 0，求操作数',
                 '示例：`num1 = 2, num2 = 3` → `3`',
                 '本视频：`(10, 4)` → 10-4, 6-4, 4-2, 2-2 共 `4` 步'],
        quote='如果 x ≥ y，那么 x 要不断减去 y，直到小于 y。这和商的定义是一样的，所以把 x 减少到小于 y 的操作数为 ⌊x/y⌋。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x ≥ y` 时要连减 `x // y` 次，`x` 变成 `x % y`',
              '交换 `x`、`y`，就不用单独处理 `x < y`',
              '循环到 `y = 0`，把每轮的商加起来'],
        summary=['时间 `O(log max(x,y))`，最坏是斐波那契相邻两项',
                 '本质是辗转相除法，只是把每步的商累加',
                 '`x // y` 要在 `x, y = y, x % y` 之前算',
                 '有一个数为 0 时，`while y > 0` 不进循环，返回 0'],
    ),
)
