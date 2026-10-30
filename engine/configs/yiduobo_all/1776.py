CARS = [[3, 4], [5, 4], [6, 3], [9, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(CARS)
    cv.text((x0 + 18, y0 + 4), '车队（蓝 = 当前车 index，粉 = 栈顶车，黄框 = 栈中的车队）', 22, T['muted'], bold=True)
    pmin, pmax = CARS[0][0] - 1, CARS[-1][0] + 1
    W = x1 - x0 - 120
    X = lambda p: x0 + 60 + (p - pmin) / (pmax - pmin) * W
    yl = y0 + 150
    cv.line([(x0 + 40, yl + 40), (x1 - 40, yl + 40)], T['border'], 4)
    k0 = S.get('index')
    st = S.get('stack') or []
    res = S.get('res') or [-1] * n
    top = st[-1] if st else None
    done = k0 if k0 is not None else n
    for k, (p, v) in enumerate(CARS):
        cx = X(p)
        col = T['panel2']
        if k == k0:
            col = T['blue']
        elif k == top:
            col = T['pink']
        if k in st:
            cv.rect((cx - 36, yl - 6, cx + 36, yl + 66), outline=T['yellow'], width=4, r=14)
        cv.rect((cx - 30, yl, cx + 30, yl + 60), fill=col, r=12, outline=T['border'])
        cv.text((cx, yl + 30), k, 30, T['bg'] if col != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((cx, yl + 88), f'p={p}', 20, T['dim'], anchor='mt', mono=True)
        cv.text((cx, yl - 26), f'v={v}', 24, T['cyan'] if v <= 2 else T['orange'], anchor='mb', bold=True)
    ya = yl + 190
    cv.text((x0 + 18, ya - 40), 'res[k]：车 k 追上前方车队的时间（-1 = 追不上，? = 还没算）', 22, T['muted'], bold=True)
    cw = (x1 - x0 - 80) / n
    for k in range(n):
        cx = x0 + 40 + cw * (k + 0.5)
        known = k > done or (k == done and S.get('_line') in (9, 10, 15, 16, 18))
        v = res[k]
        txt = '?' if not known else ('-1' if v < 0 else f'{v:g}')
        fill = T['green'] if (known and v >= 0 and k == k0) else T['panel2']
        cv.rect((cx - cw * 0.4, ya, cx + cw * 0.4, ya + 70), fill=fill, r=12, outline=T['border'])
        cv.text((cx, ya + 35), txt, 32, T['bg'] if fill == T['green'] else (T['text'] if known else T['dim']), anchor='mm', bold=True, mono=True)
        cv.text((cx, ya + 78), f'res[{k}]', 18, T['dim'], anchor='mt', mono=True)
    if k0 is not None and len(st) > 0 and S.get('_line') in (9, 10, 11) and CARS[k0][1] > CARS[st[-1]][1]:
        t = st[-1]
        dv = CARS[k0][1] - CARS[t][1]
        dp = CARS[t][0] - CARS[k0][0]
        r = res[t]
        cv.text((x0 + 18, ya + 130), f'车 {k0} 追 {t}：距离 {dp} ÷ 速度差 {dv} = {dp / dv:g}', 28, T['text'], bold=True)
        if len(st) > 1:
            cv.text((x0 + 18, ya + 176), f'栈顶 {t} 追上更前车队用时 {r:g}；车 {k0} 在这段时间内能追近 {dv * r:g}（距离 {dp}）', 24, T['muted'])


CONFIG = dict(
    num=1776, title='车队 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='从最远车队逆推 + 单调栈',
    tags=['灵神题单·单调栈', '灵神题单·常用数据结构', '难度分 2531'],
    code='''
class Solution(object):
    def getCollisionTimes(self, cars):

        n = len(cars)
        res = [-1] * n
        stack = [n - 1]
        for index in range(n - 1, -1, -1):
            if cars[index][1] <= cars[stack[0]][1]:
                res[index] = -1
                stack = [index]
            else:
                while len(stack) > 1 and (cars[index][1] - cars[stack[-1]][1]) * res[stack[-1]] < cars[stack[-1]][0] - cars[index][0]:
                    stack.pop()
                
                res[index] = (cars[stack[-1]][0] - cars[index][0]) * 1.0 / (cars[index][1] - cars[stack[-1]][1])
                stack.append(index)
        
        return res
''',
    call=f'Solution().getCollisionTimes({CARS!r})',
    expect=[2.0, 1.0, 1.5, -1],
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'purple'), ('res', 'res', 'green')],
    max_steps=90,
    captions={
        'res = [-1]': '`res` 先全设为 `-1`：默认「追不上」',
        'stack = [n - 1]': '栈里放车队：最远的那辆先进栈；`stack[0]` 是栈底，也是==最慢的车队速度==的代表',
        'for index in range(n - 1, -1, -1)': '从最远往前逆推：后面的车不影响前面车队的相遇时间',
        'if cars[index][1] <= cars[stack[0]][1]': lambda S, B, r: (
            f'当前车速度 `{S.cars[S.index][1]}`，栈底车速度 `{S.cars[S.stack[0]][1]}`：' +
            ('不比前方最慢的快，==谁也追不上==' if S.cars[S.index][1] <= S.cars[S.stack[0]][1] else '比前方最慢的快，前面有目标可追')),
        'res[index] = -1': '`res[{index}] = -1`',
        'stack = [index]': '它成了最靠前的车队，后面的车也追不上前面的了 → 栈清空，只留 `{index}`',
        'while len(stack) > 1': lambda S, B, r: (
            '栈里只剩一个车队，直接追它' if len(S.stack) <= 1 else
            (lambda t, dv, dp, rt: f'栈顶 `{t}` 用 `{rt:g}` 秒并入更前车队；这段时间 `{S.index}` 只能追近 `{dv} × {rt:g} = {dv * rt:g}`，而距离是 `{dp}`'
             + ('，不够 → 栈顶先走了，==弹出==' if dv * rt < dp else '，够 → 保留栈顶当目标'))(
                S.stack[-1], S.cars[S.index][1] - S.cars[S.stack[-1]][1], S.cars[S.stack[-1]][0] - S.cars[S.index][0], S.res[S.stack[-1]])),
        'stack.pop()': '栈顶 `{B.stack[-1]}` 在被追上之前就并入前方车队，不用再保留',
        'res[index] = (cars': '`res[{index}] = {res[index]:g}`：距离 ÷ 速度差',
        'stack.append(index)': '`{index}` 入栈，它成为后面车的候选',
        'return res': '每辆车追上前方的时间：`{res}`',
    },
    cards=dict(
        one_liner='后面的车不影响前面，从最远的车队往回逆推',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['单车道上 `n` 辆车同向行驶，相遇后合并成车队，速度取最慢那辆',
                 '求每辆车追上前方车的时间，追不上为 `-1`',
                 '示例：`[[3,4],[5,4],[6,3],[9,1]]` → `[2,1,1.5,-1]`'],
        quote='一个车队能追上前队必须要这个车队的速度比前队的速度要快，又或者是前队融入了更前面的队伍导致速度被拉低。',
        quote_src='—— yiduobo 题解原文',
        idea=['后面的车一旦追上来就并进当前车队，不改变速度 → ==能不能追上只看前面==',
              '先判断栈顶车队：`p` 能否在它并入更前车队之前追上？速度差 × 它的用时 < 距离 → 追不上，弹出',
              '栈空或当前车比栈底还慢 → `-1`；否则用距离 ÷ 速度差算时间'],
        summary=['时间 `O(n)`，每个车队至多进、出栈一次',
                 '`stack[0]` 是栈底，速度最慢的前方车队；当前车不比它快就永远追不上',
                 '`while len(stack) > 1` 保证栈里至少留一个目标',
                 '原文已是 Python 3 兼容写法（`* 1.0` 保证浮点除法），未改动',
                 '对比灵神：灵神用除法比时间；yiduobo 用「速度差 × 用时 < 距离」判断，不用求时间'],
    ),
)
