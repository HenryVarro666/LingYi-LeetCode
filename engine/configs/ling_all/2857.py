def _pt(S):
    if 'x' not in S:
        return '按顺序枚举点 `(x2, y2)`，哈希表里存==之前==点的个数'
    if 'i' not in S or S['_line'] is None:
        return f'当前点 `({S["x"]}, {S["y"]})`'
    i, k = S['i'], S['k']
    x, y = S['x'], S['y']
    return (f'当前点 `({x}, {y})`，x 异或 =={i}==、y 异或 =={k - i}==：'
            f'找 `({x ^ i}, {y ^ (k - i)})`，已有 =={S["cnt"].get((x ^ i, y ^ (k - i)), 0)}== 个')


CONFIG = dict(
    num=2857, title='统计距离为 k 的点对', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='枚举异或值 + 哈希表',
    tags=['灵神题单·位运算', '难度分 2082'],
    code='''
class Solution:
    def countPairs(self, coordinates: List[List[int]], k: int) -> int:
        ans = 0
        cnt = Counter()
        for x, y in coordinates:
            for i in range(k + 1):
                ans += cnt[x ^ i, y ^ (k - i)]  # tuple 的括号可以省略
            cnt[x, y] += 1  # tuple 的括号可以省略
        return ans
''',
    call='Solution().countPairs([[1,2],[4,2],[1,3],[5,2]], 1)',
    expect=2,
    views=[
        dict(type='table', var='coordinates', label='coordinates（每行一个点）', h=210, cell=70),
        dict(type='map', var='cnt', label='cnt（已遍历点的个数）', fmt=lambda k, v: f'{k}: {v}', h=190, font=30),
        dict(type='text', h=90, size=28, fn=_pt),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('i', 'i', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'for x, y in coordinates': lambda S, B, r: ('取下一个点 `(x2, y2) = (%d, %d)`' % (S.x, S.y)) if 'x' not in B or (S.x, S.y) != (B.x, B.y) or S.i == S.k and S.cnt[S.x, S.y] > 0 and False else '所有点都处理完了',
        'for i in range(k + 1)': lambda S, B, r: (f'枚举 `x1⊕x2 = i`，则 `y1⊕y2 = k − i`：`i = {S.i}`，`k − i = {S.k - S.i}`' if 'i' not in B or S.i != B.i or S.x != B.x else '`i` 枚举完了，这个点查询结束'),
        'ans += cnt': '异或可移项：`x1 = x2⊕i = {x ^ i}`，`y1 = y2⊕(k−i) = {y ^ (k - i)}`，之前这样的点有 `{cnt[x ^ i, y ^ (k - i)]}` 个 → `ans = {ans}`',
        'cnt[x, y] += 1': '查完再把 `({x}, {y})` 放进哈希表，==先查后加==保证 `i < j`',
        'return ans': '距离为 k 的点对共 `{ans}` 对',
    },
    max_steps=90,
    cards=dict(
        one_liner='异或结果都非负，所以每一维异或值都不超过 k',
        complexity='时间 `O(nk)`，空间 `O(n)`',
        problem=['点对距离 = `(x1⊕x2) + (y1⊕y2)`，求 `i < j` 且距离为 `k` 的点对数',
                 '示例：`[[1,2],[4,2],[1,3],[5,2]]`，`k=5` → `2`（(0,1) 与 (2,3)）',
                 '本视频：同一组点，`k=1` → `2`（(0,2) 与 (1,3)）'],
        quote='突破口：0≤k≤100。……异或运算类似加法，我们可以把 x2 和 y2 移到等式右侧。枚举 (x2,y2)，则 x1 = x2⊕i 且 y1 = y2⊕(k−i)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['异或和都是非负数，和为 k → `x` 方向异或值只可能是 `0..k`',
              '枚举 `i = x1⊕x2`，另一维异或值就是 `k − i`',
              '异或可以移项：已知 `(x2,y2)` 和 `i`，就能直接算出要找的 `(x1,y1)`，查哈希表即可'],
        summary=['时间 `O(nk)`，空间 `O(n)`；暴力 `O(n²)` 会超时',
                 '==先查询再把当前点加入哈希表==，这样只数 `i < j` 的点对',
                 '`cnt[x, y]` 的键是元组，括号可省略；也可压成 `2000000x + y`',
                 '同类：两数之和（哈希表）+ 异或移项'],
    ),
)
