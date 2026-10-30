SETUP = '''
class Street:
    def __init__(self, doors):
        self.doors = list(doors)
        self.pos = 0
    def isDoorOpen(self):
        return self.doors[self.pos]
    def closeDoor(self):
        self.doors[self.pos] = False
    def openDoor(self):
        self.doors[self.pos] = True
    def moveRight(self):
        self.pos = (self.pos + 1) % len(self.doors)
    def moveLeft(self):
        self.pos = (self.pos - 1) % len(self.doors)
'''


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    st = S.get('s')
    cv.text((x0 + 18, y0 + 4), '环形街道（绿 = 门开着，灰 = 门关着，粉框 = 当前所在的房子）', 22, T['muted'], bold=True)
    if st is None:
        return
    n = len(st.doors)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 20
    R = min(x1 - x0 - 160, y1 - y0 - 150) / 2
    cv.text((cx, cy), f"共 {n} 座房子（程序并不知道）", 22, T['dim'], anchor='mm')
    pts = []
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for k in range(n):
        px, py = pts[k]
        qx, qy = pts[(k + 1) % n]
        cv.arrow((px, py), (qx, qy), T['border'], 3, 10) if False else cv.line([(px, py), (qx, qy)], T['border'], 3)
    for k, (px, py) in enumerate(pts):
        opened = st.doors[k]
        cv.rect((px - 36, py - 36, px + 36, py + 36), fill=T['green'] if opened else T['panel2'], outline=T['pink'] if k == st.pos else T['border'],
                width=6 if k == st.pos else 2, r=12)
        cv.text((px, py), '开' if opened else '关', 30, T['bg'] if opened else T['dim'], anchor='mm', bold=True)
        if k == st.pos:
            ang = -math.pi / 2 + 2 * math.pi * k / n
            tx, ty = px + 95 * math.cos(ang), py + 70 * math.sin(ang)
            cv.text((tx, ty), '你在这', 22, T['pink'], anchor='mm', bold=True)



CONFIG = dict(
    num=2753, title='计算一个环形街道上的房屋数量 II', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='找到开着的门 · 关门计步',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def houseCount(self, s: Optional['Street'], k: int) -> int:
        while not s.isDoorOpen():
            s.moveRight()
        for i in range(1, k + 1):
            s.moveRight()
            if s.isDoorOpen():
                ans = i
                s.closeDoor()
        return ans
''',
    setup=SETUP,
    call='Solution().houseCount(Street([False, True, False, True, True]), 7)',
    expect=5,
    max_steps=100,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k', 'orange'), ('ans', 'ans', 'green'), ('当前门', 's.doors[s.pos]', 'pink')],
    captions={
        'while not s.isDoorOpen()': lambda S, B, r: ('门关着 → 继续向右找开着的门' if not S.s.doors[S.s.pos] else '找到一扇开着的门：它是==整条街的参照点==，从它右边开始数'),
        4: '门关着，向右移动一步，继续找',
        6: '向右走一步：`i = {i}`，来到下一座房子',
        'for i in range': lambda S, B, r: (f'向右第 `{S.i}` 步（最多 `k = {S.k}` 步，房子数不超过 k，保证走满一圈）' if S.get('i') != B.get('i') else f'走满 `{S.k}` 步，结束'),
        'if s.isDoorOpen()': lambda S, B, r: ('门开着 → 这是目前遇到的最后一扇开着的门，记下步数' if S.s.doors[S.s.pos] else '门关着，继续走'),
        'ans = i': '`ans = {ans}`：走了 `{i}` 步才遇到开着的门',
        's.closeDoor()': '把这扇门关上：下次再经过就不会当成新的开门了',
        'return ans': '最后一次遇到开着的门，正是绕回==参照点==：房子数 `{ret}`',
    },
    cards=dict(
        one_liner='参照点是整圈里最后被碰到的开着的门：最后一次遇到它时的步数就是房子数',
        complexity='时间 `O(k)`，空间 `O(1)`',
        problem=['环形街道，每座房子的门开或关，只能 `moveRight / isDoorOpen / closeDoor`（无法开门、无法向左）',
                 '房子数不超过 `k`，求房子数量',
                 '本视频：5 座房子，门 `关 开 关 开 开`，`k = 7`'],
        quote='不断向右找到一扇开着的门。跳过这扇门，继续向右。每向右一步，计数器 i 就加一。循环至多 k 次。如果遇到开着的门，就把门关上。答案为最后一次遇到的开着的门的 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先停在一扇开着的门前，这扇门不关，当作参照点',
              '向右走 `k` 步，沿途遇到开着的门就记 `ans = i` 并关上',
              '关了的门不会再被记；只有参照点绕一圈回来时才会再被遇到',
              '所以最后一次记下的 `i` 就是绕一圈的步数'],
        summary=['时间 `O(k)`，空间 `O(1)`；循环次数不超过 `2k`',
                 '参照点那扇门一直开着，直到绕回来才被关上',
                 '`for` 从 1 开始：先走一步再判断，`i` 就是已走步数',
                 '原文已是 Python 3 可运行，未做改动；Street 类在 setup 中定义'],
    ),
)
