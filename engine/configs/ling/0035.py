def _legend(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = x0 + 22, (y0 + y1) / 2
    for c, s in [(T['red'], '红：nums[i] < target'), (T['blue'], '蓝：nums[i] ≥ target'),
                 (T['panel2'], '灰：待定（闭区间内）')]:
        cv.rect((x, y - 14, x + 28, y + 14), fill=c, r=6, outline=T['border'])
        cv.text((x + 38, y), s, 23, T['muted'], anchor='lm')
        x += 38 + cv.tlen(s, 23) + 34


def _rb(S, i, v):
    if 'left' not in S:
        return None
    if i < S['left']:
        return 'red'
    if i > S['right']:
        return 'blue'
    return None


def _state(S):
    if 'left' not in S:
        return f"找第一个 `≥ {S['target']}` 的数的下标" if 'target' in S else ''
    l, r = S['left'], S['right']
    s = f"闭区间 `[{l}, {r}]`" + ('（空）' if l > r else '')
    if 'mid' in S and l <= r + 1:
        m = S['mid']
        s += f"   ·   mid = {m}，nums[{m}] = =={S['nums'][m]}== {'<' if S['nums'][m] < S['target'] else '≥'} {S['target']}"
    return s


def _inv(S):
    if 'left' not in S:
        return ''
    a, t, l, r = S['nums'], S['target'], S['left'], S['right']
    p1 = f"`nums[{l-1}] = {a[l-1]} < {t}`" if l - 1 >= 0 else "`left-1 = -1` 在数组外（视为红）"
    p2 = f"`nums[{r+1}] = {a[r+1]} ≥ {t}`" if r + 1 < len(a) else f"`right+1 = {len(a)}` 在数组外（视为蓝）"
    return f"不变量：{p1}   ·   {p2}"


def _while(S, B, ret):
    if B.left <= B.right:
        return f'`left = {B.left} ≤ right = {B.right}`：闭区间 `[{B.left}, {B.right}]` ==不为空==，还有待定的数 → 继续二分'
    return f'`left = {B.left} > right = {B.right}`：区间为空，==每个数都已染色== → 循环结束'


def _cmp(S, B, ret):
    x, t, m = S.nums[S.mid], S.target, S.mid
    if x < t:
        return f'`nums[{m}] = {x} < {t}`：数组有序，==mid 及左边都 < target== → 全部染红'
    return f'`nums[{m}] = {x} ≥ {t}`：数组有序，==mid 及右边都 ≥ target== → 全部染蓝'


CONFIG = dict(
    num=35, title='搜索插入位置', difficulty='Easy', category='二分查找',
    author='灵茶山艾府', technique='lower_bound · 闭区间二分（红蓝染色）',
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
    return left

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        return lower_bound(nums, target)  # 选择其中一种写法即可
''',
    call='Solution().searchInsert([1,3,5,6,8,9,11,14], 7)',
    expect=4,
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='array', var='nums', label='nums', pointers={'left': 'red', 'right': 'blue', 'mid': 'yellow'},
             window=('left', 'right'), window_color='yellow', color=_rb, cell=104, h=290),
        dict(type='custom', draw=_legend, h=60),
        dict(type='text', fn=_inv, size=26, h=70),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'),
           ('nums[mid]', 'nums[mid]'), ('target', 'target')],
    captions={
        'return lower_bound': '插入位置 = ==第一个 `≥ {target}` 的数的下标==（都小于就是 `len(nums)`）→ 交给 `lower_bound`',
        'left, right = 0': '闭区间 `[{left}, {right}]` 是==还没确定颜色==的范围：一开始整个数组都待定',
        'while left <= right': _while,
        'mid = (left': '取中点 `mid = ({left} + {right}) // 2 = {mid}`，用 `nums[{mid}] = {nums[mid]}` 和 `{target}` 比',
        'if nums[mid] < target': _cmp,
        'left = mid + 1': '红色扩到 mid：范围缩小到 `[{left}, {right}]`，`nums[left-1] < target` ==仍然成立==',
        'right = mid - 1': lambda S, B, ret: f'蓝色扩到 mid：范围缩小到 `[{S.left}, {S.right}]`' + ('（==区间空了==）' if S.left > S.right else '') + '，`nums[right+1] ≥ target` 仍然成立',
        'return left': '此时 `left = right + 1`：`left-1` 是红、`left` 是蓝 → ==第一个蓝色的下标== `{ret}` 就是答案',
    },
    cards=dict(
        one_liner='插入位置 = 第一个 ≥ target 的数；二分时把数组染成红蓝两色',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['有序、无重复数组 `nums` 和 `target`：找到就返回下标，否则返回==按顺序插入的位置==',
                 '要求 `O(log n)`',
                 '示例：`[1,3,5,6]`, `5` → `2`；`2` → `1`；`7` → `4`'],
        quote='返回 nums 中的==第一个（最左边的）大于或等于 target== 的数的下标。如果所有数都小于 target，返回 nums 的长度。',
        quote_src='—— 灵茶山艾府题解 · 题意概括',
        idea=['把每个数染色：`< target` 染==红==，`≥ target` 染==蓝==；有序 → 红在左、蓝在右',
              '看 `nums[mid]` 一眼就能==把 mid 和一侧整段一起染色==，区间每次减半',
              '循环不变量：`left-1` 永远红，`right+1` 永远蓝；结束时 `left` 就是第一个蓝'],
        result='返回 `4`：`8` 是第一个 `≥ 7` 的数，7 应插在下标 4 ✓',
        summary=['时间 `O(log n)`，空间 `O(1)`；Python 可直接 `bisect_left(nums, target)`',
                 '闭区间：`right = n - 1`、`while left <= right`、`right = mid - 1`',
                 '不必中途 `nums[mid] == target` 就返回：找“第一个 ≥”更通用（如统计 `< x` 的个数）',
                 '所有数都 `< target` 时只更新 left，自动返回 `n`，==无需特判==',
                 '原题解还给了左闭右开、开区间两种写法，结果相同，选一种写熟即可'],
    ),
)
