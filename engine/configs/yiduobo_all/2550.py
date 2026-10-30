def _text(S):
    if 'p' not in S:
        return '`2^n` 用快速幂：`2^p = (2^(p/2))^2`，`p` 为奇数时再乘 2'
    p = S['p']
    return f'`p = {p}`：求 `2^{p} mod 1000000007`'


CONFIG = dict(
    num=2550, title='猴子碰撞的方法数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='总数减去不碰撞 · 递归快速幂',
    tags=['灵神题单', '难度分 1663'],
    code='''
class Solution(object):
    def monkeyMove(self, n):

        mod = 10 ** 9 + 7

        def quickPow(p):
            if p == 1:
                return 2
            
            x = quickPow(p // 2)
            x *= x
            x %= mod

            if p % 2 == 1:
                x += x
                if x >= mod:
                    x -= mod
            
            return x
        
        res = quickPow(n) - 2
        if res < 0:
            res += mod
        
        return res
''',
    call='Solution().monkeyMove(10)',
    expect=1022,
    views=[
        dict(type='text', fn=_text, h=100),
        dict(type='calls', h=380),
    ],
    watch=['mod', 'x', ('res', 'res', 'green')],
    captions={
        'mod =': '答案对 `10^9 + 7` 取余',
        'def quickPow': '定义快速幂 `quickPow(p)` = `2^p mod mod`',
        'res = quickPow(n)': lambda S, B, r: (f'`quickPow({S.n})` 返回 `{r}`，减去不碰撞的 2 种' if 'res' in S else '调用 `quickPow(n)`，算 `2^n`'),
        'if p == 1': lambda S, B, r: ('`p = 1`：递归到底，`2^1 = 2`' if S.p == 1 else f'`p = {S.p}`，还没到 1，继续拆成一半'),
        'return 2': '`2^1 = 2`，向上返回',
        'x = quickPow': lambda S, B, r: (f'`quickPow({S.p // 2})` 返回 `x = {S.x}`，即 `2^{S.p // 2}`' if 'x' in S
                                       else f'要算 `2^{B.p}`：先递归求 `2^{B.p // 2}`（`p // 2 = {B.p // 2}`），再平方'),
        'x *= x': '平方：`x = {x}`（对应 `2^{p // 2 * 2}`）',
        'x %= mod': '取模防止数字过大：`x = {x}`',
        'if p % 2 == 1': lambda S, B, r: (f'`p = {S.p}` 是奇数，还差一个 2' if S.p % 2 == 1 else f'`p = {S.p}` 是偶数，平方就是 `2^{S.p}`'),
        'x += x': '奇数多乘一个 2：`x += x` 就是 `x * 2` → `{x}`',
        'if x >= mod': lambda S, B, r: ('`x >= mod`，要减一次 `mod`' if S.x >= S.mod else '`x < mod`，不用减'),
        'x -= mod': '减去 `mod` → `{x}`',
        'return x': '`quickPow({p})` = `{x}`',
        'res = quickPow': '`res = 2^n − 2 = {res}`',
        'if res < 0': lambda S, B, r: ('`res < 0`：`2^n mod 1000000007` 比 2 小，要补回 `mod`' if S.res < 0 else '`res >= 0`，不用补'),
        'return res': '碰撞的方法数 `{res}`',
    },
    cards=dict(
        one_liner='碰撞难数就数不碰撞：只有同向的 2 种，总数 2^n − 2',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['正 `n` 边形每个顶点一只猴子，同时顺时针或逆时针移动一步',
                 '两只猴子落在同一顶点或在边上相遇就碰撞，求至少碰撞一次的方法数（取余 `10^9 + 7`）',
                 '示例：`n=3` → `6`；本视频 `n=10` → `1022`'],
        quote='直接计算碰撞的方法数是比较困难的，不妨反过来思考不会碰撞的方法数有多少。可以发现，只有当所有猴子都往顺时针或者都往逆时针行动时才不会发生碰撞，也就是只有两种情况不会发生碰撞。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 只猴子各 2 种选择，总共 `2^n` 种',
              '不碰撞只有两种，答案 `2^n − 2`',
              '`n` 很大，递归快速幂：`2^p` 由 `2^(p//2)` 平方，奇数再翻倍'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '原文为 Python 2 写法，`quickPow` 里的 `p / 2` 已改为 `p // 2`，并删去类型文档',
                 '`x += x` 就是乘 2，翻倍后至多超过 `mod` 一次，所以减一次就够',
                 '`res` 可能为负，要补一个 `mod`',
                 '对比灵神：灵神直接用内置 `pow(2, n, MOD)`；yiduobo 手写了递归快速幂'],
    ),
)
