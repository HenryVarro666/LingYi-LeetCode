NUMS = [4, 5, 6, 7, 0, 1, 2]
BARS_H, CELL = 450, 110


def _ref_line(cv, S, B, box, T):
    """dashed line at the height of nums[right] (moves with right), drawn over the bars view above"""
    if 'right' not in S:
        return
    nums, r = S['nums'], S['right']
    n = len(nums)
    x0, y0, x1, y1 = box
    top, base = y0 - BARS_H + 40, y0 - (26 + 27 * 3) - 30
    sc = (base - top - 34) / max(nums)
    width = x1 - x0 - 40
    c = max(24, min(CELL, width / n))
    sx = x0 + 20 + (width - c * n) / 2
    y = base - nums[r] * sc
    cv.dashed((sx - 6, y), (sx + c * n + 6, y), T['pink'], 3)
    cv.text((sx - 10, y), f'nums[r]={nums[r]}', 19, T['pink'], anchor='rm', bold=True)


def _state(S):
    if 'right' not in S:
        return ''
    l, r = S['left'], S['right']
    s = f"范围 `[{l}, {r}]`"
    if 'mid' in S and l < r:
        x, y = S['nums'][S['mid']], S['nums'][r]
        s += f"   ·   nums[mid] = =={x}== {'>' if x > y else '<'} nums[right] = {y}"
    elif l == r:
        s += '：只剩一个数'
    return s


def _while(S, B, ret):
    if B.left < B.right:
        return f'`left = {B.left} < right = {B.right}`：范围里不止一个数 → 继续'
    return f'`left == right == {B.left}`：只剩一个数，==它就是最小值== → 结束'


def _cmp(S, B, ret):
    x, y = S.nums[S.mid], S.nums[S.right]
    if x > y:
        return f'`{x} > nums[right] = {y}`：mid+1 到 right 之间有一段是==最小的那部分被旋转过来了==，答案就在其中'
    return f'`{x} < nums[right] = {y}`：mid 到 right 保持升序，==nums[mid+1..right] 都比 nums[mid] 大==，答案不在其中'


CONFIG = dict(
    num=153, title='寻找旋转排序数组中的最小值', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='和区间右端 nums[right] 比较 · 二分',
    code='''
class Solution(object):
    def findMin(self, nums):
        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
''',
    call=f'Solution().findMin({NUMS})',
    expect=0,
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='bars', var='nums', pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             window=('left', 'right'), cell=CELL, h=BARS_H,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: 'green' if 'right' in S and S['left'] == S['right'] == i else None),
        dict(type='custom', draw=_ref_line, h=4),
        dict(type='text', size=24, h=80, lines=2,
             text='粉色虚线 = ==nums[right]==（图中简写 `nums[r]`），每轮拿 `nums[mid]` 和它比\n灰色 = 已排除的部分'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('nums[mid]', 'nums[mid]'), ('nums[right]', 'nums[right]', 'pink')],
    captions={
        'left = 0': '`left = 0`：从整个数组开始',
        'right = len(nums)': '范围 `[{left}, {right}]`：最小值一定在里面',
        'while left < right': _while,
        'mid = (left + right)': '`mid = ({left} + {right}) // 2 = {mid}`，考虑 `nums[mid]`',
        'if nums[mid] > nums[right]': _cmp,
        'left = mid + 1': '`left = mid + 1 = {left}`：扔掉 mid 及左边，范围 `[{left}, {right}]`',
        'right = mid': '`right = mid = {right}`：mid 自己可能是最小值，==保留==，范围 `[{left}, {right}]`',
        'return nums[left]': '返回 `nums[{left}] = {ret}`',
    },
    cards=dict(
        one_liner='nums[mid] 比 nums[right] 大，最小值就在 mid 右边',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['==元素互不相同==的升序数组，旋转若干次得到 `nums`，返回其中的==最小元素==；要求 `O(log n)`',
                 '旋转一次：`[a0, a1, …, a(n-1)]` → `[a(n-1), a0, …, a(n-2)]`',
                 '示例：`[3,4,5,1,2]` → `1`；`[4,5,6,7,0,1,2]` → `0`'],
        quote='若nums[mid]小于nums[right]，那么说明mid到right这一段都还是保持着升序，那么nums[mid + 1]到nums[right]这些数都大于nums[mid]，==因此答案不会在mid + 1到right之间，于是有right = mid。==',
        quote_src='—— yiduobo 题解原文',
        idea=['还是考虑 `nums[mid]`，拿它和==当前区间的右端== `nums[right]` 比',
              '`nums[mid] > nums[right]`：最小的那部分被旋转到了 `mid+1..right` → `left = mid + 1`',
              '否则 `mid..right` 升序，答案不在 `mid+1..right` → `right = mid`'],
        result='返回 `0`：范围缩到只剩下标 4 ✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去了 `"""type"""` 文档字符串',
                 '`while left < right` 搭配 `right = mid`：区间缩到一个数时停，不会死循环',
                 '比较对象是==会移动的== `nums[right]`；灵神固定和 `nums[n-1]` 比，两者等价'],
    ),
)
