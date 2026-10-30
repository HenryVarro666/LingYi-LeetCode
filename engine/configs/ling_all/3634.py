NUMS = [1, 6, 2, 9, 4, 12]
K = 3


def _top(S):
    if 'i' not in S:
        return f'`k = {K}`：保留的元素要满足 ==最大值 ≤ 最小值 × k=='
    l, i = S['left'], S['i']
    a = S['nums']
    ok = a[l] * K >= a[i]
    return (f"窗口 `[{l}, {i}]`：最小 `{a[l]}` × {K} = `{a[l] * K}` "
            f"{'≥' if ok else '<'} 最大 `{a[i]}` → {'==平衡==' if ok else '不平衡，left 右移'}")


def _color(S, i, v):
    if 'i' not in S:
        return None
    if i == S['i']:
        return 'pink'
    if S['left'] <= i < S['i']:
        return 'blue'
    return None


def _dim(S, i, v):
    return 'i' in S and i < S['left']


def _while(S, B, ret):
    a, l = S.nums, S.left
    if a[l] * S.k < S.mx:
        return f'`nums[{l}] × k = {a[l] * S.k} < mx = {S.mx}`：最小值太小，==它必须被移除== → left 右移'
    return f'`nums[{l}] × k = {a[l] * S.k} ≥ mx = {S.mx}`：窗口平衡，停止移动'


CONFIG = dict(
    num=3634, title='使数组平衡的最少移除数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 不定长滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1453'],
    code='''
class Solution:
    def minRemoval(self, nums: List[int], k: int) -> int:
        nums.sort()
        max_save = left = 0
        for i, mx in enumerate(nums):
            while nums[left] * k < mx:
                left += 1
            max_save = max(max_save, i - left + 1)
        return len(nums) - max_save
''',
    call=f'Solution().minRemoval({NUMS}, {K})',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=28, h=90),
        dict(type='array', var='nums', label='nums（排序后；框 = 保留的窗口，粉 = 当前最大值 mx）',
             pointers={'left': 'blue', 'i': 'pink'}, window=('left', 'i'), color=_color, dim=_dim, cell=120, h=320),
    ],
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), 'mx', ('max_save', 'max_save', 'green')],
    captions={
        'nums.sort()': '只关心最小值和最大值，与顺序无关 → ==先排序==：`{nums}`',
        'max_save = left': '`max_save`：最多能保留几个；窗口左端 `left = 0`',
        'for i, mx in': lambda S, B, r: ('枚举完毕' if 'i' in B and B.i == S.i
                                         else f'枚举最大值 `mx = nums[{S.i}] = {S.mx}`'),
        'while nums[left]': _while,
        'left += 1': '`left` → {left}：更小的数都要移除',
        'max_save = max': '窗口 `[{left}, {i}]` 长 `{i - left + 1}`：`max_save = max({B.max_save}, {i - left + 1})` = =={max_save}==',
        'return len': '保留 `{max_save}` 个，移除 `{len(nums)} − {max_save}` = =={ret}== 个',
    },
    cards=dict(
        one_liner='排序后保留的是一段连续区间：枚举最大值，滑窗找最小值',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['从 `nums` 移除若干元素，使剩余 ==最大值 ≤ 最小值 × k==',
                 '求最少移除几个（不能删空）',
                 '示例：`[1,6,2,9], k = 3` → `2`；本视频 `[1,6,2,9,4,12], k = 3` → `2`'],
        quote='在 [mn,mx] 中的元素保留，其余元素去掉。由于排序了，所以这些元素在数组中是==连续==的，问题转化成一个标准的==滑动窗口==模型。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举最大值 `mx = nums[i]`，最小值 `nums[left]` 须满足 `nums[left] × k ≥ mx`',
              '`mx` 变大时合法的 `left` 只会右移 → 越短越合法的滑窗',
              '最少移除 = `n − 最多保留`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；滑窗部分 `O(n)`',
                 '用乘法 `nums[left] * k < mx` 判断，避免除法精度问题',
                 '窗口里至少有 `nums[i]` 自己，`left` 不会越过 `i`',
                 '答案是 `len(nums) − max_save`，别直接返回窗口长度'],
    ),
)
