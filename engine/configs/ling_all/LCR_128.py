def _info(S):
    if 'left' not in S:
        return '开区间 `(left, right)`：`right` 始终是「当前数组最后一个数」的下标'
    if S['left'] + 1 >= S['right']:
        return f'区间空了：最小值就是 `nums[right] = {S["nums"][S["right"]]}`'
    return f'开区间 `({S["left"]}, {S["right"]})`，蓝格 = mid，粉格 = right，灰 = 已排除'


def _color(S, i, v):
    if 'right' not in S:
        return None
    if i == S['right']:
        return 'pink'
    if 'mid' in S and i == S['mid'] and S['left'] + 1 < S['right']:
        return 'blue'
    return None


def _dim(S, i, v):
    return 'right' in S and (i <= S['left'] or i > S['right'] and S['right'] >= 0 and False)


def _cmp(S, B, r):
    a, b = S.nums[S.mid], S.nums[S.right]
    if a == b:
        return f'`nums[{S.mid}] = {a}` == `nums[{S.right}] = {b}`：==无法判断在左还是右== → 去掉最后一个数，不会丢最小值'
    if a < b:
        return f'`nums[{S.mid}] = {a}` < `nums[{S.right}] = {b}`：mid 在右段（升序段），==最小值在 mid 或其左边=='
    return f'`nums[{S.mid}] = {a}` > `nums[{S.right}] = {b}`：mid 在左段，==最小值在 mid 右边=='


CONFIG = dict(
    num='LCR 128', title='库存管理 I', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='开区间二分 · 相等时 right 减一',
    tags=[],
    code='''
class Solution:
    def stockManagement(self, nums: List[int]) -> int:
        left, right = -1, len(nums) - 1  # 开区间 (-1, n-1)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if nums[mid] < nums[right]:  # 蓝色
                right = mid
            elif nums[mid] > nums[right]:  # 红色
                left = mid
            else:
                right -= 1
        return nums[right]
''',
    call='Solution().stockManagement([3, 3, 3, 1, 3, 3])',
    expect=1,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='nums', pointers={'left': 'blue', 'mid': 'yellow', 'right': 'pink'}, cell=96, h=330,
             color=_color, dim=lambda S, i, v: 'left' in S and i <= S['left']),
    ],
    watch=[('left', 'left', 'blue'), ('mid', 'mid', 'yellow'), ('right', 'right', 'pink')],
    captions={
        'left, right = -1': '开区间 `({left}, {right})`：`right` 当作数组最后一个数的下标',
        'while left + 1 < right': lambda S, B, r: (f'`{S.left} + 1 < {S.right}`，开区间里还有数' if S.left + 1 < S.right
                                                   else f'`{S.left} + 1 >= {S.right}`，开区间空了 → 结束'),
        'mid = (left + right)': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if nums[mid] < nums[right]': lambda S, B, r: f'`nums[{S.mid}] = {S.nums[S.mid]}` 与区间右端点 `nums[{S.right}] = {S.nums[S.right]}` 比：' + ('更小 → mid 在右段（蓝色）' if S.nums[S.mid] < S.nums[S.right] else '不更小，继续看别的情况'),
        'right = mid': '蓝色：最小值在 mid 或其左边 → `right = {right}`',
        'elif nums[mid] > nums[right]': lambda S, B, r: f'`{S.nums[S.mid]} > {S.nums[S.right]}`' + (' → 成立：mid 在左段（红色）' if S.nums[S.mid] > S.nums[S.right] else ' → 不成立：两者相等，走 else'),
        'left = mid': '红色：最小值在 mid 右边，`mid` 及左边都排除 → `left = {left}`',
        'right -= 1': '==相等==，无法确定在左还是右 → 干脆去掉右端点：它若是最小值，`nums[mid]` 也是最小值 → `right = {right}`',
        'return nums[right]': '区间空了，答案是 `nums[{right}]` = =={ret}==',
    },
    cards=dict(
        one_liner='和右端点比大小；相等无法判断，就去掉右端点',
        complexity='时间 `O(n)`（最坏全相同），空间 `O(1)`',
        problem=['库存表原本升序，现在把前面一段挪到了末尾（可能有重复 id）',
                 '找出表中最小的 id',
                 '本视频：`[3,3,3,1,3,3]` → `1`'],
        quote='当二分元素 nums[mid] 与区间右端点元素相同时，既然无法确定最小值所在区间，那么干脆去掉右端点元素，继续二分。对应到代码上，就是 right 减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums[mid]` 和右端点比：小于 → 蓝色（右段），大于 → 红色（左段）',
              '相等时左右都有可能，`right -= 1` 把问题缩小一格',
              '不会误删最小值：右端点是最小值时，`nums[mid]` 也是它'],
        summary=['时间 `O(n)`：全部相同时每轮只能 `right -= 1`',
                 '开区间写法：`left = -1`，`right = n-1`，返回 `nums[right]`',
                 '易错：要和右端点比，而不是和左端点比，左端点无法区分情形',
                 '前置题：153（无重复），本题多了相等时 `right -= 1`'],
    ),
)
