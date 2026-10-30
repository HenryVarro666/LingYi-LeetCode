NUMS, TARGET = [4, 5, 6, 7, 8, 1, 2, 3], 3


def _live(S):
    return 'mid' in S and S['left'] <= S['mid'] <= S['right']


def _sorted_half(S):
    """(lo, hi) of the half yiduobo proves is ascending, or None"""
    if not _live(S):
        return None
    l, m, r, a = S['left'], S['mid'], S['right'], S['nums']
    return (l, m) if a[l] <= a[m] else (m, r)


def _color(S, i, v):
    h = _sorted_half(S)
    if h and h[0] <= i <= h[1]:
        return 'green'
    return None


def _state(S):
    if 'right' not in S:
        return ''
    l, r = S['left'], S['right']
    s = f"范围 `[{l}, {r}]`"
    h = _sorted_half(S)
    if h:
        a = S['nums']
        s += f"   ·   ==a[{h[0]}..{h[1]}] 升序==（绿色）：`[{a[h[0]]} … {a[h[1]]}]`"
    return s


def _eq(S, B, ret):
    x, t = S.nums[S.mid], S.target
    if x == t:
        return f'`nums[{S.mid}] = {x}` 正好等于 target → ==就是要找的答案=='
    return f'`nums[{S.mid}] = {x} ≠ {t}`，继续判断哪一半有序'


def _which(S, B, ret):
    a, b = S.nums[S.left], S.nums[S.mid]
    if S.left == S.mid:
        return f'`left == mid`，`a[left] = a[mid] = {a}`：左半只有一个数，也算 ==a[left] 到 a[mid] 升序=='
    if a <= b:
        return f'`a[left] = {a} ≤ a[mid] = {b}`：==a[left] 到 a[mid] 是升序的=='
    return f'`a[left] = {a} > a[mid] = {b}`：左半跨过了分界点 → ==a[mid] 到 a[right] 是升序的=='


def _in_left(S, B, ret):
    a, b, t = S.nums[S.left], S.nums[S.mid], S.target
    if a <= t < b:
        return f'`{a} ≤ target = {t} < {b}`：target 在升序的左半里 → 去左边'
    return f'target = {t} 不在 `[{a}, {b})` 里 → 只能在右半，去右边'


def _in_right(S, B, ret):
    b, c, t = S.nums[S.mid], S.nums[S.right], S.target
    if b < t <= c:
        return f'`{b} < target = {t} ≤ {c}`：target 在升序的右半里 → 去右边'
    return f'target = {t} 不在 `({b}, {c}]` 里 → 只能在左半，去左边'


CONFIG = dict(
    num=33, title='搜索旋转排序数组', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='二分 · 先判断哪一半有序',
    code='''
class Solution(object):
    def search(self, nums, target):
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (right - left) // 2 + left
            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                if target >= nums[left] and target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            elif target > nums[mid] and target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

        return -1
''',
    call=f'Solution().search({NUMS}, {TARGET})',
    expect=7,
    views=[
        dict(type='text', fn=_state, size=27),
        dict(type='bars', var='nums', pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             window=('left', 'right'), cell=110, h=450, color=_color,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', size=24, h=90, lines=2,
             text='绿色 = 当前能确定==升序==的那一半；灰色 = 已排除\n只在升序的那一半里，才能直接判断 target 在不在'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('nums[mid]', 'nums[mid]'), ('target', 'target')],
    skip=['while left <= right', 'left = 0'],
    captions={
        4: '范围 `[{left}, {right}]`：数组可能在某处有一个==分界点==',
        6: '`mid = (right - left) // 2 + left = {mid}`',
        7: _eq,
        8: '返回 `{ret}`',
        10: _which,
        11: _in_left,
        12: '`right = mid - 1 = {right}`，范围 `[{left}, {right}]`',
        14: '`left = mid + 1 = {left}`，范围 `[{left}, {right}]`',
        15: _in_right,
        16: '`left = mid + 1 = {left}`，范围 `[{left}, {right}]`',
        18: '`right = mid - 1 = {right}`，范围 `[{left}, {right}]`',
    },
    cards=dict(
        one_liner='先比较 a[left] 和 a[mid] 认出哪一半有序，再看 target 在不在那一半',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['升序、==值互不相同==的数组在某下标处旋转，例如 `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`',
                 '在旋转后的 `nums` 中找 `target` 的下标，不存在返回 `-1`；要求 `O(log n)`',
                 '示例：`[4,5,6,7,0,1,2]`, `0` → `4`；`3` → `-1`（本视频演示 `[4,5,6,7,8,1,2,3]`, `3`）'],
        quote='如果满足a[mid] > a[left]，如果是情况(1)，那么a[mid]一定处于a[left]到a[k]之间，所以a[left]到a[mid]是升序的，==于是可以判断target是否处于a[left]到a[mid]中，从而进行二分。==',
        quote_src='—— yiduobo 题解原文',
        idea=['数组可能有分界点 k：`a[left..k]`、`a[k+1..right]` 各自升序；也可能整体升序',
              '`a[left] ≤ a[mid]`：左半 `a[left..mid]` 升序 → 判断 target 是否在其中',
              '否则右半 `a[mid..right]` 升序 → 反过来判断 target 是否在 `a[mid..right]`'],
        result='返回 `7`：`nums[7] = 3` ✓',
        summary=['每次缩小一半，时间 `O(log n)`，空间 `O(1)`',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去了 `"""type"""` 文档字符串',
                 '`nums[left] <= nums[mid]` 要带等号：`left == mid` 时左半只有一个数',
                 '注意区间开闭：左半判 `[a[left], a[mid])`，右半判 `(a[mid], a[right]]`',
                 '对比灵神：他把 x 和 target 都与 `nums[n-1]` 比来判断分段'],
    ),
)
