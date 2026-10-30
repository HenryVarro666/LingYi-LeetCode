def _eq(S):
    if 'm' in S and 'n' in S:
        return f"约分后 `p/q = {S['m']}/{S['n']}`：光线走 ==m = {S['m']}== 个边长到东墙方向、==n = {S['n']}== 个边长到北墙方向"
    if 'x' in S and 'y' in S:
        return f"辗转相除求 gcd(p, q)：`x = {S['x']}`，`y = {S['y']}`" + ('（y = 0，gcd 就是 x）' if S['y'] == 0 else '')
    return '光线水平速度 `p`、竖直速度 `q`'


def _corner(S):
    if 'm' not in S:
        return ''
    m, n = S['m'], S['n']
    return (f"m = {m} 是{'偶' if m % 2 == 0 else '奇'}数，n = {n} 是{'偶' if n % 2 == 0 else '奇'}数 → "
            + ('==角落 2==' if m % 2 == 0 else '==角落 0==' if n % 2 == 0 else '==角落 1=='))


CONFIG = dict(
    num=858, title='镜面反射', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='速度分解 + gcd 约分 + 奇偶判断',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def mirrorReflection(self, p, q):

        if p == q:
            return 1

        x, y = p, q
        while y != 0:
            x, y = y, x % y

        m = p // x
        n = q // x

        if m % 2 == 0:
            return 2
        elif n % 2 == 0:
            return 0
        else:
            return 1
''',
    call='Solution().mirrorReflection(6, 4)',
    expect=0,
    views=[
        dict(type='text', fn=_eq, size=34, h=90),
        dict(type='text', fn=lambda S: f"`p = {S['p']}`，`q = {S['q']}`" + (f"　`gcd = {S['x']}`" if 'm' in S else ''), size=34, h=70),
        dict(type='text', fn=_corner, size=34, h=90),
    ],
    watch=['p', 'q', ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('m', 'm', 'green'), ('n', 'n', 'purple')],
    captions={
        'if p == q': lambda S, B, r: ('`p == q`：光线斜 45 度，直接射入角落 1' if S.p == S.q else f'`p = {S.p}` ≠ `q = {S.q}`：不是 45 度，往下用 gcd 推'),
        'x, y = p, q': '准备求 `p` 和 `q` 的最大公约数：`x = {x}`，`y = {y}`',
        'while y != 0': lambda S, B, r: (f'`y = {S.y}` 不为 0，继续辗转相除' if S.y != 0 else '`y = 0`，循环结束：`x` 就是 gcd'),
        'x, y = y, x % y': '`x, y = y, x % y`：新 `x = {x}`，新 `y = {y}`',
        'm = p': '`m = p // gcd = {m}`：约分后的分子，也是光线到东墙的次数（时间 t = m）',
        'n = q': '`n = q // gcd = {n}`：约分后的分母，竖直方向走过的边长数',
        'if m % 2': lambda S, B, r: (f'`m = {S.m}` 是偶数 → 光线必然射入角落 2' if S.m % 2 == 0 else f'`m = {S.m}` 是奇数，还要看 n'),
        'elif n % 2': lambda S, B, r: (f'`m` 奇、`n = {S.n}` 是偶数 → 光线射入角落 0' if S.n % 2 == 0 else f'`m`、`n` 都是奇数 → 其他情况'),
        'return 2': '返回 ==2==',
        'return 0': '`m` 奇 `n` 偶：返回 ==0==',
        'return 1': '其他情况：返回 ==1==',
    },
    cards=dict(
        one_liner='把光线拆成水平、竖直两个速度，约分后看 m、n 的奇偶',
        complexity='时间 `O(log min(p, q))`，空间 `O(1)`',
        problem=['正方形房间边长 `p`，除西南角外三个角落各有接收器 0、1、2',
                 '激光从西南角射出，先接触东墙，该点距角落 0 为 `q`',
                 '求光线最先到达的角落编号（0、1 或 2）',
                 '本视频：`p = 6, q = 4` → `0`'],
        quote='既然是物理问题，那么就搞点物理的方法。对于射出的光，我们可以将其速度看成水平方向的速度和竖直方向速度的叠加。',
        quote_src='—— yiduobo 题解原文',
        idea=['设首次碰东墙为单位时间：水平速度 `p`，竖直速度 `q`',
              '射入角落要两个方向都走整数个边长：`p·t = m·p`，`q·t = n·p`',
              '得 `m / n = p / q`，约分到最简，`m`、`n` 就是分子分母',
              '`m` 偶 → 角落 2；`m` 奇 `n` 偶 → 角落 0；否则角落 1'],
        summary=['时间 `O(log min(p, q))`（gcd），空间 `O(1)`',
                 '一定要先用 gcd 约分，不约分奇偶判断会错',
                 '`p == q` 单独处理，直接是角落 1',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
