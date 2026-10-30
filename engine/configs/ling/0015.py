def _ptr(name, first_line):
    def f(S):
        if name not in S or 'x' not in S or S.get('_line', 0) < first_line:
            return None
        return S[name]
    return f


# j is assigned on line 14, k on line 15; before that they are left over from the previous i
_I, _J, _K = _ptr('i', 0), _ptr('j', 14), _ptr('k', 15)


def _jk_live(S):
    return 'j' in S and 'k' in S and S.get('_line', 0) >= 16


def _sum_text(S):
    if 'x' not in S:
        return '排序后：枚举 `nums[i]`，在它右边用双指针找另外两个数'
    a, x = S['nums'], S['x']
    if not _jk_live(S) or S['j'] >= S['k']:
        return f"`x = nums[{S['i']}] = {x}`：要在右边找 `nums[j] + nums[k] = {-x}`"
    j, k = S['j'], S['k']
    s = x + a[j] + a[k]
    rel = '等于 0' if s == 0 else ('大于 0 → k 左移' if s > 0 else '小于 0 → j 右移')
    return f"`{x} + {a[j]} + {a[k]} = {s}` =={rel}=="


def _ans_text(S):
    if 'ans' not in S:
        return ''
    return '答案 ans = ' + ('  '.join(f'`{t}`' for t in S['ans']) if S['ans'] else '`[]`')


def _dup(S, B, ret):
    i, x, a = S.i, S.x, S.nums
    if i > 0 and x == a[i - 1]:
        return f'`nums[{i}] = nums[{i - 1}] = {x}`：它能组成的三元组，前一个数==都已经组过了=='
    return '不是重复数字' if i > 0 else '`i = 0`，前面没有数，不会重复'


def _opt1(S, B, ret):
    i, x, a = S.i, S.x, S.nums
    s = x + a[i + 1] + a[i + 2]
    if s > 0:
        return f'优化一：`{x} + {a[i + 1]} + {a[i + 2]} = {s} > 0`，和后面==最小的两个数==相加都大于 0 → 后面不可能有解'
    return f'优化一：`x` + 后面最小的两个数 = `{s}` ≤ 0，还有希望'


def _opt2(S, B, ret):
    x, a = S.x, S.nums
    s = x + a[-2] + a[-1]
    if s < 0:
        return f'优化二：`{x} + {a[-2]} + {a[-1]} = {s} < 0`，和==最大的两个数==相加都不够 → 这个 x 太小'
    return f'优化二：`x` + 最大的两个数 = `{s}` ≥ 0，可以开始双指针'


def _cont(S, B, ret):
    i, x, a = S.i, S.x, S.nums
    if i > 0 and x == a[i - 1]:
        return '`continue`：跳过重复的 x'
    return '`continue` 而不是 break：x 继续变大，后面还有机会'


def _s_branch(S, B, ret):
    if S.s > 0:
        return f'`s = {S.s} > 0`：和太大，`nums[k]` 与任何 `nums[j]` 组合都太大'
    return f'`s = {S.s}` 不大于 0'


def _s_less(S, B, ret):
    if S.s < 0:
        return f'`s = {S.s} < 0`：和太小，`nums[j]` 与任何 `nums[k]` 组合都太小'
    return f'`s = 0`：找到一组！'


CONFIG = dict(
    num=15, title='三数之和', difficulty='Medium', category='双指针',
    author='灵茶山艾府', technique='排序 + 枚举第一个数 + 相向双指针',
    code='''
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        ans = []
        n = len(nums)
        for i in range(n - 2):
            x = nums[i]
            if i > 0 and x == nums[i - 1]:  # 跳过重复数字
                continue
            if x + nums[i + 1] + nums[i + 2] > 0:  # 优化一
                break
            if x + nums[-2] + nums[-1] < 0:  # 优化二
                continue
            j = i + 1
            k = n - 1
            while j < k:
                s = x + nums[j] + nums[k]
                if s > 0:
                    k -= 1
                elif s < 0:
                    j += 1
                else:  # 三数之和为 0
                    ans.append([x, nums[j], nums[k]])
                    j += 1
                    while j < k and nums[j] == nums[j - 1]:  # 跳过重复数字
                        j += 1
                    k -= 1
                    while k > j and nums[k] == nums[k + 1]:  # 跳过重复数字
                        k -= 1
        return ans
''',
    call='Solution().threeSum([-1,0,1,2,-1,-4])',
    expect=[[-1, -1, 2], [-1, 0, 1]],
    views=[
        dict(type='text', fn=_sum_text),
        dict(type='array', var='nums', pointers={_I: 'yellow', _J: 'blue', _K: 'pink'},
             pointer_labels={_I: 'i', _J: 'j', _K: 'k'}, h=300, cell=96,
             window=(lambda S: S['j'] if _jk_live(S) else None, lambda S: S['k'] if _jk_live(S) else None),
             color=lambda S, i, v: 'yellow' if 'x' in S and i == S['i'] else None,
             dim=lambda S, i, v: 'x' in S and i < S['i'],
             label='nums（排序后）'),
        dict(type='text', fn=_ans_text, size=30),
    ],
    watch=[('x', 'x', 'yellow'), ('j', 'j', 'blue'), ('k', 'k', 'pink'), 's'],
    captions={
        'nums.sort()': '先排序：==方便双指针==，也方便==跳过相同元素== → `{nums}`',
        'ans = []': '`ans` 收集三元组',
        'n = len': '`n = {n}`',
        'for i in range': lambda S, B, r: f'枚举第一个数的下标 `i = {S.i}`',
        'x = nums[i]': '`x = {x}`：问题变成在右边找两数之和 `= {-x}`（167 题）',
        'if i > 0 and x == nums[i - 1]': _dup,
        'continue': _cont,
        'if x + nums[i + 1] + nums[i + 2] > 0': _opt1,
        'break': '`break`：数组有序，后面的 x 只会更大，==直接结束外层循环==',
        'if x + nums[-2] + nums[-1] < 0': _opt2,
        'j = i + 1': '`j = {j}`：从 x 右边第一个数开始',
        'k = n - 1': '`k = {k}`：从最后一个数开始',
        's = x + nums[j] + nums[k]': '`s = {x} + {nums[j]} + {nums[k]} = {s}`',
        'if s > 0': _s_branch,
        'elif s < 0': _s_less,
        19: '`k` 左移 → {k}',
        21: '`j` 右移 → {j}',
        'ans.append': '`[{x}, {nums[j]}, {nums[k]}]` 加入答案',
        24: '记录后 `j` 右移 → {j}',
        'while j < k and nums[j] == nums[j - 1]': lambda S, B, r: ('`nums[j]` 和上一个相同 → 继续跳过' if S.j < S.k and S.nums[S.j] == S.nums[S.j - 1]
                                                                   else '`nums[j]` 和刚才不同（或 j、k 相遇），不用跳'),
        26: '跳过重复数字：`j` → {j}',
        27: '`k` 也左移 → {k}：j、k 都换掉，继续找下一组',
        'while k > j and nums[k] == nums[k + 1]': lambda S, B, r: ('`nums[k]` 和上一个相同 → 继续跳过' if S.k > S.j and S.nums[S.k] == S.nums[S.k + 1]
                                                                   else '`nums[k]` 和刚才不同（或 j、k 相遇），不用跳'),
        29: '跳过重复数字：`k` → {k}',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='排序后枚举第一个数，剩下的就是有序数组的两数之和',
        complexity='时间 `O(n²)`，空间 `O(1)`（不计返回值）',
        problem=['找出所有和为 `0` 的三元组 `[nums[i], nums[j], nums[k]]`，下标互不相同',
                 '答案中==不能有重复的三元组==',
                 '示例：`[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`'],
        quote='为方便双指针以及跳过相同元素，先把 nums 排序。枚举 nums[i]，问题变成 nums[j] + nums[k] = −nums[i]，==这和 167. 两数之和 II 是一样的==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['去重：外层 `x == nums[i−1]` 就跳过；找到解后跳过相同的 `nums[j]`、`nums[k]`',
              '优化一：`x + nums[i+1] + nums[i+2] > 0` → 后面不可能为 0，`break`',
              '优化二：`x + nums[n−2] + nums[n−1] < 0` → 这个 x 太小，`continue`'],
        summary=['时间 `O(n²)`：排序 `O(n log n)` + 每个 `i` 做一次 `O(n)` 双指针',
                 '易错：去重比较的是 `nums[i−1]`（已枚举过的），不是 `nums[i+1]`',
                 '优化一用 `break`，优化二用 `continue`：x 还会变大',
                 '写法二：找到解时，若 `j > i+1` 且 `nums[j] == nums[j−1]` 就不记录'],
    ),
)
