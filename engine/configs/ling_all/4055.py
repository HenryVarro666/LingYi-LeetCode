def _st(name):
    def f(S):
        a = S.get('a')
        st = S.get(name)
        if a is None or st is None:
            return None
        return [f'{a[i]}@{i}' for i in st]
    return f


def _seg(S):
    st, ss = S.get('low_st'), S.get('seg_starts')
    if st is None or ss is None:
        return None
    return [f'{k}→{S["a"][st[k]]}' if k < len(st) else f'{k}' for k in ss]


def _col(S, i, v):
    if 'mid_num' not in S:
        return None
    return 'blue' if v <= S['mid_num'] else 'pink'


def _cur(S):
    return S['i'] if 'mid_num' in S and 'x' in S and S['_inner'].get('i') is not None else None


def _line(S):
    if 'mid_num' not in S:
        return '`sorted_nums` 排序去重，用下标做值域分治'
    mn = S['mid_num']
    lo = [x for x in S['a'] if x <= mn]
    hi = [x for x in S['a'] if x > mn]
    return f'分界 `mid_num = {mn}`：蓝 ≤ {mn} 作 nums[i]，粉 > {mn} 作 nums[j]'


CONFIG = dict(
    num=4055, title='统计影子数对 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='值域分治 + 单调栈',
    tags=['灵神题单·常用数据结构', '难度分 2631'],
    code='''
class Solution:
    def shadowPairs(self, nums: list[int]) -> int:
        def solve(a: list[int], low: int, high: int) -> None:
            if low == high or len(a) <= 1:
                return

            nonlocal ans
            mid = (low + high) // 2
            mid_num = sorted_nums[mid]
            low_st = []
            high_st = []
            b = []
            c = []

            # 把 low_st 按照 high_st 中的数划分成若干段，维护每一段的第一个数在 low_st 中的位置
            seg_starts = []

            for i, x in enumerate(a):
                if x <= mid_num:  # x 在下部，作为 nums[i]
                    while low_st and a[low_st[-1]] < x:
                        low_st.pop()  # 因为 x 的出现，栈顶不能作为 nums[i]

                    while seg_starts and seg_starts[-1] >= len(low_st):
                        seg_starts.pop()  # 最后一段是空的

                    if not seg_starts or high_st and high_st[-1] > low_st[-1]:
                        # 即将插入 low_st 的 i 是新段的第一个数
                        seg_starts.append(len(low_st))

                    low_st.append(i)
                    b.append(x)
                else:  # x 在上部，作为 nums[j]
                    # 找到 x 左侧第一个小于 x 的最近元素，作为 nums[k]
                    while high_st and a[high_st[-1]] >= x:
                        high_st.pop()

                    p = high_st[-1] if high_st else -1
                    while len(seg_starts) > 1 and low_st[seg_starts[-2]] > p:
                        seg_starts.pop()  # 合并最后两段

                    # 统计 low_st 中 > high_st[-1] 的元素个数
                    if seg_starts and (not high_st or high_st[-1] < low_st[-1]):
                        ans += len(low_st) - seg_starts[-1]

                    high_st.append(i)
                    c.append(x)

            solve(b, low, mid)
            solve(c, mid + 1, high)

        sorted_nums = sorted(set(nums))
        ans = 0
        solve(nums, 0, len(sorted_nums) - 1)
        return ans
''',
    call='Solution().shadowPairs([3, 1, 4, 2])',
    expect=3,
    max_steps=54,
    views=[
        dict(type='text', fn=_line, size=24, h=50),
        dict(type='array', var='a', label='a（当前这一层的数组；蓝 = 下部，粉 = 上部）', cell=76, h=210,
             pointers={'i if "x" in _inner else None': 'yellow'}, pointer_labels={'i if "x" in _inner else None': 'i'},
             color=_col),
        dict(type='stack', var=_st('low_st'), label='low_st（下部，值@下标；栈底→栈顶递减）', h=110, font=24),
        dict(type='stack', var=_st('high_st'), label='high_st（上部，值@下标；栈底→栈顶递增）', h=110, font=24),
        dict(type='stack', var=_seg, label='seg_starts（low_st 的分段起点：位置→值）', h=110, font=24),
        dict(type='calls', h=130, hide=('a',)),
    ],
    skip=['high_st = []', 'low_st = []', 'b = []', 'c = []', 'b.append', 'c.append', 'mid = (low'],
    watch=[('x', 'x if "x" in _inner else None', 'yellow'), ('mid_num', 'mid_num'), ('ans', 'ans', 'green')],
    captions={
        'if low == high': lambda S, B, r: ('值域只剩一个值，或数组 ≤ 1 个：没有 nums[i] < nums[j]，返回' if (S.low == S.high or len(S.a) <= 1)
                                           else f'`a = {S.a}`，值域下标 `[{S.low}, {S.high}]`，需要继续分治'),
        'mid = (low + high)': '以值域中点为界，==按值大小==切成下部和上部',
        'mid_num = sorted': '分界值 `mid_num = sorted_nums[{mid}] = {mid_num}`：`x ≤ {mid_num}` 在下部，否则在上部',
        'seg_starts = []': 'low_st 会被 high_st 里的数分成若干段，`seg_starts` 记每段的起点',
        'for i, x in enumerate(a)': lambda S, B, r: (f'从左到右枚举 `a[{S.i}] = {S.x}`（枚举右、维护左）' if not ('i' in B and B.i == S.i and B.x == S.x) else '这一层枚举完了，分别递归下部和上部'),
        'if x <= mid_num': '`{x} ≤ {mid_num}`？{"是：x 在下部，当 nums[i] 的候选" if x <= mid_num else "否：x 在上部，当 nums[j]"}',
        'while low_st and a[low_st[-1]] < x': '栈顶 `{a[low_st[-1]] if low_st else "无"}` 比 x 小 → 有 `nums[k]=x` 夹在它和任何上部数之间，它再也不能当 nums[i]，弹出'
        if False else lambda S, B, r: (f'栈顶 `{S.a[S.low_st[-1]]}` < `{S.x}`：x 会夹在它与上部数之间，==弹出== 它' if S.low_st and S.a[S.low_st[-1]] < S.x else '栈空或栈顶 ≥ x，不弹了；low_st 保持递减'),
        'low_st.pop()': '弹出后 `low_st` = {[a[t] for t in low_st]}',
        'while seg_starts and seg_starts[-1] >= len(low_st)': lambda S, B, r: ('最后一段起点 `{}` ≥ 栈长 `{}`：那一段的数都被弹光了，弹掉这段起点'.format(S.seg_starts[-1], len(S.low_st)) if S.seg_starts and S.seg_starts[-1] >= len(S.low_st) else '最后一段还有数，不用弹'),
        'seg_starts.pop()  # 最后': '`seg_starts` 弹掉空段 → {seg_starts}',
        'if not seg_starts or high_st': lambda S, B, r: ('还没有任何段，x 开第一段' if not S.seg_starts else ('`high_st` 栈顶下标 `{}` > `low_st` 栈顶下标 `{}`：它们之间隔着上部的数，x 是新段第一个'.format(S.high_st[-1], S.low_st[-1]) if S.high_st and S.high_st[-1] > S.low_st[-1] else '上部没插进来过，x 并入最后一段')),
        'seg_starts.append': '新开一段，起点 = 当前 `low_st` 长度 `{len(low_st)}`',
        'low_st.append(i)': '`{x}` 入 `low_st`，它可能成为后面某个 nums[j] 的左端点',
        'b.append(x)': '下部的数留给递归的左半边',
        'while high_st and a[high_st[-1]] >= x': lambda S, B, r: (f'`high_st` 栈顶 `{S.a[S.high_st[-1]]}` ≥ `{S.x}`：它不可能是 x 左边“比 x 小”的最近数，弹出' if S.high_st and S.a[S.high_st[-1]] >= S.x else '栈空或栈顶 < x：栈顶就是 x 左侧最近的更小数，作为 nums[k]'),
        'p = high_st[-1]': '`p = {p}`：上部里 x 左侧最近的更小数的下标（作 nums[k]）；下标 < p 的下部数都被它夹住',
        'while len(seg_starts) > 1': lambda S, B, r: ('倒数第二段起点对应的数下标 `{}` > p = `{}`：这两段都在 nums[k] 右侧，没被隔开 → 合并'.format(S.low_st[S.seg_starts[-2]], S.p) if len(S.seg_starts) > 1 and S.low_st[S.seg_starts[-2]] > S.p else '没有可合并的段（只剩一段，或倒数第二段在 p 左侧被夹住）'),
        'seg_starts.pop()  # 合并': '合并最后两段，`seg_starts` = {seg_starts}',
        'if seg_starts and': lambda S, B, r: (('有段，且上部栈为空，没有 nums[k] 夹着，可以配对' if not S.high_st else '有段，且 `high_st` 栈顶下标 `{}` < `low_st` 栈顶下标 `{}`：最后一段没被 nums[k] 夹住，可以配对'.format(S.high_st[-1], S.low_st[-1])) if (S.seg_starts and (not S.high_st or S.high_st[-1] < S.low_st[-1])) else '没有可配的下部数（最后一段被 nums[k] 夹住或还没有下部数），这个 x 不产生答案'),
        'ans += len(low_st) - seg_starts[-1]': '最后一段大小 `{len(low_st)} - {seg_starts[-1]}` = =={len(low_st) - seg_starts[-1]}== 对，`ans` = {ans}',
        'high_st.append(i)': '`{x}` 入 `high_st`，后面更大的上部数遇到它时要弹掉',
        'c.append(x)': '上部的数留给递归的右半边',
        'solve(b, low, mid)': '下部的数递归处理：==下部内部==的影子对',
        'solve(c, mid + 1, high)': '上部的数递归处理：==上部内部==的影子对',
        'sorted_nums = sorted': '排序去重，之后用下标 `[0, {len(sorted_nums)-1}]` 做值域，每次对半切',
        'solve(nums, 0': '从整个值域开始分治',
        'return ans': '所有层累计完毕，一共 =={ret}== 个影子对',
    },
    cards=dict(
        one_liner='值域对半切，下部 × 上部的影子对用两个单调栈数出来',
        complexity='时间 `O(n log n)`，空间 `O(n log n)`',
        problem=['`(i, j)` 满足 `i < j` 且 `nums[i] < nums[j]`，',
                 '并且中间不存在下标 `k` 使 `nums[i] < nums[k] < nums[j]`',
                 '数出这样的“影子对”总数',
                 '本视频：`[3,1,4,2,5]` → `5`'],
        quote='用一个栈 lowSt 维护下部遍历过的元素，如果当前元素 x 比栈顶大，那么栈顶永远不能作为 nums[i]，弹出栈顶。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右维护左：从左到右扫，扫到 j 时看左边哪些 i 还有效',
              '值域分治：以值域中点切成下部、上部，下部配上部在本层算，内部递归',
              '下部用递减栈挡掉被夹住的 i；上部栈顶 p 作 nums[k]，只有下标 ≥ p 的下部数能配',
              '`seg_starts` 把 low_st 分段，最后一段的大小就是答案增量，省掉二分'],
        after=[dict(heading='另外两种写法', lines=['优化前：对 `low_st` 二分 `bisect_left(low_st, high_st[-1])`，`O(n log² n)`',
                                                     '空间优化：用外部辅助数组存 b、c，原地分治，空间 `O(n)`'])],
        summary=['时间 `O(n log n)`：每层每个下标进出每个栈至多一次',
                 '空间 `O(n log n)`：递归时右半边数组 `c` 暂存在栈里',
                 '易错：`low_st` 弹出用 `<`（相等不弹），`high_st` 弹出用 `>=`',
                 '易错：`p = -1` 表示上部左侧没有更小数，此时下部栈全部有效',
                 '同类：CDQ 分治 / 值域分治，先做单调栈再看这题'],
    ),
)
