PAL = ['cyan', 'pink', 'green', 'purple', 'orange', 'yellow']


def _qtxt(S):
    ids = S.get('id')
    if ids is None:
        return ''
    if S['_line'] != 9:
        return '相邻差 > maxDiff 的位置 ==编号 +1==，其余沿用左边的编号'
    return '　'.join(f'`[{u},{v}]` {ids[u]}{"=" if ids[u] == ids[v] else "≠"}{ids[v]} ==' + ('通' if ids[u] == ids[v] else '断') + '==' for u, v in S['queries'])


def _col(S, i, v):
    ids = S.get('id')
    c = S.get('i')
    if ids is None or c is None:
        return None
    if i <= c:
        return PAL[ids[i] % len(PAL)]
    return None


CONFIG = dict(
    num=3532, title='针对图的路径存在性查询 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='记录连通块编号',
    tags=['灵神题单'],
    code='''
class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[bool]:
        id = [0] * n  # 每个节点所在连通块的编号
        for i in range(1, n):
            id[i] = id[i - 1]
            if nums[i] - nums[i - 1] > maxDiff:
                id[i] += 1  # 找到了一个新的连通块

        return [id[u] == id[v] for u, v in queries]
''',
    call='Solution().pathExistenceQueries(6, [2,5,6,8,9,15], 2, [[0,1],[1,3],[3,5],[2,4]])',
    expect=[False, True, False, True],
    views=[
        dict(type='array', var='nums', label='nums（有序，颜色 = 连通块编号）', pointers={'i': 'blue'}, cell=100, h=190,
             color=_col),
        dict(type='array', var='id', label='id（每个节点所在连通块的编号）', pointers={'i': 'blue'}, cell=100, h=190,
             color=_col),
        dict(type='text', h=110, size=28, fn=_qtxt),
    ],
    watch=['i', ('maxDiff', 'maxDiff', 'yellow')],
    captions={
        'id = [0] * n': '先假设所有节点编号都是 0：`id = {id}`，第 0 个节点属于第 0 块',
        'id[i] = id[i - 1]': '先和左边邻居同块：`id[{i}] = id[{i-1}] = {id[i]}`',
        'if nums[i] - nums[i - 1] > maxDiff': lambda S, B, r: (
            f'`{S.nums[S.i]} - {S.nums[S.i-1]} = {S.nums[S.i]-S.nums[S.i-1]}` '
            + ('==大于==' if S.nums[S.i]-S.nums[S.i-1] > S.maxDiff else '不大于')
            + f' `maxDiff = {S.maxDiff}`：'
            + ('有序数组里这个缺口跨不过去 → 左右两边断开' if S.nums[S.i]-S.nums[S.i-1] > S.maxDiff else '相邻点有边，同一连通块')),
        'id[i] += 1': '断点：从 `{i}` 起是新连通块，编号加一 → `id[{i}] = {id[i]}`',
        'return [': lambda S, B, r: f'每个询问只比较两端的编号：相同才连通 → `{r}`',
    },
    cards=dict(
        one_liner='有序数组里，相邻差超过 maxDiff 就断开，其余全连通',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`n` 个点，`nums` 非递减；`|nums[i]-nums[j]| <= maxDiff` 则连边',
                 '每个询问 `[u,v]` 问两点之间是否有路径',
                 '本视频：`nums=[2,5,6,8,9,15]`，`maxDiff=2`'],
        quote='如果 nums[i]-nums[i-1] > maxDiff，那么 i 在一个新的连通块中，编号加一。否则编号不变。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums` 有序：只要相邻两点差 <= maxDiff 就连着，一段一段地连通',
              '差超过 maxDiff 的相邻位置是「间断点」，左边的点永远跳不到右边',
              '给每段编号，询问时比较 `id[u] == id[v]` 即可'],
        summary=['时间 `O(n+q)`，空间 `O(n)`，不需要并查集',
                 '方法一：记录间断点 + 二分 `bisect_left`，查询 `O(log n)`',
                 '写法二：`accumulate(..., initial=0)` 一行算出 id',
                 '易错：`id[0] = 0`，循环从 `i = 1` 开始；`u == v` 时显然为 True'],
    ),
)
