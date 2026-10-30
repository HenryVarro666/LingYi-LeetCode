CONFIG = dict(
    num=441, title='排列硬币', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='求根公式',
    setup='from math import sqrt',
    code='''
class Solution(object):
    def arrangeCoins(self, n):

        res = int(sqrt(n * 2 + 1 / 4) + 1 / 2)
        
        if res * (res + 1) // 2 > n:
            res -= 1
        return res
''',
    call='Solution().arrangeCoins(8)',
    expect=3,
    views=[
        dict(type='text', h=60, size=34, fn=lambda S: f"n = {S['n']}：第 k 行放 k 枚"),
        dict(type='text', h=60, size=34, fn=lambda S: (f"`sqrt(2n + 1/4) + 1/2` = {__import__("math").sqrt(S['n']*2+0.25)+0.5:.2f} → `res = {S['res']}`" if 'res' in S else '先用求根公式估计行数')),
        dict(type='text', h=60, size=34, fn=lambda S: (f"前 {S['res']} 行共需 `{S['res']}×{S['res']+1}/2 = {S['res']*(S['res']+1)//2}` 枚，n = {S['n']}" if 'res' in S else '')),
        dict(type='custom', h=330, draw=lambda cv, S, B, box, T: _draw(cv, S, box, T)),
    ],
    watch=['n', ('res', 'res', 'green')],
    captions={
        'res = int': '解不等式 `k(k-1)/2 < n` 得 `k < sqrt(2n + 1/4) + 1/2`：`sqrt({n}*2 + 1/4) + 1/2 = {__import__("math").sqrt(n*2+1/4)+1/2:.2f}`，取整得 `res = {res}`',
        'if res': '公式只保证前 `res-1` 行放得下；检查第 `res` 行能否放满：需要 `{res}*({res}+1)//2 = {res*(res+1)//2}` 枚，和 n = {n} 比较',
        'res -= 1': '`{B.res}*({B.res}+1)//2 = {B.res*(B.res+1)//2}` > `{n}`：最后一行放不满，行数减一，`res = {res}`',
        'return': '返回完整行数 =={ret}==',
    },
    cards=dict(
        one_liner='解不等式得行数，再检查最后一行是否放满',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['有 n 枚硬币，要摆成阶梯形：第 k 行恰好放 k 枚',
                 '求能摆出的 ==完整行== 的总数（最后一行可能不满）',
                 '示例：`n = 8` → `3`（1 + 2 + 3 = 6，第 4 行只剩 2 枚）'],
        quote='不妨设可以排成到第k行，那么一定满足 1 + 2 + ... + k - 1 < n，通过求和公式就有 k * (k - 1) / 2 < n，即(k - 1/2) ^2 < 2n + 1/4，解得k < sqrt(2n + 1/4) + 1/2',
        quote_src='—— yiduobo 题解',
        idea=['设排到第 k 行，前 k-1 行必须放得下，得到 `k < sqrt(2n+1/4) + 1/2`',
              '根号内不可能是有理数的平方，所以 k 必为非整数，取 `int(...)`',
              '再验证：若 `k(k+1)/2 > n`，说明第 k 行放不满，答案 `k - 1`'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：第 k 行不一定放得满，必须再验证一次',
                 '`1/4`、`1/2` 是浮点数，所以要用 Python 3 的真除法',
                 '原文为 Python 2 写法，其中整数除法 `res*(res+1)/2` 已改为 `//`；`sqrt` 来自 `math`'],
    ),
)


def _draw(cv, S, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    k = S.get('res')
    cv.text((x0 + 18, y0 + 4), '阶梯：第 i 行放 i 枚（绿 = 完整行，灰 = 放不满）', 24, T['muted'], bold=True)
    if k is None:
        return
    rows = k + 1
    cell = min(48, (y1 - y0 - 60) / rows, (x1 - x0 - 40) / (rows + 1))
    used = 0
    for i in range(1, rows + 1):
        full = used + i <= n
        for j in range(i):
            c = T['green'] if full else T['muted']
            X, Y = x0 + 30 + j * cell, y0 + 50 + (i - 1) * cell
            idx = used + j
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=c if idx < n else None, outline=c, r=cell / 2)
        used += i
