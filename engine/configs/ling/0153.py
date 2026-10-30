NUMS = [4, 5, 6, 7, 0, 1, 2]
BARS_H, CELL = 450, 110


def _ref_line(cv, S, B, box, T):
    """dashed line at the height of nums[n-1], drawn over the bars view right above this box"""
    if 'nums' not in S:
        return
    nums = S['nums']
    n = len(nums)
    x0, y0, x1, y1 = box
    top, base = y0 - BARS_H + 40, y0 - (26 + 27 * 3) - 30
    sc = (base - top - 34) / max(nums)
    width = x1 - x0 - 40
    c = max(24, min(CELL, width / n))
    sx = x0 + 20 + (width - c * n) / 2
    y = base - nums[-1] * sc
    cv.dashed((sx - 6, y), (sx + c * n + 6, y), T['cyan'], 3)
    cv.text((sx - 10, y), f'nums[{n - 1}]={nums[-1]}', 19, T['cyan'], anchor='rm', bold=True)


def _legend(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = x0 + 22, (y0 + y1) / 2
    for c, s in [(T['red'], '红：> nums[n-1]，在最小值左边'), (T['blue'], '蓝：≤ nums[n-1]，是最小值或在其右边')]:
        cv.rect((x, y - 14, x + 28, y + 14), fill=c, r=6, outline=T['border'])
        cv.text((x + 38, y), s, 23, T['muted'], anchor='lm')
        x += 38 + cv.tlen(s, 23) + 34


def _rb(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'blue'
    return None


def _state(S):
    if 'left' not in S:
        return ''
    l, r = S['left'], S['right']
    s = f"开区间 `({l}, {r})`" + ('（空）' if l + 1 >= r else '')
    if 'mid' in S and l + 1 < r or ('mid' in S and S['mid'] in (l, r)):
        x = S['nums'][S['mid']]
        s += f"   ·   nums[mid] = =={x}== {'<' if x < S['nums'][-1] else '>'} nums[n-1] = {S['nums'][-1]}"
    return s


def _while(S, B, ret):
    if B.left + 1 < B.right:
        return f'开区间 `({B.left}, {B.right})` 非空，还有==没染色==的数'
    return f'`left + 1 = right = {B.right}`：开区间为空，==红蓝分界找到了== → 结束'


def _cmp(S, B, ret):
    x, y = S.nums[S.mid], S.nums[-1]
    if x < y:
        return f'`{x} < nums[n-1] = {y}`：x 在第二段 → ==x 要么是最小值，要么在最小值右边==，染蓝'
    return f'`{x} > nums[n-1] = {y}`：x 在第一段，最小值在第二段 → ==x 在最小值左边==，染红'


CONFIG = dict(
    num=153, title='寻找旋转排序数组中的最小值', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='和最后一个数比大小 · 开区间二分',
    code='''
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = -1, len(nums) - 1  # 开区间 (-1, n-1)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if nums[mid] < nums[-1]:
                right = mid
            else:
                left = mid
        return nums[right]
''',
    call=f'Solution().findMin({NUMS})',
    expect=0,
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='bars', var='nums', pointers={'left': 'red', 'right': 'blue', 'mid': 'yellow'},
             window=('left + 1', 'right - 1'), window_color='yellow', color=_rb, cell=CELL, h=BARS_H),
        dict(type='custom', draw=_ref_line, h=4),
        dict(type='custom', draw=_legend, h=60),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'),
           ('nums[mid]', 'nums[mid]'), ('nums[n-1]', 'nums[-1]', 'cyan')],
    captions={
        'left, right = -1': '开区间 `(-1, {right})`：`n-1` 要么是最小值、要么在它右边 → ==直接算蓝色==，不进二分',
        'while left + 1 < right': _while,
        'mid = (left + right)': '`mid = ({left} + {right}) // 2 = {mid}`，拿 `nums[{mid}] = {nums[mid]}` 和虚线比',
        'if nums[mid] < nums[-1]': _cmp,
        'right = mid': '`right = mid = {right}`：蓝色扩到 mid，范围缩小到 `({left}, {right})`',
        'left = mid': '`left = mid = {left}`：红色扩到 mid，范围缩小到 `({left}, {right})`',
        'return nums[right]': '`left` 红、`right` 蓝且相邻 → `right` 是==第一个蓝色==，最小值 `nums[{right}] = {ret}`',
    },
    cards=dict(
        one_liner='和最后一个数比大小，就知道 mid 在最小值的左边还是右边',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['==元素互不相同==的升序数组，旋转若干次得到 `nums`，返回其中的==最小元素==；要求 `O(log n)`',
                 '旋转一次：`[a0, a1, …, a(n-1)]` → `[a(n-1), a0, …, a(n-2)]`',
                 '示例：`[3,4,5,1,2]` → `1`；`[4,5,6,7,0,1,2]` → `0`'],
        quote='只需要比较 x 和 nums[n−1] 的大小关系，就==间接地==知道了 x 和数组最小值的位置关系，从而不断地缩小数组最小值所在位置的范围，二分找到数组最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x > nums[n-1]`：数组是两个递增段，x 在第一段、最小值在第二段 → ==x 在最小值左边==',
              '`x ≤ nums[n-1]`：x 在第二段（或数组本来就递增）→ ==x 是最小值或在其右边==',
              '`n-1` 一定是蓝色 → 只需在开区间 `(-1, n-1)` 里二分'],
        result='返回 `0`：第一个蓝色就是最小值 ✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '和 `nums[n-1]` 比：没旋转的数组全是“第二段”，==无需特判==',
                 '「二分范围」≠「答案范围」：答案可以是 `n-1`，但它不必进入二分区间',
                 '也能和 `nums[0]` 比，但要在 `(0, n)` 中二分，并特判结果为 `n`',
                 '思考题：改成求最大值怎么做？'],
    ),
)
