DIG = [2, 3]


def _cur(S):
    return DIG.index(S['p']) if 'p' in S else None


def _read(S):
    if 'p' not in S:
        return '指数 `b = [2, 3]` 表示十进制数 `23`，从高位到低位一位位读'
    k = _cur(S)
    return f"已读 `{''.join(map(str, DIG[:k + 1]))}`：`res` 保存 `2^(已读部分) % 1337`，下一步 `res = res^10 × 2^{S['p']}`"


def _cache(S):
    f = S.get('f')
    if not f:
        return ''
    items = [f'{a}^{b}={v}' for a, row in enumerate(f) for b, v in enumerate(row) if v is not None]
    return '已缓存 `f[a][b]`：' + ('，'.join(items) if items else '（空）')


CONFIG = dict(
    num=372, title='超级次方', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='秦九韶式逐位幂 + 1337×11 缓存表',
    tags=[],
    code='''
class Solution(object):
    def superPow(self, a, b):

        f = [[None] * 11 for _ in range(1337)]

        res = 1
        a %= 1337
        for p in b:
            res = self.get_pow(res, 10, f) * self.get_pow(a, p, f) % 1337

        return res

    def get_pow(self, a, b, f):
        if f[a][b] is None:
            if b == 0:
                f[a][b] = 1
            elif b == 1:
                f[a][b] = a
            else:
                tmp = self.get_pow(a, b//2, f)
                if b & 1:
                    f[a][b] = tmp * tmp * a % 1337
                else:
                    f[a][b] = tmp * tmp

        return f[a][b]
''',
    call='Solution().superPow(2, [2, 3])',
    expect=8388608 % 1337,
    views=[
        dict(type='array', var=lambda S: DIG, label='b（指数 23 的数位，蓝 = 当前 p）', h=140, pointers={_cur: 'blue'}, pointer_labels={_cur: 'p'},
             color=lambda S, i, v: 'blue' if i == _cur(S) else None),
        dict(type='text', fn=_read, h=80),
        dict(type='calls', h=230),
        dict(type='text', fn=lambda S: _cache(S), size=24, h=110),
    ],
    watch=['a', 'b', ('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'f = [[None]': '`f[a][b]` 缓存「`a^b % 1337`」：底数 0..1336，指数 0..10，共 1337×11 格，一开始都是 None',
        'res = 1': '`res` 是已处理高位的幂：空幂次，`a^0 = 1`',
        'a %= 1337': '先把底数取模：`a = {a}`',
        'for p in b': lambda S, B, r: (f'`b` 的每一位都读完了，`res = {S.res}`' if B.get('p') == DIG[-1] else
                                       (f'取下一位 `p = {S.p}`' if 'p' not in B else f'上一位处理完，`res = {S.res}`；取下一位 `p = {S.p}`')),
        'res = self.get_pow(res, 10': '秦九韶：`a^(10x+p) = (a^x)^10 × a^p`，所以 `res = ({B.res})^10 × 2^{p} % 1337`',
        'return res': '`b` 的每一位都处理完：`a^b % 1337 = {res}`',
        'if f[a][b] is None': lambda S, B, r: (f'`f[{S.a}][{S.b}]` 已有缓存 → 直接用' if S.f[S.a][S.b] is not None else f'`f[{S.a}][{S.b}]` 还没算过 → 现算并缓存'),
        'if b == 0': lambda S, B, r: ('`b == 0` → `a^0 = 1`' if S.b == 0 else '`b != 0`，往下判断'),
        'f[a][b] = 1': '`{a}^0 = 1`，存入缓存',
        'elif b == 1': lambda S, B, r: ('`b == 1` → `a^1 = a`' if S.b == 1 else '`b > 1` → 用快速幂：折半再平方'),
        'f[a][b] = a': '`{a}^1 = {a}`，存入缓存',
        'tmp = self.get_pow': '快速幂：先求一半指数 `a^({b}//2)`，得 `tmp = {tmp}`',
        'if b & 1': lambda S, B, r: ('`b` 是奇数 → 还要再乘一个 `a`' if S.b & 1 else '`b` 是偶数 → 直接平方'),
        'f[a][b] = tmp * tmp * a': '`{a}^{b} = tmp² × a % 1337` = =={f[a][b]}==',
        'f[a][b] = tmp * tmp': '`{a}^{b} = tmp²` = =={f[a][b]}==（外面最后会再 % 1337）',
        'return f[a][b]': '返回 `{a}^{b}` 的缓存值 `{f[a][b]}`',
    },
    cards=dict(
        one_liner='幂次是大数：一位位读，每读一位先 10 次方再乘 a^p',
        complexity='时间 `O(len(b))`（每位幂次 ≤ 10），空间 `O(1337×11)`',
        problem=['计算 `a^b % 1337`，其中 `a` 是正整数，`b` 是以数组形式给出的超大正整数（每个元素是一位十进制数字）',
                 '示例：`a=2, b=[3]` → `8`；`a=2, b=[1,0]` → `1024`',
                 '本视频：`a=2, b=[2,3]`，即 `2^23 % 1337 = ' + str(8388608 % 1337) + '`'],
        quote='按照秦九韶公式合并10的幂次之后，可以写成 a^(((b[n]*10)+b[n-1])*10+...)，……于是，我们可以将b从左往右一趟扫描。',
        quote_src='—— yiduobo 题解原文',
        idea=['`b = [2,3]` 即指数 `2*10+3`：`a^23 = (a^2)^10 × a^3`',
              '从左往右扫：`res = res^10 × a^p`，指数只会是 0..10，快速幂很浅',
              '用 `f[a][b]` 缓存 `a^b % 1337`（0 ≤ a < 1337，0 ≤ b ≤ 10），重复的底数不再重算'],
        summary=['时间 `O(len(b))`，空间 `O(1337×11)`',
                 '易错点：每次 `res` 取模后才能当下一次的底数（下标要 < 1337）；`a %= 1337` 不能漏',
                 '`f[a][b] = tmp * tmp` 没取模，因为外层乘积最后统一 `% 1337`',
                 '原文为 Python 2 写法，`get_pow` 里的 `b/2` 已改为 `b//2`'],
    ),
)
