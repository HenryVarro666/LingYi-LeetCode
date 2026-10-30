CONFIG = dict(
    num=3550, title='数位和等于下标的最小下标', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='取模除十求数位和 · 只枚举前 28 个',
    tags=[],
    code='''
class Solution:
    def smallestIndex(self, nums: List[int]) -> int:
        for i, x in enumerate(nums[:28]):
            s = 0
            while x > 0:
                s += x % 10
                x //= 10
            if s == i:
                return i
        return -1
''',
    call='Solution().smallestIndex([9,23,12,5,4])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前下标 i）', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"`x = {S['x']}`，已累加数位和 `s = {S['s']}`，目标 `i = {S['i']}`" if 'x' in S and 's' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), 'x', ('s', 's', 'yellow')],
    captions={
        'enumerate': lambda S, B, r: f'枚举下标 `i = {S.i}`，当前数 `nums[{S.i}]` = `{S.x}`',
        's = 0': '数位和从 `0` 开始累加',
        'while x > 0': lambda S, B, r: (f'`x = {S.x} > 0`：还有数位没取完，继续' if S.x > 0 else '`x = 0`：所有数位都取完了，退出循环'),
        's += x % 10': '`x % 10 = {B.x % 10}` 是最低位，加进数位和：`s = {s}`',
        'x //= 10': '`x //= 10`：去掉最低位，`x` 变成 {x}',
        'if s == i': lambda S, B, r: (f'数位和 `{S.s}` ==等于== 下标 `{S.i}`，找到了，且是最小的下标' if S.s == S.i else f'数位和 `{S.s}` ≠ 下标 `{S.i}`，看下一个'),
        'return i': '从小到大枚举，第一个满足的就是最小下标：返回 `{i}`',
    },
    cards=dict(
        one_liner='不转字符串，反复取最低位、去掉最低位',
        complexity='时间 `O(min(n,k) log U)`，空间 `O(1)`',
        problem=['找最小的下标 `i`，使 `nums[i]` 的数位和等于 `i`，没有就返回 `-1`',
                 '示例：`[1,10,11]` → `1`，因为 `1+0 = 1`',
                 '本视频：`[9,23,12,5,4]` → `4`'],
        quote='我们可以不用转成字符串处理，而是不断取最低位（模 10），去掉最低位（除以 10），直到数字为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x % 10` 取个位，`x //= 10` 去掉个位，循环到 `x = 0`',
              '数位和最大是 `999` 的 `27`，所以下标超过 27 不可能满足',
              '只枚举 `nums[:28]`，一旦命中就是最小下标'],
        summary=['时间 `O(min(n,k) log U)`，`k = 28`，空间 `O(1)`',
                 '优化前的写法：`sum(map(int, str(x)))` 用字符串，或不限制枚举范围',
                 '易错点：先判 `s == i` 再返回，不要在循环里提前返回',
                 '`nums[i] = 0` 时数位和为 0，下标 0 就满足'],
    ),
)
