NUMS = [1, 3, 2, 4, 5, 7, 6, 2]


def _live(S):
    return 'right' in S and isinstance(S.get('left'), int)


def _color(S, i, v):
    if not _live(S):
        return None
    if S.get('_line') == 10 and i == S['right']:
        return 'green'
    m = S.get('mid')
    if isinstance(m, int) and S['left'] <= m < S['right'] + 1 and S.get('_line') in (5, 6, 7, 8, 9):
        if i == m:
            return 'orange'
        if i == m + 1:
            return 'cyan'
    return None


def _dim(S, i, v):
    # 答案范围 (left, right] 之外
    return _live(S) and not (S['left'] < i <= S['right'])


def _text(S):
    if not _live(S):
        return ''
    l, r = S['left'], S['right']
    m = S.get('mid')
    if S.get('_line') in (6, 7, 8, 9) and isinstance(m, int):
        a, b = NUMS[m], NUMS[m + 1]
        if a > b:
            return f"`nums[{m}] = {a} > nums[{m + 1}] = {b}`：==下坡==，峰顶在 `mid` 或它左边"
        return f"`nums[{m}] = {a} < nums[{m + 1}] = {b}`：==上坡==，峰顶在 `mid` 右边"
    if S.get('_line') == 10:
        return f"`left + 1 == right`：答案范围 `({l}, {r}]` 只剩 `{r}` → 峰值下标 =={r}=="
    return f"二分范围（开区间）`({l}, {r})`，答案范围 `({l}, {r}]`"


def _cap_while(S, B, ret):
    l, r = B.left, B.right
    if l + 1 < r:
        return f'`{l} + 1 < {r}`：开区间 `({l}, {r})` 不为空 → 继续二分'
    return f'`{l} + 1 == {r}`：开区间为空 → 结束'


def _cap_if(S, B, ret):
    m = S.mid
    a, b = S.nums[m], S.nums[m + 1]
    if a > b:
        return f'`nums[{m}] = {a} > nums[{m + 1}] = {b}` → ==下坡==，峰顶位置 `<= mid`'
    return f'`nums[{m}] = {a} < nums[{m + 1}] = {b}` → ==上坡==，峰顶位置 `> mid`'


CONFIG = dict(
    num=162, title='寻找峰值', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='开区间二分 · 比较 nums[mid] 与 nums[mid+1]',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        left, right = -1, len(nums) - 1  # 开区间 (-1, n-1)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if nums[mid] > nums[mid + 1]:  # 下坡，峰顶位置 <= mid
                right = mid
            else:  # 上坡，峰顶位置 > mid
                left = mid
        return right
''',
    call=f'Solution().findPeakElement({NUMS})',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='bars', var='nums', label='nums（框 = 答案范围 (left, right]，橙 = mid，青 = mid+1）', h=420,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'orange'},
             window=('left + 1', 'right'), color=_color, dim=_dim, vmax=8),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'orange')],
    captions={
        'left, right = -1': '开区间 `(-1, n-1)`：==不用包含 n-1==，若峰值在 `n-1`，每次都会更新 `left`',
        'while left + 1 < right': _cap_while,
        'mid = (left + right) // 2': '`mid = ({B.left} + {B.right}) // 2 = {mid}`，比较它和右邻居',
        'if nums[mid] > nums[mid + 1]': _cap_if,
        'right = mid': '`(left, right]` 里一定有峰值 → `right = mid = {right}`（mid 本身可能就是峰）',
        'left = mid': '`nums[mid] < nums[mid+1]`，`mid+1` 往右一定有峰值 → `left = mid = {left}`',
        'return right': '`(left, right]` 中只有 `right` 一个数 → 返回 =={ret}==（`nums[{ret}] = {nums[ret]}`）',
    },
    cards=dict(
        one_liner='比较 mid 与 mid+1：下坡则峰在左（含 mid），上坡则峰在右',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['峰值：==严格大于左右相邻值==的元素，返回任意一个峰值的下标',
                 '假设 `nums[-1] = nums[n] = -∞`，相邻元素互不相等，要求 `O(log n)`',
                 '示例：`[1,2,1,3,5,6,4]` → `1` 或 `5`',
                 '本视频：`[1,3,2,4,5,7,6,2]` → `5`'],
        quote='如果 i<n-1 且 nums[i] < nums[i+1]，那么在下标 [i+1,n-1] 中==一定存在峰值==。……通过比较 nums[i] 和 nums[i+1] 的大小关系，可以二分找到峰值。',
        quote_src='—— 灵茶山艾府题解（定理）',
        idea=['反证：若右边没有峰值，则一路严格递增到 `nums[n-1] > -∞`，它就是峰值，矛盾',
              '循环不变量：==答案范围 `(left, right]` 中一定有峰值==',
              '注意：二分范围 `(left, right)` ≠ 答案范围 `(left, right]`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '二分范围是 `[0, n-2]`（开区间 `(-1, n-1)`），所以 `mid + 1` 不会越界',
                 '常见误区：上坡不代表 `mid` 右边第一个峰就是最终答案，二分只是不断缩小范围',
                 '`-∞` 的假设保证一定有峰值：严格递减时 `nums[0]` 就是峰',
                 'Python 库函数写法：`bisect_left(range(n - 1), True, key=check)`'],
    ),
)
