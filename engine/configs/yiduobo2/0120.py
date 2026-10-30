TRI = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
MAXI = 2147483647


def _td():
    f = [[TRI[0][0]]]
    for i in range(1, len(TRI)):
        row = []
        for j in range(i + 1):
            cand = []
            if j - 1 >= 0:
                cand.append(f[i - 1][j - 1])
            if j <= i - 1:
                cand.append(f[i - 1][j])
            row.append(min(cand) + TRI[i][j])
        f.append(row)
    return f


TD = _td()


def _done_row(S, B):
    """index of the last row whose f is known"""
    line = S.get('_line')
    if 'f' not in S:
        return -1
    if line == 8:
        if 'i' in B and B.get('i') == S.get('i'):
            return len(TRI) - 1
        return S['i'] - 1
    if line == 9:
        return S['i']
    if line == 10:
        return len(TRI) - 1
    return 0


def _m(v):
    return 'MAX' if v == MAXI else str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(TRI)
    cell = 64
    done = _done_row(S, B)
    cur = S.get('i') if S.get('_line') == 9 else None
    gx = [x0 + 40, x0 + 380]
    cv.text((gx[0], y0 + 4), 'triangle', 24, T['muted'], bold=True)
    cv.text((gx[1], y0 + 4), 'f[i][j]：顶点 → (i,j) 的最小和（紫 = 哨兵）', 24, T['muted'], bold=True)
    top = y0 + 44
    for r in range(n):
        for c in range(r + 1):
            Y = top + r * cell
            X = gx[0] + c * cell
            on = cur is not None and r == cur
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=T['yellow'] if on else T['panel2'], r=8, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), TRI[r][c], 26, T['bg'] if on else T['text'], anchor='mm', bold=True)
            X2 = gx[1] + c * cell
            known = r <= done
            fill = T['green'] if (on and known) else (T['panel2'])
            cv.rect((X2 + 3, Y + 3, X2 + cell - 3, Y + cell - 3), fill=fill, r=8,
                    outline=T['yellow'] if on else T['border'], width=3 if on else 1)
            cv.text((X2 + cell / 2, Y + cell / 2), TD[r][c] if known else '?', 26,
                    T['bg'] if (on and known) else (T['text'] if known else T['dim']), anchor='mm', bold=True)
        if r <= done:  # 每一层末尾补的 MAX
            X2 = gx[1] + (r + 1) * cell
            cv.rect((X2 + 3, top + r * cell + 3, X2 + cell + 16, top + r * cell + cell - 3), fill=T['panel'], r=8,
                    outline=T['purple'], width=2)
            cv.text((X2 + cell / 2 + 8, top + r * cell + cell / 2), 'MAX', 20, T['purple'], anchor='mm', bold=True)


def _draw_calc(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur = S.get('i') if S.get('_line') == 9 else None
    cv.text((x0 + 18, y0 + 4), '这一层每个 j 的计算：min(f[j-1], f[j]) + triangle[i][j]', 24, T['muted'], bold=True)
    if cur is not None and isinstance(B.get('f'), list):
        bf, sf = B['f'], S['f']
        colw = (x1 - x0 - 40) / 2
        for j in range(cur + 1):
            a, b = bf[j - 1], bf[j]
            X = x0 + 24 + (j % 2) * colw
            Y = y0 + 44 + (j // 2) * 36
            idx = f'f[{j - 1}]' if j else 'f[-1]'
            cv.text((X, Y), f'j={j}: min({idx}={_m(a)}, f[{j}]={_m(b)}) + {TRI[cur][j]} = {sf[j]}', 21,
                    T['purple'] if (a == MAXI or b == MAXI) else T['text'], mono=True)
    elif S.get('_line') == 6:
        cv.text((x0 + 24, y0 + 44), 'j = 0 时 f[-1] 取到末尾的 MAX → min 自动选 f[0]；j = i 时 f[i] 就是 MAX', 22, T['purple'])


def _arr(S):
    f = S.get('f')
    return [_m(v) for v in f] if isinstance(f, list) else None


def _cap_f(S, B, ret):
    i = S.i
    if i == 1:
        return ('`j = 0` 时 `f[-1]` 取到末尾的 ==MAX==，只能从正上来；`j = 1` 时 `f[1]` 是 MAX，只能从左上来 → '
                f'`{S.f[:-1]}`')
    return f'第 `{i}` 层：两端由哨兵自动处理，中间取 `min(左上, 正上) + 自己` → `{S.f[:-1]}`，末尾再补 MAX'


CONFIG = dict(
    num=120, title='三角形最小路径和', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='自顶向下 DP · 滚动数组 + 末尾哨兵',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def minimumTotal(self, triangle):
        if not triangle:
            return 0

        f = [triangle[0][0], 2147483647]

        for i in range(1, len(triangle)):
            f = [min(f[j - 1], f[j]) + triangle[i][j] for j in range(i + 1)] + [2147483647]
        return min(f)
''',
    call=f'Solution().minimumTotal({TRI})',
    expect=11,
    views=[
        dict(type='custom', draw=_draw, h=310),
        dict(type='custom', draw=_draw_calc, h=130),
        dict(type='array', var=_arr, label='f（滚动数组，最后一格是哨兵 MAX = 2147483647）', cell=96, h=160,
             color=lambda S, k, v: 'purple' if v == 'MAX' else ('green' if S.get('_line') == 9 else None)),
    ],
    watch=[('i', 'i', 'yellow'), ('len(f)', 'len(f)')],
    captions={
        'if not triangle': '三角形非空，继续',
        'f = [triangle[0][0]': '第 0 层只有顶点：`f = [2]`，后面补一个 ==MAX== 当哨兵',
        'for i in range': lambda S, B, r: (f'处理第 `i = {S.i}` 层：只和上一层的 f 有关' if B.get('i') != S.get('i') or 'i' not in B
                                           else '所有层都算完了'),
        'f = [min(f[j - 1]': _cap_f,
        'return min(f)': '终点可以是最后一层的任何位置 → 取 `min(f)` = =={ret}==（哨兵 MAX 不影响）',
    },
    cards=dict(
        one_liner='f[i][j] = min(左上, 正上) + 自己；末尾补 MAX，一个式子盖住边界',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给一个三角形 `triangle`，求==自顶向下==的最小路径和',
                 '在第 `i` 层下标 `j` 时，下一步只能走到下一层的 `j` 或 `j + 1`',
                 '示例：`[[2],[3,4],[6,5,7],[4,1,8,3]]` → `11`（2 + 3 + 5 + 1）'],
        quote='在计算完每一层的f之后，在最后添加上一个maxint。这样一来，对于j = 0的情况，f[i - 1][j - 1]对应到的是==f[i - 1][-1]即最后添加的maxint==……上面的三种情况都可以通过情况3的状态转移方程覆盖住了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：从顶部到第 `i` 层第 `j` 个数的最小路径和',
              '`j = 0` 只能从正上来，`j = i` 只能从左上来，其余 `min(f[i-1][j-1], f[i-1][j]) + 自己`',
              '只依赖上一层 → 滚动数组；末尾补 MAX，Python 的 `f[-1]` 正好取到它'],
        result='最后一层 `f = [15, 11, 18, 16]`（+哨兵），`min(f) = 11`',
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：自顶向下的终点不固定，答案是最后一层的 `min`，不是某个固定格子',
                 '哨兵技巧利用了 Python 负下标；其他语言要手动判边界',
                 '对比灵神：自底向上，`f[0]` 直接就是答案，不用处理边界',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
