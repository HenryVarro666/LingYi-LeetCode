def _color(S, i, v):
    if 'left' in S and 'right' in S:
        if i <= S['left']:
            return 'red'
        if i >= S['right']:
            return 'blue'
        if S.get('_line') == 6 and 'mid' in S:     # 判断这一步：提前染上即将确定的颜色
            blue = S['nums'][S['mid']] >= S['target']
            if blue and i >= S['mid']:
                return 'blue'
            if not blue and i <= S['mid']:
                return 'red'
        return None
    if 'start' in S and 'end' in S and S['start'] <= i <= S['end']:
        return 'green'
    return None


def _formula(S):
    if 'left' in S and 'right' in S:
        t = S['target']
        return (f"找第一个 `≥ {t}`：红 = `< {t}`，蓝 = `≥ {t}`，"
                f"开区间 `({S['left']}, {S['right']})` 是还没染色的部分")
    if 'start' in S:
        return f"第一个 `{S['target']}` 在下标 `{S['start']}`" + (
            f"，最后一个在 `{S['end']}`" if 'end' in S else '')
    return '红蓝染色法：==把数组染成左红右蓝，找红蓝分界=='


CONFIG = dict(
    num=None, title='二分查找 · 通用思想与模板', author='概念讲解', category='二分查找',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def lower_bound(nums, target):       # 返回第一个 >= target 的下标
    left, right = -1, len(nums)      # 开区间 (left, right)
    while left + 1 < right:          # 区间不为空
        mid = (left + right) // 2
        # 循环不变量：nums[left] < target <= nums[right]
        if nums[mid] >= target:
            right = mid              # 蓝：范围缩小到 (left, mid)
        else:
            left = mid               # 红：范围缩小到 (mid, right)
    return right

def search_range(nums, target):      # 34. 第一个和最后一个位置
    start = lower_bound(nums, target)
    if start == len(nums) or nums[start] != target:
        return [-1, -1]              # nums 中没有 target
    end = lower_bound(nums, target + 1) - 1  # >= target+1 的前一个
    return [start, end]
''',
    call='search_range([1, 3, 4, 6, 8, 8, 8, 9, 11, 13], 8)',
    expect=[4, 6],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='nums', label='nums（左右两端外各有一个虚拟格：nums[-1] = −∞，nums[n] = +∞）',
             pointers={'left': 'red', 'mid': 'yellow', 'right': 'blue', 'start': 'green', 'end': 'green'},
             color=_color, cell=78, h=250),
        dict(type='text', fn=lambda S: (f"`nums[mid] = nums[{S['mid']}] = {S['nums'][S['mid']]}` "
                                        + ('≥' if S['nums'][S['mid']] >= S['target'] else '<') + f" {S['target']}"
                                        if 'mid' in S and 'left' in S else ''), size=28, h=60),
    ],
    watch=[('left', 'left', 'red'), ('mid', 'mid', 'yellow'), ('right', 'right', 'blue'), ('target', 'target'),
           ('start', 'start', 'green'), ('end', 'end', 'green')],
    captions={
        'left, right = -1': '开区间 `(-1, {right})`：假设 `nums[-1] = −∞` 是红色、`nums[n] = +∞` 是蓝色',
        'while left + 1 < right': lambda S, B, ret: (
            f'`({S.left}, {S.right})` 里还有 {S.right - S.left - 1} 个没染色的数，继续'
            if S.left + 1 < S.right else f'`left + 1 == right`：全部染完色，红蓝分界就在 `{S.left}` | `{S.right}`'),
        'mid = (left + right)': '看中间 `mid = ({left} + {right}) // 2 = {mid}`，`nums[{mid}] = {nums[mid]}`',
        'if nums[mid] >= target': lambda S, B, ret: (
            f'`{S.nums[S.mid]} ≥ {S.target}` → `mid` 染 ==蓝色==，它右边也全是蓝色'
            if S.nums[S.mid] >= S.target else f'`{S.nums[S.mid]} < {S.target}` → `mid` 染 ==红色==，它左边也全是红色'),
        'right = mid': '`right = {right}`：区间缩小到 `({left}, {right})`',
        'left = mid': '`left = {left}`：区间缩小到 `({left}, {right})`',
        'return right': '返回 `right = {ret}`：==第一个蓝色== 就是第一个 `≥ {target}` 的数',
        'start = lower_bound': '第一个位置 = 第一个 `≥ {target}` 的下标',
        'if start == len': lambda S, B, ret: f'`start = {S.start}`，`nums[{S.start}] = {S.nums[S.start]}`：找到了 target',
        'end = lower_bound': '最后一个位置：`> 8` 等价于 `≥ 9`，==复用同一个二分==，再减 1',
        'return [start, end]': '答案 `[{start}, {end}]`：两次二分，`O(log n)`',
    },
    cards=dict(
        one_liner='红蓝染色：每次看中点，把一半染上颜色，直到找到分界',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem_heading='什么时候用？',
        problem=['数组 ==有序== 或部分有序（旋转数组），要求 `O(log n)`',
                 '找第一个 `≥ x`、最后一个 `≤ x` 这样的 ==边界==',
                 '答案有单调性：x 可行，更大的 x 也可行 → 二分答案',
                 '两个有序数组的第 k 小 / 中位数（4）'],
        before=[dict(heading='核心概念：红蓝染色法', lines=[
            '把数组染成两段：左边红色（`< target`），右边蓝色（`≥ target`）',
            '开区间 `(left, right)` 是没染色的部分，初始 `left = -1`、`right = n`',
            '看 `mid`：蓝就 `right = mid`，红就 `left = mid`，结束时答案是 `right`',
            '`> x` 等价于 `≥ x+1`，`≤ x` 是 `(≥ x+1) - 1`：都能复用 lower_bound']),
        ],
        idea_heading='两位作者怎么说',
        quote='可以假设 nums[-1] = -∞ 以及 nums[n] = ∞，此时 nums 仍然是有序的。在这种情况下，nums[-1] < target，所以 ==-1 是红色==；nums[n] ≥ target，所以 ==n 是蓝色==。',
        quote_src='—— 灵茶山艾府 · 34. 在排序数组中查找元素的第一个和最后一个位置',
        idea=['灵神：看 `while` 条件就知道是哪种区间；开区间 ==if 更新谁，最后就返回谁==',
              'yiduobo 用闭区间 `left = mid + 1` / `right = mid - 1`，关注二分中两端的变化',
              '33 / 153：两人都先判断 `mid` 落在旋转数组的哪一段，再决定扔掉哪一半'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`35` 搜索插入位置：就是 lower_bound',
                 '`34` 第一个和最后一个位置：`lb(x)` 和 `lb(x+1) - 1`',
                 '`74` 搜索二维矩阵：看成长为 `m·n` 的有序数组',
                 '`153` 旋转数组的最小值：和最后一个数比，染红蓝',
                 '`33` 搜索旋转排序数组：先判断 `mid` 在哪一段',
                 '`4` 两个正序数组的中位数：二分第一个数组的划分点',
                 '易错：开区间的循环条件是 `left + 1 < right`；先判 `start == n`'],
    ),
)
