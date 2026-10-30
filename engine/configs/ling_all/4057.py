CONFIG = dict(
    num=4057, title='统计相交区间对 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='正难则反 · 起点终点分开排序 + 双指针',
    tags=[],
    code='''
class Solution:
    def countIntersectingIntervals(self, intervals: list[list[int]]) -> int:
        n = len(intervals)
        starts = sorted(p[0] for p in intervals)
        ends = sorted(p[1] for p in intervals)

        ans = n * (n - 1) // 2
        # 对于每个左端点 start，右端点 < start 的区间都与之不相交
        j = 0
        for start in starts:
            while j < n and ends[j] < start:
                j += 1
            # [0, j-1] 的区间与当前区间不相交，这有 j 个
            ans -= j
        return ans
''',
    call='Solution().countIntersectingIntervals([[1, 5], [2, 4], [3, 6], [8, 9]])',
    expect=3,
    views=[
        dict(type='array', var='starts', label='starts（升序）：蓝色 = 当前 start', cell=100, h=190,
             color=lambda S, i, v: 'blue' if 'start' in S and v == S['start'] else None),
        dict(type='array', var='ends', label='ends（升序）：j 指向第一个 ≥ start 的右端点，左边的都不相交', cell=100, h=230,
             pointers={'j': 'pink'},
             dim=lambda S, i, v: 'j' in S and i >= S['j'],
             color=lambda S, i, v: 'pink' if 'j' in S and i < S['j'] else None),
        dict(type='text', fn=lambda S: (f"所有区间对 `{S['n']*(S['n']-1)//2}`，减去不相交的，当前 `ans = {S['ans']}`" if 'ans' in S and 'n' in S else ''),
             size=28, h=80),
    ],
    watch=[('start', 'start', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'n = len(intervals)': '`n = {n}` 个区间',
        'starts = sorted': '把所有左端点单独拿出来排序：`{starts}`',
        'ends = sorted': '把所有右端点单独排序：`{ends}`（与下标无关，所以可以拆开）',
        'ans = n * (n - 1) // 2': '先假设所有 `{n} × {n-1} / 2` = =={ans}== 对都相交，后面减去不相交的',
        'j = 0': '`j` 是右端点数组的指针，只增不减',
        'for start in starts': lambda S, B, r: (f'枚举左端点 `start = {S.start}`' if 'start' not in B or B.start != S.start else '左端点都枚举完了'),
        'while j < n and ends[j] < start': lambda S, B, r: (
            f'`ends[{S.j}] = {S.ends[S.j]}` < `start = {S.start}`：这个区间在 start 之前就结束了 → 不相交，`j` 右移'
            if S.j < S.n and S.ends[S.j] < S.start else
            (f'`j = {S.j} = n`：右端点都比 start 小' if S.j >= S.n else f'`ends[{S.j}] = {S.ends[S.j]}` ≥ `start = {S.start}`：它和更大的右端点都与 start 相交，停下')),
        'j += 1': '`j` → {j}：又多了一个不相交的区间',
        'ans -= j': '右端点 `< {start}` 的区间有 `{j}` 个，都与当前区间不相交 → `ans` 减去 {j} → =={ans}==',
        'return ans': '相交的区间对一共 =={ret}== 对',
    },
    cards=dict(
        one_liner='正难则反：总对数减去不相交的对数，端点拆开排序 + 双指针',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`intervals[i] = [start, end]` 是闭区间，至少有一个公共点就算相交；n 可达 10^5',
                 '数出满足 `i < j` 且相交的下标对个数',
                 '示例：`[[1,5],[2,4],[3,6],[8,9]]` → `3`'],
        quote='这个问题与下标无关，我们可以把 intervals 拆成两个独立的数组 starts 和 ends，分别保存所有左端点和所有右端点。然后，把两个数组都升序排序，就可以用双指针快速求出有多少对 (i,j) 满足 end_i < start_j。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先算补集：不相交的对满足 `end_i < start_j`，按左端点排序后 `i < j` 自动成立',
              '条件与下标无关 → 左右端点各自排序，用同向双指针数个数',
              '对每个 `start`，右端点 `< start` 的有 `j` 个，答案从 `n(n-1)/2` 里减去'],
        summary=['时间 `O(n log n)`，瓶颈在排序，空间 `O(n)`',
                 '易错：不相交是 `end < start`，严格小于，只共享端点的算相交',
                 '`j` 只增不减，因为 `starts` 升序，前一个 start 不相交的，对后一个也不相交',
                 '题解方法一：按右端点排序后，对每个 start 二分查找 `bisect_left`，同样 `O(n log n)`'],
    ),
)
