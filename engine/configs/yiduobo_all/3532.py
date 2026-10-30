PAL = ['cyan', 'pink', 'green', 'purple', 'orange', 'yellow']


def _col(S, i, v):
    b = S.get('belong')
    if b is None or b[i] is None:
        return None
    return PAL[b[i] % len(PAL)]


def _txt(S):
    if 'q' not in S or S.get('p') is None or S['p'] >= len(S['nums']):
        return '`belong[i]` = 第 i 个节点所在的段；相邻差 <= maxDiff 的连续节点划为一段'
    p, q, nums = S['p'], S['q'], S['nums']
    if q < len(nums):
        d = nums[q] - nums[q - 1]
        return f'`nums[{q}] − nums[{q-1}] = {d}`，{"<=" if d <= S["maxDiff"] else "大于"} `maxDiff = {S["maxDiff"]}`'
    return f'`q = {q}` 到头了，这一段 `[{p}, {q-1}]` 结束'


CONFIG = dict(
    num=3532, title='针对图的路径存在性查询 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按相邻差分段 · belong 数组',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def pathExistenceQueries(self, n, nums, maxDiff, queries):
        
        tot = 0
        belong = [None] * n
        p = 0
        while p < len(nums):
            q = p + 1
            belong[p] = tot
            while q < len(nums) and nums[q] - nums[q - 1] <= maxDiff:
                belong[q] = tot
                q += 1
            
            p = q
            tot += 1
        
        res = []
        for x, y in queries:
            res.append(belong[x] == belong[y])
        return res
''',
    call='Solution().pathExistenceQueries(6, [2,5,6,8,9,15], 2, [[0,1],[1,3],[3,5],[2,4]])',
    expect=[False, True, False, True],
    views=[
        dict(type='array', var='nums', label='nums（非递减）', pointers={'p': 'blue', 'q': 'pink'}, cell=100, h=190,
             color=_col),
        dict(type='array', var='belong', label='belong（所在段的编号，· = 还没分）', cell=100, h=190,
             pointers={'p': 'blue', 'q': 'pink'}, color=_col,
             fmt=lambda v: '–' if v is None else str(v)),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=['tot', 'p', 'q', ('maxDiff', 'maxDiff', 'yellow')],
    captions={
        'tot = 0': '`tot` 是当前段的编号，从 0 开始',
        'belong = [None]': '`belong` 先全是 None：还没人分段',
        'p = 0': '`p` 指向当前这一段的起点',
        'q = p + 1': '`p = {p}` 自己先成一段的开头，`q = {q}` 去试探后面的点',
        'belong[p] = tot': '起点 `{p}` 归入第 `{tot}` 段：`belong[{p}] = {tot}`',
        'while q < len(nums)': lambda S, B, r: (
            f'`q = {S.q}` 越界，这一段结束' if S.q >= len(S.nums) else
            f'`nums[{S.q}] − nums[{S.q-1}] = {S.nums[S.q]-S.nums[S.q-1]}` '
            + ('<=' if S.nums[S.q]-S.nums[S.q-1] <= S.maxDiff else '==大于==') + f' `maxDiff = {S.maxDiff}`：'
            + ('有序数组里相邻都连着，就归同一段' if S.nums[S.q]-S.nums[S.q-1] <= S.maxDiff else '相邻已经断开，后面的点都过不来 → 这段结束')),
        'belong[q] = tot': '`q = {q}` 并入当前段：`belong[{q}] = {tot}`',
        'q += 1': '继续看下一个：`q` → {q}',
        'p = q': '下一段从 `q = {q}` 开始：`p` → {p}',
        'tot += 1': '段编号加一：`tot` → {tot}',
        'res = []': '分段完成：`belong = {belong}`，接着回答查询',
        'for x, y in queries': lambda S, B, r: (f'取查询 `[{S.x}, {S.y}]`' if 'x' in S else '查询处理完了'),
        'res.append': '`belong[{x}] = {belong[x]}`，`belong[{y}] = {belong[y]}` → {belong[x] == belong[y]}：同段才有路径',
        'return res': '全部查询答案：`{res}`',
    },
    cards=dict(
        one_liner='nums 有序，所以连通块一定是一段连续区间',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`nums` 非递减，`|nums[i]-nums[j]| <= maxDiff` 时两点连边',
                 '每个查询 `[u,v]`：问两点之间是否存在路径',
                 '本视频：`nums=[2,5,6,8,9,15]`，`maxDiff=2`'],
        quote='若 nums[j] - nums[i] > maxDiff，说明 i 和 j 之间不存在边，同时 i 与所有大于 j 的节点之间……也不可能存在边，因为 nums 是单调的。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文推理：有序，一旦相邻差超标，左右就彻底分开',
              '所以一趟遍历，按相邻差把 `nums` 切成若干段，段内互通、段间不通',
              '用 `belong` 记下每个节点的段号，查询只比 `belong[x] == belong[y]`'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '外层 `p` 找段起点，内层 `q` 往右扩，扩完 `p = q`，不会重复扫描',
                 '原文 `belong` 称为「哈希表」，实际用数组即可',
                 '易错：只看相邻差，不要比较段首与当前点'],
    ),
)
