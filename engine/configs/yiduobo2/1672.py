ACC = [[2, 8, 7], [7, 1, 3], [1, 9, 5]]


def _row(S):
    a = S.get('account')
    if a is None or S.get('_line') == 8:
        return None
    try:
        return ACC.index(list(a))
    except ValueError:
        return None


def _draw(cv, S, B, box, T):
    """网格：当前客户那一行黄框；右边是已算出的行和，res 绿色"""
    x0, y0, x1, y1 = box
    cur = _row(S)
    line = S.get('_line')
    a, b = S.get('account'), B.get('account')
    if line == 5 and a is not None and b is not None and list(a) == list(b):
        line, cur = 8, None  # 循环结束
    res = S.get('res')
    cell = 92
    n = len(ACC[0])
    gx = x0 + 150
    gy = y0 + 100
    cv.text((gx, y0 + 16), 'accounts（行 = 客户）', 24, T['muted'], bold=True)
    sx = gx + n * cell + 120
    cv.text((sx, y0 + 16), 'sum(account)', 24, T['muted'], bold=True, mono=True)
    # 已经算过 sum 的行：cur 之前的行；cur 行在执行完 res = max 后也算过
    for i, row in enumerate(ACC):
        Y = gy + i * cell
        if line == 8:
            seen = True
        elif cur is None:
            seen = False
        else:
            seen = i < cur or (i == cur and line == 6)
        is_cur = i == cur
        cv.text((gx - 20, Y + cell / 2), f'客户 {i}', 22, T['yellow'] if is_cur else T['dim'], anchor='rm', bold=is_cur)
        for j, v in enumerate(row):
            X = gx + j * cell
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=T['panel2'], r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), v, 32, T['text'], anchor='mm', bold=True)
        if is_cur:
            cv.rect((gx, Y, gx + n * cell, Y + cell), outline=T['yellow'], width=4, r=12)
        if seen:
            s = sum(row)
            win = res is not None and s == res
            cv.rect((sx, Y + 8, sx + 130, Y + cell - 8), fill=T['green'] if win else T['panel2'], r=10,
                    outline=T['border'])
            cv.text((sx + 65, Y + cell / 2), s, 32, T['bg'] if win else T['text'], anchor='mm', bold=True)
    for j in range(n):
        cv.text((gx + j * cell + cell / 2, gy - 8), f'银行 {j}', 20, T['dim'], anchor='mb')


def _cap_for(S, B, ret):
    if S.get('_line') == 5 and S.get('account') is not None and B.get('account') != S.get('account'):
        return f'枚举下一位客户：`account = {S.account}`'
    return '所有客户都枚举完了'


def _cap_max(S, B, ret):
    s = sum(S.account)
    if S.res > B.res:
        return f'这位客户资产 `sum = {s}` > 当前最大 `{B.res}` → 更新 `res` = =={S.res}=='
    return f'这位客户资产 `sum = {s}` ≤ 当前最大 `{B.res}` → `res` 保持 =={S.res}=='


CONFIG = dict(
    num=1672, title='最富有客户的资产总量', difficulty='Easy', category='矩阵',
    author='yiduobo', technique='枚举每个客户，维护最大值',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def maximumWealth(self, accounts):

        res = 0
        for account in accounts:
            res = max(res, sum(account))

        return res
''',
    call=f'Solution().maximumWealth({ACC})',
    expect=17,
    views=[
        dict(type='custom', h=430, draw=_draw),
        dict(type='text', h=60, size=26,
             fn=lambda S: ('`res`：目前见过的最大资产总量（黄框 = 正在看的客户）' if S.get('_line') != 6
                           else f"`res = max(res, sum(account))` = `max(.., {sum(S['account'])})` = =={S['res']}==")),
    ],
    watch=[('account', 'account', 'yellow'), ('sum(account)', 'sum(account)'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res = 0`：资产都 ≥ 1，用 0 当初始最大值就够了',
        'for account in': _cap_for,
        'res = max(': _cap_max,
        'return res': '枚举完所有客户，`res` = =={ret}== 就是最富有客户的资产总量',
    },
    cards=dict(
        one_liner='枚举每位客户，算行和，取最大',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`accounts[i][j]`：第 `i` 位客户在第 `j` 家银行的资产',
                 '客户的资产总量 = 他那一行的和；返回最大的资产总量',
                 '示例：`[[2,8,7],[7,1,3],[1,9,5]]` → `17`'],
        quote='比较基础的题目，直接==枚举每个客户==计算account内所有数的和，取其中的最大值作为答案就好了。',
        quote_src='—— yiduobo 题解',
        idea=['一行 `account` 就是一位客户，`sum(account)` 是他的资产总量',
              '用 `res` 记住目前见过的最大资产，每位客户比一次',
              '枚举完，`res` 就是答案'],
        result='`res = max(17, 11, 15) = 17`',
        summary=['时间 `O(mn)`：每个格子被加一次；空间 `O(1)`',
                 '`res` 初始为 0 没问题：题目保证 `accounts[i][j] >= 1`',
                 '易错：按行（客户）求和，不是按列（银行）',
                 '原文为 Python 2 风格写法，删去了 docstring，其余照搬'],
    ),
)
