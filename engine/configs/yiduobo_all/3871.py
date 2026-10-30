N0 = 1234567


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    ln = S.get('length')
    p10 = S.get('p10')
    line = S.get('_line', 0)
    L = len(str(n))
    cv.text((x0 + 18, y0 + 4), f'按位数分组：n = {n} 是 {L} 位数', 24, T['muted'], bold=True)
    cols = [x0 + 30, x0 + 190, x0 + 420, x0 + 700]
    heads = ['位数', '每个数的逗号', '这一组有几个数', '小计']
    yh = y0 + 56
    for c, h in zip(cols, heads):
        cv.text((c, yh), h, 22, T['dim'], bold=True)
    rh = 62
    for k in range(1, L + 1):
        y = yh + 44 + (k - 1) * rh
        commas = (k - 1) // 3
        last = (k == L)
        cnt = (n - 10 ** (k - 1) + 1) if last else 9 * 10 ** (k - 1)
        sub = commas * cnt
        if ln is None:
            state = 'todo'
        elif k < ln or (k == ln and line in (8, 9) and not last):
            state = 'done'
        elif k == ln:
            state = 'cur'
        else:
            state = 'todo'
        # while 循环里已经累加到 res 的整组（k < length）；最后一组在 return 时才算
        if line == 12 and last:
            state = 'final'
        col = {'done': T['green'], 'cur': T['yellow'], 'final': T['green'], 'todo': T['dim']}[state]
        if state in ('cur', 'final'):
            cv.rect((x0 + 14, y - 6, x1 - 14, y + rh - 14), fill=col, alpha=40, r=10)
        cv.text((cols[0], y), f'{k} 位', 28, col, bold=True)
        cv.text((cols[1], y), f'{commas} 个', 28, col, mono=True, bold=True)
        txt = f'{cnt}' if (not last or state == 'final' or True) else ''
        cv.text((cols[2], y), (f'n − 10^{k-1} + 1 = {cnt}' if last else f'9 × 10^{k-1} = {cnt}'), 24, col, mono=True)
        if state in ('done', 'final'):
            cv.text((cols[3], y), f'{sub}', 28, col, mono=True, bold=True)
        else:
            cv.text((cols[3], y), '?', 28, T['dim'], mono=True)
    cv.text((x1 - 14, y1 - 10), f"res = {S.get('res', 0)}", 30, T['green'], anchor='rb', bold=True, mono=True)


CONFIG = dict(
    num=3871, title='统计范围内的逗号 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按位数分组计数',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 1381'],
    code='''
class Solution(object):
    def countCommas(self, n):
        
        length = 1
        p10 = 1
        res = 0
        while p10 * 10 - 1 < n:
            res += (length - 1) // 3 * p10 * 9
            p10 *= 10
            length += 1
        
        return res + (length - 1) // 3 * (n - p10 + 1)
''',
    call=f'Solution().countCommas({N0})',
    expect=1468136,
    skip=['length = 1', 'p10 = 1'],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"这一组：`({S['length']}-1)//3` × `{S['p10']}×9` = `{(S['length']-1)//3}` × `{S['p10']*9}` = =={(S['length']-1)//3*S['p10']*9}==" if S.get('_line') == 8 and 'length' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('length', 'length', 'yellow'), ('p10', 'p10', 'cyan'), ('res', 'res', 'green')],
    captions={
        'length = 1': '`length` 是当前位数，从 1 位数开始',
        'p10 = 1': '`p10` 是当前位数的最小数 `10^(length-1)`',
        'res = 0': '`res` 累计逗号总数',
        'while p10 * 10 - 1 < n': lambda S, B, r: (
            f'这一组最大的数 `{S.p10 * 10 - 1}` < `n` → ==整组都在范围里==，可以整组一起算' if S.p10 * 10 - 1 < S.n
            else f'这一组最大的数 `{S.p10 * 10 - 1}` ≥ `n` → {S.length} 位数只有一部分在范围里，停下'),
        'res += (length - 1)': '`{length}` 位数每个有 `({length}-1)//3` = {(length-1)//3} 个逗号，共 `9×{p10}` = {9*p10} 个数 → `res` = =={res}==',
        'p10 *= 10': '进入下一组：`p10` → {p10}',
        'length += 1': '位数 `length` → {length}',
        'return': lambda S, B, r: (f'最后一组 {S.length} 位数只算到 `n`：`({S.length}-1)//3` × `({S.n} - {S.p10} + 1)` = '
                                  f'{(S.length-1)//3} × {S.n - S.p10 + 1}；总共 =={r}== 个逗号'),
    },
    cards=dict(
        one_liner='按位数分组：每个 length 位数有 (length-1)//3 个逗号',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['把 `1..n` 都写成千分位格式（每三位一个逗号，不足四位没有逗号），求逗号总数',
                 '`n` 最大 `10^15`，不能逐个数',
                 '本视频：`n = 1234567` → `1468136`'],
        quote='对于一个length位数，其具有(length - 1) // 3个逗号，同时一共有从10^(length - 1)到10^length - 1，这一共有9 * 10^(length - 1)个length位数。',
        quote_src='—— yiduobo 题解原文',
        idea=['逗号数只和位数有关：1–3 位没有，4–6 位一个，7–9 位两个',
              '`p10` 从 1 开始每次乘 10，`length` 每次加 1，整组整组地累加',
              '最后一组不满，只有 `n - p10 + 1` 个数，单独算'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '循环条件 `p10 * 10 - 1 < n`：整组都不超过 `n` 才整组算',
                 '最后别忘了单独算 `[p10, n]` 这一不满的组',
                 '原文为 Python 2 写法，这里无需改动（`//` 本来就是整除）',
                 '对比灵神：灵神从逗号的角度数，每个逗号 `n - low + 1` 个数；yiduobo 从位数的角度分组'],
    ),
)
