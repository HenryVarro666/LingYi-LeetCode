def _info(S):
    if 'res' not in S or 's' not in S or 'target' not in S:
        return ''
    d = S['s'] - S['target']
    if d < 0:
        tail = '还没到终点'
    elif d % 2:
        tail = '相距奇数，反向步只能改偶数'
    else:
        tail = '相距偶数，可反向若干步恰好到达'
    return f"不回头走 res = {S['res']} 步：s = =={S['s']}==，s − target = =={d}==（{tail}）"


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'res' not in S or 's' not in S or 'target' not in S:
        return
    s, t, n = S['s'], S['target'], S['res']
    hi = max(s, t, 1)
    ax0, ax1 = x0 + 50, x1 - 120
    k = (ax1 - ax0) / hi
    y = y0 + 150
    cv.text((x0 + 18, y0 + 4), '数轴：青色 = 一路向右走到的位置 s，橙色 = 终点 target', 22, T['muted'], bold=True)
    cv.line([(ax0, y), (ax1, y)], T['border'], 3)
    pos = 0
    for step in range(1, n + 1):
        nx = pos + step
        cv.rect((ax0 + pos * k + 1, y - 34, ax0 + nx * k - 1, y - 6), fill=T['cyan'], alpha=170 if step < n else 255, r=4)
        if (nx - pos) * k > 22:
            cv.text(((ax0 + pos * k + ax0 + nx * k) / 2, y - 20), step, 18, T['bg'], anchor='mm', bold=True)
        pos = nx
    cv.tri_up(ax0 + t * k, y + 8, 12, T['orange'])
    cv.text((ax0 + t * k, y + 26), f'target = {t}', 24, T['orange'], anchor='mt', bold=True)
    cv.tri_up(ax0, y + 8, 10, T['dim'])
    cv.text((ax0, y + 26), '0', 22, T['dim'], anchor='mt', bold=True)
    if s != t:
        cv.text((ax0 + s * k, y - 44), f's = {s}', 24, T['cyan'], anchor='mb', bold=True)
    if s > t:
        cv.rect((ax0 + t * k, y + 70, ax0 + s * k, y + 100), outline=T['pink'], width=3, r=6)
        cv.text(((ax0 + t * k + ax0 + s * k) / 2, y + 112), f'越过 {s - t}', 22, T['pink'], anchor='mt', bold=True)


CONFIG = dict(
    num=754, title='到达终点数字', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='加减号 · 开根号找 n + 奇偶判断', tags=['灵神题单', '贪心与思维', '难度分 2000'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def reachNumber(self, target):

        if target < 0:
            target = -target
        res = int(sqrt(target))
        s = (1 + res) * res // 2
        while s < target:
            res += 1
            s += res
        
        delta = s - target
        if delta % 2 == 0:
            return res
        elif res % 2 == 1:
            return res + 2
        else:
            return res + 1
''',
    call='Solution().reachNumber(-5)',
    expect=5,
    views=[
        dict(type='text', fn=_info, size=30),
        dict(type='custom', h=300, draw=_draw),
    ],
    watch=['target', ('res', 'res', 'blue'), ('s', 's', 'cyan'), ('delta', 'delta', 'orange')],
    captions={
        'if target < 0': '`target < 0` 吗？-target 与 target 等价（符号全反过来）',
        'target = -target': '翻成正数：`target = {target}`',
        'res = int(sqrt': '`sqrt({target})` 取整当起点：`res = {res}`，先少走几步',
        's = (1 + res)': '`s = (1+{res})×{res} // 2 = {s}`，是 1 到 res 的和',
        'while s < target': lambda S, B, r: (f'`s = {S.s} < target = {S.target}`：还没走到 → 继续' if S.s < S.target
                                             else f'`s = {S.s} >= target = {S.target}`：够了，停'),
        'res += 1': '多走一步，`res = {res}`',
        's += res': '`s = {B.s} + {res} = {s}`',
        'delta = s - target': '`delta = {s} − {target} = {delta}`：多走出来的距离，要从 1..res 里选一些数反向',
        'if delta % 2 == 0': lambda S, B, r: (f'`delta = {S.delta}` 是偶数：反向和为 `{S.delta // 2}` 的若干步即可 → 答案 `res`' if S.delta % 2 == 0
                                              else f'`delta = {S.delta}` 是奇数：反向只能改变偶数，必须再多走'),
        'elif res % 2 == 1': lambda S, B, r: (f'`res = {S.res}` 是奇数 → 下一步 `res+1` 为偶数，delta 仍奇；`res+2` 才变偶数 → 答案 `res + 2`' if S.res % 2 == 1
                                              else f'`res = {S.res}` 是偶数 → 下一步 `res+1` 为奇数，delta 变偶数 → 答案 `res + 1`'),
        'return res + 2': '返回 `res + 2 = {ret}`',
        'return res + 1': '返回 `res + 1 = {ret}`',
    },
    cards=dict(
        one_liner='把每步看成加号或减号：走够了，再用奇偶判断多走几步',
        complexity='时间 `O(√target)`，空间 `O(1)`',
        problem=['数轴 0 处出发，第 `i` 次移动走 `i` 步，方向可左可右',
                 '求到达 `target` 的最少移动次数',
                 '本视频：`target=-5` → `5`'],
        quote='题目中描述的向左向右，可以看做对于1到n这n个数，在每个数前面添加加号或者减号，然后计算这个表达式的和，使其等于target。',
        quote_src='—— yiduobo 题解原文',
        idea=['`target` 与 `-target` 等价，取正',
              '找最小 `n` 使 `s = 1+…+n >= target`，`delta = s - target`',
              '把和为 `delta / 2` 的那些数变号即可，所以 `delta` 必须是偶数',
              '`delta` 为奇数：`n` 为奇数加 2，`n` 为偶数加 1'],
        summary=['时间 `O(√target)`（本代码用 `sqrt` 做起点，循环只补几步）',
                 '易错：`delta` 为偶数一定能凑出 `delta / 2`（数学归纳可证）',
                 '奇数时：看 `n+1` 的奇偶，奇数则 `n+1` 步 delta 变偶，偶数则要 `n+2`',
                 '原文为 Python 2 写法，`s = (1 + res) * res / 2` 的整数除法已改为 `//`；`sqrt` 来自 math，已在 setup 里 import'],
    ),
)
