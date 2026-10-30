def _digits(S):
    x = S.get('x', 0)
    return list(str(x)) if x > 0 else ['0']


def _col(S, i, v):
    if 'x' not in S or S['x'] <= 0:
        return None
    if i == len(str(S['x'])) - 1:
        return 'green' if int(v) == S['digit'] else 'pink'
    return None


def _text(S):
    if 'x' not in S:
        return '把每个数不断 `// 10`，每次看最后一位 `x % 10`'
    if S['x'] <= 0:
        return f"这个数的所有数位都看完了，当前累计 `ans = {S['ans']}`"
    return f"`x = {S['x']}`：个位 `x % 10 = {S['x'] % 10}`，目标 `digit = {S['digit']}`"


CONFIG = dict(
    num=3895, title='统计数字出现总次数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='不用字符串：取模拆数位', tags=[],
    code='''
class Solution:
    def countDigitOccurrences(self, nums: List[int], digit: int) -> int:
        ans = 0
        for x in nums:
            while x > 0:
                if x % 10 == digit:
                    ans += 1
                x //= 10
        return ans
''',
    call='Solution().countDigitOccurrences([12, 54, 32, 22], 2)',
    expect=4,
    views=[
        dict(type='text', fn=_text, size=30, h=80),
        dict(type='array', var='nums', label='nums', cell=110, h=190),
        dict(type='array', var=_digits, label='当前 x 的各数位（最后一格 = x % 10：绿 = 等于 digit，粉 = 不等）', cell=110,
             color=_col, h=200),
    ],
    watch=[('x', 'x', 'blue'), ('digit', 'digit', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计 `digit` 出现的总次数',
        'for x in nums': lambda S, B, r: (f'取出一个数 `x = {S.x}`，下面逐位拆开' if S.x else '`nums` 里的数都处理完了，退出循环'),
        'while x > 0': lambda S, B, r: (f'`x = {S.x} > 0`：还有数位没看' if S.x > 0 else '`x = 0`：所有数位都看完了，换下一个数'),
        'if x % 10 == digit': '个位 `{x} % 10 = {x % 10}`，和 `digit = {digit}` {"相等 → 出现一次" if x % 10 == digit else "不相等"}',
        'ans += 1': '`digit` 又出现了一次：`ans` = =={ans}==',
        'x //= 10': '去掉个位：`x` → {x}（下取整除 10）',
        'return ans': '所有数里 `digit` 一共出现 =={ret}== 次',
    },
    cards=dict(
        one_liner='不转字符串：不断 //10 去掉个位，x % 10 就是每个数位',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['给整数数组 `nums` 和一个数字 `digit`（0~9）',
                 '统计 `digit` 在所有元素十进制表示里出现的总次数',
                 '示例：`[12,54,32,22], digit = 2` → `4`（12 一次、32 一次、22 两次）'],
        quote='不断地把 x 除以 10（下取整）直到 0，例如 123→12→1→0。在这个过程中的 x mod 10，即为每个数位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x % 10` 是个位，`x //= 10` 去掉个位',
              '每个数拆到 `x == 0` 为止，个位等于 `digit` 就 `ans += 1`',
              '题解还给了字符串写法：`str(x).count(str(digit))` 求和，更短'],
        summary=['时间 `O(n log U)`：每个数有 `log U` 个数位，`U` 是最大值',
                 '空间 `O(1)`，字符串写法是 `O(log U)`',
                 '灵神的思考题：如果 `nums` 含 `0`，`while x > 0` 不会进循环，漏掉 `0` 这一位',
                 '本题 `nums[i] >= 1`，所以这个写法是对的'],
    ),
)
