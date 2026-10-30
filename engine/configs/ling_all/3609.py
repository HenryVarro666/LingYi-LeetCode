def _pt(S):
    return [S['x'], S['y']] if 'x' in S and 'y' in S else None


def _st(S):
    return [S['sx'], S['sy']] if 'sx' in S and 'sy' in S else None


def _txt(S):
    if 'x' not in S:
        return ''
    x, y, sx, sy = S['x'], S['y'], S['sx'], S['sy']
    if x == sx and y == sy:
        return f'`({x}, {y})` == 起点 `({sx}, {sy})` → ==倒着走到起点了=='
    return f'从终点倒着走：现在在 `({x}, {y})`，要回到 `({sx}, {sy})`，已倒退 `{S["ans"]}` 步'


CONFIG = dict(
    num=3609, title='到达目标点的最小移动次数', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='逆向模拟 · 每步上一步唯一',
    tags=['灵神题单·贪心与思维', '难度分 2419'],
    code='''
class Solution:
    def minMoves(self, sx: int, sy: int, x: int, y: int) -> int:
        ans = 0
        while x != sx or y != sy:
            if x < sx or y < sy:
                return -1
            ans += 1
            if x == y:
                if sy > 0:
                    x = 0
                else:
                    y = 0
                continue
            # 保证 x > y
            if x < y:
                x, y = y, x
                sx, sy = sy, sx
            if x > y * 2:
                if x % 2 > 0:
                    return -1
                x //= 2
            else:
                x -= y
        return ans
''',
    call='Solution().minMoves(0, 1, 1, 4)',
    expect=3,
    views=[
        dict(type='array', var=_pt, label='当前点 (x, y)：从终点 (tx, ty) 倒着走', cell=110, h=210,
             color=lambda S, i, v: 'green' if S.get('x') == S.get('sx') and S.get('y') == S.get('sy') else ('blue' if i == 0 else 'pink'), index=False),
        dict(type='array', var=_st, label='起点 (sx, sy)（交换 x、y 时它也一起交换）', cell=110, h=210, index=False),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=[('ans', 'ans', 'green'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('sx', 'sx'), ('sy', 'sy')],
    captions={
        'ans = 0': '倒着走，`ans` 记倒退的步数。正着走不知道选哪个操作，倒着走每步==唯一==',
        'while x != sx': lambda S, B, r: (f'`({S.x}, {S.y})` 还不是起点 `({S.sx}, {S.sy})`，继续倒退' if (S.x != S.sx or S.y != S.sy) else '回到起点了，退出循环'),
        'if x < sx or y < sy': lambda S, B, r: ('走过头了（比起点还小）→ 到不了，返回 -1' if (S.x < S.sx or S.y < S.sy) else f'`({S.x}, {S.y})` 没有小于起点，还能继续倒退'),
        'ans += 1': '倒退一步，`ans` = {ans}',
        'if x == y': lambda S, B, r: (f'`x == y == {S.x}`：上一步只能是某一维从 0 加上 {S.x} 得来' if S.x == S.y else '`x != y`：上一步只能是给较大的 x 加数（见下面两种情形）'),
        'if sy > 0': lambda S, B, r: (f'`sy = {S.sy} > 0`：起点 y 非 0，只能把 x 还原成 0' if S.sy > 0 else f'`sy = 0`：只能把 y 还原成 0（起点 sx 才可能非 0）'),
        'x = 0': '`x` 还原为 0：`({x}, {y})`',
        'y = 0': '`y` 还原为 0：`({x}, {y})`',
        'continue': '回到循环开头，检查是否到起点',
        'x, y = y, x': '`x < y`：(x, y) 与 (y, x) 等价，镜像交换，保证 `x > y`：`x = {x}, y = {y}`',
        'sx, sy = sy, sx': '==起点也要一起交换==，否则比较的是不同的轴：`sx = {sx}, sy = {sy}`',
        'if x > y * 2': lambda S, B, r: (f'`x = {S.x} > 2y = {S.y * 2}`：上一步只能是 x 翻倍（x 加自己）' if S.x > S.y * 2 else f'`x = {S.x} <= 2y = {S.y * 2}`：上一步是 x 加上了较大数 y'),
        'if x % 2 > 0': lambda S, B, r: (f'`x = {S.x}` 是奇数，不可能由翻倍得到 → -1' if S.x % 2 > 0 else f'`x = {S.x}` 是偶数，可以减半'),
        'return -1': '不可能到达，返回 -1',
        'x //= 2': '撤销翻倍：`x` 减半为 =={x}==',
        'x -= y': '撤销 `x += y`：`x` 减去 `y` 变成 =={x}==（此时 `({x}, {y})`）',
        'return ans': '回到起点，最少 `{ans}` 步（倒退的路径唯一，所以就是最小）',
    },
    cards=dict(
        one_liner='正着不知道选哪个操作，倒着每一步都是唯一的',
        complexity='时间 `O(log(tx+ty))`，空间 `O(1)`',
        problem=['在 `(x, y)` 令 `m = max(x, y)`，可走到 `(x+m, y)` 或 `(x, y+m)`',
                 '求从 `(sx, sy)` 到 `(tx, ty)` 的最少步数，到不了返回 -1',
                 '本视频：`(0,1) → (1,4)`，答案 `3`'],
        quote='正着走，不知道该执行哪个操作，但倒着走就知道了。……注意这不是贪心，是纯模拟。如果我们没有返回 -1，那么起点与终点之间的走法是唯一的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `x >= y`（不然交换，起点一起交换）',
              '`x > 2y`：上一步是 x 翻倍，要求 x 为偶数；`x <= 2y`：上一步是 x 加了 y',
              '`x == y`：只能把某一维还原为 0，由起点哪一维为 0 决定'],
        summary=['时间 `O(log(tx+ty))`：每两步内 `x` 至少减半',
                 '交换 `x, y` 时==必须同时交换 `sx, sy`==',
                 '`x == y` 时看 `sy > 0` 决定还原哪一维；两者为 0 的情况会在减半时遇到奇数而 -1',
                 '`x < sx or y < sy` 走过头直接返回 -1',
                 '同类题：780 到达终点、2543'],
    ),
)
