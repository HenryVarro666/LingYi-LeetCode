S0 = '1100101'


def _col(S, k, v):
    if 'index' not in S or 'now' not in S:
        return None
    return 'blue' if k == S['index'] else ('green' if k < S['index'] else None)


def _fx(S):
    if 'left' not in S or 'now' not in S or S.get('_line') != 12:
        return '`cost = n−1 + (i − 2·sum[i−1]) + (2·sum[j] − j)`：`left` 记录前一项的最小值'
    j, now, left, n = S['index'], S['now'], S['left'], S['n']
    return f'`left + 2·now − j + n − 1` = `{left} + {2 * now} − {j} + {n - 1}` = =={left + 2 * now - j + n - 1}=='


CONFIG = dict(
    num=2167, title='移除所有载有违禁货物车厢所需要的最少时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前缀和 · 拆式子后维护最小值',
    tags=['其他线性 DP', '前后缀分解', '难度分 2219'],
    code='''
class Solution(object):
    def minimumTime(self, s):

        n = len(s)
        res = n
        now = 0
        left = n

        for index, char in enumerate(s):
            left = min(left, index - now - now)
            now += int(char)
            res = min(res, left + now + now - index + n - 1)
        
        return res
''',
    call=f'Solution().minimumTime({S0!r})',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前 j，绿 = 已枚举过）', h=200, cell=84, pointers={'index': 'blue'}, color=_col),
        dict(type='text', fn=_fx, size=28, h=70),
    ],
    watch=[('j', 'index', 'blue'), ('now', 'now', 'green'), ('left', 'left', 'pink'), ('res', 'res', 'orange')],
    captions={
        'n = len(s)': '`n = {n}`',
        'res = n': '`res` 初值取 `n`：==全部车厢都当前缀或后缀删==的代价；这样能避开「全按中间删」的错误情况',
        'now = 0': '`now` = `sum[j]`，前 `j+1` 节的违禁车厢数；用一个变量滚动代替前缀和数组',
        'left = n': '`left` = `i − 2·sum[i−1]` 的最小值（`i ≤ j`）',
        'for index, char': '枚举右端点 `j = {index}`，`s[{index}] = {char}`',
        'left = min(left, index - now - now)': '`left = min({B.left}, {index} − 2×{now})` = =={left}==：此时 `now = sum[j−1]`，把 `i = j` 也并入候选',
        'now += int(char)': '`now` += `{char}` → `sum[{index}]` = =={now}==',
        'res = min(res': '`cost = {left} + 2×{now} − {index} + {n - 1}` = `{left + now + now - index + n - 1}`，`res` → =={res}==',
        'return res': '所有 `j` 都枚举完，最少耗时 =={ret}==',
    },
    cards=dict(
        one_liner='把总代价拆成只含 i 和只含 j 的两项，固定 j 后维护 i 那项的最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['列车 `0/1` 串，`1` 表示违禁货物，必须全部清掉',
                 '删两端每节 1，删中间每节 2',
                 '示例：`"1100101"` → `5`'],
        quote='cost = n - 1 + (i - 2 * sum[i - 1]) + (2 * sum[j] - j)',
        quote_src='—— yiduobo 题解原文',
        idea=['答案 = 删前缀 `[0,i-1]` + 删后缀 `[j+1,n-1]` + 中间 `[i,j]` 每个 1 付 2',
              '中间的 1 的个数用前缀和 `sum` 相减；代价整理成 `n−1` + 只含 i 的项 + 只含 j 的项',
              '枚举 `j`，`left` 滚动记录 `i − 2·sum[i−1]` 的最小值，一趟 `O(n)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 初值必须是 `n`：当 `i = 0, j = n−1` 会把所有车厢当「中间」按 2 删，是错误情形',
                 '先更新 `left`（用 `sum[j−1]`），再 `now += s[j]`，最后算答案，顺序不能换',
                 '灵神用 `pre` 的 DP，yiduobo 用前缀和推式子，结果相同',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行'],
    ),
)
