ACC = [[2, 8, 7], [7, 1, 3], [1, 9, 5]]


def _draw(cv, S, B, box, T):
    """左：accounts 网格；右：map(sum) 得到的每行和；最大的那行绿色"""
    x0, y0, x1, y1 = box
    done = S.get('_line') == 3
    sums = [sum(r) for r in ACC]
    mx = max(sums)
    cell = 96
    m, n = len(ACC), len(ACC[0])
    gx = x0 + 150
    gy = y0 + 100
    cv.text((gx, y0 + 16), 'accounts（行 = 客户，列 = 银行）', 24, T['muted'], bold=True)
    sx = gx + n * cell + 140
    cv.text((sx - 20, y0 + 16), 'map(sum, accounts)', 24, T['muted'], bold=True, mono=True)
    for i, row in enumerate(ACC):
        Y = gy + i * cell
        best = done and sums[i] == mx
        cv.text((gx - 20, Y + cell / 2), f'客户 {i}', 22, T['dim'], anchor='rm')
        for j, v in enumerate(row):
            X = gx + j * cell
            fill = (T['green'] if best else T['panel2'])
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), v, 34, T['bg'] if best else T['text'], anchor='mm', bold=True)
        if done:
            cv.arrow((gx + n * cell + 16, Y + cell / 2), (sx - 14, Y + cell / 2), T['muted'], 3)
            cv.rect((sx, Y + 6, sx + 150, Y + cell - 6), fill=T['green'] if best else T['panel2'], r=10,
                    outline=T['yellow'] if best else T['border'], width=3 if best else 1)
            cv.text((sx + 75, Y + cell / 2), sums[i], 36, T['bg'] if best else T['text'], anchor='mm', bold=True)
            cv.text((sx + 170, Y + cell / 2), ' + '.join(map(str, ACC[i])), 22, T['dim'], anchor='lm')
    for j in range(n):
        cv.text((gx + j * cell + cell / 2, gy - 8), f'银行 {j}', 20, T['dim'], anchor='mb')
    if done:
        Y = gy + m * cell + 30
        cv.text((sx + 75, Y), f'max = {mx}', 34, T['orange'], anchor='mt', bold=True)


CONFIG = dict(
    num=1672, title='最富有客户的资产总量', difficulty='Easy', category='矩阵',
    author='灵茶山艾府', technique='一行：max(map(sum, accounts))',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def maximumWealth(self, accounts: List[List[int]]) -> int:
        return max(map(sum, accounts))
''',
    call=f'Solution().maximumWealth({ACC})',
    expect=17,
    views=[
        dict(type='custom', h=470, draw=_draw),
        dict(type='text', h=60, size=26,
             fn=lambda S: ('`max(map(sum, accounts))` = `max(17, 11, 15)` = ==17==' if S.get('_line') == 3
                           else '`map(sum, accounts)`：把每一行变成它的和')),
    ],
    watch=[('m', 'len(accounts)'), ('n', 'len(accounts[0])')],
    captions={
        'return max(map(': lambda S, B, ret: (f'`map(sum, accounts)` 把每位客户（每一行）求和 → `{[sum(r) for r in S.accounts]}`；'
                                              f'再取 `max` = =={ret}=='),
    },
    cards=dict(
        one_liner='每行求和，取最大值',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`accounts[i][j]`：第 `i` 位客户在第 `j` 家银行的资产',
                 '客户的资产总量 = 他那一行的和；返回最大的资产总量',
                 '示例：`[[2,8,7],[7,1,3],[1,9,5]]` → `17`（第 0 位客户 2 + 8 + 7）'],
        quote='==题意==：计算 accounts[i] 的元素和的最大值。遍历每个 accounts[i]，计算元素和，更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「简单题，简单做」：一行 = 一位客户，资产总量就是==行和==',
              '`map(sum, accounts)` 对每一行调用 `sum`，惰性生成每行的和',
              '外面套一个 `max` 边生成边比较，不需要额外的列表'],
        result='三行的和是 `17, 11, 15`，最大 `17`',
        after=[dict(heading='拆开这一行', lines=[
            '`map(sum, accounts)` ≈ `(sum(row) for row in accounts)`',
            '等价的循环：`ans = 0`，对每个 `row`：`ans = max(ans, sum(row))`',
            '`m, n >= 1`：每行至少一个数，`max` 不会遇到空序列'])],
        summary=['时间 `O(mn)`：每个格子恰好加一次',
                 '空间 `O(1)`：`map` 是惰性的，不会先建一个和的列表',
                 '易错：是对每一行（客户）求和，不是对每一列（银行）',
                 '其它语言就是双重循环：内层求行和，外层更新最大值'],
    ),
)
