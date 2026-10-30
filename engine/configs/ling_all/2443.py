def _eq(S):
    if 'i' not in S:
        return ''
    i = S['i']
    x = S.get('x', i)
    rev = S.get('rev', 0)
    line = S.get('_line', 0)
    if line >= 9:
        return f"`{i} + {rev}` = =={i + rev}==　目标 `num = {S['num']}`　{'==相等==' if i + rev == S['num'] else '不等'}"
    return f"枚举 `i = {i}`：正在把它反转，已得 `rev = {rev}`，还剩 `x = {x}`"


CONFIG = dict(
    num=2443, title='反转之后的数字和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举 · 不用字符串反转',
    tags=['灵神题单'],
    code='''
class Solution:
    def sumOfNumberAndReverse(self, num: int) -> bool:
        for i in range(num + 1):
            rev, x = 0, i
            while x:
                rev = rev * 10 + x % 10
                x //= 10
            if i + rev == num:
                return True
        return False
''',
    call='Solution().sumOfNumberAndReverse(33)',
    expect=True,
    views=[
        dict(type='text', fn=_eq, size=30),
        dict(type='array', var=lambda S: list(str(S['i'])) if 'i' in S else [], label='i 的各位数字（从左到右）', h=170, cell=90),
        dict(type='array', var=lambda S: list(str(S['rev'])) if S.get('rev') else [], label='已反转得到的 rev', h=170, cell=90),
    ],
    watch=['num', ('i', 'i', 'blue'), ('x', 'x', 'pink'), ('rev', 'rev', 'green')],
    captions={
        'for i in range': '`num ≤ 10^5`，直接从 `0` 到 `num` 枚举每个 `k`（这里叫 `i`）：现在是 `i = {i}`',
        'rev, x = 0': '`rev` 存反转结果，`x` 存还没取走的部分：`x = i = {x}`',
        'while x': lambda S, B, r: (f'`x = {S.x}` 还有数位 → 继续取最低位' if S.x else '`x = 0`：数位取完，反转完成'),
        'rev = rev * 10': '取 `x` 的最低位 `{B.x % 10}`，接到 `rev` 末尾：`{B.rev} * 10 + {B.x % 10}` = =={rev}==',
        'x //= 10': '`x` 去掉最低位 → {x}',
        'if i + rev == num': lambda S, B, r: (f'`{S.i} + {S.rev} = {S.i + S.rev}` ==等于== `num = {S.num}` → 找到了' if S.i + S.rev == S.num else f'`{S.i} + {S.rev} = {S.i + S.rev}` 不等于 `{S.num}` → 试下一个 i'),
        'return True': '存在 `k = {i}`，满足 `k + reverse(k) = num` → ==True==',
    },
    skip=[],
    max_steps=48,
    cards=dict(
        one_liner='num 只有 10^5，直接枚举 k，反转后看和是否等于 num',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['非负整数 `num`，是否存在非负整数 `k` 使 `k + reverse(k) = num`',
                 '`reverse(k)` 是把 `k` 的数位反转，可以有前导零（`140 → 041`）',
                 '示例：`443 → true`（172+271），`63 → false`；本视频用 `33`（12+21）'],
        quote='一行写法（由于 Python 在处理反转时调用了底层的 C 库，这种写法实际比不用字符串的写法还要快）',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k ≤ num`，所以枚举 `i` 从 `0` 到 `num`',
              '不用字符串：不断取最低位接到 `rev` 末尾，`x` 每次整除 10',
              '`i + rev == num` 就立即返回 `True`；全部枚举完才 `False`'],
        summary=['时间 `O(n log n)`：枚举 `n` 个数，每个反转 `O(log n)`',
                 '`range(num + 1)` 要包含 `num` 自己（`num = 0` 时 `k = 0`）',
                 '`reverse(140) = 41`，前导零自然消失，不需要特判',
                 '灵神还给了一行写法：`any(i + int(str(i)[::-1]) == num ...)`，本视频演示不用字符串的写法'],
    ),
)
