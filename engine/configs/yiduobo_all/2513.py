D1, D2, C1, C2 = 2, 7, 1, 3


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '1 ~ mid 分四类（灰 = 第一类丢弃，橙 = 第二类进 arr2，蓝 = 第三类进 arr1，绿 = 第四类两边都行）', 20, T['muted'], bold=True)
    line = S.get('_line', 0)
    if 'mid' not in S or 'lcm' not in S or line < 14:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '二分答案 mid：1 ~ mid 里的数够分吗？', 30, T['dim'], anchor='mm', bold=True)
        return
    mid, d1, d2, l = S['mid'], S['divisor1'], S['divisor2'], S['lcm']
    n = max(mid, 1)
    cell = min(64, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = y0 + 70
    for v in range(1, mid + 1):
        a, b = v % d1 == 0, v % d2 == 0
        if a and b:
            fill, tc = T['panel2'], T['dim']
        elif a:
            fill, tc = T['orange'], T['bg']
        elif b:
            fill, tc = T['blue'], T['bg']
        else:
            fill, tc = T['green'], T['bg']
        X = sx + (v - 1) * cell
        cv.rect((X + 2, ys, X + cell - 2, ys + cell - 4), fill=fill, r=6, outline=T['border'])
        cv.text((X + cell / 2, ys + cell / 2 - 2), v, int(min(26, cell * 0.45)), tc, anchor='mm', bold=True)
    cv.text((x0 + 20, ys + cell + 24), f'mid = {mid}，范围 [{S["left"]}, {S["right"]}]', 26, T['yellow'], bold=True)
    ly = ys + cell + 70
    c1 = mid // d2 - mid // l
    c2 = mid // d1 - mid // l
    cv.text((x0 + 20, ly), f'第一类（同时整除，丢弃）：{mid // l} 个', 24, T['muted'], bold=True)
    cv.text((x0 + 20, ly + 38), f'第二类（只被 d1 整除，进 arr2）：{c2} 个', 24, T['orange'], bold=True)
    cv.text((x0 + 20, ly + 76), f'第三类（只被 d2 整除，进 arr1）：{c1} 个', 24, T['blue'], bold=True)
    cv.text((x0 + 20, ly + 114), f'第四类（都不整除）：{mid - mid // d1 - mid // d2 + mid // l} 个', 24, T['green'], bold=True)
    if 'cnt' in S and line >= 20:
        need = S['cnt']
        have = mid - (mid // d1 + mid // d2 - mid // l)
        ok = have >= need
        cv.text((x0 + 20, ly + 164), f'第四类要补 {need} 个，实有 {have} 个：{"够" if ok else "不够"}', 26, T['green'] if ok else T['red'], bold=True)


CONFIG = dict(
    num=2513, title='最小化两个数组中的最大值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 四类整数计数',
    tags=['数学算法', '难度分 2302'],
    code='''
class Solution(object):
    def minimizeSet(self, divisor1, divisor2, uniqueCnt1, uniqueCnt2):

        x, y = divisor1, divisor2
        while y > 0:
            x, y = y, x % y
        
        lcm = divisor1 * divisor2 // x

        left = 1
        right = (uniqueCnt1 + uniqueCnt2) * 2 + 1

        while left < right:
            mid = (left + right) >> 1
            cnt1 = mid // divisor2 - mid // lcm
            cnt2 = mid // divisor1 - mid // lcm

            cnt = max(0, uniqueCnt1 - cnt1) + max(0, uniqueCnt2 - cnt2)

            if cnt + mid // divisor1 + mid // divisor2 - mid // lcm <= mid:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call=f'Solution().minimizeSet({D1}, {D2}, {C1}, {C2})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('lcm', 'lcm'), ('cnt', 'cnt', 'green')],
    skip=['while y > 0'],
    captions={
        'x, y = divisor1, divisor2': '先用辗转相除求最大公约数，再算最小公倍数 `lcm`',
        'x, y = y, x % y': '辗转相除：`(x, y) = ({x}, {y})`',
        'lcm = divisor1': '最大公约数 `{x}` → `lcm = {divisor1} × {divisor2} // {x} = {lcm}`（原文的 `/` 在 Python 3 要写 `//`）',
        'left = 1': '`left = 1`：答案至少是 1',
        'right = (uniqueCnt1': '`right = ({uniqueCnt1} + {uniqueCnt2}) × 2 + 1 = {right}`：最坏情况只能取奇数，这个上界一定够',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`：还没锁定，继续二分' if B.left < B.right
                                               else f'`left == right = {B.left}`：二分结束'),
        'mid = (left + right)': '猜答案 `mid = ({left} + {right}) >> 1 = {mid}`：1~mid 里的数够分吗？',
        'cnt1 = mid': '第三类（只被 d2 整除）：`{mid}//{divisor2} − {mid}//{lcm} = {cnt1}` 个，只能进 `arr1`',
        'cnt2 = mid': '第二类（只被 d1 整除）：`{mid}//{divisor1} − {mid}//{lcm} = {cnt2}` 个，只能进 `arr2`',
        'cnt = max(0': '不够的部分要从第四类补：`max(0, {uniqueCnt1} − {cnt1}) + max(0, {uniqueCnt2} − {cnt2}) = {cnt}`',
        'if cnt + mid': lambda S, B, r: (
            f'第四类共 `{S.mid - S.mid // S.divisor1 - S.mid // S.divisor2 + S.mid // S.lcm}` 个，要补 `{S.cnt}`：'
            + ('够 → `mid` ==可行==' if S.cnt + S.mid // S.divisor1 + S.mid // S.divisor2 - S.mid // S.lcm <= S.mid else '不够 → `mid` ==太小==')),
        'right = mid': '可行 → 答案 <= mid：`right = {right}`',
        'left = mid + 1': '不可行 → 答案 > mid：`left = {left}`',
        'return left': '`left == right`，答案 =={left}==',
    },
    max_steps=100,
    cards=dict(
        one_liner='1~k 的数分四类，先填独享的，缺的从都不整除的里补',
        complexity='时间 `O(log(d) + log(cnt))`，空间 `O(1)`',
        problem=['往 `arr1`、`arr2` 各放 `uniqueCnt1`、`uniqueCnt2` 个互不相同的正整数',
                 '`arr1` 的数不能被 `divisor1` 整除，`arr2` 的不能被 `divisor2` 整除',
                 '求两数组里最大元素的最小值',
                 '本视频：`divisor1 = 2, divisor2 = 7, uniqueCnt1 = 1, uniqueCnt2 = 3` → `4`'],
        quote='为了使得最终答案最小，那么就应该将所有小于等于这个答案的正整数都充分利用起来。注意到题目的k越大，可行性就越高，因此在这里可以二分答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['小于等于 k 的数分四类：同时整除（丢）、只被 d1 整除（进 arr2）、只被 d2 整除（进 arr1）、都不整除（两边都行）',
              '先用二、三类填满各自的数组，不够的从第四类抽',
              '第四类数量 `>=` 缺口，k 就是可行解；k 越大越可行 → 二分'],
        summary=['时间 `O(log d + log cnt)`，空间 `O(1)`',
                 '`lcm` 由辗转相除得到：`d1 * d2 // gcd`',
                 '判定写成 `缺口 + 前三类总数 <= mid`，等价于第四类够用',
                 '原文为 Python 2 写法，整数除法 `/` 已全部改为 `//`',
                 '对比灵神：灵神直接用容斥写判定，还给出了不用二分的公式解'],
    ),
)
