D1, D2, C1, C2 = 2, 4, 8, 2


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x = S.get('x')
    cv.text((x0 + 18, y0 + 4), '1 ~ x 的每个数归哪边（蓝 = 只能进 arr1，橙 = 只能进 arr2，绿 = 两边都行，灰 = 都不行）', 20, T['muted'], bold=True)
    if x is None or 'l' not in S:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '二分猜答案 x：前 x 个正整数够不够分？', 30, T['dim'], anchor='mm', bold=True)
        return
    d1, d2, l = S['d1'], S['d2'], S['l']
    n = max(x, 1)
    cell = min(64, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = y0 + 70
    for v in range(1, x + 1):
        a, b = v % d1 == 0, v % d2 == 0
        if a and b:
            fill, tc = T['panel2'], T['dim']
        elif b:
            fill, tc = T['blue'], T['bg']
        elif a:
            fill, tc = T['orange'], T['bg']
        else:
            fill, tc = T['green'], T['bg']
        X = sx + (v - 1) * cell
        cv.rect((X + 2, ys, X + cell - 2, ys + cell - 4), fill=fill, r=6, outline=T['border'])
        cv.text((X + cell / 2, ys + cell / 2 - 2), v, int(min(26, cell * 0.45)), tc, anchor='mm', bold=True)
    cv.text((x0 + 20, ys + cell + 24), f'x = {x}', 26, T['yellow'], bold=True)
    if 'common' in S:
        c1 = x // d2 - x // l
        c2 = x // d1 - x // l
        ly = ys + cell + 70
        cv.text((x0 + 20, ly), f'arr1 独享（只被 d2 整除）：{c1} 个', 24, T['blue'], bold=True)
        cv.text((x0 + 20, ly + 40), f'arr2 独享（只被 d1 整除）：{c2} 个', 24, T['orange'], bold=True)
        cv.text((x0 + 20, ly + 80), f'共享（都不整除）：{S["common"]} 个', 24, T['green'], bold=True)
        if 'left2' in S:
            ok = S['common'] >= S['left1'] + S['left2']
            cv.text((x0 + 20, ly + 130), f'arr1 还缺 {S["left1"]}，arr2 还缺 {S["left2"]}：共享 {S["common"]} {">=" if ok else "<"} {S["left1"] + S["left2"]}', 26,
                    T['green'] if ok else T['red'], bold=True)


CONFIG = dict(
    num=2513, title='最小化两个数组中的最大值', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 容斥原理',
    tags=['数学算法', '难度分 2302'],
    setup='from math import lcm',
    code='''
class Solution:
    def minimizeSet(self, d1: int, d2: int, uniqueCnt1: int, uniqueCnt2: int) -> int:
        l = lcm(d1, d2)
        def check(x: int) -> bool:
            left1 = max(uniqueCnt1 - x // d2 + x // l, 0)
            left2 = max(uniqueCnt2 - x // d1 + x // l, 0)
            common = x - x // d1 - x // d2 + x // l
            return common >= left1 + left2
        return bisect_left(range((uniqueCnt1 + uniqueCnt2) * 2 - 1), True, key=check)
''',
    call=f'Solution().minimizeSet({D1}, {D2}, {C1}, {C2})',
    expect=15,
    views=[
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('x', 'x', 'yellow'), ('l', 'l'), ('left1', 'left1', 'blue'), ('left2', 'left2', 'pink'), ('common', 'common', 'green')],
    captions={
        'l = lcm(d1, d2)': '`LCM = lcm({d1}, {d2}) = {l}`：容斥要用，同时被两个数整除的数不能放进任何数组',
        'left1 = max': '`arr1` 还缺多少：先拿独享的 `x//d2 − x//l = {x // d2 - x // l}` 个，缺 `max({uniqueCnt1} − {x // d2 - x // l}, 0) = {left1}`',
        'left2 = max': '`arr2` 还缺多少：独享 `x//d1 − x//l = {x // d1 - x // l}` 个，缺 `max({uniqueCnt2} − {x // d1 - x // l}, 0) = {left2}`',
        'common = x': '共享的数（容斥）：`{x} − {x // d1} − {x // d2} + {x // l} = {common}`',
        'return common >= left1 + left2': '共享 `{common}` {">=" if ret else "<"} 缺口 `{left1} + {left2} = {left1 + left2}` → x = {x} ==`{ret}`==：{"够分，答案 <= x" if ret else "不够分，答案 > x"}',
        'return bisect_left': '二分猜 x：`bisect_left` 在 `[0, {(uniqueCnt1 + uniqueCnt2) * 2 - 2}]` 里找第一个让 `check(x)` 为真的 x；每猜一个 x 就跑一遍 `check`',
    },
    max_steps=100,
    cards=dict(
        one_liner='二分最大数 x，用容斥算：独享的先放，缺的从共享里补',
        complexity='时间 `O(log(d) + log(cnt))`，空间 `O(1)`',
        problem=['往 `arr1` 放 `uniqueCnt1` 个、`arr2` 放 `uniqueCnt2` 个正整数',
                 '`arr1` 的数不能被 `divisor1` 整除，`arr2` 的不能被 `divisor2` 整除，两个数组不重复',
                 '求两数组里==最大元素的最小值==',
                 '示例：`divisor1 = 2, divisor2 = 4, uniqueCnt1 = 8, uniqueCnt2 = 2` → `15`'],
        quote='最大元素越大，约束条件越宽松，越能够满足要求；最大元素越小，约束条件越严苛，越不能满足要求。看到「最小化最大值」就要先尝试二分答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['1~x 分三类：只能进 arr1、只能进 arr2、两边都行（还有同时被整除的，谁也不能进）',
              '==独享的先用掉==，缺口只能由共享的数补',
              '判定：`common >= left1 + left2`，用容斥算出各类个数'],
        summary=['时间 `O(log d + log cnt)`，空间 `O(1)`',
                 '二分上界：`d1 = d2 = 2` 时只能取奇数，所以是 `(cnt1 + cnt2) * 2 - 1`',
                 '易错：独享个数不够时缺口是 `max(.., 0)`，富余不能抵别人的缺口',
                 '`lcm` 为 Python 3.9+ 的 `math.lcm`，视频里已在 setup 中导入',
                 '另一种写法：公式 `max(f(c1,d1), f(c2,d2), f(c1+c2,lcm))`，`f(cnt,d) = cnt + (cnt-1)//(d-1)`'],
    ),
)
