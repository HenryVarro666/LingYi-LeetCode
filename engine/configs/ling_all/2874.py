_K = 'nums.index(x) if _line != 8 else None'


def _col(S, i, v):
    if 'x' not in S or S.get('_line') == 8:
        return None
    k = S['nums'].index(S['x'])
    if i == k:
        return 'blue'
    return None


def _txt(S):
    if 'x' not in S:
        return '枚举 k：答案 = ==k 左边的最大差值== × `nums[k]`'
    return (f"`pre_max = {S['pre_max']}`（左边最大值）　"
            f"`max_diff = {S['max_diff']}`（左边最大差）")


CONFIG = dict(
    num=2874, title='有序三元组中的最大值 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举 k · 维护 max_diff 与 pre_max',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1583'],
    code='''
class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        ans = max_diff = pre_max = 0
        for x in nums:
            ans = max(ans, max_diff * x)
            max_diff = max(max_diff, pre_max - x)
            pre_max = max(pre_max, x)
        return ans
''',
    call='Solution().maximumTripletValue([5,12,6,1,2,7,10])',
    expect=110,
    views=[
        dict(type='bars', var='nums', label='nums（x = 当前枚举的 nums[k]）', pointers={_K: 'blue'}, pointer_labels={_K: 'x'}, h=400,
             color=_col, dim=lambda S, i, v: 'x' in S and S.get('_line') != 8 and i > S['nums'].index(S['x'])),
        dict(type='text', fn=_txt, h=90, size=28),
    ],
    watch=[('x', 'x', 'blue'), ('pre_max', 'pre_max', 'orange'), ('max_diff', 'max_diff', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = max_diff = pre_max = 0': '三个变量都从 0 开始：答案至少是 0',
        'for x in nums': lambda S, B, r: ('遍历结束' if B.get('x') == S.x else f'枚举 `x = {S.x}`，依次把它当作 k、j、i'),
        'ans = max(ans': lambda S, B, r: (f'x 当 ==k==：`max_diff` 是==左边==的最大差值，`{S.max_diff} × {S.x} = {S.max_diff * S.x}` → `ans = {S.ans}`'),
        'max_diff = max': lambda S, B, r: (f'x 当 ==j==：`pre_max` 还不含 x，`{S.pre_max} − {S.x} = {S.pre_max - S.x}` → `max_diff = {S.max_diff}`'),
        'pre_max = max': '最后把 x 当 ==i==：`pre_max = max({B.pre_max}, {x}) = {pre_max}`',
        'return ans': '最大值为 `{ans}`',
    },
    cards=dict(
        one_liner='先更新 ans，再更新 max_diff，最后更新 pre_max',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `i < j < k` 时 `(nums[i] − nums[j]) * nums[k]` 的最大值，全为负数则返回 `0`',
                 '示例：`[12,6,1,2,7]` → `77`',
                 '本视频：`[5,12,6,1,2,7,10]` → `(12 − 1) × 10 = 110`'],
        quote='ans 依赖 maxDiff，maxDiff 依赖 preMax。如果修改更新顺序，那么 maxDiff 或者 preMax 会包含当前元素，就==不是左边元素的计算结果了==，这违反了题目 i<j<k 的规定。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 k：需要 k 左边 `nums[i] − nums[j]` 的最大值 `max_diff`',
              '类似 121. 买卖股票：算最大差值要维护左边最大值 `pre_max`',
              '更新顺序 ans → max_diff → pre_max，保证都是==左边==的值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：三行顺序不能换，否则会用到当前元素自己',
                 '方法一：枚举 j，预处理后缀最大值 `suf_max`，空间 `O(n)`',
                 '初值 0 很巧：`max_diff ≥ 0`，答案自动不小于 0'],
    ),
)
