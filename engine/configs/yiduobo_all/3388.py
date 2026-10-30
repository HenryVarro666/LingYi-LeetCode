_st = {}


def _loop(key, text_done, text_new):
    def fn(S, B, ret):
        k = tuple(S.get(x) for x in key)
        done = _st.get(key) == k
        _st[key] = k
        return text_done if done else text_new(S)
    return fn


def _top(S):
    if 'res' not in S:
        if 'i' in S and 'j' in S:
            return f"`f[{S['i']}][{S['j']}]`：后缀 `nums[{S['i']}:]` 与 `nums[{S['j']}:]` 的最长公共前缀长度"
        return '`f[i][j]`：后缀 `nums[i:]` 与 `nums[j:]` 的最长公共前缀长度'
    if S['_line'] < 18:
        return '第二趟：枚举两个分割点 `i`、`j`，数一数有多少美丽分割'
    i, j, n = S['i'], S['j'], S['n']
    return f'三段：蓝 `nums[:{i}]` | 黄 `nums[{i}:{j}]` | 粉 `nums[{j}:]`'


def _color(S, k, v):
    if 'res' not in S or S['_line'] < 18:
        return None
    i, j = S['i'], S['j']
    return 'blue' if k < i else ('yellow' if k < j else 'pink')


def _gcolor(S, r, c, v):
    if 'i' not in S or 'j' not in S:
        return None
    i, j, n = S['i'], S['j'], S['n']
    if 'res' not in S:
        if S['nums'][i] == S['nums'][j] and i + 1 < n and j + 1 < n and (r, c) == (i + 1, j + 1):
            return 'blue'
        return None
    if S['_line'] >= 18 and (r, c) == (0, i):
        return 'cyan'
    return None


def _if1(S, B, ret):
    i, j, a = S.i, S.j, S.nums
    if a[i] == a[j]:
        return f'`nums[{i}] = {a[i]}` == `nums[{j}] = {a[j]}`：这一位相同，可以接在后面的匹配上'
    return f'`nums[{i}] = {a[i]}` ≠ `nums[{j}] = {a[j]}`：第一位就不同，`f[{i}][{j}]` 保持 0'


def _cond(S, B, ret):
    i, j, f = S.i, S.j, S.f
    c1 = f[0][i] >= i
    c2 = j - i >= i
    c3 = f[i][j] >= j - i
    p1 = f'`f[0][{i}] = {f[0][i]} >= {i}`（{"是" if c1 else "否"}）且 `j-i = {j - i} >= {i}`（{"是" if c2 else "否"}）'
    p2 = f'`f[{i}][{j}] = {f[i][j]} >= j-i = {j - i}`（{"是" if c3 else "否"}）'
    return f'nums1 是 nums2 前缀：{p1}；nums2 是 nums3 前缀：{p2} → ' + ('==美丽分割==' if (c1 and c2) or c3 else '不是')


CONFIG = dict(
    num=3388, title='统计数组中的美丽分割', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举分割点 + 后缀 LCP 动态规划',
    tags=['灵神题单', '字符串', '难度分 2365'],
    code='''
class Solution(object):
    def beautifulSplits(self, nums):
        
        n = len(nums)
        f = [[0] * n for _ in range(n)]

        for i in range(n - 2, -1, -1):
            for j in range(n - 1, i, -1):
                if nums[i] == nums[j]:
                    if j + 1 < n:
                        f[i][j] = f[i + 1][j + 1] + 1
                    else:
                        f[i][j] = 1
        
        res = 0
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if (f[0][i] >= i and j - i >= i) or f[i][j] >= j - i:
                    res += 1
                    
        return res
''',
    call='Solution().beautifulSplits([1,1,2,1])',
    expect=2,
    skip=['n = len(nums)', 'else:'],
    max_steps=90,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='nums', label='nums（第二趟：蓝 = nums1，黄 = nums2，粉 = nums3）', color=_color, pointers={'i': 'blue', 'j': 'pink'}, h=230),
        dict(type='grid', var='f', label='f[i][j]（行 i，列 j；黄框 = 当前格，蓝 = 依赖的 f[i+1][j+1]，青 = f[0][i]）', rows=lambda S: list(range(len(S['f']))),
             cols=lambda S: list(range(len(S['f']))), cursors=[('i', 'j', 'yellow')], color=_gcolor, cell=64, h=380),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = [[0]': '`f[i][j]` 是后缀 `nums[i:]` 与 `nums[j:]` 的==最长公共前缀长度==，先全填 0',
        'for i in range(n - 2': _loop(('i',), '`i` 都填完了，表完成', lambda S: f'从后往前填表：`i = {S.i}`（`f[i][j]` 依赖右下角的 `f[i+1][j+1]`）'),
        'for j in range(n - 1, i, -1)': _loop(('i', 'j'), '这一行填完', lambda S: f'`j = {S.j}`：比较后缀 `nums[{S.i}:]` 和 `nums[{S.j}:]`（只用 `j > i` 的上三角）'),
        'if nums[i] == nums[j]': _if1,
        'if j + 1 < n': lambda S, B, ret: (f'`j + 1 = {S.j + 1} < n`：右下角 `f[{S.i + 1}][{S.j + 1}]` 存在，可以接上去' if S.j + 1 < S.n
                                           else '`j + 1 = n`：`j` 已是最后一位，后面没有字符了，LCP 只能是 1'),
        'f[i][j] = f[i + 1][j + 1] + 1': '`f[{i}][{j}] = f[{i + 1}][{j + 1}] + 1 = {f[i][j]}`：后一位的 LCP 再加上这一位',
        'f[i][j] = 1': '`f[{i}][{j}] = 1`：只有最后一位相同',
        'res = 0': lambda S, B, ret: (_st.clear(), '表填好了。第二趟：枚举两个分割点，`res` 统计美丽分割数')[1],
        'for i in range(1, n - 1)': _loop(('i', 'ph2'), '`i` 都枚举完了', lambda S: f'第二段从 `i = {S.i}` 开始（`nums1 = nums[:{S.i}]`）'),
        'for j in range(i + 1, n)': _loop(('i', 'j', 'ph2'), '`j` 都枚举完了', lambda S: f'第三段从 `j = {S.j}` 开始：`nums2 = nums[{S.i}:{S.j}]`，`nums3 = nums[{S.j}:]`'),
        'if (f[0][i]': _cond,
        'res += 1': '这是一个美丽分割：`res` = =={res}==',
        'return res': '全部分割数完，答案 =={ret}==',
    },
    cards=dict(
        one_liner='先用 DP 预处理所有后缀的 LCP，再枚举两个分割点判断前缀关系',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['把 `nums` 分成三段非空子数组 `nums1`、`nums2`、`nums3`',
                 '`nums1` 是 `nums2` 的前缀，或者 `nums2` 是 `nums3` 的前缀，就是美丽分割',
                 '本视频：`[1,1,2,1]` → `4`（示例 1 是 `[1,1,2,1]` → `2`）'],
        quote='当f[0][i] >= i且j - i >= i，或者f[i][j] >= j - i时，i和j就是一个美丽分割。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：后缀 `nums[i:]` 与 `nums[j:]` 的最长公共前缀；相等就 `f[i+1][j+1] + 1`，否则 0',
              'nums1 是 nums2 的前缀：长度够（`j - i >= i`）且 `f[0][i] >= i`',
              'nums2 是 nums3 的前缀：`f[i][j] >= j - i`（LCP 够长，长度必然也够）'],
        result='`[1,1,2,1]` 共 4 个美丽分割 ✓',
        summary=['时间 `O(n^2)`，空间 `O(n^2)`；`n <= 5000` 刚好能过',
                 '填表必须从后往前，`f[i][j]` 依赖 `f[i+1][j+1]`',
                 '`j + 1 == n` 时没有右下角，单独写成 `f[i][j] = 1`',
                 '原文本来就能在 Python 3 运行，代码未改动',
                 '对比灵神：灵神方法二用 Z 数组把空间降到 `O(n)`；这里是二维 LCP 表'],
    ),
)
