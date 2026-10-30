W, H = 6, 3
DIRS = ['East', 'North', 'West', 'South']


class _V:
    def __init__(self, S):
        self.w, self.h = S['self.w'], S['self.h']
        self.x, self.y, self.d = S['self.x'], S['self.y'], S['self.d']
        self.num = S.get('num')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '网格图（左下角 (0,0)；亮格 = 最外圈，机器人只会在外圈上走）', 24, T['muted'], bold=True)
    w, h = S.get('self.w', W), S.get('self.h', H)
    st = (S['self.x'], S['self.y'], S['self.d']) if 'self.x' in S else None
    cell = min(120, (x1 - x0 - 120) / w, (y1 - y0 - 150) / h)
    sx = x0 + 60 + ((x1 - x0 - 120) - cell * w) / 2
    base = y0 + 70 + cell * h
    for x in range(w):
        for y in range(h):
            ring = x in (0, w - 1) or y in (0, h - 1)
            X, Y = sx + x * cell, base - (y + 1) * cell
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=T['panel2'] if ring else T['bg'],
                    outline=T['border'], r=8)
            if ring:
                cv.text((X + cell / 2, Y + cell - 8), f'{x},{y}', 16, T['dim'], anchor='mb', mono=True)
    if st is None:
        return
    x, y, d = st
    cx, cy = sx + x * cell + cell / 2, base - y * cell - cell / 2
    cv.rect((cx - cell / 2 + 3, cy - cell / 2 + 3, cx + cell / 2 - 3, cy + cell / 2 - 3), fill=T['yellow'], alpha=70, r=8,
            outline=T['yellow'], width=3)
    dx, dy = [(1, 0), (0, -1), (-1, 0), (0, 1)][d]
    cv.arrow((cx - dx * cell * 0.28, cy - dy * cell * 0.28), (cx + dx * cell * 0.34, cy + dy * cell * 0.34), T['blue'], 8, 22)
    cv.text((sx + w * cell / 2, base + 24), f'机器人 ({x}, {y})，面朝 {DIRS[d]}   |   一圈 = 2(w+h-2) = {2 * (w + h - 2)} 步',
            26, T['text'], anchor='mt', bold=True)


CONFIG = dict(
    num=2069, title='模拟行走机器人 II', difficulty='Medium', category='模拟',
    author='yiduobo', technique='先折成外圈上的一维位置，再取模',
    tags=[],
    code='''
class Robot(object):

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.x = self.y = self.d = 0

    def step(self, num):

        if self.d == 0:
            num += self.x
        elif self.d == 1:
            num += self.w + self.y - 1
        elif self.d == 2:
            num += self.w + self.h - 2 + self.w - self.x - 1
        else:
            num += self.w + self.h + self.w - 3 + self.h - self.y - 1
        
        num %= (self.w + self.h + self.w + self.h - 4)
        if num < self.w:
            self.x = num
            self.y = 0
        elif self.w <= num < self.w + self.h - 1:
            self.x = self.w - 1
            self.y = num - self.w + 1
        elif self.w + self.h - 1 <= num < self.w + self.h - 2 + self.w:
            self.x = self.w - (num - self.w - self.h + 2) - 1
            self.y = self.h - 1
        else:
            self.x = 0
            self.y = self.h - (num - self.w - self.h - self.w + 3) - 1

        if self.y == 0 and 1 <= self.x < self.w:
            self.d = 0
        elif self.x == self.w - 1 and 1 <= self.y < self.h:
            self.d = 1
        elif self.y == self.h - 1 and 0 <= self.x < self.w - 1:
            self.d = 2
        else:
            self.d = 3

    def getPos(self):
        return [self.x, self.y]

    def getDir(self):
        if self.d == 0:
            return "East"
        elif self.d == 1:
            return "North"
        elif self.d == 2:
            return "West"
        else:
            return "South"
''',
    call=f'''r = Robot({W}, {H})
out = []
r.step(4)
r.step(5)
out.append(r.getPos())
out.append(r.getDir())
r.step(2)
out.append(r.getPos())
out''',
    expect=[[3, 2], 'West', [1, 2]],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"位置 `({S['self.x']}, {S['self.y']})`，方向 `d = {S['self.d']}`（0 东 / 1 北 / 2 西 / 3 南）" if 'self.x' in S else ''),
    ],
    watch=[('x', 'self.x', 'blue'), ('y', 'self.y', 'pink'), ('d', 'self.d', 'orange'), ('num', 'num', 'green')],
    skip=[22, 25, 28, 31],
    captions={
        6: '`x, y, d` 分别是坐标和朝向（0 东 / 1 北 / 2 西 / 3 南）；每次 `step` 后重新算出来',
        10: lambda S, B, r: f"先把「当前位置」折成外圈上的距离（起点 (0,0) 算 0）：朝向 `d = {S['self.d']}`，" + ('朝东在底边' if S['self.d'] == 0 else '不是朝东，继续看是哪条边'),
        11: lambda S, B, r: f"朝东在底边：已走距离就是 `x = {S['self.x']}` → `num = 步数 + x = {S.num}`",
        12: lambda S, B, r: '`d == 1`？朝北在右边' if S['self.d'] != 1 else '朝北：在右边',
        13: lambda S, B, r: f"朝北：底边走了 `w-1`，再往上 `y = {S['self.y']}` 步 → `num = {S.num}`",
        14: lambda S, B, r: '`d == 2`？朝西在顶边' if S['self.d'] != 2 else '朝西：在顶边',
        15: lambda S, B, r: f"朝西：右边、顶边走完，再加上 `w-1-x` → `num = {S.num}`",
        16: '否则朝南在左边',
        17: lambda S, B, r: f"朝南：已走了三条边，再加上 `h-1-y` → `num = {S.num}`",
        19: lambda S, B, r: f"一圈是 `(w+h-2)*2 = {2 * (S['self.w'] + S['self.h'] - 2)}` 步，取模：`num` → =={S.num}==，就是从起点算起的圈上位置",
        20: lambda S, B, r: (f'`num = {S.num} < w = {_V(S).w}` → 落在底边' if S.num < _V(S).w else f'`num = {S.num} ≥ w = {_V(S).w}` → 不在底边'),
        21: lambda S, B, r: f'底边：`x = num = {_V(S).x}`，`y = 0`',
        23: lambda S, B, r: (f'`{_V(S).w} ≤ num = {S.num} < {_V(S).w + _V(S).h - 1}` → 落在右边'
                             if _V(S).w <= S.num < _V(S).w + _V(S).h - 1 else f'`num = {S.num}` 不在右边'),
        24: lambda S, B, r: f'右边：`x = w-1 = {_V(S).x}`，`y = num - w + 1`',
        26: lambda S, B, r: (f'`num = {S.num} < {_V(S).w * 2 + _V(S).h - 2}` → 落在顶边'
                             if S.num < _V(S).w * 2 + _V(S).h - 2 else f'`num = {S.num}` 已超过顶边 → 落在左边'),
        27: lambda S, B, r: f'顶边：从右上角往西走了 `num-w-h+2` 格 → `x = {_V(S).x}`，`y = h-1 = {_V(S).h - 1}`',
        30: '左边：`x = 0`',
        33: lambda S, B, r: (f'坐标 `({_V(S).x}, {_V(S).y})` 在底边且 `x ≥ 1` → ==朝东=='
                             if _V(S).y == 0 and 1 <= _V(S).x < _V(S).w else f'坐标 `({_V(S).x}, {_V(S).y})` 不在底边（`x = 0` 的起点不算）'),
        35: lambda S, B, r: (f'坐标 `({_V(S).x}, {_V(S).y})` 在右边且 `y ≥ 1` → ==朝北=='
                             if _V(S).x == _V(S).w - 1 and 1 <= _V(S).y < _V(S).h else '不在右边（右下角算底边，仍朝东）'),
        37: lambda S, B, r: (f'坐标 `({_V(S).x}, {_V(S).y})` 在顶边且 `x < w-1` → ==朝西=='
                             if _V(S).y == _V(S).h - 1 and 0 <= _V(S).x < _V(S).w - 1 else '不在顶边（右上角算右边，仍朝北）'),
        34: '朝东 `d = 0`',
        36: '朝北 `d = 1`',
        38: '朝西 `d = 2`',
        40: '其余（左边、左下角）朝南 `d = 3`',
        43: lambda S, B, r: f'返回当前坐标 `[{_V(S).x}, {_V(S).y}]`',
        46: '`getDir` 按 `d` 翻译成方向名：先看 `d == 0`？',
        48: '`d != 0`，再看 `d == 1`？',
        50: '`d != 1`，再看 `d == 2`？',
        47: '返回 `East`', 49: '返回 `North`', 51: '返回 `West`', 53: '返回 `South`',
    },
    cards=dict(
        one_liner='把当前位置折成外圈上的一维距离，加上步数，再对一圈取模',
        complexity='`step` 为 `O(1)`，`getPos`、`getDir` 为 `O(1)`，空间 `O(1)`',
        problem=['`w × h` 网格，机器人从 `(0,0)` 出发，初始朝东',
                 '每步前进一格；下一步会出界就先 ==逆时针转 90 度== 再走',
                 '`num` 最大 `10^5`、最多 `10^4` 次操作，不能一步步模拟',
                 '示例：`Robot(6, 3)` 走 4、5 步 → `[3,2]` 朝 `West`'],
        quote='注意到题目中的机器人只会贴着网格的边走，因此走完一圈的步数就固定下来了，为(width + height - 2) * 2，那么对于每次行走操作，可以先让num对这个值取模。',
        quote_src='—— yiduobo 题解原文',
        idea=['机器人只走外圈，一圈固定 `(w+h-2)*2` 步',
              '`step` 里先按当前方向，把 `num` 加上机器人已离起点的圈上距离',
              '再取模，按余数落在哪段判断新坐标，最后由坐标反推朝向',
              '拐角处朝向不变：所以朝向是看坐标不看余数'],
        summary=['时间 `O(1)`，空间 `O(1)`；每次只保存 `x, y, d`',
                 '易错：拐角朝向 —— 右下角仍朝东，右上角仍朝北，左上角仍朝西；回到 `(0,0)` 时朝南',
                 '起点 `(0,0)` 初始朝东，但走满一圈回来是朝南，所以 `d` 要靠坐标重新判断',
                 '代码与原文一致，只保留了 Python 3 可运行的写法'],
    ),
)
