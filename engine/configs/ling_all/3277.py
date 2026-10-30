NUMS = [2, 8, 4, 32, 16]
QS = [[0, 2], [1, 4], [0, 4]]


def _mc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line', 0) < 8:
        return 'green' if (i is not None and S.get('_line', 0) >= 6 and r == i and c == i) else None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i + 1, j), (i, j - 1)):
        return 'blue'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line', 0) < 8:
        return '`f[i][j]` = 区间 `[i, j]` 的「异或值」；`mx[i][j]` = 区间内所有子数组异或值的最大值'
    f = S['f']
    return f'`f[{i}][{j}] = f[{i}][{j-1}] ^ f[{i+1}][{j}]`；`mx[{i}][{j}] = max(f[{i}][{j}], mx[{i+1}][{j}], mx[{i}][{j-1}])`'


CONFIG = dict(
    num=3277, title='查询子数组最大异或分数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP（f 原地压缩成一维）',
    tags=['灵神题单', '动态规划', '难度分 2693'],
    code='''
class Solution:
    def maximumSubarrayXor(self, f: List[int], queries: List[List[int]]) -> List[int]:
        n = len(f)
        mx = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            mx[i][i] = f[i]
            for j in range(i + 1, n):
                f[j] ^= f[j - 1]
                mx[i][j] = max(f[j], mx[i + 1][j], mx[i][j - 1])
        return [mx[l][r] for l, r in queries]
''',
    call=f'Solution().maximumSubarrayXor({NUMS!r}, {QS!r})',
    expect=[12, 60, 60],
    skip=['n = len(f)', 'for j in range'],
    views=[
        dict(type='array', var='f', label='f（蓝 = i，粉 = j）：压缩后 f[j] 表示区间 [i, j] 的异或值', h=210, cell=84,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='mx', label='mx[i][j]（黄 = 正在算，蓝 = 它依赖的格子）', h=330, cell=56,
             rows=lambda S: [f'{k}' for k in range(5)], cols=lambda S: [f'{k}' for k in range(5)], color=_mc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'mx = [[0]': '`mx[i][j]`：下标 `i..j` 内所有子数组「异或值」的最大值，先全 0',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：==i 倒序==，算 `mx[i][·]` 要先有 `mx[i+1][·]`' if S.get('i') != B.get('i')
                                           else '所有区间都算完了，下面回答询问'),
        'mx[i][i] = f[i]': '单个元素的异或值就是它自己：`mx[{i}][{i}] = {f[i]}`',
        'f[j] ^= f[j - 1]': '`f[{j}]` 原来是 `f[{i+1}][{j}]`，异或上 `f[{i}][{j-1}]`（即 `f[{j-1}]`）→ `f[{i}][{j}]` = =={f[j]}==（区间 `[{i},{j}]` 的异或值）',
        'mx[i][j] = max': '`mx[{i}][{j}] = max({f[j]}, {mx[i+1][j]}, {mx[i][j-1]})` = =={mx[i][j]}==：取整段 / 去掉左端 / 去掉右端 三者最大',
        'return [mx': '每个询问 `[l, r]` 直接查 `mx[l][r]` → =={ret}==',
    },
    cards=dict(
        one_liner='两个区间 DP：先算区间异或值，再算区间内最大值',
        complexity='时间 `O(n^2 + q)`，空间 `O(n^2)`',
        problem=['数组的「异或分数」：反复让 `a[i] = a[i] ^ a[i+1]` 并删掉末尾，直到只剩一个数',
                 '每个询问 `[l, r]`：求 `nums[l..r]` 里==所有子数组异或分数的最大值==',
                 '示例：`[2,8,4,32,16,1]`，询问 `[[0,2],[1,4],[0,5]]` → `[12,60,60]`'],
        quote='可以发现，ab³c³d 相当于数组 [a,b,c] 的异或值，再异或 [b,c,d] 的异或值。',
        quote_src='—— 灵茶山艾府题解（数组的异或值）',
        idea=['第一个区间 DP：`f[i][j] = f[i][j-1] ^ f[i+1][j]`',
              '第二个区间 DP：`mx[i][j] = max(f[i][j], mx[i+1][j], mx[i][j-1])`',
              '优化：去掉 `f` 的第一维，直接拿 `nums` 当 `f`，`f[j] ^= f[j-1]`'],
        summary=['时间 `O(n^2 + q)`，空间 `O(n^2)`',
                 '易错：`i` 倒序、`j` 正序；原地修改后 `f[j-1]` 已经是区间 `[i, j-1]` 的值',
                 '原地写法会改写输入 `nums`，只能用一遍',
                 '灵神还给了未压缩 `f` 二维的版本和另一种 Python 写法，这里用压缩版',
                 '思考题：只求整个数组的异或值，可用 Lucas 定理做到 `O(n)`'],
    ),
)
