def _sidx(S, name):
    v = S.get(name)
    a = S.get('a')
    if v is None or not a or v not in a:
        return None
    return a.index(v)


CONFIG = dict(
    num=3464, title='正方形上的点之间的最大距离', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='二分答案 + 二分查找',
    tags=['二分算法', '难度分 2806'],
    code='''
class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # 正方形边上的点，按照顺时针映射到一维数轴上
        a = []
        for x, y in points:
            if x == 0:
                a.append(y)
            elif y == side:
                a.append(side + x)
            elif x == side:
                a.append(side * 3 - y)
            else:
                a.append(side * 4 - x)
        a.sort()

        def check(low: int) -> bool:
            for start in a:  # 枚举第一个点
                end = start + side * 4 - low
                cur = start
                for _ in range(k - 1):  # 还需要找 k-1 个点
                    j = bisect_left(a, cur + low)
                    if j == len(a) or a[j] > end:  # 不能离第一个点太近
                        break
                    cur = a[j]
                else:
                    return True
            return False

        left, right = 1, side * 4 // k + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call='Solution().maxDistance(3, [[0,0],[0,2],[2,3],[3,3],[3,0],[1,0]], 4)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"二分下界 `low` = =={S['low']}==：要选 `{S['k']}` 个点，相邻至少差 `{S['low']}`，首尾至多差 `{S['end'] - S['start']}`"
                                        if 'low' in S and 'end' in S else
                                        (f"二分区间：`left = {S['left']}` 可行，`right = {S['right']}` 不可行" if 'left' in S and 'right' in S else ''))),
        dict(type='array', var='a', label='a：正方形周长拉直后的坐标（周长 = side×4 = 12，环形）', h=210,
             pointers={'a.index(start)': 'blue', 'a.index(cur)': 'green', 'j': 'pink'},
             pointer_labels={'a.index(start)': 'start', 'a.index(cur)': 'cur'},
             color=lambda S, i, v: ('blue' if i == _sidx(S, 'start') else 'green' if i == _sidx(S, 'cur') else None),
             dim=lambda S, i, v: False),
    ],
    watch=['left', 'right', ('mid', 'mid', 'yellow'), ('low', 'low', 'cyan'), ('start', 'start', 'blue'), ('cur', 'cur', 'green'), ('j', 'j', 'pink')],
    captions={
        'a = []': '把正方形的点按顺时针映射成一维坐标，放进 `a`',
        'a.append(y)': '左边界的点 `(0, y)`：坐标就是 `y`',
        'a.append(side + x)': '上边界的点：先走完左边 `side`，再走 `x`',
        'a.append(side * 3 - y)': '右边界的点：已走 `side*2`，再向下走 `side - y`，合起来 `side*3 - y`',
        'a.append(side * 4 - x)': '下边界的点：从右下角向左走，坐标 `side*4 - x`',
        'a.sort()': '排序后 `a = {a}`：现在是环形数组上选 k 个点',
        'left, right = 1, side * 4 // k + 1': '开区间二分：`left = 1` 一定可行；`right = side*4 // k + 1 = {right}` 均分周长也凑不出，一定不可行',
        'while left + 1 < right': lambda S, B, r: (f'`left + 1 = {S.left + 1} < right = {S.right}` → 区间里还有答案可猜' if S.left + 1 < S.right
                                                   else f'`left + 1 = {S.left + 1} ≥ right = {S.right}` → 答案就是 left'),
        'mid = (left + right) // 2': '区间 `({left}, {right})` 里猜距离下界 `mid = {mid}`：最小距离能否 ≥ mid？越大越难，有单调性',
        'if check(mid)': '调用 `check({mid})`：试探「最小距离 ≥ {mid}」能不能做到',
        'left = mid': '`mid` 可行 → 答案至少是 mid：`left = {left}`',
        'right = mid': '`mid` 不可行 → 答案比 mid 小：`right = {right}`',
        'def check': '`check(low)`：能否选出 k 个点，任意相邻距离 ≥ low',
        'for start in a': '枚举第一个点 `start = {start}`；最后一个点不能超过 `end = {start + side * 4 - low}`，否则绕一圈后离它不足 `low`',
        'end = start + side * 4 - low': '最后一个点不能超过 `end = {end}`：否则绕一圈后离第一个点不足 `low`',
        'cur = start': '`cur` = 当前已选的最后一个点，从 `start` 出发',
        'j = bisect_left(a, cur + low)': lambda S, B, r: f'二分找第一个 `≥ {S.cur + S.low}` 的点：`j = {S.j}`',
        'if j == len(a) or a[j] > end': lambda S, B, r: ('`j` 越界：后面没有点了 → 以这个起点凑不齐，==break==' if S.j == len(S.a)
                                                         else (f'`a[{S.j}] = {S.a[S.j]} > end = {S.end}` → 离第一个点太近，==break==' if S.a[S.j] > S.end
                                                               else f'`a[{S.j}] = {S.a[S.j]} ≤ end = {S.end}` → 合格，选它，`cur` 更新为 {S.a[S.j]}')),
        'return True': '一个起点凑齐了 k 个点 → ==可行==',
        'return False': '所有起点都凑不齐 → ==不可行==',
        'return left': '`left + 1 = {left + 1} ≥ right = {right}`，区间收拢 → 答案 `left = {left}`',
    },
    skip=['if x == 0', 'elif y == side', 'elif x == side', 'break', 'cur = start', 'end = start', 'for _ in range', 'cur = a[j]', 'while left + 1 < right', 'if check(mid)'],
    max_steps=140,
    cards=dict(
        one_liner='最大化最小值 → 二分距离下界，再贪心二分找下一个点',
        complexity='时间 `O(nk log side log n)`，空间 `O(n)`',
        problem=['正方形边长 `side`，`points` 是边界上互不相同的点，选 `k` 个点',
                 '使任意两点的==最小曼哈顿距离==尽量大，返回这个最大值',
                 '示例：`side=2`，`[[0,0],[1,2],[2,0],[2,2],[2,1]]`，`k=4` → `1`；本视频：`side=3`，6 个点，`k=4` → `2`'],
        quote='最大化最小值，考虑二分答案，即二分距离的下界 low。为什么？因为 low 越大，可以选的点越少，有单调性。把正方形拉成一条线，示例 2 的 5 个点在一维上的坐标为 a=[0,3,4,5,6]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把正方形边界顺时针拉直成环形数组 `a`，距离 ≥ `low` 就是坐标差 ≥ `low`',
              '`check(low)`：枚举第一个点，用 `bisect_left` 不断跳到「相距至少 low 的最近点」',
              '首尾也要相距 ≥ low：环绕后即要求最后一个点 `≤ start + side*4 - low`',
              '`k ≥ 4` 保证答案 ≤ side，所以二分找下一个点是对的'],
        summary=['二分上界 `side*4 // k + 1`：均分周长就是理论最大值',
                 '不用绕回数组开头再找一圈：从最后一个点出发搜不会更差',
                 '必须枚举第一个点：a 离 b 很近、离 c 很远时，换起点才可能成功',
                 '题解另有 k 指针、倍增、建树 DFS、二分 + DP 等写法，本视频用最直接的二分查找版'],
    ),
)
