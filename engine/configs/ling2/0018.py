NUMS = [1, 0, -1, 0, -2, 2]
TARGET = 0


def _sum(S):
    ln = S.get('_line', 0)
    if 'x' not in S:
        return f'target = =={TARGET}=='
    if ln >= 15 and 'y' in S:
        t = f"固定 `x = {S['x']}`、`y = {S['y']}`，还需两数之和 = =={TARGET - S['x'] - S['y']}=="
        if ln == 26:
            t += f"；当前 `nums[c] + nums[d] = {S['s'] - S['x'] - S['y']}`"
        return t
    return f"固定第一个数 `x = {S['x']}`，target = =={TARGET}=="


def _ans(S):
    a = S.get('ans')
    if not a:
        return '答案：（暂无）'
    return '答案：' + '，'.join(f'`{q}`' for q in a)


def _cap_dup_a(S, B, r):
    a = S.a
    if a and S.x == S.nums[a - 1]:
        return f'`x = {S.x}` 和前一个数相同：它的所有组合==之前都找过== → 跳过'
    return '`a = 0`，第一个数不用判重' if a == 0 else f'`x = {S.x}` 和前一个数 `{S.nums[a - 1]}` 不同'


def _cap_opt1a(S, B, r):
    n = S.nums; a = S.a
    v = S.x + n[a + 1] + n[a + 2] + n[a + 3]
    if v > TARGET:
        return f'x 能凑出的最小和 `{v} > {TARGET}`：再往后只会更大 → ==break=='
    return f'优化一：x 加紧挨着的三个数 = `{v}`（最小和）≤ target，还有希望'


def _cap_opt2a(S, B, r):
    n = S.nums
    v = S.x + n[-3] + n[-2] + n[-1]
    if v < TARGET:
        return f'x 能凑出的最大和 `{v} < {TARGET}`：这个 x 不行，但更大的 x 也许行 → ==continue=='
    return f'优化二：x 加最大的三个数 = `{v}`（最大和）≥ target，值得往下枚举'


def _cap_dup_b(S, B, r):
    b = S.b
    if b > S.a + 1 and S.y == S.nums[b - 1]:
        return f'`y = {S.y}` 和前一个数相同 → 跳过（`b > a + 1` 保证 y 不是和 x 比）'
    if b == S.a + 1:
        return '`b = a + 1`：第二个数的第一个候选，==不判重==（否则会漏掉 `x == y` 的答案）'
    return f'`y = {S.y}` 和前一个数 `{S.nums[b - 1]}` 不同'


def _cap_opt1b(S, B, r):
    n = S.nums; b = S.b
    v = S.x + S.y + n[b + 1] + n[b + 2]
    if v > TARGET:
        return f'x + y + 紧挨着的两个数 = `{v} > {TARGET}` → ==break=='
    return f'x + y 能凑出的最小和 `{v}` ≤ target，继续'


def _cap_opt2b(S, B, r):
    n = S.nums
    v = S.x + S.y + n[-2] + n[-1]
    if v < TARGET:
        return f'x + y + 最大的两个数 = `{v} < {TARGET}` → 换更大的 y，==continue=='
    return f'x + y 能凑出的最大和 `{v}` ≥ target → 跑双指针'


def _cap_s(S, B, r):
    s = S.s
    head = f'`s = {S.x} + {S.y} + {S.nums[S.c]} + {S.nums[S.d]} = {s}`'
    if s > TARGET:
        return head + f' > {TARGET}：和太大 → 换更小的 `nums[d]`'
    if s < TARGET:
        return head + f' < {TARGET}：和太小 → 换更大的 `nums[c]`'
    return head + ' ==等于 target==：找到一组！'


CONFIG = dict(
    num=18, title='四数之和', difficulty='Medium', category='双指针',
    author='灵茶山艾府', technique='排序 + 两重枚举 + 相向双指针 + 剪枝',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        ans = []
        n = len(nums)
        for a in range(n - 3):  # 枚举第一个数
            x = nums[a]
            if a and x == nums[a - 1]:  # 跳过重复数字
                continue
            if x + nums[a + 1] + nums[a + 2] + nums[a + 3] > target:  # 优化一
                break
            if x + nums[-3] + nums[-2] + nums[-1] < target:  # 优化二
                continue
            for b in range(a + 1, n - 2):  # 枚举第二个数
                y = nums[b]
                if b > a + 1 and y == nums[b - 1]:  # 跳过重复数字
                    continue
                if x + y + nums[b + 1] + nums[b + 2] > target:  # 优化一
                    break
                if x + y + nums[-2] + nums[-1] < target:  # 优化二
                    continue
                # 双指针枚举第三个数和第四个数
                c = b + 1
                d = n - 1
                while c < d:
                    s = x + y + nums[c] + nums[d]  # 四数之和
                    if s > target:
                        d -= 1
                    elif s < target:
                        c += 1
                    else:  # s == target
                        ans.append([x, y, nums[c], nums[d]])
                        c += 1
                        while c < d and nums[c] == nums[c - 1]:  # 跳过重复数字
                            c += 1
                        d -= 1
                        while d > c and nums[d] == nums[d + 1]:  # 跳过重复数字
                            d -= 1
        return ans
''',
    call=f'Solution().fourSum({NUMS}, {TARGET})',
    expect=[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]],
    skip=['n = len', 'y = nums[b]', 'x = nums[a]', 'if s > target', 'elif s < target'],
    max_steps=75,
    views=[
        dict(type='text', fn=_sum, size=26, h=70),
        dict(type='array', var='nums', label='nums（排序后；紫 = a，蓝 = b，绿/粉 = 双指针 c/d）', h=330,
             pointers={'a': 'purple', 'b if _line >= 14 else None': 'blue',
                       'c if _line >= 23 else None': 'green', 'd if _line >= 24 else None': 'pink'},
             pointer_labels={'b if _line >= 14 else None': 'b', 'c if _line >= 23 else None': 'c',
                             'd if _line >= 24 else None': 'd'},
             color=lambda S, i, v: ('purple' if i == S.get('a') else
                                    'blue' if i == S.get('b') and S['_line'] >= 14 else
                                    'green' if i == S.get('c') and S['_line'] >= 23 else
                                    'pink' if i == S.get('d') and S['_line'] >= 24 else None)),
        dict(type='text', fn=_ans, size=28, h=110, lines=2),
    ],
    watch=[('a', 'a', 'purple'), ('b', 'b', 'blue'), ('c', 'c', 'green'), ('d', 'd', 'pink'), 's'],
    captions={
        'nums.sort()': '先排序：`{nums}`，才能剪枝和用双指针',
        'for a in range': lambda S, B, r: (f'枚举第一个数 `a = {S.a}`，`x = {S.nums[S.a]}`' if S.a != B.get('a') else '第一个数枚举完'),
        8: _cap_dup_a,
        10: _cap_opt1a,
        12: _cap_opt2a,
        'for b in range': lambda S, B, r: (f'枚举第二个数 `b = {S.b}`，`y = {S.nums[S.b]}`' if S.b != B.get('b') else f'x = `{S.x}` 的第二个数枚举完 → 换下一个 x'),
        16: _cap_dup_b,
        18: _cap_opt1b,
        20: _cap_opt2b,
        'c = b + 1': '剩下两个数用双指针：`c = {c}` 从 y 右边开始',
        'd = n - 1': '`d = {d}` 从最右开始',
        'while c < d:': lambda S, B, r: (f'`c = {S.c} < d = {S.d}`，继续' if S.c < S.d else f'`c = {S.c} ≥ d = {S.d}`：这组 x、y 的组合都看过了'),
        's = x + y': _cap_s,
        'if s > target': lambda S, B, r: ('和太大 → 换更小的 `nums[d]`' if S.s > TARGET else f'`{S.s}` 不大于 target'),
        'd -= 1': lambda S, B, r: f'`d` 左移到 {S.d}',
        'elif s < target': lambda S, B, r: ('和太小 → 换更大的 `nums[c]`' if S.s < TARGET else '`s == target`：找到一组！'),
        'c += 1': lambda S, B, r: f'`c` 右移到 {S.c}',
        'ans.append': '记录答案 =={ans[-1]}==',
        'while c < d and': lambda S, B, r: (f'`nums[{S.c}]` 和前一个相同 → 继续右移，避免重复四元组' if S.c < S.d and S.nums[S.c] == S.nums[S.c - 1] else '右边没有重复的 c 了'),
        'while d > c and': lambda S, B, r: (f'`nums[{S.d}]` 和后一个相同 → 继续左移' if S.d > S.c and S.nums[S.d] == S.nums[S.d + 1] else '左边没有重复的 d 了'),
        9: '跳过重复的 x',
        11: '更大的 x 只会让和更大 → 结束全部枚举',
        13: '这个 x 太小，直接换下一个 x',
        17: '跳过重复的 y，看下一个',
        19: '更大的 y 只会更大 → 换下一个 x',
        21: '这个 y 太小，换下一个 y',
        'return ans': '返回全部 `{len(ans)}` 个不重复的四元组',
    },
    cards=dict(
        one_liner='三数之和再套一层：排序，枚举前两个数，后两个数用双指针',
        complexity='时间 `O(n^3)`，空间 `O(1)`（忽略返回值和排序栈开销）',
        problem=['在 `nums` 里找出所有==不重复==的四元组，四个下标互不相同，和等于 `target`',
                 '示例：`nums = [1,0,-1,0,-2,2], target = 0`',
                 '→ `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]`'],
        quote='排序后，枚举 nums[a] 作为第一个数，枚举 nums[b] 作为第二个数，那么问题变成找到另外两个数，使得这四个数的和等于 target，这可以用==双指针==解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和 15. 三数之和一样，只是==多套一层循环==',
              '每层都有三个优化：重复跳过；最小和 > target 就 `break`；最大和 < target 就 `continue`',
              '`b > a + 1` 的判断必不可少，否则 `[2,2,2,2,2]` 会漏答案'],
        summary=['时间 `O(n^3)`：两重枚举 × 双指针 `O(n)`',
                 '去重三处：x 重复、y 重复（`b > a + 1`）、找到答案后 c/d 跳过相同值',
                 '易错：剪枝条件里 `break` 和 `continue` 别写反',
                 'Java/C++ 要用 64 位整数存四数之和，防溢出',
                 '只求个数可以更快：见 454. 四数相加 II'],
    ),
)
