def _info(S):
    if 'x' not in S:
        return '先把 (nums1, nums2) 绑成点对，按 nums1 从大到小排序'
    st = S.get('st') or []
    s = f'当前询问 `x = {S["x"]}, y = {S["y"]}`（询问下标 {S["i"]}）'
    if S.get('j', 0) is not None and 'a' in S:
        s += f'　已处理 `{S["j"]}` 个点对'
    return s


def _stinfo(S):
    st = S.get('st')
    if not st:
        return '单调栈：栈底到栈顶 `ay` 递增，`ax+ay` 递减'
    return '单调栈：' + '，'.join(f'(ay={p[0]}, 和={p[1]})' for p in st)


def _gcol(S, i, v):
    return None


CONFIG = dict(
    num=2736, title='最大和查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='离线 + 排序 + 单调栈二分',
    tags=['灵神题单·单调栈', '灵神题单·常用数据结构', '难度分 2533'],
    code='''
class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        ans = [-1] * len(queries)
        a = sorted(((a, b) for a, b in zip(nums1, nums2)), key=lambda p: -p[0])
        j = 0
        st = []
        for i, (x, y) in sorted(enumerate(queries), key=lambda p: -p[1][0]):
            while j < len(a) and a[j][0] >= x:  # 下面只需关心 ay (a[j][1])
                ax, ay = a[j]
                while st and st[-1][1] <= ax + ay:  # ay >= st[-1][0]
                    st.pop()
                if not st or st[-1][0] < ay:
                    st.append((ay, ax + ay))
                j += 1
            p = bisect_left(st, (y,))
            if p < len(st):
                ans[i] = st[p][1]
        return ans
''',
    call='Solution().maximumSumQueries([2,9,4,6,3], [4,1,3,2,6], [[3,2],[7,1],[10,1],[5,4]])',
    expect=[9, 10, -1, -1],
    skip=['j = 0', 'st = []'],
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='array', var='a', label='a：按 nums1 从大到小排序的 (nums1, nums2)', pointers={'j': 'blue'}, h=230,
             fmt=lambda v: f'{v[0]},{v[1]}', cell=120,
             color=lambda S, i, v: 'green' if 'j' in S and i < S['j'] else None),
        dict(type='stack', var='st', label='st：(ay → ax+ay)，栈底 ay 小、和大', fmt=lambda p: f'{p[0]}→{p[1]}', h=170),
        dict(type='array', var='ans', label='ans（-1 表示还没有答案）', h=170,
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=['j', ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('p', 'p', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = [-1]': '每个询问的答案先设为 `-1`（没有满足条件的点）',
        'a = sorted': '把 nums1、nums2 绑成点对，按 nums1 ==从大到小==排序：`{a}`',
        'for i, (x, y)': lambda S, B, r: (
            '所有询问都回答完了，循环结束' if 'i' in B and B.i == S.i and 'x' in B else
            f'按 `x` 从大到小回答询问：现在是 `x = {S.x}, y = {S.y}`（原下标 {S.i}）'),
        'while j < len(a)': lambda S, B, r: (
            f'`a[{S.j}][0] = {S.a[S.j][0]} ≥ x = {S.x}` → 这个点的 nums1 满足要求，==加入栈==' if S.j < len(S.a) and S.a[S.j][0] >= S.x
            else f'没有更多 nums1 ≥ {S.x} 的点了 → 开始查栈'),
        'ax, ay = a[j]': '取出点 `({ax}, {ay})`，它的和是 `{ax + ay}`',
        'while st and st[-1][1] <= ax + ay': lambda S, B, r: (
            f'栈顶的和 `{S.st[-1][1]}` ≤ 新和 `{S.ax + S.ay}`，而新点 ay 更大 → ==栈顶永远不会是最优==，弹出'
            if S.st and S.st[-1][1] <= S.ax + S.ay else
            ('栈空了，不用再弹' if not S.st else f'栈顶的和 `{S.st[-1][1]}` > 新和 `{S.ax + S.ay}` → 停止弹出')),
        'st.pop()': '弹出栈顶，栈中还剩 `{len(st)}` 个',
        'if not st or st[-1][0] < ay': lambda S, B, r: (
            ('栈已空 → 直接入栈' if not S.st else f'栈顶 ay = {S.st[-1][0]} < {S.ay} → 新点 ay 更大，可以入栈') if (not S.st or S.st[-1][0] < S.ay)
            else f'栈顶 ay = {S.st[-1][0]} ≥ {S.ay} 且和更大 → 新点被栈顶压住，==不入栈=='),
        'st.append': '入栈 `(ay, ax+ay) = ({st[-1][0]}, {st[-1][1]})`，栈中 ay 递增、和递减',
        'j += 1': '`j` → {j}',
        'p = bisect_left': '在栈里二分 ==第一个 ay ≥ y== 的位置：`p = {p}`（栈长 {len(st)}）。这个位置的和就是最大的',
        'if p < len(st)': lambda S, B, r: (
            f'`p = {S.p} < {len(S.st)}`，栈里有 ay ≥ {S.y} 的点' if S.p < len(S.st)
            else f'`p = {S.p}` 越界：所有点的 ay 都 < {S.y} → 答案保持 `-1`'),
        'ans[i] = st[p][1]': '询问 {i} 的答案 = `st[{p}][1]` = =={ans[i]}==',
        'return ans': '全部询问回答完毕：`{ans}`',
    },
    cards=dict(
        one_liner='离线按 x 从大到小答询问，单调栈里二分 y',
        complexity='时间 `O(n log n + q log q + q log n)`，空间 `O(n + q)`',
        problem=['给两个数组 `nums1`、`nums2` 和若干询问 `[x, y]`',
                 '每个询问：在 `nums1[j] ≥ x` 且 `nums2[j] ≥ y` 的 `j` 中，求 `nums1[j]+nums2[j]` 最大值，没有则 `-1`',
                 '官方示例：`[4,3,1,2]`、`[2,4,9,5]`，`[[4,1],[1,3],[2,5]]` → `[6,10,7]`',
                 '本视频用 5 个点、4 个询问，演示弹栈和 `-1`'],
        quote='如果 nums1[j]+nums2[j] 不低于栈顶的 nums1[j\']+nums2[j\']，那么可以弹出栈顶。因为更大的 nums2[j] 更能满足 ≥ y 的要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['点对按 `nums1` 降序，询问按 `x` 降序：==x 这一维自动满足==，只需关心 `y`',
              '新点和更大且 ay 更大 → 栈顶没用，弹出；栈内 ay 递增、和递减',
              '查询时二分第一个 `ay ≥ y`：它的和==最大=='],
        summary=['时间 `O(n log n + q log q + q log n)`，空间 `O(n + q)`',
                 '先用排序把一维消掉，另一维交给单调栈 + 二分：「离线」的典型套路',
                 '入栈条件 `st[-1][0] < ay`：ay 不更大的点被栈顶压住，不能入栈',
                 '`bisect_left(st, (y,))` 利用元组比较：`(y,)` 小于任何 `(y, 和)`',
                 '同类：本题也可用树状数组做，见灵神题单树状数组一节'],
    ),
)
