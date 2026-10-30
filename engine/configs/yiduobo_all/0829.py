CONFIG = dict(
    num=829, title='连续整数求和', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='枚举项数 k · 求和公式',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def consecutiveNumbersSum(self, N):

        N += N
        k = 1
        res = 0
        while k * k <= N:
            if N % k == 0:
                tmp = N // k
                if (tmp - k + 1) % 2 == 0:
                    p = (tmp - k + 1) // 2
                    if p > 0:
                        res += 1
                    else:
                        return res
            
            k += 1
        
        return res
''',
    call='Solution().consecutiveNumbersSum(15)',
    expect=4,
    views=[
        dict(type='text', h=110, size=34, fn=lambda S: (f"`2n = {S['N']}`，项数 `k = {S['k']}`：`k × k = {S['k']*S['k']}`" + (" ≤ 2n，继续" if S['k'] * S['k'] <= S['N'] else " > 2n，k 到头了") if 'k' in S and 'N' in S else '')),
        dict(type='text', h=110, size=34, fn=lambda S: (f"`p×2 + k − 1 = 2n / k = {S['tmp']}` → `p×2 = {S['tmp'] - S['k'] + 1}`" if 'tmp' in S and S.get('_line', 0) >= 10 else '')),
        dict(type='custom', h=230, draw=lambda cv, S, B, box, T: _draw(cv, S, B, box, T)),
    ],
    watch=['N', 'k', 'tmp', 'p', ('res', 'res', 'green')],
    captions={
        'N += N': '`n` 翻倍：`2n = {N}`，因为 `p + … + (p+k-1) = (2p + k - 1) × k / 2`',
        'k = 1': '`k` 是连续整数的个数，从 1 开始枚举',
        'res = 0': '`res` 数合法的拆法',
        'while k * k': lambda S, B, r: (f'`{S.k}×{S.k} = {S.k*S.k} <= {S.N}`：因为 `2n = (2p+k-1)×k >= (k+1)×k`，k 还有可能' if S.k * S.k <= S.N else f'`{S.k}×{S.k} = {S.k*S.k} > {S.N}`：k 超过 sqrt(2n)，不可能再有解 → 结束'),
        'if N % k': lambda S, B, r: (f'`{S.N} % {S.k} == 0`：`2n` 能被 k 整除，才可能写成 `(2p+k-1)×k`' if S.N % S.k == 0 else f'`{S.N} % {S.k} != 0`：凑不出，k 加一'),
        'tmp = N': '`tmp = 2n / k` = =={tmp}==，应等于 `2p + k - 1`',
        'if (tmp': lambda S, B, r: (f'`({S.tmp} − {S.k} + 1) = {S.tmp - S.k + 1}` 是偶数 → p 是整数' if (S.tmp - S.k + 1) % 2 == 0 else f'`({S.tmp} − {S.k} + 1) = {S.tmp - S.k + 1}` 是奇数 → p 不是整数，这个 k 无解'),
        'p = (tmp': '`p = ({tmp} − {k} + 1) // 2` = =={p}==：首项',
        'if p > 0': lambda S, B, r: (f'`p = {S.p} > 0`：==找到一种拆法==：从 {S.p} 开始连续 {S.k} 个' if S.p > 0 else f'`p = {S.p} <= 0`：首项不是正整数，而且 k 越大 p 越小，后面全无解'),
        'res += 1': '`res` = =={res}==',
        'return res': lambda S, B, r: f'`p` 已经 <= 0，不用再往后枚举 → 返回 =={r}==' if S.get('p', 1) <= 0 and S.get('_line') != 18 else f'共有 =={r}== 种拆法',
        'k += 1': '`k` → {k}',
    },
    cards=dict(
        one_liner='设首项 p、共 k 项，枚举 k 反解 p',
        complexity='时间 `O(sqrt(n))`，空间 `O(1)`',
        problem=['给定正整数 `n`，问有多少种方式把它写成连续正整数的和',
                 '例如 `15 = 15 = 7+8 = 4+5+6 = 1+2+3+4+5`',
                 '示例：`n = 15` → `4`'],
        quote='p + (p + 1) + ... + (p + k - 1) = (p * 2 + k - 1) * k = n * 2',
        quote_src='—— yiduobo 题解原文',
        idea=['`2n = (2p + k − 1) × k`：k 必须整除 `2n`',
              '`2p = 2n / k − k + 1` 必须是正偶数',
              '`2n >= (k+1) k`，所以 k 只到 `sqrt(2n)`；k 增大 p 变小，p <= 0 就可以收工'],
        summary=['时间 `O(sqrt(n))`',
                 '原文为 Python 2 写法，`N / k` 与 `/ 2` 已改为 `//`（整除）',
                 '`p` 必须 > 0，且 `(tmp − k + 1)` 必须是偶数',
                 '`p <= 0` 时直接 `return res`，因为后面的 k 只会让 p 更小',
                 '本视频示例：`n = 15`，共 4 种：`15`、`7+8`、`4+5+6`、`1+2+3+4+5`'],
    ),
)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '当前 k 对应的连续整数', 24, T['muted'], bold=True)
    if 'p' not in S or 'k' not in S or S.get('_line', 0) not in (11, 12, 13):
        return
    p, k = S['p'], S['k']
    if p <= 0 or k > 12:
        return
    cell = min(80, (x1 - x0 - 40) / k)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * k) / 2
    y = y0 + 70
    for i in range(k):
        cv.rect((sx + i * cell + 3, y, sx + (i + 1) * cell - 3, y + 70), fill=T['blue'] if i else T['green'], r=8)
        cv.text((sx + i * cell + cell / 2, y + 35), p + i, 30, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + 20, y + 100), f'从 {p} 开始连续 {k} 个，和 = {sum(range(p, p + k))}', 26, T['text'])
