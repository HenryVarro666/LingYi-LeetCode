def _ids(S):
    return [a[0] for a in S['restrictions']] if 'm' in S else []


def _lim(S):
    return ['∞' if a[1] == float('inf') else a[1] for a in S['restrictions']] if 'm' in S else []


def _txt(S):
    if 'h' not in S:
        return '先加两个哨兵约束 `[1,0]`、`[n,inf]`，再按编号排序'
    r, ln = S['restrictions'], S.get('_line', 0)
    if ln >= 13:
        k = max(range(len(r) - 1), key=lambda i: r[i + 1][0] - r[i][0] + S['h'][i] + S['h'][i + 1])
        return f"区间 `[{r[k][0]}, {r[k+1][0]}]` 峰顶最高：`({r[k+1][0]}-{r[k][0]}+{S['h'][k]}+{S['h'][k+1]})//2 = {(r[k+1][0]-r[k][0]+S['h'][k]+S['h'][k+1])//2}`"
    return '`h[i]`：编号 `id[i]` 的建筑实际最高能到多高'


CONFIG = dict(
    num=1840, title='最高建筑高度', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='两次扫描 + 相邻限制点之间的峰顶公式',
    tags=['灵神题单', '难度分 2374'],
    code='''
class Solution:
    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        restrictions += [[1, 0], [n, inf]]
        restrictions.sort(key=lambda a: a[0])  # 按照 id 从小大到大排序

        m = len(restrictions)
        h = [0] * m  # h[i] 表示编号为 id[i] 的建筑的最大高度
        for i in range(1, m):
            h[i] = min(h[i - 1] + restrictions[i][0] - restrictions[i - 1][0], restrictions[i][1])
        for i in range(m - 2, -1, -1):
            h[i] = min(h[i], h[i + 1] + restrictions[i + 1][0] - restrictions[i][0])

        return max(restrictions[i + 1][0] - restrictions[i][0] + h[i] + h[i + 1] for i in range(m - 1)) // 2
''',
    call='Solution().maxBuilding(10, [[5,3],[2,5],[7,4],[9,1]])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=26, h=110),
        dict(type='array', var=_ids, label='编号 id（排序后）', pointers={'i': 'yellow'}, h=200),
        dict(type='array', var=_lim, label='限高 maxHeight（∞ = 无限制）', h=200),
        dict(type='array', var=lambda S: S['h'] if 'h' in S else [], label='h：实际最大高度', pointers={'i': 'yellow'}, h=240,
             color=lambda S, i, v: 'green' if S.get('_line', 0) >= 13 else None),
    ],
    watch=['n', 'm', 'i'],
    captions={
        'restrictions += ': '加两个哨兵：`[1, 0]` 建筑 1 高度必须是 0，`[{n}, inf]` 让最右端不用单独讨论',
        'restrictions.sort': '输入的 id 无序，==按 id 排序==：`{[a[0] for a in restrictions]}`',
        'm = len': '现在一共 `m = {m}` 个限制点',
        'h = [0] * m': '`h[i]` 表示编号 `id[i]` 的建筑最高能到多少，先全部填 0',
        'for i in range(1, m)': '第一次扫描（从左到右）：看第 `{i}` 个限制点',
        'for i in range(m - 2': '第二次扫描（从右到左）：看第 `{i}` 个限制点',
        'h[i] = min(h[i - 1]': '从左边爬上来最多 `{h[i-1]} + {restrictions[i][0]-restrictions[i-1][0]}`，自己限高 `{restrictions[i][1]}` → `h[{i}] = {h[i]}`',
        'h[i] = min(h[i], h[i + 1]': '从右边爬上来最多 `{h[i+1]} + {restrictions[i+1][0]-restrictions[i][0]}`，与已有的取小 → `h[{i}] = {h[i]}`',
        'return max': '每对相邻限制点：峰顶 `(id差 + h[i] + h[i+1]) // 2`，取最大 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='先两次扫描算出每个限制点的真实上限，再用公式算相邻点之间的峰顶',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['`n` 栋建筑排成一列，1 号高度必须是 0，相邻高度差不超过 1',
                 '`restrictions[i] = [id, maxHeight]` 给部分建筑限高，求最高建筑的最大高度',
                 '示例：`n=10, [[5,3],[2,5],[7,4],[10,3]]` → `5`', '本视频：`n=10, [[5,3],[2,5],[7,4],[9,1]]` → `4`'],
        quote='编号在 id_i 和 id_{i+1} 之间的建筑，最大高度先递增再递减，用数学方法可以 O(1) 算出峰顶的最大高度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n` 高达 `10^9`，不能建数组，只处理有限制的建筑',
              '两次扫描：限制会通过「高度差 ≤ 1」传到远处，左右各扫一遍收紧',
              '两个限制点之间，高度先升后降，两条斜率 ±1 的直线交点就是峰顶',
              '峰顶高度 `(id[i+1] - id[i] + h[i] + h[i+1]) // 2`'],
        summary=['时间 `O(m log m)`，瓶颈在排序；空间 `O(m)`',
                 '易错点：`restrictions` 的 id 不一定有序，要先排序',
                 '加哨兵 `[1,0]` 和 `[n,inf]`，就不用单独处理两端',
                 '是 3796 题 `diff[i] = 1` 的特例，那题 n 小可直接建数组',
                 '最右端哨兵是 `inf`，所以最后一段公式等价于一路上升到 `n`'],
    ),
)
