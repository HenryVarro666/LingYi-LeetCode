TARGET = 12
POS = [10, 8, 0, 5, 3]
SPD = [2, 4, 1, 1, 3]
INFO = sorted(zip(POS, SPD), key=lambda d: -d[0])


def _groups():
    g, now, res = [0] * len(INFO), 0, 0
    while now < len(INFO):
        res += 1
        d0, v0 = TARGET - INFO[now][0], INFO[now][1]
        g[now] = res
        while now + 1 < len(INFO):
            d1, v1 = TARGET - INFO[now + 1][0], INFO[now + 1][1]
            if d0 * v1 < d1 * v0:
                break
            now += 1
            g[now] = res
        now += 1
    return g


GROUP = _groups()
FLEET_C = ['orange', 'cyan', 'pink', 'green', 'purple']


def _leader(S):
    if 'now_dis' not in S:
        return None
    return [i for i, (p, v) in enumerate(INFO) if TARGET - p == S['now_dis']][0]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '按位置从大到小处理（同色 = 同一车队，★ = 领头车，蓝框 = 正在判断的车）', 24, T['muted'], bold=True)
    lx0, lx1 = x0 + 60, x1 - 90
    Y = (y0 + y1) / 2 - 10
    sc = (lx1 - lx0) / TARGET
    cv.line([(lx0, Y), (lx1, Y)], T['border'], 4)
    for u in range(TARGET + 1):
        cv.line([(lx0 + u * sc, Y - 6), (lx0 + u * sc, Y + 6)], T['border'], 2)
        cv.text((lx0 + u * sc, Y + 12), u, 16, T['dim'], anchor='mt', mono=True)
    cv.text((lx1 + 10, Y - 20), '终点', 22, T['green'], anchor='lm', bold=True)
    cv.line([(lx1, Y - 40), (lx1, Y + 10)], T['green'], 4)
    now = S.get('now')
    lead = _leader(S)
    ln = S.get('_line')
    cand = now + 1 if (now is not None and 'next_dis' in S and ln in (12, 13, 14, 15)) else None
    fin = ln == 20
    for i, (p, v) in enumerate(INFO):
        X = lx0 + p * sc
        assigned = fin or (now is not None and lead is not None and (i <= now or i == lead))
        c = T[FLEET_C[(GROUP[i] - 1) % len(FLEET_C)]] if assigned else T['panel2']
        cv.rect((X - 26, Y - 50, X + 26, Y - 14), fill=c, outline=T['blue'] if i == cand else T['muted'],
                width=5 if i == cand else 2, r=8)
        cv.text((X, Y - 32), f'v{v}', 20, T['bg'] if assigned else T['text'], anchor='mm', bold=True)
        if i == lead and not fin:
            cv.text((X, Y - 58), '★', 26, T['yellow'], anchor='mb', bold=True)
        cv.text((X, Y + 44), f'距{TARGET - p}', 20, T['muted'], anchor='mt')


def _cmp(S):
    if 'next_dis' not in S or S.get('_line') not in (13, 14, 15, 16):
        if 'now_dis' in S:
            return f"领头车：距离 `{S['now_dis']}`，速度 `{S['now_v']}`，用时 `t = {S['now_dis']}/{S['now_v']}`"
        return '先按位置从大到小排序'
    a = S['now_dis'] * S['next_v']
    b = S['next_dis'] * S['now_v']
    return (f"`now_dis×next_v = {S['now_dis']}×{S['next_v']} = {a}` " + ('<' if a < b else '≥')
            + f" `next_dis×now_v = {S['next_dis']}×{S['now_v']} = {b}`")


def _if(S, B, ret):
    a = S.now_dis * S.next_v
    b = S.next_dis * S.now_v
    if a < b:
        return f'`{a} < {b}`：时间 t 内到不了终点 → ==追不上==，它将是新车队的领头车'
    return f'`{a} ≥ {b}`：时间 t 内能到终点 → ==追得上==，并入当前车队'


CONFIG = dict(
    num=853, title='车队', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序 + 领头车分组（交叉相乘）',
    tags=['labuladong', '灵神核心路线', '难度分 1678'],
    code='''
class Solution(object):
    def carFleet(self, target, position, speed):

        sorted_info = sorted(zip(position, speed), key=lambda d:-d[0])
        now = 0
        res = 0
        while now < len(position):
            res += 1
            now_dis = target - sorted_info[now][0]
            now_v = sorted_info[now][1]
            while now + 1 < len(position):
                next_dis = target - sorted_info[now + 1][0]
                next_v = sorted_info[now + 1][1]
                if now_dis * next_v < next_dis * now_v:
                    break
                now += 1

            now += 1

        return res
''',
    call=f'Solution().carFleet({TARGET}, {POS}, {SPD})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_cmp, size=26, h=80),
    ],
    watch=[('now', 'now', 'blue'), ('now_dis', 'now_dis', 'orange'), ('now_v', 'now_v', 'orange'),
           ('next_dis', 'next_dis', 'cyan'), ('next_v', 'next_v', 'cyan'), ('res', 'res', 'green')],
    captions={
        'sorted_info = sorted': '按位置==从大到小==排序：`{sorted_info}`，最靠前的车必是领头车',
        'now = 0': '`now` 指向当前处理到的车',
        'res = 0': '`res` 统计车队数',
        'while now < len(position)': lambda S, B, r: (f'第 `{S.now}` 辆车还没归队 → 它是==新车队的领头车=='
                                                      if S.now < len(S.position) else '所有车都已归队，结束'),
        'res += 1': '车队数 +1 → `res = {res}`',
        'now_v = sorted_info': '领头车（位置 `{sorted_info[now][0]}`）距终点 `{now_dis}`，速度 `{now_v}` → 用时 `t = {now_dis}/{now_v}`',
        'while now + 1 < len(position)': lambda S, B, r: ('看下一辆车能不能追上这个车队'
                                                          if S.now + 1 < len(S.position) else '后面没有车了'),
        'next_v = sorted_info': '下一辆车位置 `{sorted_info[now + 1][0]}`：距终点 `{next_dis}`，速度 `{next_v}`',
        'if now_dis * next_v < next_dis * now_v': _if,
        'break': '跳出内层循环，开始新车队',
        '                now += 1': '它属于当前车队，`now` → {now}',
        '            now += 1': '`now` → {now}：指向下一个车队的领头车',
        'return res': '一共 =={res}== 个车队',
    },
    skip=['now_dis = target', 'next_dis = target'],
    cards=dict(
        one_liner='最前面的车领头；后车在领头车用时内能到终点就归队，否则另起一队',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['单行道上 n 辆车开往 `target`，车不能超车，追上就以慢车速度同行',
                 '并排行驶的车算一个车队（在终点追上也算），求到达终点的车队数',
                 '示例：`target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3]` → `3`'],
        quote='若该车在有限时间内可以追上前车，那么该车就属于前车的车队，否则该车就是一个新车队的领头车辆。',
        quote_src='—— yiduobo 题解原文',
        idea=['位置最靠前的车必然是某个车队的领头车',
              '领头车到终点用时 `t`：后车在 `t` 内能到终点 → 归入该车队',
              '比较 `now_dis/now_v` 与 `next_dis/next_v`：==交叉相乘==避免浮点'],
        summary=['时间 `O(n log n)`，排序后每辆车只看一次',
                 '一直和==领头车==比较，而不是和前一辆车比：车队速度由领头车决定',
                 '`<` 才另起一队：恰好在终点追上也算同一车队',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神正序遍历用栈删车，这里倒序按领头车分组'],
    ),
)
