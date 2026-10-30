SRC = [[1, 3], [5, 4]]
TGT = [[3, 1], [6, 5]]

CONFIG = dict(
    num='LCP 39', title='无人机方阵', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · 多重集差',
    tags=[],
    code='''
class Solution(object):
    def minimumSwitchingTimes(self, source, target):

        cnt = {}
        n = len(source)
        m = len(source[0])
        for i in range(n):
            for j in range(m):
                cnt[source[i][j]] = cnt.get(source[i][j], 0) + 1
        
        res = 0
        for i in range(n):
            for j in range(m):
                if cnt.get(target[i][j], 0) > 0:
                    cnt[target[i][j]] -= 1
                else:
                    res += 1
        
        return res
''',
    call=f'Solution().minimumSwitchingTimes({SRC}, {TGT})',
    expect=1,
    skip=['cnt = {}', 'n = len(source)', 'm = len(source[0])', 'for i in range', 'for j in range'],
    views=[
        dict(type='grid', var='source', label='source（蓝框 = 正在统计的无人机）', cell=90, h=210,
             cursors=[(lambda S: S.get('i') if 'res' not in S else None, 'j', 'blue')]),
        dict(type='grid', var='target', label='target（粉框 = 正在配对的目标颜色）', cell=90, h=210,
             cursors=[(lambda S: S.get('i') if 'res' in S else None, 'j', 'pink')],
             ),
        dict(type='map', var='cnt', label='cnt：source 中还没被用掉的各颜色数量', h=200,
             fmt=lambda k, v: f'颜色 {k} × {v}'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '准备哈希表 `cnt`，统计 source 里每种颜色有几架无人机',
        'cnt[source[i][j]] = ': '`source[{i}][{j}] = {source[i][j]}` → 颜色 {source[i][j]} 的数量变成 `{cnt[source[i][j]]}`',
        'res = 0': '统计完了：位置可以随便换，所以==只看颜色的个数==。`res` 记录要换色的无人机数',
        'if cnt.get(target[i][j], 0) > 0': lambda S, B, r: (
            f'target 需要颜色 `{S.target[S.i][S.j]}`，source 里还剩 `{B.cnt.get(S.target[S.i][S.j], 0)}` 架 → ==有现成的，不用换色=='
            if B.cnt.get(S.target[S.i][S.j], 0) > 0 else
            f'target 需要颜色 `{S.target[S.i][S.j]}`，source 里已经没有（剩 0 架）→ ==必须换色=='),
        'cnt[target[i][j]] -= 1': '用掉一架颜色 `{target[i][j]}` 的无人机：`cnt` 剩 `{cnt[target[i][j]]}`',
        'res += 1': '这架无人机要换色：`res` → =={res}==',
        'return res': '换色次数 `res = {res}`',
    },
    cards=dict(
        one_liner='位置随便换，只要数一数两个矩阵里颜色差了几个',
        complexity='时间 `O(nm)`，空间 `O(k)`（k 为颜色数）',
        problem=['`source`、`target` 是 `N×M` 的颜色矩阵，无人机的位置可以任意调换',
                 '换位置不耗能，==切换灯光颜色==才耗能，求最少换色次数',
                 '示例：`source=[[1,3],[5,4]]`，`target=[[3,1],[6,5]]` → `1`'],
        quote='由于题目中的无人机可以任意调整位置，那么实际上问的就是两个矩阵中有多少个不一样的数字。',
        quote_src='—— yiduobo 题解原文',
        idea=['位置能随意调 → 只和==每种颜色的个数==有关',
              '先遍历 source，哈希表统计每种颜色的数量',
              '再遍历 target：有现成的就扣 1，没有就得换色，答案加 1'],
        summary=['时间 `O(nm)`，空间 `O(k)`',
                 '易错：不是逐格比较，因为位置可以换；用 `cnt.get(x, 0)` 防止颜色不存在时报错',
                 '换色次数也等于 target 中无法在 source 里配对的数量',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
