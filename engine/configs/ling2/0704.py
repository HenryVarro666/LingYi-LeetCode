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
        if 'i' in S and isinstance(S['i'], int):
            return 'red' if i < S['i'] else 'blue'
        return None
    if i < S['left']:
        return 'red'
    if i > S['right']:
        return 'blue'
    return None


def _state(S):
    if 'left' not in S:
        if 'i' in S:
            return f"`lower_bound` 返回 `i = {S['i']}`：第一个 `≥ {S['target']}` 的数的下标"
        return f"先找第一个 `≥ {S['target']}` 的数的下标" if 'target' in S else ''
    l, r = S['left'], S['right']
    s = f"target = =={S['target']}==   ·   闭区间 `[{l}, {r}]`" + ('（空）' if l > r else '')
    if 'mid' in S and l <= r + 1:
        m = S['mid']
        s += f"   ·   nums[{m}] = {S['nums'][m]} {'<' if S['nums'][m] < S['target'] else '≥'} {S['target']}"
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
        return f'`left = {B.left} ≤ right = {B.right}`：闭区间 `[{B.left}, {B.right}]` ==不为空== → 继续二分'
    return f'`left = {B.left} > right = {B.right}`：区间为空，==每个数都已染色== → 循环结束'


def _cmp(S, B, ret):
    x, t, m = S.nums[S.mid], S.target, S.mid
    if x < t:
        return f'`nums[{m}] = {x} < {t}`：有序 → ==mid 及左边都 < target==，全部染红'
    tail = '（==相等也染蓝==，不急着返回）' if x == t else ''
    return f'`nums[{m}] = {x} ≥ {t}`：有序 → ==mid 及右边都 ≥ target==，全部染蓝{tail}'


def _final(S, B, ret):
    i, n, t = S.i, len(S.nums), S.target
    if i < n and S.nums[i] == t:
        return f'`i = {i} < n` 且 `nums[{i}] = {t}` == target → 找到了，返回 =={ret}=='
    if i == n:
        return f'`i = n`：所有数都 `< {t}` → 不存在，返回 `-1`'
    return f'`nums[{i}] = {S.nums[i]}` ≠ `{t}`：第一个 `≥ {t}` 的数都不是它 → ==不存在==，返回 `-1`'


CONFIG = dict(
    num=704, title='二分查找', difficulty='Easy', category='二分查找',
    author='灵茶山艾府', technique='lower_bound · 闭区间二分（红蓝染色）',
    tags=['字节30天', '热题173'],
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
    def search(self, nums: List[int], target: int) -> int:
        i = lower_bound(nums, target)  # 选择其中一种写法即可
        return i if i < len(nums) and nums[i] == target else -1
''',
    call='[Solution().search([-1, 0, 3, 5, 9, 12], 9), Solution().search([-1, 0, 3, 5, 9, 12], 2)]',
    expect=[4, -1],
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='array', var='nums', label='nums', pointers={'left': 'red', 'right': 'blue', 'mid': 'yellow', 'i': 'green'},
             window=('left', 'right'), window_color='yellow', color=_rb, cell=110, h=290),
        dict(type='custom', draw=_legend, h=60),
        dict(type='text', fn=_inv, size=26, h=70),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'),
           ('nums[mid]', 'nums[mid]'), ('target', 'target'), ('i', 'i', 'green')],
    captions={
        'i = lower_bound': '调用 `lower_bound`：找==第一个 ≥ {target} 的数==的下标',
        'left, right = 0': '闭区间 `[{left}, {right}]` 是==还没确定颜色==的范围：一开始整个数组都待定',
        'while left <= right': _while,
        'mid = (left': '取中点 `mid = ({left} + {right}) // 2 = {mid}`',
        'if nums[mid] < target': _cmp,
        'left = mid + 1': '红色扩到 mid：范围缩小到 `[{left}, {right}]`',
        'right = mid - 1': lambda S, B, ret: f'蓝色扩到 mid：范围缩小到 `[{S.left}, {S.right}]`' + ('（==区间空了==）' if S.left > S.right else ''),
        'return left': '`left = right + 1`：`left` 是==第一个蓝色==的下标 → 返回 `{ret}`',
        'return i if': _final,
    },
    cards=dict(
        one_liner='先找第一个 ≥ target 的位置，再看它是不是 target',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['升序、元素互不相同的数组 `nums`，找 `target` 的下标，不存在返回 `-1`；要求 `O(log n)`',
                 '示例：`[-1,0,3,5,9,12]`，`target = 9` → `4`；`target = 2` → `-1`'],
        quote='问：为什么不在二分的过程中，找到 target 就立刻返回？答：==这种写法适用范围很窄==。……返回==第一个等于 target 的数的下标==，可以解决更复杂的题目。',
        quote_src='—— 灵茶山艾府题解 · 答疑',
        idea=['`lower_bound`：把 `< target` 染红、`≥ target` 染蓝，二分找==第一个蓝色==',
              '闭区间 `[left, right]` 是待定范围；不变量 `left-1` 永远红、`right+1` 永远蓝',
              '最后判断 `i < len(nums) and nums[i] == target`：是就返回 i，否则 `-1`'],
        result='`target = 9` → `4`；`target = 2` → `-1` ✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '闭区间三要素：`right = n − 1`、`while left <= right`、`right = mid − 1`',
                 '易错：`i` 可能等于 `n`（全都 `< target`），要先判 `i < len(nums)` 再访问',
                 '原题解还给了左闭右开、开区间写法；这套模板直接用于 34 题'],
    ),
)
