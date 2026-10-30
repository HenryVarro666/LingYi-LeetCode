def _events(S):
    tp = S['time_points']
    n = len(S['persons'])
    if S.get('_line', 0) >= 18:
        tp = sorted(tp)
    return [f"{t}" + ('开' if k == -1 else '落' if k == n else f'人{k}') for t, k in tp]


CONFIG = dict(
    num=2251, title='花期内花的数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='事件排序扫描',
    tags=['灵神题单', '常用数据结构', '难度分 2022'],
    code='''
class Solution(object):
    def fullBloomFlowers(self, flowers, persons):

        m = len(flowers)
        n = len(persons)

        res = [0] * n

        time_points = []
        for start, end in flowers:
            time_points.append([start, -1])
            time_points.append([end, n])
        
        for index, person in enumerate(persons):
            time_points.append([person, index])
        
        cnt = 0
        for t, index in sorted(time_points):
            if index == -1:
                cnt += 1
            elif index == n:
                cnt -= 1
            else:
                res[index] = cnt
        
        return res
''',
    call='Solution().fullBloomFlowers([[1,4],[3,6],[7,9]], [4,3,8])',
    expect=[2, 2, 1],
    views=[
        dict(type='array', var=_events, label='时间点（数字 = 时刻）：开 = 花开，落 = 花落，人k = 第 k 个人；绿 = 正在处理', h=190, cell=96, index=False,
             color=lambda S, i, v: 'green' if 't' in S and S.get('_line', 0) >= 19 and i < len(S['time_points']) and sorted(S['time_points'])[i] == [S['t'], S['index']] else None),
        dict(type='array', var='res', label='res（每个人看到的花数）', h=170, cell=90),
        dict(type='text', fn=lambda S: (f"`cnt = {S['cnt']}`：当前正开着的花" + (f"；事件 `({S['t']}, {S['index']})`" if 't' in S and S.get('_line', 0) >= 20 else '') if 'cnt' in S else ''), h=50),
    ],
    watch=['t', 'index', ('cnt', 'cnt', 'green')],
    captions={
        'res = [0]': '`res[i]` 存第 `i` 个人看到的花数',
        'time_points = []': '时间太大，不能逐点模拟：只收集「花开、花落、人来」三类时间点',
        'append([start, -1])': '花在 `{start}` 开：记 `[{start}, -1]`，-1 排在同一时刻的最前面',
        'append([end, n])': '花在 `{end}` 落：记 `[{end}, {n}]`，`n` 最大，排在同一时刻的最后（当天还能看）',
        'append([person, index])': '第 `{index}` 个人在 `{person}` 到：记 `[{person}, {index}]`，居中',
        'cnt = 0': '`cnt` 统计当前开着多少朵花',
        'for t, index in sorted': lambda S, B, r: ('事件扫描完毕' if 'index' in B and 't' in B and B.t == S.t and B.index == S.index else f'按时间排序后处理事件 `({S.t}, {S.index})`'),
        'if index == -1': lambda S, B, r: (f'`index = -1`：花开' if S.index == -1 else f'`index = {S.index}` 不是 -1，不是花开'),
        'cnt += 1': '花开：`cnt` → `{cnt}`',
        'elif index == n': lambda S, B, r: (f'`index = {S.index} = n`：花落' if S.index == len(S.res) else f'`index = {S.index}` 不是 n，是第 `{S.index}` 个人到了'),
        'cnt -= 1': '花落：`cnt` → `{cnt}`',
        'res[index] = cnt': '人到：他看到的就是此刻的 `cnt` 为 =={cnt}== → `res[{index}]`',
        'return res': '`res = {res}`',
    },
    cards=dict(
        one_liner='把花开、花落、人来排成一条时间线，边走边数',
        complexity='时间 `O((n+m) log(n+m))`，空间 `O(n+m)`',
        problem=['每朵花有花期 `[start, end]`（含两端），每个人在某个时刻来看花',
                 '返回每个人到达时正在开的花的数量',
                 '示例：`flowers=[[1,4],[3,6],[7,9]], persons=[4,3,8]` → `[2,2,1]`'],
        quote='需要注意的是，按照题目的描述，若三种事件同时发生，那么优先级应该是花开 -> 看花人到达 -> 花落，因此在一开始排序的时候可以引入第二优先级。',
        quote_src='—— yiduobo 题解原文',
        idea=['人只关心当时开着几朵花，不关心是哪几朵',
              '用 `cnt` 计数，只在花开、花落时变化，其余时刻不用关心',
              '把三类事件抽出排序，`[时刻, 类型]` 用类型当第二关键字：-1 < 人的下标 < n'],
        summary=['时间 `O((n+m) log(n+m))`，空间 `O(n+m)`',
                 '同一时刻必须先开花、再看人、最后花落（花期含两端）',
                 '第二关键字 `-1`、`index`、`n` 的大小关系就是优先级，别写错',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
