CONFIG = dict(
    num=3447, title='将元素分配给有约束条件的组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛法 · f[v] 记下标',
    tags=['灵神题单', '数论', '难度分 1731'],
    code='''
class Solution(object):
    def assignElements(self, groups, elements):
        
        ma = max(groups)
        f = [-1] * (ma + 1)
        for index, v in enumerate(elements):
            if v <= ma and f[v] == -1:
                for x in range(v, ma + 1, v):
                    if f[x] == -1:
                        f[x] = index
        
        return [f[v] for v in groups]
''',
    call='Solution().assignElements([12,6,5,9,4], [3,6,2,4])',
    expect=[0, 0, -1, 0, 2],
    views=[
        dict(type='array', var='groups', label='groups', h=120, cell=70),
        dict(type='array', var='elements', label='elements', pointers={'index': 'blue'}, h=200, cell=70),
        dict(type='array', var='f', label='f[x]：x 分给哪个下标', pointers={'x': 'pink'}, h=210, cell=56,
             color=lambda S, i, v: 'green' if v >= 0 else None),
    ],
    watch=['ma', 'index', 'v', 'x'],
    captions={
        'ma = max': '值域到 `ma = {ma}` 就够了',
        'f = [-1]': '`f[x]` 表示 x 分配到哪个下标，初始 `-1` = 还没分配',
        'for index, v': '当前 `elements[{index}] = {v}`',
        'if v <= ma': lambda S, B, r: (f'`{S.v}` 比所有组都大，没用' if S.v > S.ma else (f'`f[{S.v}] = -1`：此前没有它的约数出现过 → ==它有用==，从 {S.v} 开始以 {S.v} 为步长筛' if S.f[S.v] == -1 else f'`f[{S.v}] = {S.f[S.v]}`：之前已有 {S.v} 的约数，{S.v} 的倍数全被抢先分配 → ==派不上用场==')),
        'for x in range': '`x = {x}` 是 {v} 的倍数',
        'if f[x] == -1': lambda S, B, r: (f'`f[{S.x}] = -1`：还没人要' if S.f[S.x] == -1 else f'`f[{S.x}] = {S.f[S.x]}`：下标更小的已占位，保持不动'),
        'f[x] = index': '`f[{x}] = {index}`：{x} 分给下标 {index} 的元素 {v}',
        'return [': '遍历 `groups`，对每个值直接读 `f` → =={ret}==',
    },
    cards=dict(
        one_liner='和筛法一样：谁的约数先出现，谁先占住倍数',
        complexity='时间 `O(n + M log M)`，空间 `O(M)`',
        problem=['`groups[i]` 能被 `elements[j]` 整除就可分配 j，取最小下标',
                 '没有符合的则为 `-1`，一个元素可分给多个组',
                 '示例：`groups=[8,4,3,2,4]`，`elements=[4,2]` → `[0,0,-1,1,0]`'],
        quote='若f[v]不为-1，说明在此之前已经出现过v的约数，v已经派不上用场了。',
        quote_src='—— yiduobo 题解原文',
        idea=['对 `v = elements[j]`，所有 `v、2v、3v…` 的组都可以分给 j',
              '数组遍历顺序就是下标顺序，所以先到先得，不用再比较大小',
              '照搬筛法：`f[x] == -1` 时才写，保证最小下标'],
        summary=['`v <= ma` 防止越界，`f[v] == -1` 过滤无用元素',
                 '`f` 初值 `-1` 同时承担"没有合适元素"的答案',
                 '对比灵神：思路一致，灵神把"已标记就整轮跳过"的原因写成了注意点',
                 '本视频示例：`elements=[3,6,2,4]`，6 和 4 被前面的 3、2 抢占而无用'],
    ),
)
