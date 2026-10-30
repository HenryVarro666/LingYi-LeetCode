def _state(S):
    if 'left' not in S:
        return ''
    phase = '第二次二分：找==右边界==（相等时继续向右）' if 'right_pos' in S else '第一次二分：找==左边界==（相等时继续向左）'
    l, r = S['left'], S['right']
    return phase + f"   范围 `[{l}, {r}]`" + ('（空）' if l > r else '')


def _color(S, i, v):
    if S.get('right_pos', -1) == i:
        return 'purple'
    if S.get('left_pos', -1) == i:
        return 'green'
    return None


def _dim(S, i, v):
    if i in (S.get('left_pos', -1), S.get('right_pos', -1)):
        return False
    return 'left' in S and not (S['left'] <= i <= S['right'])


def _single(S, B, ret):
    if B.left == B.right:
        return f'`left == right == {B.left}`：范围只剩一个位置，单独检查它'
    return f'`left = {B.left}`，`right = {B.right}`：范围里不止一个数 → 二分'


def _eq(side):
    def f(S, B, ret):
        x, t = S.nums[S.mid], S.target
        if x == t:
            if side == 'L':
                return f'`nums[{S.mid}] = {x} == target`：mid 是==可行的左边界==，但 `a[left]` 到 `a[mid-1]` 也可能有 target'
            return f'`nums[{S.mid}] = {x} == target`：mid 是==可行的右边界==，但 `a[mid+1]` 到 `a[right]` 也可能有 target'
        return f'`nums[{S.mid}] = {x} ≠ {t}`，按普通二分处理'
    return f


def _gt(S, B, ret):
    x, t = S.nums[S.mid], S.target
    if x > t:
        return f'`{x} > {t}`：普通情况，target 只能在左边'
    return f'`{x} < {t}`：普通情况，target 只能在右边'


def _lt(S, B, ret):
    x, t = S.nums[S.mid], S.target
    if x < t:
        return f'`{x} < {t}`：普通情况，target 只能在右边'
    return f'`{x} > {t}`：普通情况，target 只能在左边'


def _last(var, pos):
    def f(S, B, ret):
        i = S[var]
        if S.nums[i] == S.target:
            return f'`nums[{i}] = {S.nums[i]}` 是 target → 它就是{pos}'
        return f'`nums[{i}] = {S.nums[i]}` 不是 target → 保持之前记下的{pos}'
    return f


CONFIG = dict(
    num=34, title='在排序数组中查找元素的第一个和最后一个位置', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='两次二分：相等时继续向左 / 向右收缩',
    code='''
class Solution(object):
    def searchRange(self, nums, target):
        if not nums:
            return [-1, -1]

        left = 0
        right = len(nums) - 1
        left_pos = -1
        while left <= right:
            if left == right:
                if nums[left] == target:
                    left_pos = left
                break
            else:
                mid = (left + right) // 2
                if nums[mid] == target:
                    left_pos = mid
                    right = mid - 1
                elif nums[mid] > target:
                    right = mid - 1
                else:
                    left = mid + 1

        left = 0
        right = len(nums) - 1
        right_pos = -1
        while left <= right:
            if left == right:
                if nums[right] == target:
                    right_pos = right
                break
            else:
                mid = (left + right) // 2
                if nums[mid] == target:
                    right_pos = mid
                    left = mid + 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1

        return [left_pos, right_pos]
''',
    call='Solution().searchRange([5,7,7,8,8,10], 8)',
    expect=[3, 4],
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             window=('left', 'right'), dim=_dim, color=_color, cell=110, h=300),
        dict(type='text', size=25, lines=2, h=100,
             text='`target < a[mid]` → `right = mid - 1`；`target > a[mid]` → `left = mid + 1`\n'
                  '`target == a[mid]`：记下 mid，==找左边界继续向左，找右边界继续向右=='),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('left_pos', 'left_pos', 'green'), ('right_pos', 'right_pos', 'purple')],
    skip=['left = 0', 'right = len(nums) - 1', 'while left <= right'],
    captions={
        3: '特判空数组（本例非空）',
        8: '`left_pos = -1`：先假设没有 target；第一次二分在 `[0, {len(nums) - 1}]` 里找==左边界==',
        10: _single,
        11: _last('left', '左边界'),
        12: '更新 `left_pos = left = {left_pos}`',
        13: '`break`：左边界确定为 `left_pos = {left_pos}`',
        15: '`mid = ({left} + {right}) // 2 = {mid}`',
        16: _eq('L'),
        17: '先记下 `left_pos = {left_pos}`（目前最靠左的 target）',
        18: '继续检索==左半边==：`right = mid - 1 = {right}`，范围 `[{left}, {right}]`',
        19: _gt,
        20: '`right = mid - 1 = {right}`，范围 `[{left}, {right}]`',
        22: '`left = mid + 1 = {left}`，范围 `[{left}, {right}]`',
        26: '`right_pos = -1`：第二次二分，范围重置为 `[{left}, {right}]`，找==右边界==',
        28: _single,
        29: _last('right', '右边界'),
        30: '更新 `right_pos = right = {right_pos}`',
        31: '`break`：右边界确定为 `right_pos = {right_pos}`',
        33: '`mid = ({left} + {right}) // 2 = {mid}`',
        34: _eq('R'),
        35: '先记下 `right_pos = {right_pos}`（目前最靠右的 target）',
        36: '继续检索==右半边==：`left = mid + 1 = {left}`，范围 `[{left}, {right}]`',
        37: _lt,
        38: '`left = mid + 1 = {left}`，范围 `[{left}, {right}]`',
        40: '`right = mid - 1 = {right}`，范围 `[{left}, {right}]`',
        42: '两次二分分别得到左右边界，返回 `[{left_pos}, {right_pos}]`',
    },
    cards=dict(
        one_liner='两次二分：碰到 target 先记下，再继续往左 / 往右找',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['非递减数组 `nums`，找 `target` 的==开始和结束位置==，不存在返回 `[-1, -1]`；要求 `O(log n)`',
                 '示例：`[5,7,7,8,8,10]`, `8` → `[3,4]`；`6` → `[-1,-1]`'],
        quote='如果找的是左边界，那么当前mid为可行的左边界，但是在a[left]到a[mid - 1]之间也可能出现target，==因此应该继续检索左半边，即 right = mid - 1。==',
        quote_src='—— yiduobo 题解原文',
        idea=['还是二分查找，需要关注二分过程中 ==left 与 right 的变化==',
              '`target < a[mid]` / `target > a[mid]`：和普通二分一样收缩',
              '`target == a[mid]`：mid 先记为答案；找左边界 `right = mid - 1`，找右边界 `left = mid + 1`'],
        result='返回 `[3, 4]`：绿色是左边界，紫色是右边界 ✓',
        summary=['两次二分，时间 `O(log n)`，空间 `O(1)`',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去了 `"""type"""` 文档字符串',
                 '相等时==不要立刻返回==：先记录，再朝要找的方向继续缩',
                 '`left_pos / right_pos` 初始化为 `-1`，target 不存在时自然返回 `[-1, -1]`',
                 '`left == right` 时单独判断一次再 `break`'],
    ),
)
