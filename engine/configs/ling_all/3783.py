CONFIG = dict(
    num=3783, title='整数的镜像距离', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='字符串反转',
    code='''
class Solution:
    def mirrorDistance(self, n: int) -> int:
        rev = int(str(n)[::-1])
        return abs(n - rev)
''',
    call='Solution().mirrorDistance(1230)',
    expect=909,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"`n = {S['n']}`，反转得到 `rev = {S['rev']}`（前导零 0321 自动变成 321），差 ==" + str(abs(S['n'] - S['rev'])) + '==') if 'rev' in S else f"`n = {S['n']}`：把数字反转，再和原数相减"),
        dict(type='string', var=lambda S: str(S['n']), h=200, label='n 的数位'),
        dict(type='string', var=lambda S: str(S['n'])[::-1], h=200, label='反转后的字符串'),
    ],
    watch=['n', 'rev'],
    captions={
        'rev = int': '`str(n)[::-1]` 把 `{n}` 的数位倒过来得到 "{str(n)[::-1]}"，`int` 去掉前导零 → rev 变成 =={rev}==',
        'return abs': '`abs(n - rev) = abs({n} - {rev})` = =={ret}==，取绝对值是因为反转后可能比原数大',
    },
    cards=dict(
        after=[dict(heading='写法二：逐位取数', lines=['`x, d = divmod(x, 10)` 每次取出最低位 `d`', '`rev = rev * 10 + d` 把 `d` 接到 `rev` 末尾', '例如 `32 * 10 + 1 = 321`，空间只要 `O(1)`'])],
        one_liner='把数反转，再和原数取绝对差',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['镜像距离 = `abs(n - reverse(n))`，`reverse(n)` 是把数字反转后形成的整数',
                 '示例：`n=25` → `abs(25 - 52) = 27`；`n=10` → `reverse=1`，答案 `9`',
                 '演示用：`n=1230` → 反转为 `321`，答案 `909`'],
        quote='不断地把 n 除以 10（下取整）直到 0，例如 123→12→1→0。在这个过程中的 d = n mod 10，即为每个数位。',
        quote_src='—— 灵茶山艾府题解（写法二的思路）',
        idea=['本视频演示最简写法：转成字符串，切片反转，再转回整数',
              '`int` 会自动去掉前导零，`10` 反转得到 `01` 即 `1`',
              '写法二：用 `divmod(x, 10)` 取数位，`rev = rev * 10 + d` 拼接'],
        summary=['时间 `O(log n)`（数位个数）；字符串写法空间 `O(log n)`',
                 '写法二用 `divmod` 逐位取出数位，空间 `O(1)`',
                 '易错点：结尾为 0 的数反转后位数变少，例如 `10 → 1`',
                 '要加 `abs`：反转后可能比原数大'],
    ),
)
