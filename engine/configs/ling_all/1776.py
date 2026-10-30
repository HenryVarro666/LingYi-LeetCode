CARS = [[3, 4], [5, 4], [6, 3], [9, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(CARS)
    cv.text((x0 + 18, y0 + 4), '车道（蓝 = 当前车 i，粉 = 栈顶车 j，黄框 = 栈中候选）', 22, T['muted'], bold=True)
    pmin, pmax = CARS[0][0] - 1, CARS[-1][0] + 1
    W = x1 - x0 - 120
    X = lambda p: x0 + 60 + (p - pmin) / (pmax - pmin) * W
    yl = y0 + 150
    cv.line([(x0 + 40, yl + 40), (x1 - 40, yl + 40)], T['border'], 4)
    i = S.get('i')
    st = S.get('st') or []
    ans = S.get('ans') or [-1.0] * n
    top = st[-1] if st else None
    done = i if i is not None else n
    for k, (p, v) in enumerate(CARS):
        cx = X(p)
        col = T['panel2']
        if k == i:
            col = T['blue']
        elif k == top:
            col = T['pink']
        if k in st:
            cv.rect((cx - 36, yl - 6, cx + 36, yl + 66), outline=T['yellow'], width=4, r=14)
        cv.rect((cx - 30, yl, cx + 30, yl + 60), fill=col, r=12, outline=T['border'])
        cv.text((cx, yl + 30), k, 30, T['bg'] if col != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((cx, yl + 88), f'p={p}', 20, T['dim'], anchor='mt', mono=True)
        cv.text((cx, yl - 26), f'v={v}', 24, T['cyan'] if v <= 2 else T['orange'], anchor='mb', bold=True)
    # 速度箭头在车上方
    # 已算出的答案
    ya = yl + 190
    cv.text((x0 + 18, ya - 40), 'ans[k]：车 k 与下一辆车相遇的时间（-1 = 不会相遇，? = 还没算）', 22, T['muted'], bold=True)
    cw = (x1 - x0 - 80) / n
    for k in range(n):
        cx = x0 + 40 + cw * (k + 0.5)
        known = k > done or (k == done and S.get('_line') in (13, 14, 17, 18))
        v = ans[k]
        txt = '?' if not known else ('-1' if v < 0 else f'{v:g}')
        fill = T['green'] if (known and v >= 0 and k == i) else T['panel2']
        cv.rect((cx - cw * 0.4, ya, cx + cw * 0.4, ya + 70), fill=fill, r=12, outline=T['border'])
        cv.text((cx, ya + 35), txt, 32, T['bg'] if fill == T['green'] else (T['text'] if known else T['dim']), anchor='mm', bold=True, mono=True)
        cv.text((cx, ya + 78), f'ans[{k}]', 18, T['dim'], anchor='mt', mono=True)
    # 相遇时间公式
    if i is not None and S.get('q') is not None and 'w' in S and S.get('j') is not None and S['v'] > S['w']:
        t = (S['q'] - S['p']) / (S['v'] - S['w'])
        cv.text((x0 + 18, ya + 130), f"车 {i} 追车 {S['j']}：({S['q']} − {S['p']}) ÷ ({S['v']} − {S['w']}) = {t:g}", 28, T['text'], bold=True)


CONFIG = dict(
    num=1776, title='车队 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='倒着遍历 + 单调栈删掉无效相遇对象',
    tags=['灵神题单·单调栈', '灵神题单·常用数据结构', '难度分 2531'],
    code='''
class Solution:
    def getCollisionTimes(self, cars: List[List[int]]) -> List[float]:
        ans = [-1.0] * len(cars)
        st = []  # 栈底用时长，栈顶用时短
        for i in range(len(cars) - 1, -1, -1):
            p, v = cars[i]
            while st:
                j = st[-1]
                q, w = cars[j]
                if v > w:
                    t = (q - p) / (v - w)
                    if ans[j] < 0 or t <= ans[j]:  # 车 i 与车 j 相遇
                        ans[i] = t
                        break
                # 车 j 已合并（删除）
                st.pop()
            st.append(i)
        return ans
''',
    call=f'Solution().getCollisionTimes({CARS!r})',
    expect=[2.0, 1.0, 1.5, -1.0],
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('i', 'i', 'blue'), ('st', 'st', 'purple'), ('ans', 'ans', 'green')],
    max_steps=90,
    captions={
        'ans = [-1.0]': '`ans` 先全设为 `-1.0`：默认「不会相遇」',
        'st = []': '栈里存还「有效」的车下标，栈底相遇用时长、栈顶用时短',
        'p, v = cars[i]': '倒着看：当前车 `{i}`，位置 `{p}`，速度 `{v}`',
        'while st': lambda S, B, r: ('栈空：前面没有可追的车 → `ans[i]` 保持 `-1`' if not S.st else f'栈里还有车，继续找 `{S.i}` 号车能追上的目标'),
        'j = st[-1]': '取栈顶车 `j = {j}` 作为候选目标',
        'q, w = cars[j]': '车 `{j}`：位置 `{q}`，速度 `{w}`',
        'if v > w': lambda S, B, r: (f'`v = {S.v}` > `w = {S.w}`？' + ('速度更快，才可能追上' if S.v > S.w else '不快于前车，==永远追不上==，它对 i 无效 → 弹出')),
        't = (q - p)': '追及：距离 `{q - p}` ÷ 速度差 `{v - w}` = `{t}`',
        'if ans[j] < 0 or': lambda S, B, r: (
            '`ans[j] < 0`：车 j 追不上任何车，不会被合并 → 车 i 一定先追上它' if S.ans[S.j] < 0
            else (f'`t = {S.t:g}` ≤ `ans[{S.j}] = {S.ans[S.j]:g}`：i 在 j 合并之前追上 → 相遇成立' if S.t <= S.ans[S.j]
                  else f'`t = {S.t:g}` > `ans[{S.j}] = {S.ans[S.j]:g}`：j 早已并入前面的车队，==追不上它了==')),
        'ans[i] = t': '`ans[{i}] = {t:g}`',
        'break': '找到了目标，跳出循环',
        'st.pop()': '车 `{B.j}` 已合并或追不上：从栈删掉，对 `{i}` 及其左边所有车都不再有效',
        'st.append(i)': '`{i}` 入栈，成为后面（左边）的车的候选',
        'return ans': '每辆车的相遇时间 `{ans}`',
    },
    cards=dict(
        one_liner='相遇太晚的车，已经并进别的车队，从候选里删掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['单车道上 `n` 辆车同向行驶，相遇后合并成车队，速度取最慢那辆',
                 '求每辆车与下一辆车（或车队）相遇的时间，不会相遇为 `-1`',
                 '示例：`[[3,4],[5,4],[6,3],[9,1]]` → `[2,1,1.5,-1]`'],
        quote='综上，C 对于 B 及其左边的所有车来说都不再是有效的相遇对象，可以直接从候选车辆中删除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['若 `B` 与 `C` 相遇用时 > `C` 与 `D` 相遇用时，`C` 已并进 `D`，==C 作废==',
              '左边的车 `A` 要么先撞 `B`，速度变成 `B` 的 → 追不上 `C`，所以 `C` 对左边都没用',
              '倒着遍历 + 栈：速度不快、或相遇太晚的栈顶都弹出，弹完仍有车就是答案'],
        summary=['时间 `O(n)`：每辆车至多入栈、出栈一次',
                 '`v > w` 才可能追上；`t <= ans[j]` 才是「合并前相遇」（相等也算）',
                 '`ans[j] < 0` 说明 j 不会被合并，一定先追上',
                 '为避免浮点误差，可以把除法比较改成交叉相乘',
                 '同类：栈 · 邻项消除专题'],
    ),
)
