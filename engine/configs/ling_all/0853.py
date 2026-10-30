TARGET = 12
POS = [10, 8, 0, 5, 3]
SPD = [2, 4, 1, 1, 3]
CARS = sorted(zip(POS, SPD))
L_FOR, L_T, L_WHILE, L_POP, L_APP, L_RET = 4, 5, 6, 7, 8, 9


def _cur(S):
    if 'p' not in S:
        return None
    return CARS.index((S['p'], S['v']))


def _ids(S, fin=False):
    """stack of car indices consistent with S['st']; plus set of merged cars"""
    cur = _cur(S)
    if cur is None:
        return [], set(), None
    st, merged = [], set()
    for i in range(cur):
        p, v = CARS[i]
        t = (TARGET - p) / v
        while st and (TARGET - CARS[st[-1]][0]) / CARS[st[-1]][1] <= t:
            merged.add(st.pop())
        st.append(i)
    n = len(S.get('st') or [])
    done = fin or S.get('_line') in (L_APP, L_RET)
    while len(st) > n - (1 if done else 0):
        merged.add(st.pop())
    if done:
        st.append(cur)
    return st, merged, cur


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '单行道（按位置排序；紫 = 栈里的车，灰 = 已被合并删除，蓝 = 当前车）', 24, T['muted'], bold=True)
    lx0, lx1 = x0 + 60, x1 - 90
    Y = (y0 + y1) / 2 - 10
    sc = (lx1 - lx0) / TARGET
    cv.line([(lx0, Y), (lx1, Y)], T['border'], 4)
    for u in range(TARGET + 1):
        cv.line([(lx0 + u * sc, Y - 6), (lx0 + u * sc, Y + 6)], T['border'], 2)
        cv.text((lx0 + u * sc, Y + 12), u, 16, T['dim'], anchor='mt', mono=True)
    cv.text((lx1 + 10, Y - 20), '终点', 22, T['green'], anchor='lm', bold=True)
    cv.line([(lx1, Y - 40), (lx1, Y + 10)], T['green'], 4)
    st, merged, cur = _ids(S, S.get('_line') == L_FOR and 'p' in B and B.get('p') == S.get('p'))
    for i, (p, v) in enumerate(CARS):
        X = lx0 + p * sc
        t = (TARGET - p) / v
        if cur is not None and i == cur:
            c = T['blue']
        elif i in st:
            c = T['purple']
        elif i in merged:
            c = (80, 86, 96)
        else:
            c = T['panel2']
        cv.rect((X - 26, Y - 50, X + 26, Y - 14), fill=c, outline=T['muted'], width=2, r=8)
        cv.text((X, Y - 32), f'v{v}', 20, T['text'], anchor='mm', bold=True)
        lab = f't={t:g}'
        cv.text((X, Y + 44), lab, 22, T['yellow'] if (cur is not None and (i < cur or (i == cur and S.get('_line') != L_FOR) or S.get('_line') == L_RET)) else T['dim'], anchor='mt', bold=True)
        if i in merged:
            cv.text((X, Y + 74), '已合并', 18, T['muted'], anchor='mt')


def _while(S, B, ret):
    st = S.st
    if st and st[-1] <= S.t:
        return f'栈顶用时 `{st[-1]:g} ≤ t = {S.t:g}`：左边的栈顶车==能追上==当前车 → 合并（删掉栈顶）'
    if st:
        return f'栈顶用时 `{st[-1]:g} > t = {S.t:g}`：追不上当前车，停止弹栈'
    return '栈为空，停止弹栈'


CONFIG = dict(
    num=853, title='车队', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='算用时 + 正序遍历栈',
    tags=['labuladong', '灵神核心路线', '难度分 1678'],
    code='''
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        st = []
        for p, v in sorted(zip(position, speed)):
            t = (target - p) / v
            while st and st[-1] <= t:
                st.pop()  # 栈顶车追上当前车，与当前车合并（删除栈顶车）
            st.append(t)
        return len(st)
''',
    call=f'Solution().carFleet({TARGET}, {POS}, {SPD})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='stack', var='st', label='st（每辆车到终点的用时，栈底 → 栈顶严格递减）', fmt=lambda x: f'{x:g}', h=110),
    ],
    watch=[('p', 'p', 'blue'), ('v', 'v', 'blue'), ('t', lambda S: (int(S['t']) if S['t'] == int(S['t']) else round(S['t'], 2)) if 't' in S else '', 'yellow'),
           ('len(st)', lambda S: len(S['st']) if 'st' in S else '', 'green')],
    captions={
        'st = []': '栈里存==遍历过的车到终点的用时==',
        'for p, v in sorted': lambda S, B, r: ('所有车都遍历完了' if B.get('p') == S.p
                                                else f'按位置从左到右：当前车位置 `p = {S.p}`，速度 `v = {S.v}`'),
        't = (target - p) / v': lambda S, B, r: (f'用时 `t = ({S.target} − {S.p}) / {S.v}` = =={S.t:g}=='
                                                 + ('：==关键不是速度，是用时==' if 'st' in S and not S.st else '')),
        'while st and st[-1] <= t': _while,
        'st.pop()': '删掉用时 `{B.st[-1]:g}` 的车：它会在终点前追上当前车，跟着慢车走',
        'st.append(t)': '当前车（用时 `{t:g}`）入栈',
        'return len(st)': '栈中用时严格递减，谁也追不上右边的车 → 车队数 = 栈大小 =={ret}==',
    },
    cards=dict(
        one_liner='比用时不比速度：左边的车用时 ≤ 右边就会被合并',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['单行道上 n 辆车开往 `target`，车不能超车，追上就以慢车速度同行',
                 '并排行驶的车算一个车队（在终点追上也算），求到达终点的车队数',
                 '示例：`target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3]` → `3`'],
        quote='计算每辆车开到 target 的用时。只要比右边的车更早（或者同时）到达 target，那么就能与右边的车组成一个车队（合并）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合并时右边的车更慢 → 相当于==删除左边的车==',
              '按位置排序后从左到右遍历，栈顶用时 `≤ t` 就弹出',
              '最后栈中用时严格递减，每辆都追不上右边 → 答案 = 栈大小'],
        summary=['时间 `O(n log n)`，瓶颈在排序；每辆车至多入栈出栈一次',
                 '易错：`<=` 不能写成 `<`，同时到达终点也算同一车队',
                 '写法二：把 `a/b ≤ c/d` 改成 `a·d ≤ c·b`，避免浮点误差',
                 '方法二：按位置倒序遍历，维护最大用时 `max_t`，`t > max_t` 时答案加一'],
    ),
)
