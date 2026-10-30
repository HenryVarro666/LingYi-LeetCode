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
    st = S.get('street')
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
    num=2728, title='计算一个环形街道上的房屋数量', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='先关全部门，再数到开着的门',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def houseCount(self, street, k):

        for i in range(k):
            if street.isDoorOpen():
                street.closeDoor()
            street.moveRight()
        
        street.openDoor()
        street.moveRight()
        res = 1
        while not street.isDoorOpen():
            street.moveRight()
            res += 1
        
        return res
''',
    setup=SETUP,
    call='Solution().houseCount(Street([True, False, True, True]), 6)',
    expect=4,
    max_steps=100,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k', 'orange'), ('res', 'res', 'green'), ('当前门', 'street.doors[street.pos]', 'pink')],
    captions={
        'for i in range(k)': lambda S, B, r: (f'第 `{S.i + 1}` 轮 / 共 `{S.k}` 轮：房子最多 `k` 座，走满 k 步必定绕街一圈以上' if S.get('i') != B.get('i') else f'走满了 `{S.k}` 步，每座房子都至少经过一次'),
        'if street.isDoorOpen()': lambda S, B, r: ('门是开着的 → 关上它' if S.street.doors[S.street.pos] else '门本来就是关着的，什么也不用做'),
        'street.closeDoor()': '关门：此后这座房子的门不会再开',
        7: '向右走一步，去下一座房子（不管门开关，本轮结束）',
        10: '向右走一步，离开起点：此后遇到的第一扇开着的门必是起点',
        13: '向右走一步，来到下一座房子',
        'street.openDoor()': '走完 k 步后所有门都关着。现在把当前这扇门打开，作为==起点标记==',
        'res = 1': '`res = 1`：刚才打开的这座房子算一座，然后向右走了一步',
        'while not street.isDoorOpen()': lambda S, B, r: ('门是关着的 → 还没绕回起点，继续走' if not S.street.doors[S.street.pos] else '遇到开着的门：就是起点那座，绕完一圈了'),
        'res += 1': '又经过一座房子：`res = {res}`',
        'return res': '一共 `{ret}` 座房子',
    },
    cards=dict(
        one_liner='先把所有门关上，再打开一扇做标记，绕一圈数步数',
        complexity='时间 `O(k)`，空间 `O(1)`',
        problem=['环形街道上有若干座房子，每座房子的门是开或关，你站在某座房子前',
                 '只能调用 `isDoorOpen / openDoor / closeDoor / moveRight` 操作，不知道房子总数',
                 '已知房子数不超过 `k`，求房子数量',
                 '本视频：4 座房子，门 `开 关 开 开`，`k = 6`'],
        quote='街道上的房屋数量不超过k，那么可以先向右移动k轮，并将过程中所有开着的房门都关上。',
        quote_src='—— yiduobo 题解原文',
        idea=['走 `k` 步一定绕了整条街至少一圈，把路过的开着的门全关上',
              '此时所有门都是关着的：打开当前这扇，作为起点标记',
              '再向右走，直到又遇到开着的门，说明回到起点',
              '走过的步数就是房子数'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '第一步必须走满 `k` 步：房子数未知，k 是上界，走 k 步才能保证全部门被关',
                 '`res` 从 1 开始：打开标记后先走了一步（相当于数了起点这座）',
                 '原文已是 Python 3 可运行，未做改动；Street 类在 setup 中定义'],
    ),
)
