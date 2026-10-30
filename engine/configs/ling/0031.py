def _while1(S, B, ret):
    i, a = B.i, B.nums
    if i < 0:
        return '`i = -1`：整个数组是递减的（最后一个排列）'
    if a[i] >= a[i + 1]:
        return f'`nums[{i}] = {a[i]} ≥ nums[{i + 1}] = {a[i + 1]}`：右边没有比它大的，这一位==不能增大==，继续左移'
    return f'`nums[{i}] = {a[i]} < nums[{i + 1}] = {a[i + 1]}`：找到了！右边有更大的数，`{a[i]}` 这一位==可以增大=='


def _while2(S, B, ret):
    i, j, a = B.i, B.j, B.nums
    if a[j] <= a[i]:
        return f'`nums[{j}] = {a[j]} ≤ {a[i]}`，不够大，继续左移'
    return f'`nums[{j}] = {a[j]} > {a[i]}`：后缀递减，所以它就是右边==最小的==比 `{a[i]}` 大的数'


def _color(S, i, v):
    if S.get('_line', 0) >= 21 and isinstance(S.get('left'), int) and S['left'] <= i <= S['right']:
        return None
    if i == S.get('i'):
        return 'blue'
    if i == S.get('j'):
        return 'pink'
    return None


CONFIG = dict(
    num=31, title='下一个排列', difficulty='Medium', category='技巧',
    author='灵茶山艾府', technique='找可增大的位 · 交换 · 反转',
    code='''
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)

        # 第一步：从右到左找到第一个小于 nums[i+1] 的数 nums[i]
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        # 如果找到了，进入第二步；否则跳过第二步，反转整个数组
        if i >= 0:
            # 第二步：从右到左找到 nums[i] 右边最小的大于 nums[i] 的数 nums[j]
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            # 交换 nums[i] 和 nums[j]
            nums[i], nums[j] = nums[j], nums[i]

        # 第三步：反转 nums[i+1:]（如果上面跳过第二步，此时 i = -1）
        # nums[i+1:] = nums[i+1:][::-1] 这样写也可以，但空间复杂度不是 O(1) 的
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
''',
    call='''nums = [1, 3, 5, 4, 2]
Solution().nextPermutation(nums)
nums''',
    expect=[1, 4, 2, 3, 5],
    views=[
        dict(type='text', fn=lambda S: '类比：`13999` → 找能增大的 `3` → 变 `4` → 右边变最小 → `14000`', size=26, h=60),
        dict(type='array', var='nums', label='nums', h=250, cell=110,
             pointers={'i': 'blue', 'j': 'pink', 'left': 'green', 'right': 'purple'},
             window=(lambda S: S['i'] + 1 if isinstance(S.get('i'), int) else None,
                     lambda S: S['n'] - 1 if isinstance(S.get('i'), int) else None),
             color=_color),
        dict(type='text', fn=lambda S: ('==青框== = 后缀 `nums[i+1:]`，它始终是==递减==的' if S.get('_line', 0) < 21
                                        else '第三步：后缀是递减的，==反转==后就是递增（最小的排列）'), size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('left', 'left', 'green'), ('right', 'right', 'purple')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'i = n - 2': '第一步：从右往左找第一个 `nums[i] < nums[i+1]`，从 `i = n - 2 = {i}` 开始',
        'while i >= 0 and': _while1,
        'i -= 1': '`i` 左移到 `{i}`',
        'if i >= 0': lambda S, B, ret: (f'找到了 `x = nums[{S.i}] = {S.nums[S.i]}` → 进入第二步' if S.i >= 0
                                        else '没找到 → 跳过第二步，直接反转整个数组'),
        'j = n - 1': '第二步：从右往左找第一个比 `{nums[i]}` 大的数，`j` 从 `{j}` 开始',
        'while nums[j] <= nums[i]': _while2,
        'j -= 1': '`j` 左移到 `{j}`',
        'nums[i], nums[j] = nums[j], nums[i]': '交换 `x` 和 `y`：`nums = {nums}`，排列变大了，且右边==仍然递减==',
        'left, right = i + 1, n - 1': '第三步：反转 `nums[{left}..{right}]`，让右边变成==最小==的排列',
        'while left < right': lambda S, B, ret: (f'`left = {B.left} < right = {B.right}` → 交换这一对' if B.left < B.right
                                                 else f'`left = {B.left} ≥ right = {B.right}` → 反转完成'),
        'nums[left], nums[right] = nums[right], nums[left]': '交换 `nums[{left}]` 和 `nums[{right}]`：`{nums}`',
        'left += 1': '`left` → `{left}`',
        'right -= 1': '`right` → `{right}`',
    },
    cards=dict(
        one_liner='从右找第一个能增大的数，换成稍大一点的，再把右边变最小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` ==原地==改成字典序中的下一个排列',
                 '已经是最大排列（如 `[3,2,1]`）则改成最小排列 `[1,2,3]`',
                 '示例：`[1,2,3]` → `[1,3,2]`，`[1,1,5]` → `[1,5,1]`'],
        before=[dict(heading='引入：下一个整数', lines=[
            '`13999` 的下一个整数是 `14000`，怎么算的？',
            '① 从右到左，找第一个==可以增大==的数字（小于 9 的），即 `3`',
            '② 把 `3` 加一变成 `4`　③ 把 `4` 右边的数都变成 `0`（最小）'])],
        quote='如果 1 保持不变，只重新排列 3,5,4,2，这是可以的，因为 ==3 右边有比 3 大的数，重排后可以让 3 这个位置上的数变大==，从而得到更大的排列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['① 从右到左找第一个 `nums[i] < nums[i+1]` 的 `x`（它右边一定递减）',
              '② 在右边找==最小的==大于 `x` 的 `y`，交换 → 排列只“大一点点”',
              '③ 交换后右边仍递减，==反转==成递增，即右边最小的排列'],
        result='`[1,3,5,4,2]` 的下一个排列是 `[1,4,2,3,5]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：第一步比较用 `>=`，第二步用 `<=`，相等的数不能算“更大”',
                 '找不到 `x`（`i = -1`）时，直接反转整个数组',
                 '用双指针反转而不是切片，才是 `O(1)` 额外空间'],
    ),
)
