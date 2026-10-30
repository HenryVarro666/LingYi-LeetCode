NUMS = [-5, 0, -1, 3, -5, 7]
TARGET = 8


def _d(ans):
    return '∞' if ans == float('inf') else abs(ans - TARGET)


def _info(S):
    if 'x' not in S or 's' not in S:
        return f'target = =={TARGET}==，ans 初始为 ∞'
    s, ans = S['s'], S.get('ans')
    d_ans = '∞' if ans == float('inf') else abs(ans - TARGET)
    return f"当前和 `s = {s}`，离 target 差 `{abs(s - TARGET)}`；ans = `{ans if ans != float('inf') else '∞'}`，差 `{d_ans}`"


def _range(S):
    if 'x' not in S or S.get('i') is None:
        return ''
    i, nums = S['i'], S['nums']
    if i + 2 >= len(nums):
        return ''
    x = nums[i]
    lo, hi = x + nums[i + 1] + nums[i + 2], x + nums[-2] + nums[-1]
    where = ('==target 落在区间内==' if lo <= TARGET <= hi else
             '最小和都 > target' if lo > TARGET else '最大和都 < target')
    return f'x = `{x}` 能凑出的和在 `[{lo}, {hi}]` 之间（最小 = 紧挨着的两个，最大 = 最右两个）→ {where}'


def _cap_dup(S, B, ret):
    i, x = S.i, S.x
    if i and x == S.nums[i - 1]:
        return f'`nums[{i}] = {x}` 和前一个数相同：它能凑出的和==之前都算过== → 跳过'
    if i == 0:
        return f'`i = 0`：第一个 x 不用判重'
    return f'`x = {x}` 和前一个数 `{S.nums[i - 1]}` 不同 → 不跳过'


def _cap_min3(S, B, ret):
    s = S.s
    if s > TARGET:
        return f'最小的三数之和 `{s} > {TARGET}`：后面怎么选都不会比 s 更小 → ==直接 break=='
    return f'最小的三数之和 `{s} ≤ {TARGET}` → 还有希望，继续'


def _cap_max3(S, B, ret):
    s = S.s
    if s < TARGET:
        return f'x 能凑出的最大和 `{s} < {TARGET}`：双指针不用跑了 → 用 s 试着更新 ans 后 ==continue=='
    return f'x 能凑出的最大和 `{s} ≥ {TARGET}` → target 落在范围内，跑双指针'


def _cap_closer(S, B, ret):
    s, ans = S.s, B.ans
    da = '∞' if ans == float('inf') else abs(ans - TARGET)
    if abs(s - TARGET) < (float('inf') if ans == float('inf') else abs(ans - TARGET)):
        return f'`|{s} − {TARGET}| = {abs(s - TARGET)}` < 旧差 `{da}` → s 离 target ==更近=='
    return f'`|{s} − {TARGET}| = {abs(s - TARGET)}` ≥ 旧差 `{da}` → 不更新'


def _cap_gt(S, B, ret):
    if S.s > TARGET:
        return f'`s = {S.s} > {TARGET}`：和太大 → 换更小的 nums[k]'
    return f'`s = {S.s} < {TARGET}`：和太小 → 换更大的 nums[j]'


CONFIG = dict(
    num=16, title='最接近的三数之和', difficulty='Medium', category='双指针',
    author='灵茶山艾府', technique='排序 + 相向双指针 + 剪枝',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()

        n = len(nums)
        ans = inf
        for i in range(n - 2):
            x = nums[i]
            # 优化
            if i and x == nums[i - 1]:
                continue

            # 优化
            s = x + nums[i + 1] + nums[i + 2]
            if s > target:  # 后面无论怎么选，选出的三数之和不会比 s 还小
                if s - target < abs(ans - target):
                    ans = s
                break

            # 优化
            s = x + nums[-2] + nums[-1]
            if s < target:  # x 加上后面任意两个数都不超过 s，所以下面的双指针就不需要跑了
                if target - s < abs(ans - target):
                    ans = s
                continue

            # 双指针
            j, k = i + 1, n - 1
            while j < k:
                s = x + nums[j] + nums[k]
                if s == target:
                    return target
                if abs(s - target) < abs(ans - target):  # s 离 target 更近
                    ans = s
                if s > target:
                    k -= 1
                else:  # s < target
                    j += 1
        return ans
''',
    call=f'Solution().threeSumClosest({NUMS}, {TARGET})',
    expect=9,
    skip=['n = len'],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='nums', label='nums（排序后；蓝 = 第一个数 x，绿/粉 = 双指针 j/k）', h=220,
             pointers={'i': 'blue', 'j if _line >= 28 else None': 'green', 'k if _line >= 28 else None': 'pink'},
             pointer_labels={'j if _line >= 28 else None': 'j', 'k if _line >= 28 else None': 'k'},
             color=lambda S, i, v: ('blue' if i == S.get('i') else
                                    'green' if i == S.get('j') and S['_line'] >= 28 else
                                    'pink' if i == S.get('k') and S['_line'] >= 28 else None)),
        dict(type='text', fn=_range, size=26, h=110, lines=2),
        dict(type='text', fn=lambda S: ('双指针：`s > target` 则 `k -= 1`，`s < target` 则 `j += 1`' if S.get('_line', 0) >= 28
                                        else '先用两条剪枝判断要不要跑双指针'), size=24, h=56),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('j', 'j', 'green'), ('k', 'k', 'pink'), 's', ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '先排序：`{nums}`，才能用双指针和剪枝',
        'ans = inf': '`ans` 初始为 ∞：任何三数之和都比它更近',
        'for i in range': lambda S, B, r: (f'枚举第一个数的下标 `i = {S.i}`' if S.get('i') != B.get('i') else '枚举结束'),
        'x = nums[i]': '第一个数 `x = nums[{i}] = {x}`',
        'if i and x ==': _cap_dup,
        11: '跳过重复的 x，直接看下一个',
        's = x + nums[i + 1]': 'x 能凑出的==最小==和：`{x} + {nums[i+1]} + {nums[i+2]} = {s}`',
        15: _cap_min3,
        'if s - target <': lambda S, B, r: (f'`{S.s} − {TARGET} = {S.s - TARGET}` < 旧差 `{_d(B.ans)}` → 更新 ans' if S.s - TARGET < abs(B.ans - TARGET)
                                            else f'`{S.s} − {TARGET} = {S.s - TARGET}` ≥ 旧差 `{_d(B.ans)}` → 不更新'),
        'break': '更大的 x 只会让和更大，==不会更近== → 结束外层循环',
        's = x + nums[-2]': 'x 能凑出的==最大==和：`{x} + {nums[-2]} + {nums[-1]} = {s}`',
        'if s < target:': _cap_max3,
        'if target - s <': lambda S, B, r: (f'`{TARGET} − {S.s} = {TARGET - S.s}` < 旧差 `{_d(B.ans)}` → 更新 ans' if TARGET - S.s < abs(B.ans - TARGET)
                                            else f'`{TARGET} − {S.s} = {TARGET - S.s}` ≥ 旧差 `{_d(B.ans)}` → 不更新'),
        'ans = s': '`ans = {ans}`',
        25: '直接换下一个更大的 x',
        'j, k = i + 1': '双指针：`j = {j}` 从 x 右边开始，`k = {k}` 从最右开始',
        'while j < k': lambda S, B, r: (f'`j = {B.j} < k = {B.k}`，继续' if B.j < B.k else f'`j = {B.j} ≥ k = {B.k}`：x 的所有组合都看过了'),
        's = x + nums[j] + nums[k]': '`s = {x} + {nums[j]} + {nums[k]} = {s}`',
        'if s == target': lambda S, B, r: ('`s == target`：不可能更近了 → 直接返回' if S.s == TARGET else f'`{S.s} ≠ {TARGET}`'),
        'if abs(s - target) < abs(ans - target)': _cap_closer,
        35: _cap_gt,
        'k -= 1': '`k` 左移到 {k}：和变小',
        'j += 1': '`j` 右移到 {j}：和变大',
        'return ans': '返回最接近的和 =={ret}==',
    },
    cards=dict(
        one_liner='排序后枚举第一个数，剩下两个数用相向双指针逼近 target',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['从 `nums` 里选==三个不同下标==的数，使它们的和与 `target` 最接近，返回这个和',
                 '示例：`nums = [-1,2,1,-4], target = 1` → `2`（`-1+2+1`）',
                 f'本视频：`nums = {NUMS}`，`target = {TARGET}` → `9`'],
        quote='设 s=nums[i]+nums[j]+nums[k]。如果 |s−target| < |ans−target|，那么==更新 ans=s==。如果 s>target，那么和三数之和一样，把 k 减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和 15. 三数之和一样：排序，枚举 `x = nums[i]`，另外两个数用==双指针==',
              '每算一个 `s` 就和 ans 比谁离 target 近；`s > target` 则 `k -= 1`，否则 `j += 1`',
              '三个优化：重复的 x 跳过；==最小和 > target 就 break==；最大和 < target 就 continue'],
        summary=['时间 `O(n^2)`：排序 `O(n log n)` + 外层 n 次 × 双指针 n 次',
                 '`s == target` 时可以直接返回，不可能更近',
                 '易错：break / continue 之前==别忘了用 s 更新 ans==',
                 '比较远近用 `abs(s - target)`，ans 初始用 ∞ 而不是 0'],
    ),
)
