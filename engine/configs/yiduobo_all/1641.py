N = 3
V = 'aeiou'
# 展示用：按 yiduobo 的 DP 递推 f[i][j] = f[i][j-1] + f[i-1][j]
_F = [[1] * 5 for _ in range(N + 1)]
for _i in range(1, N + 1):
    _F[_i][0] = 1
    for _j in range(1, 5):
        _F[_i][_j] = _F[_i][_j - 1] + _F[_i - 1][_j] if _i > 1 else 1


def _tbl(S):
    return [[V[j]] + [str(_F[i][j]) for i in range(1, N + 1)] for j in range(5)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = N
    cv.text((x0 + 18, y0 + 4), f'长度 i、以某个元音结尾的字典序字符串数 f[i][j]（n = {n}）', 24, T['muted'], bold=True)
    cw = 130
    ch = min(70, (y1 - y0 - 120) / 5)
    sx = x0 + 60
    sy = y0 + 70
    cv.text((sx + 70, sy), '结尾', 22, T['dim'], anchor='mm')
    for i in range(1, n + 1):
        cv.text((sx + 70 + i * cw, sy), f'i = {i}', 24, T['dim'], anchor='mm', bold=True)
    for j in range(5):
        y = sy + 40 + j * ch
        cv.text((sx + 70, y + ch / 2), V[j], 34, T['cyan'], anchor='mm', bold=True)
        for i in range(1, n + 1):
            last = i == n
            cv.rect((sx + 70 + i * cw - cw / 2 + 6, y + 4, sx + 70 + i * cw + cw / 2 - 6, y + ch - 4),
                    fill=T['green'] if last else (60, 66, 76), r=8, alpha=200 if last else 255)
            cv.text((sx + 70 + i * cw, y + ch / 2), _F[i][j], 32, T['bg'] if last else T['text'], anchor='mm', bold=True)
    tot = sum(_F[n])
    cv.text((sx + 70 + (n + 1) * cw - 20, sy + 40 + 2.5 * ch), f'求和 = {tot}', 34, T['yellow'], anchor='lm', bold=True)


CONFIG = dict(
    num=1641, title='统计字典序元音字符串的数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='隔板法 · 组合数 C(n+4, 4)',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countVowelStrings(self, n):

        return (n + 4) * (n + 3) * (n + 2) * (n + 1) // 24
''',
    call=f'Solution().countVowelStrings({N})',
    expect=35,
    views=[
        dict(type='custom', draw=_draw, h=500),
        dict(type='text', fn=lambda S: ('用隔板法：`C(n+4, 4) = (n+4)(n+3)(n+2)(n+1) / 24`' if 'n' in S else ''), h=80),
        dict(type='text', fn=lambda S: (f"n = {S['n']}：`{S['n']+4}×{S['n']+3}×{S['n']+2}×{S['n']+1} / 24` = =={(S['n']+4)*(S['n']+3)*(S['n']+2)*(S['n']+1)//24}==" if 'n' in S else ''), h=80),
    ],
    watch=['n'],
    captions={
        'def countVowelStrings': '只有一行公式：它就是组合数 `C(n+4, 4)`',
        'return': lambda S, B, r: f'`({S.n}+4)({S.n}+3)({S.n}+2)({S.n}+1) // 24` = `{(S.n+4)*(S.n+3)*(S.n+2)*(S.n+1)}` // 24 = =={r}==，和 DP 表里最后一列求和一致',
    },
    cards=dict(
        one_liner='相同元音必然连续：n 个球之间插 4 块隔板',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['由元音 `a e i o u` 组成、长度为 `n`、字典序不降的字符串有多少个',
                 '示例：`n = 1` → `5`；`n = 2` → `15`',
                 '本视频：`n = 3` → `35`'],
        quote='对于合法的答案，相同的元音字符都是连续出现的。……n个球之间插入4块隔板，隔板的位置可以重叠，问有多少种情况。……答案就是C(n + 4, 4)了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想 DP：`f[i][j] = f[i][j−1] + f[i−1][j]`，各结尾的数目累加',
              '再观察：相同元音必须连续，字符串被切成 5 段，段长之和为 `n`',
              '等价于 `n + 4` 个位置里选 4 个当隔板：==`C(n+4, 4)`=='],
        after=[dict(heading='DP 表：n = 3', lines=['`f[i][j]` 表示长度 i、结尾是第 j 个元音的数目',
                                                    '`f[i][j] = f[i][j−1] + f[i−1][j]`',
                                                    'n = 3 时 i = 3 一列：`1+3+6+10+15 = 35`，与公式一致'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '乘积 `(n+4)(n+3)(n+2)(n+1)` 一定是 24 的倍数，可以整除',
                 '同类：隔板法 / 组合计数'],
    ),
)
