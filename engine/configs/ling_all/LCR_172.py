def _text(S):
    I = S['_inner']
    if 'left' not in I or 'nums' not in I:
        return '二分找第一个 `>= target` 的位置：求两次，相减就是个数'
    left, right, t = I['left'], I['right'], I['target']
    return f"区间 `[{left}, {right}]` 内还没确定；左边都 `< {t}`，右边都 `>= {t}`"


def _color(S, i, v):
    I = S['_inner']
    if 'left' not in I or 'target' not in I:
        return None
    if i < I['left']:
        return 'blue'
    if i > I['right']:
        return 'pink'
    return None


def _dim(S, i, v):
    I = S['_inner']
    return 'left' in I and 'right' in I and not (I['left'] <= i <= I['right'])


CONFIG = dict(
    num='LCR 172', title='统计目标成绩的出现次数', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='二分查找 · lower_bound 闭区间', tags=[],
    code='''
# lower_bound 返回最小的满足 nums[i] >= target 的 i
# 如果数组为空，或者所有数都 < target，则返回 len(nums)
# 要求 nums 是非递减的，即 nums[i] <= nums[i + 1]

# 闭区间写法
def lower_bound(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1  # 闭区间 [left, right]
    while left <= right:  # 区间不为空
        # 循环不变量：
        # nums[left-1] < target
        # nums[right+1] >= target
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1  # 范围缩小到 [mid+1, right]
        else:
            right = mid - 1  # 范围缩小到 [left, mid-1]
    return left  # 或者 right+1

class Solution:
    def countTarget(self, nums: List[int], target: int) -> int:
        start = lower_bound(nums, target)  # 选择其中一种写法即可
        end = lower_bound(nums, target + 1)
        # target 在 [start, end) 中出现
        return end - start
''',
    call='Solution().countTarget([2, 2, 3, 4, 4, 4, 5, 6, 6, 8], 4)',
    expect=3,
    views=[
        dict(type='text', fn=_text),
        dict(type='array', var=lambda S: S['_inner'].get('nums') or S.get('nums'),
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             window=('left', 'right'), color=_color, dim=_dim, cell=80, h=330, label='nums（蓝 = 已知 < target，粉 = 已知 >= target）'),
    ],
    watch=[('left', lambda S: S['_inner'].get('left'), 'blue'), ('right', lambda S: S['_inner'].get('right'), 'pink'),
           ('mid', lambda S: S['_inner'].get('mid'), 'yellow'), ('target', lambda S: S['_inner'].get('target')),
           ('start', lambda S: S['_inner'].get('start'), 'green'), ('end', lambda S: S['_inner'].get('end'), 'green')],
    captions={
        'left, right = 0': '闭区间 `[left, right] = [{left}, {right}]`：待判断的位置都在里面',
        'while left <= right': lambda S, B, r: (f'区间 `[{S.left}, {S.right}]` 不为空 → 继续二分' if S.left <= S.right
                                                 else f'区间空了（`left = {S.left} > right = {S.right}`）→ 停止，`left` 就是答案'),
        'mid = (left': '取中点 `mid = ({left} + {right}) // 2 = {mid}`，`nums[{mid}] = {nums[mid]}`',
        'if nums[mid] < target': lambda S, B, r: (f'`nums[{S.mid}] = {S.nums[S.mid]} < {S.target}` → 成立：==mid 及左边都太小，不可能是答案=='
                                                  if S.nums[S.mid] < S.target
                                                  else f'`nums[{S.mid}] = {S.nums[S.mid]} >= {S.target}` → ==mid 及右边都满足 >= target，往左找更小的位置=='),
        'left = mid + 1': '`left = mid + 1 = {left}`：丢掉左半边（含 mid）',
        'right = mid - 1': '`right = mid - 1 = {right}`：丢掉右半边（含 mid）',
        'return left': '`left = {left}` 就是第一个 `>= {target}` 的下标（也等于 `right + 1`）',
        'start = lower_bound': '第一次二分：`lower_bound(nums, target)`，找 target 的起点（第一个 `>= target` 的位置）',
        'end = lower_bound': '已得 `start = {start}`；第二次二分：`lower_bound(nums, target + 1)`，找 target 最后一个的后面',
        'return end - start': '`target` 在 `[start, end) = [{start}, {end})` 里 → 出现 ==`{end} - {start} = {end - start}`== 次',
    },
    cards=dict(
        one_liner='次数 = 第一个 `>= target+1` 的位置 − 第一个 `>= target` 的位置',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['非递减数组 `scores`，求目标成绩 `target` 出现了几次',
                 '示例：`[2,2,3,4,4,4,5,6,6,8]`，`target = 4` → `3`',
                 '要求用二分，不要从头扫一遍'],
        quote='循环不变量：`nums[left-1] < target`，`nums[right+1] >= target`。……`target` 在 `[start, end)` 中出现。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`lower_bound`：二分找最小的满足 `nums[i] >= target` 的 `i`',
              '整数数组里，`> target` 等价于 `>= target + 1`',
              '所以 `start = lower_bound(target)`，`end = lower_bound(target + 1)`，答案是 `end - start`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '闭区间写法：循环条件 `left <= right`，返回 `left`',
                 '易错：`left = mid + 1`、`right = mid - 1` 都要 ±1，否则死循环',
                 '另有左闭右开、开区间两种写法，以及 `bisect_right - bisect_left` 的一行库函数写法',
                 '同主站 34 题（那题要返回首尾下标）'],
    ),
)
