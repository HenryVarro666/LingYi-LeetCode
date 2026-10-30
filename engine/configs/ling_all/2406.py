def _cur(S):
    if 'left' not in S or 'right' not in S:
        return None
    try:
        return S['intervals'].index([S['left'], S['right']])
    except Exception:
        return None


def _cmp(S):
    if 'left' not in S or 'right' not in S or 'h' not in S:
        return ''
    if not S['h']:
        return f"当前区间 `[{S['left']}, {S['right']}]`　堆为空：还没有任何组"
    return f"当前区间 `[{S['left']}, {S['right']}]`　`left = {S['left']}` 对比 堆顶 `h[0] = {S['h'][0]}`（最早结束的组）"


def _if(S, B, ret):
    left, h = B.left, B.h
    if not h:
        return f'堆为空，没有组可接 → 新建一个组'
    if left > h[0]:
        return f'`left = {left} > h[0] = {h[0]}`：最早结束的组已经结束，==可以接在它后面==，堆顶换成 `right = {B.right}`，组数不变'
    return f'`left = {left} ≤ h[0] = {h[0]}`：连最早结束的组都还没结束 → 所有组都与它相交，==必须新建一个组=='


CONFIG = dict(
    num=2406, title='将区间分为最少组数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 最小堆模拟',
    tags=['常用数据结构', '贪心与思维', '难度分 1713'],
    code='''
class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda p: p[0])
        h = []
        for left, right in intervals:
            if h and left > h[0]: heapreplace(h, right)
            else: heappush(h, right)
        return len(h)
''',
    call='Solution().minGroups([[5,10],[6,8],[1,5],[2,3],[1,10]])',
    expect=3,
    views=[
        dict(type='text', fn=_cmp, h=60),
        dict(type='intervals', var='intervals', pointer=_cur, label='数轴：每条是一个区间（黄 = 当前区间）', h=300),
        dict(type='heap', var='h', label='h：每个组最后一个区间的 right（最小堆）', top_color='green', h=140),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('组数 len(h)', lambda S: len(S['h']) if 'h' in S else 0, 'green')],
    captions={
        'intervals.sort': '按左端点从小到大排序：`{intervals}`',
        'h = []': '`h` 是最小堆：每个组==最后一个区间的 right==，堆顶是最早结束的组',
        'for left, right in intervals': '取出下一个区间 `[{left}, {right}]`',
        'if h and left > h[0]': _if,
        'heapreplace': '接在堆顶组后面：把堆顶换成新的 `right = {right}`，组数不变，堆 `{h}`',
        'heappush': '新建一个组，它的结尾是 `right = {right}`，组数变成 =={len(h)}==',
        'return len(h)': '堆里有几个元素就有几个组：返回 `{ret}`',
    },
    cards=dict(
        one_liner='按左端点排序，能接就接在最早结束的组后面，接不了再开新组',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把区间分成若干组，==同一组内的区间互不相交==（端点相同也算相交），求最少组数',
                 '示例：`[[5,10],[6,8],[1,5],[2,3],[1,10]]` → `3`',
                 '示例：`[[1,3],[5,6],[8,10],[11,13]]` → `1`'],
        quote='按照 left 排序后，用最小堆模拟，堆顶存储每个组最后一个区间的 right。如果当前的 left 大于堆顶，则可以接在这个组的末尾，更新堆顶为 right；否则需要创建一个新的组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['堆里每个元素对应一个组，值是这个组目前的结尾',
              '看堆顶（最早结束的组）：连它都接不上，别的组更接不上 → 开新组',
              '最后堆的大小 = 组数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '判断是 `left > h[0]`，不能写成 `>=`：`[1,5]` 和 `[5,8]` 相交',
                 '另一种思路：上下车模型，`left` 上车、`right+1` 下车，答案是同时在车上的最大人数（差分数组）',
                 '题解末尾的思考题：随机选 n 个区间，答案的期望是多少'],
    ),
)
