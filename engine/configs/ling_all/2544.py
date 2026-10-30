_N = 52143
_D = [int(c) for c in str(_N)]


def _done(S):
    n = S.get('n')
    if n is None:
        return 0
    return len(_D) - (len(str(n)) if n else 0)


CONFIG = dict(
    num=2544, title='交替数字和', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='从低位取数 · 符号翻转',
    tags=[],
    code='''
class Solution:
    def alternateDigitSum(self, n: int) -> int:
        ans, sign = 0, 1
        while n:
            ans += n % 10 * sign
            sign = -sign
            n //= 10
        return ans * -sign
''',
    call='Solution().alternateDigitSum(52143)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"`n = {S['n']}`，个位 `{S['n'] % 10}`；`sign` 当前为 `{'+' if S['sign'] > 0 else '-'}`" if 'sign' in S and S['n'] else '从最低位开始，逐位取出再乘符号'), size=30, h=70),
        dict(type='array', var=lambda S: _D, label='原数 52143 的各位（灰 = 已处理）', h=260,
             dim=lambda S, i, v: i >= len(_D) - _done(S),
             color=lambda S, i, v: 'blue' if i == len(_D) - 1 - _done(S) else None),
    ],
    watch=[('n', 'n', 'blue'), ('sign', 'sign', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans, sign = 0, 1': '`ans = 0` 累计答案；`sign = 1` 先假设个位取正号',
        'while n': '`n = {n}`：还有数位没取，继续',
        'ans += n % 10 * sign': '个位 `{n % 10}` × 符号 `{sign}` 加进答案 → `ans = {ans}`',
        'sign = -sign': '相邻数位符号相反：`sign` 翻转成 `{sign}`',
        'n //= 10': '`n //= 10` 去掉个位，`n` 变成 `{n}`',
        'return ans * -sign': '循环结束时 `sign` 已多翻转一次，它是最高位的==相反号==。最高位应取正，所以乘 `-sign = {-sign}` → `{ans * -sign}`',
    },
    cards=dict(
        one_liner='从低位取数，最高位若是负号就整体取反',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['最高位取正号，之后每一位符号与前一位相反，求带符号数位和',
                 '示例：`n = 521` → `5 − 2 + 1 = 4`',
                 '本视频：`n = 52143` → `5 − 2 + 1 − 4 + 3 = 3`'],
        quote='我们可以从最低位开始，通过 n mod 10 得到个位数，再把 n 除以 10，重复前面的过程，得到十位数、百位数、……最后得到最高位，如果发现它取的是负号，则把答案取反。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不转字符串：`n % 10` 取个位，`n //= 10` 去个位',
              '从低位走，不知道总位数，所以==先给个位正号==，之后每位翻转',
              '最高位若得到负号，整体取反即可；最后一次翻转后的 `sign` 正是最高位符号的相反数'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：返回 `ans * -sign`，不是 `ans * sign`；`sign` 在循环里多翻转了一次',
                 '另一种写法：转成字符串后按下标奇偶加减，更直观'],
    ),
)
