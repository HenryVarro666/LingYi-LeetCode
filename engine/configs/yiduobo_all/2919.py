NUMS = [3, 1, 0, 2, 5, 6]
K = 4


def _i(S):
    if 'v' in S:
        return S['nums'].index(S['v'])
    return None


def _txt(S):
    if 'f' not in S:
        return '`f` / `g` / `h` = 以 `index`、`index-1`、`index-2` 结尾且该位 `>= k` 的最小修改次数'
    return f"`f = {S['f']}`（最新一位），`g = {S['g']}`（前一位），`h = {S['h']}`（前两位）"


CONFIG = dict(
    num=2919, title='使数组变美的最小增量运算数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='以某位 >= k 结尾的 DP · 三变量',
    tags=['灵神题单', '动态规划', '难度分 2031'],
    code='''
class Solution(object):
    def minIncrementOperations(self, nums, k):

        f = k - min(k, nums[2])
        g = k - min(k, nums[1])
        h = k - min(k, nums[0])
        
        for v in nums[3:]:
            delta = k - min(k, v)
            f, g, h = min(f, g, h) + delta, f, g
        
        return min(f, g, h)
''',
    call=f'Solution().minIncrementOperations({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='array', var='nums', label=f'nums（k = {K}）', cell=96, h=190,
             color=lambda S, j, v: 'blue' if j == _i(S) else None),
        dict(type='array', var=lambda S: [S['h'], S['g'], S['f']] if 'f' in S else [0, 0, 0],
             label='h（前两位） | g（前一位） | f（最新一位）', cell=120, h=200, index=False,
             color=lambda S, j, v: 'green' if j == 2 else None),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('v', 'v', 'blue'), ('delta', 'delta', 'orange'), ('f', 'f', 'green'), ('g', 'g', 'cyan'), ('h', 'h', 'purple')],
    captions={
        'f = k - min': '前 3 个数里只要有一个 `>= k` 就行：`f` = 第 3 位（下标 2）改到 k 的代价 `{f}`',
        'g = k - min': '`g` = 下标 1 作为那个 `>= k` 的数的代价 `{g}`',
        'h = k - min': '`h` = 下标 0 的代价 `{h}`',
        'for v in nums[3:]': '从下标 3 开始往后：`v = {v}`',
        'delta =': '把 `{v}` 改到 `>= k` 的代价：`k - min(k, v)` = ==`{delta}`==（本来就够就是 0）',
        'f, g, h =': '新的 `f` = 前三个状态取最小 `min(f, g, h)` + `delta`（旧值都能衔接：它们覆盖的窗口间隔不超过 2）→ ==`{f}`==；`g, h` 顺延',
        'return min': '最后三位都可能是最后一个 `>= k` 的数，答案取 `min(f, g, h)` = =={ret}==',
    },
    cards=dict(
        one_liner='只看长度为 3 的窗口：状态 = 以哪位 >= k 结尾',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可把一个数加 1；要让所有长度 ≥ 3 的子数组最大值都 `>= k`',
                 '求最少的加 1 次数',
                 f'本视频：`nums = {NUMS}`，`k = {K}`'],
        quote='所有大于等于3的子数组至少包含了一个长度为3的子数组，而所有长度为3的子数组中存在一个大于等于k的数时，其中的最大值也必然大于等于k',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]`：前缀满足要求，且 `nums[index] >= k`（必要时改到 k）的最小次数',
              '`f[index] = min(f[index-1], f[index-2], f[index-3]) + 代价`：上一个 `>= k` 的位置距离不能超过 3',
              '前 3 位里至少有一个 `>= k`，作为初始值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：答案是 `min(f, g, h)`，不是只取最后一位 `f`',
                 '初始化要处理前三位，循环从下标 3 开始',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神状态是“右边连续没增大的个数”；这里是“以哪位 >= k 结尾”'],
    ),
)
