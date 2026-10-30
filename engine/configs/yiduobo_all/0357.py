def _terms(S):
    """res 里已经累加的各项：[1, 9, 81, ...]"""
    if 'res' not in S:
        return None
    out, t, tot, k = [1], 9, 1, 0
    while tot < S['res']:
        out.append(t)
        tot += t
        t *= (9 - k)
        k += 1
    return out


def _formula(S):
    if 'now' not in S:
        return ''
    k = S.get('index')
    ts = _terms(S)
    return '`res` = ' + ' + '.join(f'`{x}`' for x in ts) + f' = =={S["res"]}=='


CONFIG = dict(
    num=357, title='计算各个位数不同的数字个数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='排列组合 · 逐位累加',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def countNumbersWithUniqueDigits(self, n):

        now = 9
        res = 1
        for index in range(n):
            res += now
            now *= (9 - index)

        return res
''',
    call='Solution().countNumbersWithUniqueDigits(4)',
    expect=5275,
    views=[
        dict(type='array', var=_terms, label='res 里累加的每一项（下标 0 = 数字 0 本身，下标 k = k 位数）', cell=110, h=190),
        dict(type='text', h=80, fn=_formula),
        dict(type='text', h=80, fn=lambda S: (f"下一项 `now` = =={S['now']}==：{S['index'] + 1 if 'index' in S else 1} 位数里数字互不相同的个数" if 'now' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'now = 9': '`now = 9`：==一位数== 里首位不能 0，所以先看 `1~9` 共 9 种（0 在 `res` 里单算）',
        'res = 1': '`res = 1`：先把 ==0== 这一个数算上',
        'for index in range(n)': lambda S, B, r: ('位数从 1 到 `n` 逐个累加' if 'index' not in S else ('`n = 4` 位都处理完了，循环结束' if B.get('index') == S.index and S.index == 3 else f'枚举位数：现在处理 `{S.index + 1}` 位数')),
        'res += now': '`{index + 1}` 位数共 `{now}` 个，加进去：`res = {B.res} + {now} = {res}`',
        'now *= (9 - index)': '再多一位：这一位不能和前面 `{index + 1}` 位重复，`10 − {index + 1} = {9 - index}` 种选择 → `now = {now}`',
        'return res': '`n = 4` 时，0 位到 4 位的个数加起来，一共 `{res}` 个',
    },
    cards=dict(
        one_liner='k 位数：首位 9 种，之后每位比前一位少 1 种选择',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定非负整数 `n`，统计 `[0, 10^n)` 中各位数字都不同的数的个数',
                 '示例：`n = 2` → `91`（去掉 `11, 22, ..., 99` 共 9 个）',
                 '本视频：`n = 4` → `5275`'],
        quote='因为最高位不能为0，只有9中选择，其他位上的选择则是逐位减1，即3位数一共有9 * 9 * 8种组合，4位数则是9 * 9 * 8 * 7种组合',
        quote_src='—— yiduobo 题解原文',
        idea=['一位数：`0~9` 共 10 个；两位数首位 9 种、个位 9 种 → `81`',
              '`k` 位数 = `9 × 9 × 8 × …`，每多一位乘的数减 1',
              '一趟循环，逐位算出各位数的个数并累加；`res` 初始为 1 代表数字 0'],
        summary=['时间 `O(n)`，空间 `O(1)`（`n > 10` 时之后全是 0 项，也能自然结束）',
                 '易错点：`res` 从 1 开始（单独的 0），`now` 从 9 开始',
                 '`now *= (9 - index)`：第 `k` 位数的乘数是 `9 - (k-1)`',
                 '和 2376 同族：那题要数 `[1, n]`，要在此基础上逐位卡上界'],
    ),
)
