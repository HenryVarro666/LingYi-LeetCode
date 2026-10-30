def _two(S):
    nums = S['nums']
    idx = sorted(range(1, len(nums)), key=lambda i: (nums[i], i))[:2]
    return idx


def _txt(S):
    nums = S['nums']
    a, b = _two(S)
    return f'第一段起点固定 `nums[0] = {nums[0]}`；下标 1..n-1 里最小的两个：`{nums[a]}`、`{nums[b]}` → ==总代价 {nums[0] + nums[a] + nums[b]}=='


CONFIG = dict(
    num=3010, title='将数组分成最小总代价的子数组 I', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='取下标 1.. 中最小的两个数',
    tags=['贪心与思维', '难度分 1292'],
    code='''
class Solution:
    def minimumCost(self, nums: List[int]) -> int:
        return nums[0] + sum(nsmallest(2, nums[1:]))
''',
    setup='from heapq import nsmallest',
    call='Solution().minimumCost([7,5,4,9,1,6,2])',
    expect=10,
    views=[
        dict(type='text', h=110, size=30, fn=_txt),
        dict(type='array', var='nums', label='nums（绿 = 第一段起点，黄 = 另外两段的起点）', cell=100, h=230,
             color=lambda S, i, v: 'green' if i == 0 else ('yellow' if i in _two(S) else None),
             dim=lambda S, i, v: i != 0 and i not in _two(S)),
    ],
    watch=[('nums[0]', 'nums[0]', 'green'), ('最小两个', 'nsmallest(2, nums[1:])', 'yellow')],
    captions={
        'return nums[0]': '`nums[0] = {nums[0]}` 一定是第一段的代价；再从 `nums[1:]` 取最小的两个 `{nsmallest(2, nums[1:])}` 当另外两段的起点 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='第一段起点固定，另两段起点在后面随便选：取最小的两个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 分成 3 段连续子数组，每段的代价是它的==第一个元素==',
                 '求三段代价之和的最小值',
                 '本视频：`[7,5,4,9,1,6,2]` → `10`（7 + 1 + 2）'],
        quote='第一段的第一个数是确定的，即 nums[0]。……这两个下标可以在 [1,n-1] 中随意取。所以问题变成求下标在 [1,n-1] 中的两个最小的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一段必从下标 0 开始，代价固定为 `nums[0]`',
              '后两段的起点是下标 `[1, n-1]` 里任意两个不同位置，划分方案随之唯一确定',
              '要总和最小，就直接选这些位置上最小的两个数'],
        after=[dict(heading='为什么可以随便选', lines=['第二段起点 `i`、第三段起点 `j`（`1 ≤ i < j ≤ n-1`）决定一种划分', '总代价 = `nums[0] + nums[i] + nums[j]`', '`i`、`j` 互不约束 → 直接取最小的两个值，位置顺序无所谓', '例：`[7,5,4,9,1,6,2]` 取 1 和 2，划成 `[7,5,4,9]`、`[1,6]`、`[2]`']),
               ],
        summary=['时间 `O(n)`（`nsmallest(2, …)` 一趟扫描），空间 `O(1)`',
                 '易错：最小值要从 `nums[1:]` 里找，`nums[0]` 不参与选择',
                 '方法一直接排序 `nums[0] + sum(sorted(nums[1:])[:2])`，`O(n log n)`，本视频选线性写法',
                 '`nsmallest` 来自 heapq，这里在 setup 里导入'],
    ),
)
