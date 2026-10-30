CONFIG = dict(
    num=447, title='回旋镖的数量', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间点 + 哈希表',
    code='''
class Solution:
    def numberOfBoomerangs(self, points: List[List[int]]) -> int:
        ans = 0
        for x1, y1 in points:
            cnt = defaultdict(int)
            for x2, y2 in points:
                d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
                ans += cnt[d2] * 2
                cnt[d2] += 1
        return ans
''',
    call='Solution().numberOfBoomerangs([[0,0],[1,0],[2,0],[1,1]])',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: f"中间点 i = `({S['x1']}, {S['y1']})`，枚举 j = `({S['x2']}, {S['y2']})`" if 'x2' in S else (f"中间点 i = `({S['x1']}, {S['y1']})`" if 'x1' in S else ''), h=60),
        dict(type='text', fn=lambda S: f"d2 = `({S['x1']}−{S['x2']})^2 + ({S['y1']}−{S['y2']})^2` = =={S['d2']}==" if 'd2' in S and 'x2' in S else '', h=60),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k}: {v}', h=300, label='cnt：距离平方 → 出现次数'),
    ],
    watch=[('x1', 'x1', 'blue'), ('y1', 'y1', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '换一个中间点 i，哈希表 `cnt` 清空，重新统计',
        'd2 = ': '`i` 到 `j` 的距离平方 = =={d2}==（不开方，避免精度问题）',
        'ans += cnt[d2] * 2': '前面已有 `{cnt[d2]}` 个点距离也是 `{d2}`，都能和当前 j 配对；(j,k) 与 (k,j) 算两个 → `ans` += `2 × {cnt[d2]}` → =={ans}==',
        'cnt[d2] += 1': '把当前 j 记入：距离 `{d2}` 的点现在有 `{cnt[d2]}` 个',
        'return ans': '所有中间点都枚举完，共 `{ans}` 个回旋镖',
    },
    cards=dict(
        one_liner='枚举中间点 i，同距离的点两两配对，顺序不同算两个',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['平面上互不相同的点，找三元组 `(i, j, k)`，使 i 到 j 与 i 到 k 距离相等',
                 '==要考虑顺序==：(i,j,k) 与 (i,k,j) 是两个',
                 '示例：`[[0,0],[1,0],[2,0]]` → `2`；本视频多加一个点 `(1,1)` → `8`'],
        quote='枚举「中间」的点 i，然后统计有多少对 j 和 k，满足点 i 到点 j 的欧式距离等于点 i 到点 k 的欧式距离。',
        quote_src='—— 灵茶山艾府题解',
        idea=['外层枚举 i，内层枚举 j，哈希表 `cnt` 记录距离平方的出现次数',
              '枚举到 j 时，前面每个同距离的点都能当 k：先 `ans += 2·cnt[d2]`，再 `cnt[d2] += 1`',
              'j = i 时距离为 0 且只出现一次，贡献为 0，不用特判'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '距离用平方，全是整数，不要开方',
                 '先加答案再加计数：这样每个 j 只和它之前的点配对，乘 2 补上顺序',
                 '同类思路：枚举「中间」的题，如 2909、2874'],
    ),
)
