CONFIG = dict(
    num=1921, title='消灭怪物的最大数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='到达时间排序 · 贪心',
    code='''
class Solution(object):
    def eliminateMaximum(self, dist, speed):

        t = []
        n = len(dist)
        for index in range(n):
            t.append(dist[index] // speed[index])
            if dist[index] % speed[index] > 0:
                t[-1] += 1
        
        t.sort()
        for index in range(n):
            if t[index] <= index:
                return index
        
        return n
''',
    call='Solution().eliminateMaximum([3,5,7,4,5], [2,3,6,3,2])',
    expect=2,
    views=[
        dict(type='array', var='dist', label='dist 距离', h=210,
             color=lambda S, i, v: None),
        dict(type='array', var='speed', label='speed 速度', h=210,
             color=lambda S, i, v: None),
        dict(type='array', var='t', label='t 到达时间（向上取整）', h=240,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if 'index' in S and i < S['index'] and S['_line'] >= 10 else None)),
        dict(type='text', fn=lambda S: (f"第 `{S['index']}` 分钟开枪：怪物到达时间 `{S['t'][S['index']]}`" if 'index' in S and S.get('t') and S['index'] < len(S['t']) and S['_line'] >= 10 else ''), size=28),
    ],
    watch=['n', 'index', ('t', 't', 'cyan')],
    captions={
        't = []': '`t` 存每只怪物到达城市的时间',
        'n = len': 'n = `{n}`',
        'for index in range(n):': lambda S, B, r: ('逐个算到达时间' if S._line < 8 else f'按时间从小到大检查：`index = {S.index}` 就是第 {S.index} 分钟开枪'),
        'dist[index] // speed[index]': '怪物 `{index}`：`{dist[index]} // {speed[index]}` = `{t[-1]}` 分钟（整除部分）',
        'if dist[index] % speed[index] > 0': lambda S, B, r: f'`{S.dist[S.index]} % {S.speed[S.index]} = {S.dist[S.index] % S.speed[S.index]}`' + ('，有余数 → 还要多走一分钟才到' if S.dist[S.index] % S.speed[S.index] > 0 else '，刚好整除 → 不用补'),
        "t[-1] += 1": '向上取整：怪物 `{index}` 到达时间 = `{t[-1]}`',
        't.sort()': '先到的先杀：到达时间从小到大排序 → `{t}`',
        'if t[index] <= index': lambda S, B, r: f'`t[{S.index}] = {S.t[S.index]}` {"≤" if S.t[S.index] <= S.index else ">"} 开枪时间 `{S.index}`' + ('：怪物已到达，来不及开枪 → 游戏结束' if S.t[S.index] <= S.index else '：还没到达，来得及消灭'),
        'return index': '怪物此刻已到，前面恰好杀了 `{ret}` 只',
        'return n': '每只都来得及，全部消灭：`{ret}`',
    },
    cards=dict(
        one_liner='哪只先到先杀哪只：按到达时间排序，第 i 分钟开第 i 枪',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['怪物以恒定速度走向城市，武器每分钟能杀一只（第 0 分钟已充满）',
                 '有怪物到达（距离为 0）就输，求输之前最多杀几只',
                 '本视频：`dist=[3,5,7,4,5]`，`speed=[2,3,6,3,2]` → `2`'],
        quote='哪只怪物先到就应该先杀哪只怪物，因此可以先计算每只怪物到达的时间，然后从小到大排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['到达时间 = `dist / speed` 向上取整',
              '排序后下标恰好是开火的分钟数',
              '若 `t[index] <= index`：开火前它就到了，已杀 `index` 只'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '向上取整：整除后有余数就加一，到达时间恰好等于开火时间也算输',
                 '全部都来得及就返回 `n`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去类型说明文档字符串'],
    ),
)
