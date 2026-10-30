NUMS = [1, 2, 3, -1, 4]
MUL = [3, 2, -1, 1]


def _ij(S):
    I = S['_inner']
    return I.get('i'), I.get('j')


def _cell(S, r, c, v):
    i, j = _ij(S)
    ln = S.get('_line')
    if i is None or ln not in (8, 9, 11, 13, 14):
        return None
    if ln == 8:
        return 'yellow' if (r, c) == (0, 0) else None
    if ln == 9:
        return 'yellow' if (r, c) == (0, 1) else None
    if ln == 11:
        return 'yellow' if (r, c) == (i, 0) else ('blue' if (r, c) == (i - 1, 0) else None)
    if ln == 14:
        return 'yellow' if (r, c) == (i, i + 1) else ('green' if (r, c) == (i - 1, i) else None)
    if j is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) == (i - 1, j):
        return 'blue'
    if (r, c) == (i - 1, j - 1):
        return 'green'
    return None


def _ncolor(S, k, v):
    i, j = _ij(S)
    ln = S.get('_line')
    if i is None or ln not in (11, 13, 14):
        return None
    n = len(S['nums'])
    if ln == 11:
        return 'blue' if k == n - i - 1 else None
    if ln == 14:
        return 'green' if k == i else None
    if j is None:
        return None
    if k == j - 1:
        return 'green'
    if k == n - (i - j) - 1:
        return 'blue'
    return None


def _formula(S):
    i, j = _ij(S)
    ln = S.get('_line')
    if i is None or ln not in (8, 9, 11, 13, 14):
        return '`f[i][j]`：做了 `i+1` 步、其中 `j` 个数取自头部时的最大分数'
    nums, mul, n = S['nums'], S['multipliers'], len(S['nums'])
    if ln in (8, 9):
        return '第 1 步（`i = 0`）：只能取头或取尾，乘 `multipliers[0]`'
    if ln == 11:
        return f'`j = 0`：{i + 1} 个数全取自尾部，这步取 `nums[{n - i - 1}] = {nums[n - i - 1]}`'
    if ln == 14:
        return f'`j = i+1 = {i + 1}`：全取自头部，这步取 `nums[{i}] = {nums[i]}`'
    return (f'头：`f[{i - 1}][{j - 1}] + nums[{j - 1}]×mul[{i}]`　尾：`f[{i - 1}][{j}] + nums[{n - (i - j) - 1}]×mul[{i}]`')


CONFIG = dict(
    num=1770, title='执行乘法运算的最大分数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='线性 DP（状态=操作次数 × 头部用掉的个数）',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def maximumScore(self, nums, multipliers):

        n = len(nums)
        m = len(multipliers)

        f = [[0] * (m + 1) for _ in range(m)]
        f[0][0] = nums[n - 1] * multipliers[0]
        f[0][1] = nums[0] * multipliers[0]
        for i in range(1, m):
            f[i][0] = f[i - 1][0] + nums[n - i - 1] * multipliers[i]
            for j in range(1, i + 1):
                f[i][j] = max(f[i - 1][j] + nums[n - (i - j) - 1] * multipliers[i], f[i - 1][j - 1] + nums[j - 1] * multipliers[i])
            f[i][i + 1] = f[i - 1][i] + nums[i] * multipliers[i]
        
        return max(f[-1])
''',
    call=f'Solution().maximumScore({NUMS!r}, {MUL!r})',
    expect=18,
    skip=['for j in range', 'for i in range', 'n = len(nums)', 'm = len(multipliers)'],
    max_steps=70,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 这步取头部的数，蓝 = 取尾部的数）', h=150, cell=72, color=_ncolor),
        dict(type='array', var='multipliers', label='multipliers', h=185, cell=72, pointers={'i': 'pink'}),
        dict(type='text', fn=_formula, size=22, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，绿 = 取头部的来源，蓝 = 取尾部的来源）', h=250, cell=56,
             rows=lambda S: [f'i={k}' for k in range(len(S['multipliers']))],
             cols=lambda S: [f'j={k}' for k in range(len(S['multipliers']) + 1)],
             color=_cell),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'pink'), ('j', lambda S: S['_inner'].get('j'), 'blue')],
    captions={
        'f = [[0]': '`f[i][j]`：前 `i+1` 步里，==头部用掉 j 个数==时的最大分数；`m` 行 `m+1` 列，不用 `n × n`',
        'f[0][0] =': '第 1 步取尾部（`j = 0`）：`nums[{n-1}] × multipliers[0] = {nums[n-1]} × {multipliers[0]}` = =={f[0][0]}==',
        'f[0][1] =': '第 1 步取头部（`j = 1`）：`nums[0] × multipliers[0] = {nums[0]} × {multipliers[0]}` = =={f[0][1]}==',
        'f[i][0] =': '`j = 0`：前 {i+1} 步全取尾部，这步取 `nums[{n-i-1}] = {nums[n-i-1]}`：`f[{i}][0]` = `{f[i-1][0]} + {nums[n-i-1]}×{multipliers[i]}` = =={f[i][0]}==',
        'f[i][j] = max(': '`尾 = {f[i-1][j]} + {nums[n-(i-j)-1]}×{multipliers[i]}`，`头 = {f[i-1][j-1]} + {nums[j-1]}×{multipliers[i]}` → `f[{i}][{j}]` = =={f[i][j]}==',
        'f[i][i + 1] =': '`j = i+1`：前 {i+1} 步全取头部，这步取 `nums[{i}] = {nums[i]}`：`f[{i}][{i+1}]` = `{f[i-1][i]} + {nums[i]}×{multipliers[i]}` = =={f[i][i+1]}==',
        'return max(f[-1])': '最后一步所有 `j` 都是合法的拆分，取 `max(f[-1])` = `max({f[-1]})` = =={ret}==',
    },
    cards=dict(
        one_liner='状态不用 l、r：用「第几步」和「头部取了几个」',
        complexity='时间 `O(m^2)`，空间 `O(m^2)`',
        problem=['做 `m` 次操作，第 `i` 次从 `nums` 的==最左或最右==取一个数 `x`，得分 `x × multipliers[i]`，并把它删掉',
                 '求 `m` 次操作后的==最大总分==',
                 '示例：`[-5,-3,-3,-2,7,1]`，`[-10,-5,3,4,6]` → `102`',
                 '本视频：`[1,2,3,-1,4]`，`[3,2,-1,1]` → `18`'],
        quote='这里的区间长度n非常大，直接使用f[l][r]表示的话空间复杂度承受不住，必须另想办法。注意到操作次数m的规模是比较小的……',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：做了 `i+1` 步，其中 ==j 个数取自头部==',
              '尾部取的个数 = `i+1-j`，所以头尾位置都能算出来',
              '头：`f[i-1][j-1] + nums[j-1]×mul[i]`；尾：`f[i-1][j] + nums[n-(i-j)-1]×mul[i]`，取大'],
        summary=['时间 `O(m^2)`，空间 `O(m^2)`；`n` 很大但 `m ≤ 1000`',
                 '易错：`j = 0` 与 `j = i+1` 只有一个来源，要单独处理',
                 '易错：尾部下标 `n - (i - j) - 1`，别写成 `n - i - 1`',
                 '答案是最后一行的 `max`，不是 `f[-1][-1]`',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
