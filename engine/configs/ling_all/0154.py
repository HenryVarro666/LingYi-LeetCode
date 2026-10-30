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
    num=154, title='寻找旋转排序数组中的最小值 II', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='开区间二分 · 相等时 right 减一',
    tags=['灵神题单'],
    code='''
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = -1, len(nums) - 1  # 开区间 (-1, n-1)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if nums[mid] == nums[right]:
                right -= 1
            elif nums[mid] < nums[right]:
                right = mid
            else:
                left = mid
        return nums[right]
''',
    call='Solution().findMin([2, 2, 2, 0, 1, 2, 2])',
    expect=0,
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
        'if nums[mid] == nums[right]': _cmp,
        'right -= 1': '去掉 `nums[right]`：它要么不是最小值，要么 `nums[mid]` 也是最小值 → `right = {right}`',
        'elif nums[mid] < nums[right]': lambda S, B, r: f'不相等，比大小：`{S.nums[S.mid]} < {S.nums[S.right]}` → ' + ('成立，看右段' if S.nums[S.mid] < S.nums[S.right] else '不成立，走 else'),
        'right = mid': '右边 `mid` 之后的数都不会更小 → `right = {right}`',
        'left = mid': '最小值在 mid 右边，`mid` 及左边全部排除 → `left = {left}`',
        'return nums[right]': '区间空了，答案是 `nums[{right}]` = =={ret}==',
    },
    cards=dict(
        one_liner='相等时无法判断，就干脆去掉最后一个数',
        complexity='时间 `O(n)`（最坏全相同），空间 `O(1)`',
        problem=['升序数组旋转若干次，元素可能重复，找最小值',
                 '和 153 题的区别：允许重复',
                 '本视频：`[2,2,2,0,1,2,2]` → `0`'],
        quote='既然无法确定最小值所在区间，那么干脆去掉 nums 的最后一个数，继续二分。',
        quote_src='—— 灵茶山艾府题解',
        idea=['拿 `nums[mid]` 和==最后一个数==比：小于 → 在右段，大于 → 在左段',
              '相等时左右都有可能 → `right -= 1`，规模变成 `n-1` 的子问题',
              '不会误删最小值：被删的若是最小值，`nums[mid]` 也是最小值'],
        summary=['时间 `O(n)`：全部相同时每轮只能 `right -= 1`；平均仍接近 `O(log n)`',
                 '易错：`right` 是最后一个数的下标，所以相等时是 `right -= 1`',
                 '开区间写法：`left = -1`，`right = n-1`，返回 `nums[right]`',
                 '同类题：153. 寻找旋转排序数组中的最小值（无重复，不用处理相等）'],
    ),
)
