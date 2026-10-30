def _digits(S):
    return list(str(S['res']).zfill(S['n'])) if 'n' in S else []


def _pos(S):
    p = S.get('p10')
    if p is None or p <= 0 or 'res' not in S:
        return None
    return S['n'] - len(str(p))


class _P:
    def __call__(self, S):
        return _pos(S)

    def __str__(self):
        return '位'


def _txt(S):
    if 'res' not in S:
        return f"`n = {S['n']}`，`s = {S['s']}`：每位最大 9，总和上限 `{9 * S['n']}`"
    return f"`res = {S['res']}`，`p10 = {S['p10']}`（当前位的权值），还剩 `s = {S['s']}`"


CONFIG = dict(
    num=4000, title='给定数位和的最大整数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='填满 n 位 · 高位优先放 9',
    tags=['灵神题单', '贪心与思维', '难度分 1200'],
    code='''
class Solution(object):
    def largestInteger(self, n, s):
        
        if s > n * 9:
            return -1
        
        if s == 0:
            return 0
        
        res = 0
        p10 = 10 ** (n - 1)
        for _ in range(n):
            d = min(s, 9)
            res += d * p10
            p10 //= 10
            s -= d
        
        return res
''',
    call='Solution().largestInteger(5, 20)',
    expect=99200,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var=_digits, pointers={_P(): 'blue'}, label='res 的 n 位（未填的位是 0，蓝箭头 = 下一个要填的位）',
             color=lambda S, i, v: 'green' if v != '0' else None, h=240),
    ],
    watch=[('s', 's', 'yellow'), ('d', 'd', 'blue'), ('p10', 'p10', 'cyan'), ('res', 'res', 'green')],
    captions={
        'if s > n * 9': lambda S, B, r: (f'`n * 9 = {S["n"] * 9}`，`s = {S["s"]}` 没超过 → 一定有解' if S['s'] <= S['n'] * 9 else '`s` 超过 `9n` → 返回 -1'),
        'if s == 0': '`s` 不为 0，继续',
        'res = 0': '`res` 是累加出来的答案',
        'p10 = 10': '`p10 = 10^(n-1) = {p10}`：最高位的权值，先假设是个 n 位数',
        'for _ in range': lambda S, B, r: ('`n` 位都填完了，循环结束' if S['p10'] == 0 else f'从高到低填下一位，当前权值 `p10 = {S["p10"]}`'),
        'd = min(s, 9)': '这一位填 `min({s}, 9) = {d}`：有 9 就放 9，不足 9 就全放进去',
        'res += d * p10': '`res += {d} × {p10}` → {res}',
        'p10 //= 10': '权值缩小十倍，去看低一位：`p10` → {p10}',
        's -= d': '还剩 `s = {s}`',
        'return res': '最大的整数是 `{res}`',
    },
    cards=dict(
        one_liner='打满 n 位，高位先放 9',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['非负整数 `n` 和 `s`：求最多 `n` 位、各位数之和为 `s` 的最大整数',
                 '不存在则返回 `-1`',
                 '本视频：`n = 5, s = 20` → `99200`'],
        quote='为了使得这个整数尽量大，就应该让这个整数的位数打满n，同时高位上尽可能大。……不断从s中分离出9填充到这个数的高位上，若s不足9，就全部填进去。',
        quote_src='—— yiduobo 题解原文',
        idea=['数位和范围是 `0 ~ 9n`，所以 `s > 9n` 时无解',
              '位数越多越大，所以假设是 `n` 位数，用 `p10 = 10^(n-1)` 记当前位权值',
              '每位填 `min(s, 9)`，乘权值累加进答案，权值每次除以 10'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`s == 0` 要特判返回 0',
                 '`p10 //= 10` 本来就是整数除法，原文代码无需修改',
                 '对比灵神：灵神把数字放进字符串数组再拼接，yiduobo 直接用权值累加成整数'],
    ),
)
