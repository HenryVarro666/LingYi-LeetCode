N, K = 3, 7


def _fmt(xs):
    xs = sorted(xs)
    return ', '.join(map(str, xs)) if xs else '—'


def _draw_dp(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    i = S.get('i')
    cur_round = i if i is not None else 1
    cv.text((x0 + 18, y0 + 4), f'DP 表：f[j] = 末位为 j 的合法数（左 = {cur_round - 1 if "tmp" in S else cur_round} 位，右 = {cur_round} 位）'
            if 'tmp' in S else 'DP 表：f[j] = 末位为 j 的 1 位数（0 不能当首位）', 22, T['muted'], bold=True)
    f = S.get('f')
    if f is None:
        return
    tmp = S.get('tmp')
    top = y0 + 74
    rh = min(44, (y1 - top - 6) / 10)
    cx0, cw0 = x0 + 30, 70               # 末位 j
    cx1 = cx0 + cw0 + 10                 # f[j]
    cw1 = (x1 - cx1 - 30 - 80) / 2
    cx2 = cx1 + cw1 + 80                 # tmp[j]
    cv.text((cx0 + cw0 / 2, top - 6), 'j', 20, T['dim'], anchor='mb', bold=True)
    cv.text((cx1 + cw1 / 2, top - 6), 'f[j]', 20, T['dim'], anchor='mb', bold=True)
    if tmp is not None:
        cv.text((cx2 + cw1 / 2, top - 6), 'tmp[j]', 20, T['dim'], anchor='mb', bold=True)
    ln = S.get('_line')
    last = S.get('last') if ln in (6, 9, 12) else None
    tgt = None
    if ln == 9:
        tgt = last + K
    elif ln == 12:
        tgt = last - K
    for j in range(10):
        Y = top + j * rh
        cv.text((cx0 + cw0 / 2, Y + rh / 2), j, 22, T['muted'], anchor='mm', bold=True, mono=True)
        hl = j == last
        cv.rect((cx1, Y + 3, cx1 + cw1, Y + rh - 3), fill=(60, 52, 30) if hl else T['panel2'], r=6,
                outline=T['yellow'] if hl else T['border'], width=3 if hl else 1)
        cv.text((cx1 + 12, Y + rh / 2), _fmt(f[j]), 20, T['text'], anchor='lm', bold=True, mono=True)
        if tmp is not None:
            th = j == tgt
            cv.rect((cx2, Y + 3, cx2 + cw1, Y + rh - 3), fill=(30, 70, 45) if th else T['panel2'], r=6,
                    outline=T['green'] if th else T['border'], width=3 if th else 1)
            cv.text((cx2 + 12, Y + rh / 2), _fmt(tmp[j]), 20, T['text'], anchor='lm', bold=True, mono=True)
    if tgt is not None:
        ya, yb = top + last * rh + rh / 2, top + tgt * rh + rh / 2
        cv.arrow((cx1 + cw1 + 4, ya), (cx2 - 6, yb), T['green'], 3)
        cv.text(((cx1 + cw1 + cx2) / 2 + 14, (ya + yb) / 2), f'{"+" if ln == 9 else "−"}{K}', 22, T['green'], anchor='lm', bold=True)


def _last_cap(S, B, ret):
    if B.get('last') == S.get('last') and S.get('i') == B.get('i') and 'last' in B:
        return f'{S.i} 位数的 `tmp` 算完了'
    j = S.last
    up, down = j + K, j - K
    can = []
    if up <= 9:
        can.append(f'`{j}+{K}={up}`')
    if down >= 0:
        can.append(f'`{j}−{K}={down}`')
    if not can:
        return f'`last = {j}`：`{j}+{K} > 9` 且 `{j}−{K} < 0` → 末位 {j} 后面==接不上任何数字=='
    if not S.f[j]:
        return f'`last = {j}`：可以接 ' + '、'.join(can) + f'，但 `f[{j}]` 是空的'
    return f'`last = {j}`：`f[{j}]` 里的数后面可以接 ' + '、'.join(can)


CONFIG = dict(
    num=967, title='连续差相同的数字', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按末位分组的 DP + 滚动数组',
    tags=['字节30天'],
    code='''
class Solution(object):
    def numsSameConsecDiff(self, n, k):
        f = [[], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
        for i in range(2, n + 1):
            tmp = [set() for _ in range(10)]
            for last in range(10):
                if last + k <= 9:
                    for x in f[last]:
                        tmp[last + k].add(x * 10 + last + k)
                if last - k >= 0:
                    for x in f[last]:
                        tmp[last - k].add(x * 10 + last - k)
            f = tmp[:]

        res = []
        for last in range(10):
            res += f[last]

        return res
''',
    call=f'Solution().numsSameConsecDiff({N}, {K})',
    result_fn=sorted,
    expect=[181, 292, 707, 818, 929],
    # if / 内层 for 的判断已写进 last 那一行的字幕；收集答案的 for 头也不单独成步
    skip=['if last + k <= 9', 'if last - k >= 0', 'for x in f[last]', 16],
    views=[
        dict(type='custom', draw=_draw_dp, h=520),
        dict(type='array', var=lambda S: sorted(S['res']) if 'res' in S else None, label='res（收集 f[0..9]，按大小显示）', cell=90, min_slots=5),
    ],
    watch=[('i', 'i', 'blue'), ('last', 'last', 'yellow'), ('x', 'x'), ('k', 'k')],
    captions={
        'f = [[], [1]': '`f[j]`：==1 位数==、末位为 `j` 的合法答案；`f[0]` 为空（不能有前导 0）',
        'for i in range': lambda S, B, ret: (f'由 {S.i - 1} 位数推出 =={S.i} 位数==' if B.get('i') != S.get('i') or 'i' not in B
                                             else f'推到 `n = {S.n}` 位了'),
        'tmp = [set()': '`tmp[j]`：本轮末位为 `j` 的数；用 `set` ==防止 k = 0 时重复加入==',
        'for last in range(10)': _last_cap,
        'tmp[last + k].add': '`{x}` 末位 `{last}`，后面接 `{last}+{k}={last + k}` → `{x * 10 + last + k}` 放进 `tmp[{last + k}]`',
        'tmp[last - k].add': '`{x}` 末位 `{last}`，后面接 `{last}−{k}={last - k}` → `{x * 10 + last - k}` 放进 `tmp[{last - k}]`',
        'f = tmp[:]': '只依赖上一轮 → ==滚动数组==：`f = tmp`，开始下一位',
        'res = []': '全部计算完成，把 `f[0]` 到 `f[9]` 收集起来',
        'res += f[last]': lambda S, B, ret: (f'收集 `f[{S.last}]` = {{{_fmt(S.f[S.last])}}}' if S.f[S.last] else f'`f[{S.last}]` 为空'),
        'return res': '返回全部 `{len(res)}` 个答案',
    },
    cards=dict(
        one_liner='f[j] 记末位为 j 的数，下一位只能是 j+k 或 j−k',
        complexity='时间 `O(10n + 2^n)`，空间 `O(2^n)`',
        problem=['返回所有长度为 `n`、==每两个相邻位之差的绝对值都是 `k`== 的非负整数',
                 '不能有前导零（如 `01` 不合法），顺序任意',
                 '示例：`n = 3, k = 7` → `[181,292,707,818,929]`'],
        quote='令f[i][j]表示i位数，最后一位为j时有哪些合法的答案……若j + k <= 9，那么对于f[i][j]中的所有数而言，将这个数乘以10再加上j + k必然符合要求的i + 1位数。',
        quote_src='—— yiduobo 知乎题解',
        idea=['状态：`f[j]` = 当前位数下、末位为 `j` 的所有合法数',
              '转移：末位 `j` 后面只能接 `j+k`（≤ 9）或 `j−k`（≥ 0），即 `x * 10 + 新末位`',
              '每轮只依赖上一轮 → 滚动数组 `f = tmp[:]`'],
        summary=['时间 `O(10n + 2^n)`：每轮扫 10 个末位，每个数最多扩展出 2 个新数',
                 '易错：`k = 0` 时 `j+k` 与 `j−k` 相同，用 `set` 去重',
                 '`f[0]` 初始为空：首位不能是 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '另一种常见写法：从每个首位 DFS/BFS 逐位扩展'],
    ),
)
