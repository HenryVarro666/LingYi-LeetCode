def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    ln = S.get('_line')
    if i is None or j is None or 'zero_cnt' not in S:
        return None
    if ln == 15:
        if (r, c) == (i, j):
            return 'yellow'
        if (r, c) == (i - S['zero_cnt'], j - S['one_cnt']):
            return 'blue'
    elif ln == 20 and (r, c) == (i, j):
        return 'yellow'
    return None


def _formula(S):
    if 'zero_cnt' not in S:
        return '`f[i][j]` = 用 `i` 个 0、`j` 个 1 最多能拿几个字符串'
    if S.get('_line') in (6, 7):
        return f'轮到 `"{S["str"]}"`，先数它有几个 0、几个 1'
    base = f'`"{S["str"]}"`：花 `{S["zero_cnt"]}` 个 0、`{S["one_cnt"]}` 个 1'
    if S.get('_line') == 15:
        return base + f'；`f[{S["i"]}][{S["j"]}]` 对比 `f[{S["i"] - S["zero_cnt"]}][{S["j"] - S["one_cnt"]}] + 1`'
    if S.get('_line', 0) >= 17:
        return '最后扫一遍整张表，取最大值'
    return base


CONFIG = dict(
    num=474, title='一和零', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='背包变种 · 二维费用 + 滚动数组',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def findMaxForm(self, strs, m, n):

        f = [[0] * (n + 1) for _ in range(m + 1)]

        for str in strs:
            zero_cnt = one_cnt = 0
            for char in str:
                if char == '0':
                    zero_cnt += 1
                else:
                    one_cnt += 1
            for i in range(m, zero_cnt - 1, -1):
                for j in range(n, one_cnt - 1, -1):
                    f[i][j] = max(f[i][j], f[i - zero_cnt][j - one_cnt] + 1)
        
        res = 0
        for i in range(m + 1):
            for j in range(n + 1):
                res = max(f[i][j], res)
        
        return res
''',
    call='Solution().findMaxForm(["10", "001", "1", "0"], 2, 2)',
    expect=3,
    max_steps=95,
    skip=["if char ==", 'zero_cnt += 1', 'one_cnt += 1', 'else:', 'for i in range(m, zero', 'for j in range(n, one',
          'for i in range(m + 1)', 'for j in range(n + 1)'],
    views=[
        dict(type='array', var='strs', label='strs（蓝 = 当前字符串）', h=150, cell=90,
             color=lambda S, i, v: 'blue' if v == S.get('str') and 'zero_cnt' in S and S.get('_line', 0) < 17 else None),
        dict(type='text', fn=_formula, size=22, h=70),
        dict(type='table', var='f', label='f[i][j]：i 个 0、j 个 1 最多拿几个（黄 = 更新，蓝 = f[i-zero][j-one]）', h=330, cell=80,
             rows=lambda S: [f'{k}个0' for k in range(S['m'] + 1)], cols=lambda S: [f'{k}个1' for k in range(S['n'] + 1)],
             color=_cell),
    ],
    watch=[('str', 'str', 'blue'), ('zero_cnt', 'zero_cnt', 'cyan'), ('one_cnt', 'one_cnt', 'orange'),
           ('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = [[0]': '`f[i][j]`：花 `i` 个 0、`j` 个 1，最多拿几个字符串。一开始都是 0',
        'for str in strs': '轮到 `"{str}"`：拿它要花一些 0 和一些 1',
        'zero_cnt = one_cnt': '先把 0、1 的个数清零，再数字符',
        'for char in str': '逐个字符数 0 和 1：目前 `{zero_cnt}` 个 0、`{one_cnt}` 个 1',
        'f[i][j] = max': '`f[{i}][{j}]`：不拿 = `{B.f[i][j]}`；拿 = `f[{i - zero_cnt}][{j - one_cnt}] + 1` = `{B.f[i - zero_cnt][j - one_cnt] + 1}` → ==`{f[i][j]}`==',
        'res = 0': '`res` 记录整张表的最大值',
        'res = max': '`res = max(f[{i}][{j}], …)` = =={res}==',
        'return res': '答案 = ==`{res}`==',
    },
    cards=dict(
        one_liner='拿一个字符串要花「几个 0 + 几个 1」：二维背包',
        complexity='时间 `O(kmn+L)`，空间 `O(mn)`',
        problem=['给若干二进制字符串，以及 `m` 个 0 和 `n` 个 1',
                 '每个字符串拿一次，用掉它含的 0 和 1，问最多能拿几个字符串',
                 '示例：`["10","0001","111001","1","0"], m=5, n=3` → `4`；本视频：`["10","001","1","0"], m=2, n=2` → `3`'],
        quote='背包问题的变种。可以将问题看成，有若干个str，选择其中某个str需要花费x个0和y个1，现在给出一定量的0和1最多可以拿多少个str。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用三维 `f[i][j][k]`（前 `i` 个串）推导，转移 `f[i-1][j-zero][k-one] + 1`',
              '`i` 这一维只由 `i-1` 更新 → 滚动数组，只留 `f[i][j]`',
              '拿每个字符串时，`i`、`j` 都从大到小更新'],
        summary=['时间 `O(kmn+L)`，空间 `O(mn)`',
                 '易错：两层都要倒序，否则同一个字符串会被拿多次',
                 '`f[i][j]` 表示「至多」`i` 个 0、`j` 个 1，所以 `f[m][n]` 本身也是答案；yiduobo 扫了全表取最大',
                 '原文变量名 `str` 遮住了内置函数，但在这里不影响运行'],
    ),
)
