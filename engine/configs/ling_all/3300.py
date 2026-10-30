def _digits(S):
    if 'x' not in S:
        return ''
    return f"当前数：`{S['x']}`，已累加数位和 `s = {S['s']}`"


CONFIG = dict(
    num=3300, title='替换为数位和以后的最小元素', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举数位 · 求数位和取最小',
    tags=[],
    code='''
class Solution:
    def minElement(self, nums: List[int]) -> int:
        ans = inf
        for x in nums:
            s = 0
            while x:
                s += x % 10
                x //= 10
            ans = min(ans, s)
        return ans
''',
    call='Solution().minElement([999, 19, 199])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums', pointers={}, h=150),
        dict(type='text', h=90, size=32, fn=_digits),
    ],
    watch=['x', ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '`ans` 记录最小数位和，先设为无穷大，任何数位和都会比它小',
        'for x in nums': lambda S, B, r: (f'枚举 `nums` 中的下一个数 `x = {S.x}`' if S.x else '`nums` 已经枚举完，退出循环'),
        's = 0': '为 `x` 重新开始累加数位和：`s = 0`',
        'while x': lambda S, B, r: ('`x = %d` 还不是 0，还有数位没取' % S['x'] if S['x'] else '`x` 变成 0：所有数位都取完了'),
        's += x % 10': '`x % 10` 取出最低位 ==`{x % 10}`==，加到 `s` → {s}',
        'x //= 10': '`x //= 10` 去掉最低位，`x` → {x}',
        'ans = min': '数位和 `s = {s}`，`ans = min({B.ans}, {s})` = =={ans}==',
        'return ans': '所有数都处理完，最小数位和是 `{ans}`',
    },
    cards=dict(
        one_liner='不断 %10 取末位、//10 去末位，求每个数的数位和',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['把每个数替换成它的各位数字之和，返回替换后的最小值',
                 '示例：`[999,19,199]` → 替换为 `[27,10,19]` → `10`',
                 '`1 <= nums[i] <= 10^4`'],
        quote='不断地把 x 除以 10（下取整）直到 0，例如 123→12→1→0。在这个过程中的 x mod 10，即为每个数位（从低到高）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x % 10` 是最低位，`x //= 10` 把最低位丢掉',
              '循环到 `x == 0` 结束，累加的 `s` 就是数位和',
              '边算边更新最小值，不需要真的改写数组'],
        summary=['时间 `O(n log U)`，`U` 是最大值，每个数有 `log U` 个数位',
                 '空间 `O(1)`：不修改 `nums`，只用几个变量',
                 '易错点：`ans` 初值要足够大（`inf`）；`s` 每个数都要清零',
                 '同类题：数位和、各位相乘等"取末位 + 去末位"模板'],
    ),
)
