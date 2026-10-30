NUMS = [4, 7, 6, 1, 5, 2, 9, 3, 8]
K, DIST = 3, 3


def _i(S):
    return S.get('i')


def _win(S):
    i = _i(S)
    if i is not None:
        return (i - DIST, i)
    if 'L' in S:
        return (1, DIST + 1)
    return None


def _color(S, j, v):
    L, R = S.get('L'), S.get('R')
    if L is None or j == 0:
        return 'yellow' if j == 0 else None
    w = _win(S)
    if w is None or not (w[0] - 1 <= j <= w[1]):
        return None
    if v in L:
        return 'green'
    if R is not None and v in R:
        return 'purple'
    return None


def _formula(S, B):
    L = S.get('L')
    if L is None:
        return '`nums[0]` 一定是第一段的代价；剩下要在窗口里挑 `k−1` 个最小的'
    parts = ' + '.join(str(x) for x in L)
    s = f'`sum_left = nums[0] + sum(L)` = {NUMS[0]} + {parts} = =={S.get("sum_left")}=='
    if 'ans' in S:
        s += f'　`ans = {S.ans}`'
    return s


def _sl(name):
    return lambda S: list(S[name]) if name in S else None


CONFIG = dict(
    num=3013, title='将数组分成最小总代价的子数组 II', difficulty='Hard', category='滑动窗口',
    author='灵茶山艾府', technique='两个有序集合维护前 k−1 小',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        k -= 1
        sum_left = sum(nums[:dist + 2])
        L = SortedList(nums[1:dist + 2])
        R = SortedList()
        def L2R() -> None:
            x = L.pop()
            nonlocal sum_left
            sum_left -= x
            R.add(x)
        def R2L() -> None:
            x = R.pop(0)
            nonlocal sum_left
            sum_left += x
            L.add(x)
        while len(L) > k:
            L2R()
        ans = sum_left
        for i in range(dist + 2, len(nums)):
            # 移除 out
            out = nums[i - dist - 1]
            if out in L:
                sum_left -= out
                L.remove(out)
            else:
                R.remove(out)
            # 添加 in
            in_val = nums[i]
            if in_val < L[-1]:
                sum_left += in_val
                L.add(in_val)
            else:
                R.add(in_val)
            # 维护大小
            if len(L) == k - 1:
                R2L()
            elif len(L) == k + 1:
                L2R()
            ans = min(ans, sum_left)
        return ans
''',
    setup='from sortedcontainers import SortedList',
    call=f'Solution().minimumCost({NUMS}, {K}, {DIST})',
    expect=7,
    skip=['nonlocal sum_left', '# 移除 out', '# 添加 in', '# 维护大小'],
    max_steps=80,
    views=[
        dict(type='array', var='nums', h=220,
             label='nums（黄 = nums[0]，青框 = 窗口，绿 = 在 L 中，紫 = 在 R 中）',
             pointers={_i: 'pink'}, pointer_labels={_i: 'i'}, window=(lambda S: (_win(S) or (None, None))[0],
                                                                    lambda S: (_win(S) or (None, None))[1]),
             color=_color),
        dict(type='array', var=_sl('L'), label='L：窗口里最小的 k 个（有序）', h=140, cell=90,
             color=lambda S, j, v: 'green'),
        dict(type='array', var=_sl('R'), label='R：窗口里其余的数（有序）', h=140, cell=90,
             color=lambda S, j, v: 'purple'),
        dict(type='text', fn=_formula, size=26, h=90),
    ],
    watch=[('k', 'k'), ('i', 'i', 'pink'), ('out', 'out', 'red'), ('in_val', 'in_val', 'cyan'),
           ('sum_left', 'sum_left', 'green'), ('ans', 'ans', 'yellow')],
    captions={
        'k -= 1': '为方便计算，把 `k` 减一：`k = {k}`，要选的是第 2~k 段的开头',
        'sum_left = sum(': '`sum_left` 先把 `nums[0]` 和整个初始窗口都加上：`{sum_left}`',
        'L = SortedList(': '初始窗口 `nums[1..dist+1]` 全放进 `L`：`{list(L)}`',
        'R = SortedList()': '`R` 存窗口里==不在前 k 小==的数',
        'x = L.pop()': '`L` 的最大值 `{x}` 弹出',
        'sum_left -= x': '`sum_left -= {x}` → {sum_left}',
        'R.add(x)': '`{x}` 放进 `R`：`R = {list(R)}`',
        'x = R.pop(0)': '`R` 的最小值 `{x}` 弹出',
        'sum_left += x': '`sum_left += {x}` → {sum_left}',
        'L.add(x)': '`{x}` 放进 `L`：`L = {list(L)}`',
        'while len(L) > k': lambda S, B, ret: (f'`len(L) = {len(S.L)} > k = {S.k}` → 把最大的移到 R'
                                               if len(S.L) > S.k else f'`L` 只剩最小的 `{S.k}` 个了'),
        'ans = sum_left': '第一个窗口的代价：`ans = {ans}`',
        'for i in range': lambda S, B, ret: (f'窗口右移：新窗口 `[{S.i - DIST}, {S.i}]`' if S.get('i') != B.get('i')
                                             else '窗口滑到底了'),
        'out = nums[i - dist - 1]': '`out = nums[{i - dist - 1}] = {out}` 离开窗口',
        'if out in L': lambda S, B, ret: (f'`{S.out}` 在 `L` 中 → 从 L 删除，并从 `sum_left` 减掉' if S.out in S.L
                                          else f'`{S.out}` 不在 `L` 中 → 从 R 删除即可'),
        'sum_left -= out': '`sum_left -= {out}` → {sum_left}',
        'L.remove(out)': '`L = {list(L)}`',
        'R.remove(out)': '`R = {list(R)}`',
        'in_val = nums[i]': '`in_val = nums[{i}] = {in_val}` 进入窗口',
        'if in_val < L[-1]': lambda S, B, ret: (f'`{S.in_val} < L[-1] = {S.L[-1]}` → 它可能是前 k 小，==放进 L=='
                                                if S.in_val < S.L[-1] else
                                                f'`{S.in_val} ≥ L[-1] = {S.L[-1]}` → 放进 R'),
        'sum_left += in_val': '`sum_left += {in_val}` → {sum_left}',
        'L.add(in_val)': '`L = {list(L)}`',
        'R.add(in_val)': '`R = {list(R)}`',
        'if len(L) == k - 1': lambda S, B, ret: (f'`len(L) = {len(S.L)}`，少了一个 → ==从 R 补最小的==' if len(S.L) == S.k - 1
                                                 else f'`len(L) = {len(S.L)}`，不缺'),
        'elif len(L) == k + 1': lambda S, B, ret: (f'`len(L) = {len(S.L)}`，多了一个 → ==把最大的挪到 R==' if len(S.L) == S.k + 1
                                                   else f'`len(L) = {len(S.L)} = k`，大小正好'),
        'R2L()': '调用 `R2L()`',
        'L2R()': '调用 `L2R()`',
        'ans = min(ans, sum_left)': '`ans = min({B.ans}, {sum_left})` = =={ans}==',
        'return ans': '最小总代价 `{ret}`',
    },
    cards=dict(
        one_liner='大小为 dist+1 的滑动窗口里，求前 k−1 小的元素和',
        complexity='时间 `O(n log dist)`，空间 `O(dist)`',
        problem=['把 `nums` 切成 `k` 段，代价 = 每段第一个数之和',
                 '要求第 2 段开头 `i₁` 与第 k 段开头满足 `i_(k−1) − i₁ ≤ dist`',
                 '示例：`[1,3,2,6,4,2], k=3, dist=3` → `5`（1+2+2）',
                 '本视频：`[4,7,6,1,5,2,9,3,8], k=3, dist=3` → `7`'],
        quote='考虑到 q−p ≤ dist，本题相当于在一个大小固定为 dist+1 的滑动窗口内，求前 k−1 小的元素和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一段代价固定是 `nums[0]`；其余 `k−1` 个开头落在长 `dist+1` 的窗口里',
              '仿照 480 题：`L` 存窗口里最小的 `k−1` 个，`R` 存其余的',
              '滑窗时先移出 out、再移入 in，最后==把 L 的大小调回 k−1=='],
        result='所有窗口里 `sum_left` 的最小值 `7` = 4 + 1 + 2 ✓',
        summary=['时间 `O(n log dist)`，空间 `O(dist)`',
                 '易错：`sum_left` 只随 `L` 变化，进出 `R` 不影响它',
                 '易错：代码里 `k` 已减一，`L` 的目标大小是 `k`',
                 '另一种写法：对顶堆 + 懒删除（没有有序集合的语言用）'],
    ),
)
