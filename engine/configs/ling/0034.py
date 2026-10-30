def _legend(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = x0 + 22, (y0 + y1) / 2
    for c, s in [(T['red'], '红：nums[i] < target'), (T['blue'], '蓝：nums[i] ≥ target'),
                 (T['green'], '绿：[start, end]')]:
        cv.rect((x, y - 14, x + 28, y + 14), fill=c, r=6, outline=T['border'])
        cv.text((x + 38, y), s, 23, T['muted'], anchor='lm')
        x += 38 + cv.tlen(s, 23) + 34


def _color(S, i, v):
    if 'left' in S:
        if i <= S['left']:
            return 'red'
        if i >= S['right']:
            return 'blue'
        return None
    if 'end' in S and S['start'] <= i <= S['end']:
        return 'green'
    if 'start' in S and i == S['start'] and S['start'] < len(S['nums']) and S['nums'][i] == S['target']:
        return 'green'
    return None


def _state(S):
    if 'left' in S:
        t = S['target']
        s = f"lower_bound(nums, =={t}==)" + ('（= target + 1）' if 'start' in S else '')
        s += f"   开区间 `({S['left']}, {S['right']})`"
        if S['left'] + 1 >= S['right']:
            s += '（空）'
        return s
    if 'end' in S:
        return f"start = =={S['start']}==   ·   end = =={S['end']}=="
    if 'start' in S:
        return f"start = =={S['start']}==（第一个 `≥ {S['target']}` 的下标）"
    return ''


def _inv(S):
    if 'left' not in S:
        return ''
    a, t, l, r = S['nums'], S['target'], S['left'], S['right']
    p1 = f"`nums[{l}] = {a[l]} < {t}`" if l >= 0 else "`nums[-1]` 视为 ==-∞==（红）"
    p2 = f"`nums[{r}] = {a[r]} ≥ {t}`" if r < len(a) else f"`nums[{len(a)}]` 视为 ==+∞==（蓝）"
    return f"不变量：{p1}   ·   {p2}"


def _while(S, B, ret):
    if B.left + 1 < B.right:
        return f'开区间 `({B.left}, {B.right})` 非空，还有==没染色==的数'
    return f'`left + 1 = right = {B.right}`：开区间为空，==红蓝分界已经找到== → 结束循环'


def _cmp(S, B, ret):
    x, t, m = S.nums[S.mid], S.target, S.mid
    if x >= t:
        return f'`nums[{m}] = {x} ≥ {t}`：数组有序 → ==mid 及右边都 ≥ target==，染蓝'
    return f'`nums[{m}] = {x} < {t}`：数组有序 → ==mid 及左边都 < target==，染红'


def _exists(S, B, ret):
    if S.start == len(S.nums):
        return f'`start = n`：所有数都 `< {S.target}` → ==target 不存在=='
    if S.nums[S.start] != S.target:
        return f'`nums[{S.start}] = {S.nums[S.start]} ≠ {S.target}` → ==target 不存在=='
    return f'`nums[{S.start}] = {S.nums[S.start]} == {S.target}`：==target 存在==，start 就是开始位置'


CONFIG = dict(
    num=34, title='在排序数组中查找元素的第一个和最后一个位置', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='两次 lower_bound · 开区间二分',
    code='''
class Solution:
    # lower_bound 返回最小的满足 nums[i] >= target 的下标 i
    # 如果数组为空，或者所有数都 < target，则返回 len(nums)
    # 要求 nums 是非递减的，即 nums[i] <= nums[i + 1]
    def lower_bound(self, nums: List[int], target: int) -> int:
        left, right = -1, len(nums)  # 开区间 (left, right)
        while left + 1 < right:  # 区间不为空
            mid = (left + right) // 2
            # 循环不变量：
            # nums[left] < target
            # nums[right] >= target
            if nums[mid] >= target:
                right = mid  # 范围缩小到 (left, mid)
            else:
                left = mid  # 范围缩小到 (mid, right)
        # 循环结束后 left+1 = right
        # 此时 nums[left] < target 而 nums[right] >= target
        # 所以 right 就是第一个 >= target 的元素下标
        return right

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        start = self.lower_bound(nums, target)  # 选择其中一种写法即可
        if start == len(nums) or nums[start] != target:
            return [-1, -1]  # nums 中没有 target
        # 如果 start 存在，那么 end 必定存在
        end = self.lower_bound(nums, target + 1) - 1
        return [start, end]
''',
    call='Solution().searchRange([5,7,7,8,8,10], 8)',
    expect=[3, 4],
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='array', var='nums', pointers={'left': 'red', 'right': 'blue', 'mid': 'yellow'},
             window=('left + 1', 'right - 1'), window_color='yellow', color=_color, cell=110, h=290),
        dict(type='custom', draw=_legend, h=56),
        dict(type='text', fn=_inv, size=26, h=64),
        dict(type='calls', h=120),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'),
           ('target', 'target'), ('start', 'start', 'green'), ('end', 'end', 'green')],
    captions={
        'start = self.lower_bound': '开始位置 = ==第一个 `≥ {target}` 的下标== → 调用 `lower_bound(nums, {target})`',
        'left, right = -1': '开区间 `({left}, {right})`：`-1` 和 `n` 是==虚拟位置==，可看成 `-∞`（红）和 `+∞`（蓝）',
        'while left + 1 < right': _while,
        'mid = (left + right)': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if nums[mid] >= target': _cmp,
        'right = mid': '`right = mid = {right}`：范围缩小到 `({left}, {right})`，`nums[right] ≥ target` ==仍成立==',
        'left = mid': '`left = mid = {left}`：范围缩小到 `({left}, {right})`，`nums[left] < target` ==仍成立==',
        'return right': '`left` 红、`right` 蓝且相邻 → ==right 是第一个 `≥ {target}` 的下标==，返回 `{ret}`',
        'if start == len(nums)': _exists,
        'end = self.lower_bound': '结束位置 = 最后一个 `≤ {target - 1}`；整数里 `> {target - 1}` ⇔ `≥ {target}` → ==复用 lower_bound 再减一==',
        'return [start, end]': '`end = lower_bound(nums, {target + 1}) - 1 = {end}`，返回 `[{start}, {end}]`',
    },
    cards=dict(
        one_liner='只写一个 lower_bound：end = lower_bound(target + 1) − 1',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['非递减数组 `nums`，找 `target` 的==开始和结束位置==，不存在返回 `[-1, -1]`；要求 `O(log n)`',
                 '示例：`[5,7,7,8,8,10]`, `8` → `[3,4]`；`6` → `[-1,-1]`'],
        quote='要想找到 ≤ target 的最后一个数，==无需单独再写一个二分==。先找到它右边相邻的数，也就是 > target 的第一个数。在所有数都是整数的前提下，==> target 等价于 ≥ target+1==。',
        quote_src='—— 灵茶山艾府题解 · 答疑',
        idea=['`start = lower_bound(nums, target)`：越界或 `nums[start] ≠ target` → 不存在',
              '`end = lower_bound(nums, target + 1) - 1`：第一个 `> target` 的左边',
              '开区间 `(-1, n)`：假设 `nums[-1] = -∞` 是红色、`nums[n] = +∞` 是蓝色'],
        result='返回 `[3, 4]`：两个 8 在下标 3 和 4 ✓',
        after=[dict(heading='二分查找常用转化表', lines=[
            '`≥ x` 的第一个下标：`lowerBound(nums, x)`，不存在时为 `n`',
            '`> x` 的第一个下标：`lowerBound(nums, x + 1)`，不存在时为 `n`',
            '`< x` 的最后一个下标：`lowerBound(nums, x) - 1`，不存在时为 `-1`',
            '`≤ x` 的最后一个下标：`lowerBound(nums, x + 1) - 1`，不存在时为 `-1`'])],
        summary=['两次二分：时间 `O(log n)`，空间 `O(1)`',
                 '开区间三件套：`left, right = -1, n`、`while left + 1 < right`、`left/right = mid`',
                 '==先判断 start 是否存在==；start 存在则 end 必定存在',
                 '原题解还有闭区间、左闭右开写法（看 while 条件区分）；库函数用 `bisect_left/right`'],
    ),
)
