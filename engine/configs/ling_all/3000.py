def _txt(S, B, ret):
    d = B['dimensions']
    keys = [(x * x + y * y, x * y) for x, y in d]
    best = max(keys)
    return ('每个矩形变成二元组 `(x²+y², x·y)`，Python 按元组字典序取 max：先比对角线平方，平局再比面积；'
            f'最大是 ==({best[0]}, {best[1]})==，取 `[1]` 得面积 =={best[1]}==')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = S.get('dimensions') or B['dimensions']
    keys = [(x * x + y * y, x * y) for x, y in d]
    best = max(keys)
    cv.text((x0 + 18, y0 + 6), '每个矩形 → 二元组（对角线平方, 面积）', 26, T['muted'], bold=True)
    cols = [x0 + 40, x0 + 190, x0 + 400, x0 + 640]
    hy = y0 + 70
    for c, t in zip(cols, ['下标', '长×宽', '对角线² = x²+y²', '面积 x·y']):
        cv.text((c, hy), t, 22, T['dim'], bold=True)
    rh = 64
    mx = max(k[0] for k in keys)
    for i, ((x, y), (a, b)) in enumerate(zip(d, keys)):
        Y = hy + 44 + i * rh
        win = (a, b) == best
        tie = a == mx
        if win:
            cv.rect((x0 + 20, Y - 6, x1 - 20, Y + rh - 14), fill=T['green'], alpha=60, r=8)
        elif tie:
            cv.rect((x0 + 20, Y - 6, x1 - 20, Y + rh - 14), fill=T['yellow'], alpha=50, r=8)
        cv.text((cols[0], Y), str(i), 28, T['text'], mono=True)
        cv.text((cols[1], Y), f'{x} × {y}', 28, T['text'], mono=True)
        cv.text((cols[2], Y), f'{x*x} + {y*y} = {a}', 28, T['yellow'] if tie else T['text'], mono=True, bold=tie)
        cv.text((cols[3], Y), str(b), 28, T['green'] if win else T['text'], mono=True, bold=win)
    cv.text((x0 + 40, hy + 44 + len(d) * rh + 14),
            '黄 = 并列最长对角线，绿 = 其中面积最大 → 答案', 24, T['muted'])


CONFIG = dict(
    num=3000, title='对角线最长的矩形的面积', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='双关键字取最大 · 元组比较',
    code='''
class Solution:
    def areaOfMaxDiagonal(self, dimensions: List[List[int]]) -> int:
        return max((x * x + y * y, x * y) for x, y in dimensions)[1]
''',
    call='Solution().areaOfMaxDiagonal([[2,3],[1,7],[5,5],[4,2]])',
    expect=25,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[],
    captions={
        'return max': _txt,
    },
    cards=dict(
        one_liner='对角线平方当第一关键字，面积当第二关键字，元组直接比大小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个矩形给出长和宽，找 ==对角线最长== 的矩形，返回它的面积',
                 '对角线一样长时，返回 ==面积最大== 的那个',
                 '示例：`[[3,4],[4,3]]` → 对角线都是 5 → `12`'],
        quote='第一关键字是对角线长度，直接用其平方值。如果遍历到更大的长度，则覆盖矩形面积。第二关键字是矩形面积，即 x·y。',
        quote_src='—— 灵茶山艾府题解',
        idea=['勾股定理：对角线² = `x² + y²`，不用开根号，整数比较没有精度问题',
              '把 `(x*x+y*y, x*y)` 作为元组，Python 先比第一项，平局才比第二项',
              '`max(...)[1]` 取出最大元组里的面积'],
        after=[dict(heading='为什么用平方', lines=['对角线 = `sqrt(x² + y²)`，开方后是小数', '比较大小时平方保持顺序，整数比较又快又准', '本例 `(1,7)` 和 `(5,5)` 平方都是 50，对角线并列']),
               dict(heading='元组比较', lines=['`(50, 7) < (50, 25)`：第一项相同，比第二项', '所以并列时自动挑面积更大的矩形', '不用写 if / elif，一行搞定'])],
        summary=['时间 `O(n)`，空间 `O(1)`（生成器不建列表）',
                 '比较对角线时用平方，避免 `sqrt` 的浮点误差',
                 '易错：并列时要取面积最大，而不是第一个遇到的',
                 '本题代码只有一行，视频里的表格把每个矩形的二元组展开给你看'],
    ),
)
