NUMS = [2, 8, 4, 32, 16]
QS = [[0, 2], [1, 4], [0, 4]]


def _gc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 12:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if i != j and (r, c) in ((i + 1, j), (i, j - 1)):
        return 'blue'
    return None


def _fc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 12:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if i != j and (r, c) in ((i + 1, j), (i, j - 1)):
        return 'blue'
    return None


CONFIG = dict(
    num=3277, title='查询子数组最大异或分数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按长度枚举的区间 DP',
    tags=['灵神题单', '动态规划', '难度分 2693'],
    code='''
class Solution(object):
    def maximumSubarrayXor(self, nums, queries):

        n = len(nums)
        f = [[0] * n for _ in range(n)]
        g = [[0] * n for _ in range(n)]
        for length in range(1, n + 1):
            for i in range(n):
                j = i + length - 1
                if j >= n:
                    break
                if i == j:
                    f[i][j] = nums[i]
                    g[i][j] = nums[i]
                else:
                    f[i][j] = f[i + 1][j] ^ f[i][j - 1]
                    g[i][j] = max(f[i][j], g[i + 1][j], g[i][j - 1])

        res = []
        for x, y in queries:
            res.append(g[x][y])
        
        return res
''',
    call=f'Solution().maximumSubarrayXor({NUMS!r}, {QS!r})',
    expect=[12, 60, 60],
    skip=['n = len(nums)', 'for i in range', 'if j >= n', 'break', 'j = i + length', 'if i == j', 'else:', 'res = []', 'for x, y in', 'g[i][j] = nums[i]'],
    views=[
        dict(type='table', var='f', label='f[i][j]：nums[i..j] 的异或值（黄 = 正在算，蓝 = 依赖）', h=290, cell=52,
             rows=lambda S: [str(k) for k in range(5)], cols=lambda S: [str(k) for k in range(5)], color=_fc),
        dict(type='table', var='g', label='g[i][j]：nums[i..j] 内所有子数组异或值的最大值', h=290, cell=52,
             rows=lambda S: [str(k) for k in range(5)], cols=lambda S: [str(k) for k in range(5)], color=_gc),
        dict(type='array', var='res', label='res（每个询问的答案）', h=130, cell=90),
    ],
    watch=[('length', 'length', 'orange'), ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'f = [[0]': '`f[i][j]`：区间 `[i, j]` 的异或值',
        'g = [[0]': '`g[i][j]`：区间 `[i, j]` 内任意子数组异或值的最大值',
        'for length in range': lambda S, B, r: (f'`length = {S.length}`：==按区间长度从短到长==，长区间依赖的短区间都已算好'
                                                if S.get('length') != B.get('length') else '长度枚举完毕，所有区间都算好了'),
        'f[i][j] = nums[i]': '长度 1：`f[{i}][{j}] = {nums[i]}`，最大值 `g[{i}][{j}]` 也是它',
        'f[i][j] = f[i + 1][j] ^': '`f[{i}][{j}] = f[{i+1}][{j}] ^ f[{i}][{j-1}]` = `{f[i+1][j]} ^ {f[i][j-1]}` = =={f[i][j]}==（`i` 与 `j` 地位对称）',
        'g[i][j] = max': '`g[{i}][{j}] = max({f[i][j]}, {g[i+1][j]}, {g[i][j-1]})` = =={g[i][j]}==：整段、起点后移、终点前移',
        'res.append': '询问 `[{x}, {y}]`：直接取 `g[{x}][{y}]` = =={g[x][y]}==',
        'return res': '全部询问答案：=={ret}==',
    },
    cards=dict(
        one_liner='数据 n≤2000，开 O(n²) 区间 DP：f 求异或值，g 求最大值',
        complexity='时间 `O(n^2 + q)`，空间 `O(n^2)`',
        problem=['数组的异或值：对除最后一个外每个 `a[i] ^= a[i+1]`，删掉最后一个，直到只剩一个数',
                 '每个询问 `[l, r]`：求 `nums[l..r]` 中任意子数组异或值的==最大值==',
                 '本视频：`[2,8,4,32,16]`，询问 `[[0,2],[1,4],[0,4]]` → `[12,60,60]`'],
        quote='因为i和j在计算nums[i : j + 1]的异或值时处于完全对称的地位，而nums[i]参与的运算结果刚好就是f[i][j - 1]，因此nums[j]参与的运算结果一定是f[i + 1][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：除开 `nums[j]` 的运算刚好是 `f[i][j-1]`；对称地，`nums[i]` 的贡献是 `f[i+1][j]`',
              '所以 `f[i][j] = f[i+1][j] ^ f[i][j-1]`',
              '`g[i][j]` 取三者最大：以 `i..j` 为整段、起点大于 `i`、终点小于 `j`',
              '实现按==区间长度==从小到大枚举'],
        summary=['时间 `O(n^2 + q)`，空间 `O(n^2)`',
                 '易错：必须先枚举长度，保证依赖的两个短区间已算好',
                 '`f[i][j]` 的转移是 `^`，不是 `+`；`g` 才用 `max`',
                 '原文为 Python 2 风格，代码未做修改即可在 Python 3 运行',
                 '对比灵神：灵神 `i` 倒序 + 一维压缩 `f`；yiduobo 按长度枚举，保留完整二维 `f`'],
    ),
)
