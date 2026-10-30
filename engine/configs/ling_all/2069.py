W, H = 6, 3
DIRS = ['East', 'North', 'West', 'South']


def _state(S):
    """按灵神的分类讨论，从总步数 s 算出 (x, y, 方向下标)；只用于画图。"""
    w, h, s = S.get('self.w'), S.get('self.h'), S.get('self.s')
    if w is None or s is None:
        return None
    if s < w:
        return s, 0, 0
    if s < w + h - 1:
        return w - 1, s - w + 1, 1
    if s < w * 2 + h - 2:
        return w * 2 + h - s - 3, h - 1, 2
    return 0, (w + h) * 2 - s - 4, 3


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '网格图（左下角 (0,0)；亮格 = 最外圈，机器人只会在外圈上走）', 24, T['muted'], bold=True)
    w, h = S.get('self.w', W), S.get('self.h', H)
    st = _state(S)
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
    author='灵茶山艾府', technique='只走外圈 · 总步数取模',
    tags=[],
    code='''
class Robot:
    def __init__(self, width: int, height: int) -> None:
        self.w = width
        self.h = height
        self.s = 0

    def step(self, num: int) -> None:
        # 由于机器人只能走外圈，那么走 (w+h-2)*2 步后会回到起点
        # 把 s 取模调整到 [1, (w+h-2)*2]，这样不需要特判 s == 0 时的方向
        self.s = (self.s + num - 1) % ((self.w + self.h - 2) * 2) + 1

    def _getState(self) -> Tuple[int, int, str]:
        w, h, s = self.w, self.h, self.s
        if s < w:
            return s, 0, "East"
        if s < w + h - 1:
            return w - 1, s - w + 1, "North"
        if s < w * 2 + h - 2:
            return w * 2 + h - s - 3, h - 1, "West"
        return 0, (w + h) * 2 - s - 4, "South"

    def getPos(self) -> List[int]:
        x, y, _ = self._getState()
        return [x, y]

    def getDir(self) -> str:
        return self._getState()[2]
''',
    setup='',
    call=f'''r = Robot({W}, {H})
out = []
r.step(2)
r.step(2)
out.append(r.getPos())
out.append(r.getDir())
r.step(2)
r.step(1)
r.step(4)
out.append(r.getPos())
out.append(r.getDir())
out''',
    expect=[[4, 0], 'East', [1, 2], 'West'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"总步数 `s = {S['self.s']}`（取模后落在 [1, {2 * (S['self.w'] + S['self.h'] - 2)}]）" if 'self.s' in S else ''),
    ],
    watch=[('w', 'self.w'), ('h', 'self.h'), ('s', 'self.s', 'blue'), ('num', 'num', 'orange')],
    captions={
        'self.s = 0': '只记一个量：走过的 ==总步数 s==（不记坐标）；初始 `s = 0`',
        'self.s = (self.s': lambda S, B, r: (f'`s = ({B["self.s"]} + {S.num} − 1) % {2 * (S["self.w"] + S["self.h"] - 2)} + 1 = {S["self.s"]}`'
                                            f'：转满一圈回到起点，所以对 `{2 * (S["self.w"] + S["self.h"] - 2)}` 取模，不必一步步走'),
        'w, h, s = self.w': '取出 `w = {w}`，`h = {h}`，`s = {s}`，按 s 落在哪一段来分类',
        'if s < w:': lambda S, B, r: (f'`s = {S.s} < w = {S.w}` → 还在底边，只往东走了 `s` 步' if S.s < S.w
                                      else f'`s = {S.s} ≥ w = {S.w}` → 已经拐过右下角，不在底边'),
        'return s, 0': '底边：位置 `({s}, 0)`，面朝 ==East==',
        'if s < w + h - 1': lambda S, B, r: (f'`s = {S.s} < w+h-1 = {S.w + S.h - 1}` → 在右边那条竖边，面朝北'
                                             if S.s < S.w + S.h - 1 else f'`s = {S.s} ≥ {S.w + S.h - 1}` → 已经拐过右上角'),
        'return w - 1, s - w + 1': '右边：先走 `w-1` 步，再往北 `s-(w-1)` 步 → `({w - 1}, {s - w + 1})`，面朝 ==North==',
        'if s < w * 2 + h - 2': lambda S, B, r: (f'`s = {S.s} < 2w+h-2 = {S.w * 2 + S.h - 2}` → 在顶边，面朝西'
                                                 if S.s < S.w * 2 + S.h - 2 else f'`s = {S.s} ≥ {S.w * 2 + S.h - 2}` → 只剩左边那条竖边了'),
        'return w * 2 + h - s - 3': '顶边：从右上角往西走 → `({w * 2 + h - s - 3}, {h - 1})`，面朝 ==West==',
        'return 0, (w + h) * 2 - s - 4': '左边：从左上角往南走 → `(0, {(w + h) * 2 - s - 4})`，面朝 ==South==',
        'x, y, _ = self._getState()': '调用 `_getState()` 由 `s` 直接算出位置',
        'return [x, y]': '返回位置 `[{x}, {y}]`',
        'return self._getState()[2]': '`getDir` 同样调用 `_getState()`，只取下标 2 的方向',
    },
    cards=dict(
        one_liner='机器人只走外圈：记总步数 s，取模后按边分类算位置',
        complexity='`step`、`getPos`、`getDir` 均为 `O(1)`，空间 `O(1)`',
        problem=['`w × h` 网格，机器人从 `(0,0)` 出发，初始朝东',
                 '每步前进一格；下一步会出界就先 ==逆时针转 90 度== 再走',
                 '实现 `step(num)`、`getPos()`、`getDir()`，`num` 最大 `10^5`，不能一步步模拟',
                 '示例：`Robot(6, 3)` 走 2、2 步 → `[4,0]` 朝 `East`'],
        quote='根据题意，机器人只能在网格图的最外圈中移动，移动一整圈需要 2(w+h-2) 步。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只存总步数 `s`，对一圈步数取模，位置由 `s` 落在哪条边决定',
              '分四段：底边朝东、右边朝北、顶边朝西、左边朝南',
              '把取模范围调成 `[1, 2(w+h-2)]`：整圈的倍数落在左边（朝南），==不用特判 s = 0=='],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：总步数为 0 时朝东，走满整圈的正整数倍时却朝南（拐角处方向不变，下一步才转）',
                 '`(s + num - 1) % 周长 + 1` 把范围从 `[0, 周长-1]` 挪到 `[1, 周长]`',
                 '拐角属于哪一段要靠 `<` 的边界：右下角 `s = w-1` 仍归底边'],
    ),
)
