SC0, AG0 = [4, 5, 6, 5, 2], [512, 256, 512, 256, 768]


def _nz(S):
    a = S.get('index_array')
    if a is None:
        return {}
    return {k: v for k, v in enumerate(a) if v}


def _top(S):
    if 'score' not in S:
        return '先按分数排序，再只看年龄：找“年龄 ≤ 当前”的最大队伍分（前缀最大值）'
    return f"当前球员：分数 `{S['score']}`，年龄 `{S['age']}`；`index_array` 是年龄上的树状数组，只列出非 0 的格子"


CONFIG = dict(
    num=1626, title='无矛盾的最佳球队', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='排序 + 树状数组求前缀最大值',
    tags=['灵神题单', '动态规划', '难度分 2027'],
    code='''
class Solution(object):
    def bestTeamScore(self, scores, ages):

        infos = sorted(zip(scores, ages), key=lambda d:(d[0], d[1]))
        index_array = [0] * 1001
        res = 0
        for score, age in infos:
            now = age
            tmp = 0
            while now >= 1:
                tmp = max(tmp, index_array[now])
                now -= now & -now
            
            tmp += score
            res = max(tmp, res)
            
            now = age
            while now <= 1000:
                index_array[now] = max(index_array[now], tmp)
                now += now & -now

        return res
''',
    call=f'Solution().bestTeamScore({SC0}, {AG0})',
    expect=16,
    skip=['while now >= 1', 'while now <= 1000', 'tmp = 0', 'for score, age in'],
    max_steps=80,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='array', var=lambda S: [s for s, a in sorted(zip(S['scores'], S['ages']))] if 'scores' in S else [], label='按分数排序后的分数', h=150, cell=80, index=False),
        dict(type='map', var=_nz, label='index_array 中非 0 的格子（年龄下标 → 以该年龄段为结尾的最大队伍分）', h=330,
             fmt=lambda k, v: f'[{k}] = {v}'),
    ],
    watch=['score', 'age', 'now', 'tmp', ('res', 'res', 'green')],
    captions={
        'infos = sorted': '按（分数，年龄）排序：分数从小到大，之后只需保证年龄不下降',
        'index_array = [0] * 1001': '`index_array` 是年龄 1..1000 上的树状数组，初始全 0',
        'res = 0': '`res` 记录目前最大队伍分',
        'now = age': lambda S, B, r: (f'查询：从 `now = age = {S.now}` 开始，向下找年龄 ≤ {S.now} 的最大队伍分' if S['_line'] == 8
                                      else f'更新：再从 `now = age = {S.now}` 开始，向上写回所有覆盖它的格子'),
        'tmp = max(tmp, index_array[now])': '查询 `index_array[{B.now}] = {index_array[B.now]}`：`tmp = max({B.tmp}, {index_array[B.now]})` = =={tmp}==',
        'now -= now & -now': lambda S, B, r: f'去掉最低位的 1：`now` → {S.now}' + ('，前缀查完了' if S.now == 0 else '，继续查前一段'),
        'tmp += score': '加入当前球员：`tmp` = 前缀最大队伍分 + `{score}` = =={tmp}==',
        'res = max(tmp, res)': '`res = max({tmp}, {B.res})` = =={res}==',
        'index_array[now] = max': '更新：`index_array[{now}] = max({B.index_array[now]}, {tmp})` = =={index_array[now]}==',
        'now += now & -now': lambda S, B, r: f'加上最低位：`now` → {S.now}' + ('，越界 → 更新完毕' if S.now > 1000 else '，继续更新覆盖它的更大一段'),
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='先按分数排序，问题变成“年龄上的带权上升子序列”',
        complexity='时间 `O(n log n)`，空间 `O(U)`（U = 1000）',
        problem=['年龄小的球员分数严格大于年龄大的，就有矛盾；选出==无矛盾==的球队使总分最大',
                 '示例：`scores = [4,5,6,5]`，`ages = [2,1,2,1]` → `16`',
                 '本视频：`[4,5,6,5,2]`、年龄 `[512,256,512,256,768]` → `16`'],
        quote='首先可以将球员按分数从小到大排序。排序完成后，对于某个球员而言，其前面的球员分数都比当前球员要小，因此只需要考察年龄就好了，于是问题就转化成了经典的动态规划问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：选了第 `i` 位球员时的最大总分；转移要找年龄 ≤ 他的、`f` 最大的那位',
              '朴素做法 `O(n^2)`；这是前缀最大值问题 → 树状数组',
              '先查年龄 `1..age` 的最大分 `tmp`，加上自己的分数，再写回树状数组并更新 `res`'],
        summary=['时间 `O(n log n)`，空间 `O(U)`',
                 '易错：排序必须分数在前、年龄在后；同分按年龄升序',
                 '易错：树状数组下标从 1 开始；写回时用 `max`，不是累加',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神的树状数组按 `max(ages)` 开长度，yiduobo 固定开 1001'],
    ),
)
