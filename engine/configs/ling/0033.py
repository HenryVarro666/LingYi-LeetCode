NUMS, TARGET = [4, 5, 6, 7, 0, 1, 2], 7
BARS_H, CELL = 450, 110


def _ref_lines(cv, S, B, box, T):
    """dashed lines at nums[n-1] (cyan) and target (green), drawn over the bars view right above this box"""
    if 'nums' not in S:
        return
    nums, t = S['nums'], S['target']
    n = len(nums)
    x0, y0, x1, y1 = box
    top, base = y0 - BARS_H + 40, y0 - (26 + 27 * 3) - 30
    sc = (base - top - 34) / max(nums)
    width = x1 - x0 - 40
    c = max(24, min(CELL, width / n))
    sx = x0 + 20 + (width - c * n) / 2
    for v, colr, name in [(nums[-1], T['cyan'], f'nums[{n - 1}]={nums[-1]}'), (t, T['green'], f'target={t}')]:
        y = base - v * sc
        cv.dashed((sx - 6, y), (sx + c * n + 6, y), colr, 3)
        cv.text((sx - 10, y), name, 19, colr, anchor='rm', bold=True)


def _legend(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = x0 + 22, (y0 + y1) / 2
    for c, s in [(T['red'], '红：target 在它右边'), (T['blue'], '蓝：target 是它或在它左边')]:
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


def _seg(v, last):
    return '第一段' if v > last else '第二段'


def _state(S):
    if 'left' not in S:
        return ''
    l, r, last, t = S['left'], S['right'], S['nums'][-1], S['target']
    s = f"开区间 `({l}, {r})`" + ('（空）' if l + 1 >= r else '')
    if 'x' in S:
        s += f"   ·   x = {S['x']} 在=={_seg(S['x'], last)}==，target = {t} 在=={_seg(t, last)}=="
    return s


def _while(S, B, ret):
    if B.left + 1 < B.right:
        return f'开区间 `({B.left}, {B.right})` 非空 → 继续二分'
    return f'`left + 1 = right = {B.right}`：开区间为空 → 结束循环'


def _c1(S, B, ret):
    t, last, x = S.target, S.nums[-1], S.x
    if t > last >= x:
        return f'`target={t} > {last} ≥ x={x}`：target 在第一段、x 在第二段 → ==target 在 x 左边=='
    return f'`target > nums[-1] ≥ x`（`{t} > {last} ≥ {x}`）不成立：不是“target 在第一段、x 在第二段”'


def _c2(S, B, ret):
    t, last, x = S.target, S.nums[-1], S.x
    if x > last >= t:
        return f'`x={x} > {last} ≥ target={t}`：x 在第一段、target 在第二段 → ==target 在 x 右边=='
    return f'`x > nums[-1] ≥ target`（`{x} > {last} ≥ {t}`）也不成立 → x 和 target ==在同一段=='


def _c3(S, B, ret):
    t, x = S.target, S.x
    if x >= t:
        return f'同一段内递增，和 lower_bound 一样比大小：`x={x} ≥ target={t}` → target 是 x 或在 x 左边'
    return f'同一段内递增，和 lower_bound 一样比大小：`x={x} < target={t}` → ==target 在 x 右边=='


CONFIG = dict(
    num=33, title='搜索旋转排序数组', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='一次二分 · x 和 target 都与 nums[n-1] 比',
    code='''
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = -1, len(nums) - 1  # 开区间 (-1, n-1)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            x = nums[mid]
            if target > nums[-1] >= x:  # target 在第一段，x 在第二段
                right = mid  # 下轮循环去左边找
            elif x > nums[-1] >= target:  # x 在第一段，target 在第二段
                left = mid  # 下轮循环去右边找
            elif x >= target:  # 否则，x 和 target 在同一段，这就和方法一的 lower_bound 一样了
                right = mid
            else:
                left = mid
        return right if nums[right] == target else -1
''',
    call=f'Solution().search({NUMS}, {TARGET})',
    expect=3,
    views=[
        dict(type='text', fn=_state, size=27),
        dict(type='bars', var='nums', pointers={'left': 'red', 'right': 'blue', 'mid': 'yellow'},
             window=('left + 1', 'right - 1'), window_color='yellow', color=_rb, cell=CELL, h=BARS_H),
        dict(type='custom', draw=_ref_lines, h=4),
        dict(type='custom', draw=_legend, h=60),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'),
           ('x', 'x'), ('target', 'target', 'green'), ('nums[n-1]', 'nums[-1]', 'cyan')],
    captions={
        3: '开区间 `(-1, {right})`：若 target 就是 `nums[n-1]`，循环只动 left，right 停在 `n-1` → ==n-1 不必进二分==',
        4: _while,
        5: '`mid = ({left} + {right}) // 2 = {mid}`',
        6: '`x = nums[{mid}] = {x}`：和青色虚线 `nums[n-1] = {nums[-1]}` 比 → x 在=={"第一段" if x > nums[-1] else "第二段"}==',
        7: _c1,
        8: '`right = mid = {right}`：下轮循环去左边找（mid 染蓝）',
        9: _c2,
        10: '`left = mid = {left}`：下轮循环去右边找（mid 染红）',
        11: _c3,
        12: '`right = mid = {right}`：mid 染蓝，范围缩小到 `({left}, {right})`',
        14: '`left = mid = {left}`：mid 染红，范围缩小到 `({left}, {right})`',
        15: lambda S, B, ret: (f'循环结束，`nums[right] = nums[{S.right}] = {S.nums[S.right]}`，等于 target → 返回下标 =={ret}=='
                               if ret != -1 else f'`nums[{S.right}] ≠ target` → 返回 `-1`'),
    },
    cards=dict(
        one_liner='把 x 和 target 都与 nums[n−1] 比，就知道谁在左、谁在右',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['升序、==值互不相同==的数组在某下标处旋转，例如 `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`',
                 '在旋转后的 `nums` 中找 `target` 的下标，不存在返回 `-1`；要求 `O(log n)`',
                 '示例：`[4,5,6,7,0,1,2]`, `0` → `4`；`3` → `-1`（本视频演示 `target = 7`）'],
        quote='把 x 和 target 这两个数都与 nums[n−1] 比大小，可以知道这两个数分别在哪一段。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['`> nums[n-1]` 在第一段，`≤ nums[n-1]` 在第二段；==第一段整体都比第二段大==',
              'target 第一段、x 第二段 → target 在 x 左边；x 第一段、target 第二段 → 在右边',
              '同一段内是递增的 → 和 lower_bound 一样比 `x ≥ target`'],
        result='返回 `3`：`nums[3] = 7` ✓',
        summary=['一次二分：时间 `O(log n)`，空间 `O(1)`',
                 '在 `(-1, n-1)` 中二分；target 不存在时 `nums[right] ≠ target`，自然返回 `-1`',
                 '方法一（两次二分）：先用 153 题找最小值下标 i，再在 `[0,i-1]` 或 `[i,n-1]` 中 lower_bound',
                 '写法二把判断封装成 `check(i)`，可直接套 `bisect_left(..., key=check)`'],
    ),
)
