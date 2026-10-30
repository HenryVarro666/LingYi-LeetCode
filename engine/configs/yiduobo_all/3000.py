def _cur(S):
    if 'x' not in S:
        return -1
    try:
        return [list(r) for r in S['dimensions']].index([S['x'], S['y']])
    except ValueError:
        return -1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = S.get('dimensions') or B['dimensions']
    cur = _cur(S)
    cv.text((x0 + 18, y0 + 6), 'dimensions（逐个矩形比较 对角线² t 与当前最大 ma）', 26, T['muted'], bold=True)
    cols = [x0 + 40, x0 + 170, x0 + 360, x0 + 600]
    hy = y0 + 70
    for c, t in zip(cols, ['下标', '长×宽', 't = x²+y²', '面积 x·y']):
        cv.text((c, hy), t, 22, T['dim'], bold=True)
    rh = 64
    for i, (x, y) in enumerate(d):
        Y = hy + 44 + i * rh
        if i == cur:
            cv.rect((x0 + 20, Y - 6, x1 - 20, Y + rh - 14), fill=T['blue'], alpha=70, r=8)
        seen = i < cur or S.get('_line') == 14
        col = T['muted'] if seen else T['text']
        cv.text((cols[0], Y), str(i), 28, col, mono=True)
        cv.text((cols[1], Y), f'{x} × {y}', 28, col, mono=True)
        cv.text((cols[2], Y), str(x * x + y * y), 28, col, mono=True)
        cv.text((cols[3], Y), str(x * y), 28, col, mono=True)
    Y = hy + 44 + len(d) * rh + 20
    if 'ma' in S:
        cv.text((x0 + 40, Y), f"当前最长对角线²  ma = {S['ma']}", 30, T['yellow'], bold=True)
        cv.text((x0 + 40, Y + 46), f"对应最大面积    res = {S['res']}", 30, T['green'], bold=True)


def _cmp1(S, B, ret):
    t, ma = S.t, S.ma
    if t > ma:
        return f'`t = {t} > ma = {ma}`：==对角线更长== → 它才是目前最长的'
    return f'`t = {t} > ma = {ma}`？不成立，往下看是不是并列'


def _cmp2(S, B, ret):
    if S.t == S.ma:
        return f'`t = {S.t} == ma`：==对角线并列== → 要比面积'
    return f'`t = {S.t} ≠ ma = {S.ma}`：对角线更短，直接跳过'


CONFIG = dict(
    num=3000, title='对角线最长的矩形的面积', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 平方和最大前提下取最大面积',
    code='''
class Solution(object):
    def areaOfMaxDiagonal(self, dimensions):

        res = 0
        ma = 0
        for x, y in dimensions:
            t = x ** 2 + y ** 2
            if t > ma:
                ma = t
                res = x * y
            elif t == ma:
                res = max(res, x * y)
        
        return res
''',
    call='Solution().areaOfMaxDiagonal([[2,3],[1,7],[5,5],[4,2]])',
    expect=25,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('ma', 'ma', 'yellow'), ('res', 'res', 'green'), 't'],
    captions={
        'res = 0': '`res` 记录答案（面积）',
        'ma = 0': '`ma` 记录目前见过的最大「边长平方和」',
        't = x ** 2': '勾股定理：对角线² = `{x}² + {y}²` = =={t}==，不开根号',
        'if t > ma': _cmp1,
        'ma = t': '更长的对角线：`ma = {ma}`',
        'res = x * y': '面积直接覆盖：`res = {x} × {y} = {res}`',
        'elif t == ma': _cmp2,
        'res = max': '并列时取面积大的：`max({B.res}, {x * y}) = {res}`',
        'return res': '答案：`{res}`',
    },
    cards=dict(
        one_liner='边长平方和最大的前提下，取最大的矩形面积',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给出每个矩形的长和宽，求对角线最长的矩形的面积',
                 '对角线一样长，取面积最大的',
                 '本视频：`[[2,3],[1,7],[5,5],[4,2]]` → `25`'],
        quote='矩形对角线的长度可以通过边长以及勾股定理计算出来，那么就只需一趟遍历，在保证边长平方和最大的前提下，计算最大的矩形面积即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`ma` 存最大的边长平方和，`res` 存对应的面积',
              '`t > ma`：对角线更长，直接更新 `ma` 和 `res`',
              '`t == ma`：并列，`res` 取两者面积的较大值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用平方和比较，不用开方，没有浮点误差',
                 '易错：并列时要 `max` 比面积，不能直接覆盖',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用元组一行 max，yiduobo 用 if / elif 分情况'],
    ),
)
