CONFIG = dict(
    num=2543, title='判断一个点是否可以到达', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='gcd 是否为 2 的幂', tags=['灵神题单', '数学算法', '难度分 2221'],
    code='''
class Solution:
    def isReachable(self, targetX: int, targetY: int) -> bool:
        g = gcd(targetX, targetY)
        return (g & (g - 1)) == 0
''',
    call='Solution().isReachable(12, 20)',
    expect=True,
    views=[
        dict(type='text', h=150, size=34, fn=lambda S: f"`gcd({S['targetX']}, {S['targetY']})` = =={S['g']}==" if 'g' in S else f"终点 `({S['targetX']}, {S['targetY']})`，先求两坐标的 gcd"),
        dict(type='text', h=150, size=34, fn=lambda S: f"`g = {S['g']}` 的二进制 `{S['g']:b}`，`g & (g−1)` = =={S['g'] & (S['g']-1)}==" if 'g' in S else '前两种移动不改 gcd，后两种让 gcd 乘 2'),
    ],
    watch=['targetX', 'targetY', ('g', 'g', 'green')],
    captions={
        'g = gcd': '前两种移动像辗转相除，`g` 不变；后两种让 `g` 乘 2。起点 `g = 1`，所以终点 `g` 只能是 2^k：`g = {g}`',
        'return': '`g & (g-1)` = `{g} & {g-1}` = {g & (g-1)}，为 0 说明 `g` 是 2 的幂 → =={ret}==',
    },
    cards=dict(
        one_liner='把移动看成辗转相除，gcd 只能乘 2，所以 gcd 必须是 2 的幂',
        complexity='时间 `O(log min(x, y))`，空间 `O(1)`',
        problem=['无限网格从 `(1,1)` 出发，每步 `(x,y)` 可变为：',
                 '`(x,y-x)`、`(x-y,y)`、`(2x,y)`、`(x,2y)` 之一',
                 '问能否到达 `(targetX, targetY)`；`(4,7)` → `True`，`(6,9)` → `False`'],
        quote='前两个移动很像辗转相除法，g 不变；后两个移动可以让 g 乘上 2^k。而一开始 1,1 的 g=1，那么最终 targetX,targetY 的 g 只能是 2^k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先看不变量：减法移动保持 `gcd`，倍增移动让 `gcd` 翻倍',
              '判断 2 的幂用 `g & (g-1) == 0`（第 231 题）',
              '充分性：从终点倒着走，有偶数就除 2；都是奇数时走两步到 `(x, (x+y)/2)`，数值不断变小，最后到 `(1,1)`'],
        before=[dict(heading='构造方案（倒着走）', lines=[
            '倒着走：`(x,y)` 可到 `(x,x+y)`、`(x+y,y)`、`(x/2,y)`、`(x,y/2)`',
            '只要有偶数就除以 2；都是奇数时，`x < y` 则走两步得 `(x, (x+y)/2)`',
            '`x`、`y` 总能变小，直到 `x = y = 1`，所以条件也是充分的'])],
        summary=['时间 `O(log)`，空间 `O(1)`',
                 '关键是找不变量 `gcd`，再从起点 `gcd = 1` 推出终点的限制',
                 '判断 2 的幂：`g & (g-1) == 0`，`g ≥ 1` 时成立',
                 '题解还给出了具体移动方案的构造（倒推）'],
    ),
)
