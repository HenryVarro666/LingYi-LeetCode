NUMS = [2, 5, 6, 0, 0, 1, 2]


def _col(S, i, v):
    if 'right' not in S or 'left' not in S:
        return None
    if i == S.get('mid') and S['left'] < S['mid'] < S['right']:
        return 'yellow'
    if i == S['right']:
        return 'pink'
    return None


def _dim(S, i, v):
    if 'right' not in S or 'left' not in S:
        return False
    return i <= S['left'] or i > S['right']


def _text(S):
    if 'right' not in S or 'left' not in S:
        return '开区间 `(left, right)` 之外的数都已排除；`right` 指向「当前数组最后一个数」'
    l, r = S['left'], S['right']
    nr = S['nums'][r]
    return f"`target = {S['target']}`，当前末尾 `nums[right] = nums[{r}] = {nr}`；开区间 `({l}, {r})` 里还有 =={max(0, r - l - 1)}== 个数待定"


def _eq(S, B, ret):
    m, r = S.mid, S.right
    if S.nums[m] == S.nums[r]:
        return f'`nums[{m}] = nums[{r}] = {S.nums[m]}`：==无法判断== target 在 mid 哪一侧 → 干脆去掉末尾这个数'
    return f'`nums[{m}] = {S.nums[m]}` ≠ `nums[{r}] = {S.nums[r]}`：可以像 33 题一样判断'


def _check_x(S, B, ret):
    x, nr, t = S.x, S.nums[S.right], S.target
    if x > nr:
        return f'`x = nums[{S.i}] = {x} > nums[right] = {nr}`：mid 在==左边那段==（比末尾所在段大）'
    return f'`x = nums[{S.i}] = {x} <= nums[right] = {nr}`：mid 和末尾在==同一段=='


def _ret1(S, B, ret):
    t, nr, x = S.target, S.nums[S.right], S.x
    return (f'target 也要在左边那段（`{t} > {nr}`：{"是" if t > nr else "否"}）且 `x >= target`（`{x} >= {t}`：{"是" if x >= t else "否"}）'
            f' → =={ret}==：{"target 在 mid 左边或就是 mid" if ret else "target 在 mid 右边"}')


def _ret2(S, B, ret):
    t, nr, x = S.target, S.nums[S.right], S.x
    return (f'target 在左边那段（`{t} > {nr}`：{"是" if t > nr else "否"}）或 `x >= target`（`{x} >= {t}`：{"是" if x >= t else "否"}）'
            f' → =={ret}==：{"target 在 mid 左边或就是 mid" if ret else "target 在 mid 右边"}')


CONFIG = dict(
    num=81, title='搜索旋转排序数组 II', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='开区间二分 · 相等时去掉末尾',
    tags=['labuladong', '灵神题单·二分算法'],
    code='''
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def check(i: int) -> bool:
            x = nums[i]
            if x > nums[right]:
                return target > nums[right] and x >= target
            return target > nums[right] or x >= target

        left, right = -1, len(nums) - 1  # 开区间 (-1, n-1)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if nums[mid] == nums[right]:
                right -= 1
            elif check(mid):
                right = mid
            else:
                left = mid
        return nums[right] == target
''',
    call=f'[Solution().search({NUMS}, 0), Solution().search({NUMS}, 3)]',
    expect=[True, False],
    views=[
        dict(type='text', fn=_text, size=24, h=70),
        dict(type='array', var='nums', cell=100, h=300,
             label='nums（暗 = 已排除，粉 = 末尾 nums[right]，黄 = mid）',
             pointers={'left': 'blue', 'mid': 'yellow', 'right': 'pink'},
             color=_col, dim=_dim),
        dict(type='text', size=24, h=70,
             fn=lambda S: 'check(i) = true ⇔ `nums[i]` 在 target ==右边或就是 target==（相对旋转前的顺序）'),
    ],
    watch=[('target', 'target', 'green'), ('left', 'left', 'blue'), ('mid', 'mid', 'yellow'),
           ('right', 'right', 'pink'), 'x'],
    skip=['def check', 'x = nums[i]'],
    captions={
        'left, right = -1': '开区间 `(-1, {right})`：`right = n-1` 当作==数组最后一个数的下标==',
        'while left + 1 < right': lambda S, B, r: ('开区间不为空，继续二分' if S.left + 1 < S.right
                                                   else f'`left + 1 = {S.left + 1} = right`：开区间为空 → 结束'),
        'mid = (left + right) // 2': '`mid = ({left} + {right}) // 2 = {mid}`，`nums[mid] = {nums[mid]}`',
        'if nums[mid] == nums[right]': _eq,
        'right -= 1': '去掉的不会是唯一的 target：若它等于 target，`nums[mid]` 也等于 target → `right` 减一到 {right}',
        'elif check(mid)': lambda S, B, r: f'`check({S.mid})` 判断 `nums[{S.mid}]` 是否在 target 右边（或就是它）',
        'x = nums[i]': '`x = nums[{i}] = {x}`',
        'if x > nums[right]': _check_x,
        'return target > nums[right] and': _ret1,
        'return target > nums[right] or': _ret2,
        'right = mid': 'check 为 true：mid 右边的数都在 target 右边 → 去掉，`right = {right}`',
        'left = mid': 'check 为 false：mid 及左边都不可能是答案 → `left = {left}`',
        'return nums[right] == target': lambda S, B, r: f'最后看 `nums[{S.right}] = {S.nums[S.right]}` 是否等于 `{S.target}` → =={r}==',
    },
    cards=dict(
        one_liner='和 33 题一样二分；遇到 nums[mid] == nums[right] 就去掉末尾，规模减一',
        complexity='平均 `O(log n)`，最坏 `O(n)`（全相同）；空间 `O(1)`',
        problem=['非降序数组（==可能有重复==）在某处旋转后得到 `nums`，判断 `target` 是否在其中',
                 '示例：`nums = [2,5,6,0,0,1,2]`，`target = 0` → `true`；`target = 3` → `false`',
                 '本视频依次演示这两个 target'],
        quote='既然无法确定最小值所在区间，那么==干脆去掉 nums 的最后一个数==，继续二分。换句话说，此时问题变成了一个规模为 n−1 的子问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `right` 当作「数组最后一个数的下标」，用 `nums[right]` 判断 mid 在旋转的哪一段',
              '`nums[mid] == nums[right]` 时分不清 → `right -= 1`；==不会误删 target==：若删的是 target，mid 处还有一个',
              '否则用 `check(mid)` 决定 `right = mid` 还是 `left = mid`，最后看 `nums[right]`'],
        summary=['平均 `O(log n)`；数组全相同且不含 target 时退化为 `O(n)`',
                 '开区间写法：`left = -1`，循环条件 `left + 1 < right`',
                 '易错：`check` 里用的是==当前==的 `nums[right]`，right 一变，基准也随之变',
                 '前置题：33. 搜索旋转排序数组（无重复，不需要 `right -= 1` 这一支）'],
    ),
)
