CONFIG = dict(
    num=1921, title='消灭怪物的最大数量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='按到达时间排序 · 第 t 分钟打第 t 个（Go 原文转写）',
    tags=[],
    setup='from functools import cmp_to_key',
    code='''
class Solution:
    def eliminateMaximum(self, dis: List[int], speed: List[int]) -> int:
        n = len(dis)
        a = [None] * n
        for i, d in enumerate(dis):
            a[i] = (d, speed[i])
        # 按照怪物到达城市的时间从小到大排序
        a.sort(key=cmp_to_key(lambda a, b: a[0] * b[1] - b[0] * a[1]))
        for t, p in enumerate(a):
            if t * p[1] >= p[0]:
                return t
        return n
''',
    call='Solution().eliminateMaximum([4,2,6,3], [2,1,3,1])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: ('每只怪物 `(距离, 速度)`，到达时间 = 距离 ÷ 速度' if 'a' not in S else '怪物按到达时间从早到晚排队，第 `t` 分钟打第 `t` 只'), size=28),
        dict(type='array', var='dis', label='dis 距离', cell=100, h=150),
        dict(type='array', var='speed', label='speed 速度', cell=100, h=150),
        dict(type='array', var='a', label='a：(距离, 速度)，蓝框 = 当前第 t 只', cell=130, h=250, pointers={'t': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('t') else None) if v is not None else None),
        dict(type='text', fn=lambda S: (f"第 `{S['t']}` 分钟：怪物 `{S['p']}` 已走 `{S['t']}×{S['p'][1]} = {S['t']*S['p'][1]}`，离城市 `{S['p'][0]}`" if 't' in S and 'p' in S else ''), size=26),
    ],
    watch=[('t', 't', 'blue'), 'p', ('n', 'n')],
    captions={
        'n = len(dis)': '一共 `{n}` 只怪物',
        'a[i] = (d, speed[i])': '把距离和速度打包成一对 `{a[i]}`',
        'a.sort(': '到达时间 `d/spd` 小的先到 → 先打。排序后 `{a}`（比较时用交叉相乘 `d1*spd2` 与 `d2*spd1`，避免小数）',
        'for t, p in enumerate(a)': '第 `{t}` 分钟，武器充好电，轮到打 `{p}`',
        'if t * p[1] >= p[0]': lambda S, B, ret: (f"怪物已走 `{S.t}×{S.p[1]} = {S.t*S.p[1]}` >= 距离 `{S.p[0]}` → ==已经到城市了==，来不及开枪" if S.t * S.p[1] >= S.p[0] else f"怪物才走 `{S.t*S.p[1]}` < 距离 `{S.p[0]}` → 还没到，这一枪打得上"),
        'return t': '前 `{t}` 只都打掉了，第 `{t}` 只已到达 → 最多消灭 `{t}` 只',
        'return n': '所有怪物都在到达前被打掉 → 返回 `n = {n}`',
    },
    cards=dict(
        one_liner='先到的先打：按到达时间排序，第 t 分钟打第 t 只',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['怪物以固定速度走向城市，武器每分钟能打一只，开局已充满',
                 '有怪物到达城市（距离 0）就输，求输之前最多打几只',
                 '示例：`dist=[1,1,2,3]`，`speed=[1,1,1,1]` → `1`'],
        quote='按照怪物到达城市的时间从小到大排序',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['到得早的怪物更危险，所以按到达时间从小到大排队来打',
              '第 `t` 分钟开枪时，第 `t` 只怪物若已走完距离（`t*spd >= d`），就输了',
              '排序比较用交叉相乘 `d1*spd2 < d2*spd1`，不用除法，避免浮点误差'],
        result='排序后 `(4,2) (2,1) (6,3)` 都在第 2 分钟到，第 `t=2` 只已到达 → 返回 2',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Slice` 的比较函数用 `cmp_to_key` 实现）；`cmp_to_key` 的 import 放在 setup 里',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错：恰好在某分钟开始时到达（`t*spd == d`）也算输，所以用 `>=`',
                 '到达时间也可以用 `ceil(d/spd)` 排序后与下标比较'],
    ),
)
