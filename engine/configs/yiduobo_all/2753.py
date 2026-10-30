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
    num=2753, title='计算一个环形街道上的房屋数量 II', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='开着的门当标记 · 从其右侧起数',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def houseCount(self, street, k):

        while not street.isDoorOpen():
            street.moveRight()
        
        street.moveRight()
        res = None
        for index in range(1, k + 1):
            if street.isDoorOpen():
                res = index
                street.closeDoor()
            
            street.moveRight()

        return res
''',
    setup=SETUP,
    call='Solution().houseCount(Street([False, True, False, True, True]), 7)',
    expect=5,
    max_steps=100,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('index', 'index', 'blue'), ('k', 'k', 'orange'), ('res', 'res', 'green'), ('当前门', 'street.doors[street.pos]', 'pink')],
    captions={
        'while not street.isDoorOpen()': lambda S, B, r: ('门关着 → 向右走，找一扇开着的门' if not S.street.doors[S.street.pos] else '找到开着的门：这扇门作==标记==，后面它是一轮中最后被访问到的开门'),
        5: '门关着，向右走一步，继续找',
        7: '先向右走一步，站到标记门的右侧：现在==数的起点就是标记门右边那座==',
        14: '无论门开关，都向右走一步',
        'res = None': '`res` 记录最后一次关门时走过的步数',
        'for index in range': lambda S, B, r: (f'第 `{S.index}` 步（最多 `k = {S.k}` 步，走满后至少绕了一圈）' if S.get('index') != B.get('index') else f'走满 `{S.k}` 步，结束'),
        'if street.isDoorOpen()': lambda S, B, r: ('当前门开着 → 记下步数，再关掉' if S.street.doors[S.street.pos] else '当前门关着，什么也不做'),
        'res = index': '`res = {res}`：从标记门右侧出发，走了 `{index}` 座房子（含当前）',
        'street.closeDoor()': '关门：这座房子不会再被当成标记',
        'return res': '最后关的那扇门就是最初的标记门，步数 `{ret}` 就是房子数',
    },
    cards=dict(
        one_liner='开着的门当标记：从它右边出发，最后一次关门的步数就是房子数',
        complexity='时间 `O(k)`，空间 `O(1)`',
        problem=['环形街道，每座房子的门开或关，只能 `moveRight / isDoorOpen / closeDoor`',
                 '房子数不超过 `k`，求房子数量（前一题的加强版：没有开门、没有向左走）',
                 '本视频：5 座房子，门 `关 开 关 开 开`，`k = 7`'],
        quote='对于一扇开着的门，如果从这扇门右侧开始向右走，那么这扇门将是一轮遍历中最后一扇被访问到的开着的门，在这里就可以利用这一点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一直向右走，直到遇到开着的门，把它当作标记',
              '从标记右侧的门开始走，路上遇到开着的门就关上并记下步数',
              '走 `k` 步后至少绕了一圈，最后关的那扇就是标记门',
              '所以最后一次记下的步数就是从标记右侧走到它的步数，即房子数'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '先 `moveRight` 再进循环：循环里第 `index` 步才对应第 `index` 座房子',
                 '循环内先判断再 `moveRight`，所以 `index` 恰好等于站在当前门前时已数的房子数',
                 '原文已是 Python 3 可运行，未做改动；Street 类在 setup 中定义',
                 '对比灵神：灵神停在标记门上先走再判断；这里先越过标记门，再先判断后走'],
    ),
)
