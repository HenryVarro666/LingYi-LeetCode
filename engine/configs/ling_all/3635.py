def _phase(S):
    if S['_line'] == 9:
        return '两种顺序都算完了，取较小者'
    if 'min_finish' not in S:
        if 'land_water' in S:
            return '现在算：==先玩水上，再玩陆地==（solve 的参数已对调）'
        return '现在算：==先玩陆地，再玩水上=='
    mf = S['min_finish']
    side = '水上' if 'land_water' in S else '陆地'
    other = '陆地' if 'land_water' in S else '水上'
    return f'先玩{side}最早 ==`{mf}`== 结束 → 玩{other}时，开始时间 = `max(start, {mf})`'


CONFIG = dict(
    num=3635, title='最早完成陆地和水上游乐设施的时间 II', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='分类讨论 + 贪心',
    tags=['贪心与思维', '难度分 1870'],
    code='''
class Solution:
    def solve(self, landStartTime: List[int], landDuration: List[int], waterStartTime: List[int], waterDuration: List[int]) -> int:
        min_finish = min(start + duration for start, duration in zip(landStartTime, landDuration))
        return min(max(start, min_finish) + duration for start, duration in zip(waterStartTime, waterDuration))

    def earliestFinishTime(self, landStartTime: List[int], landDuration: List[int], waterStartTime: List[int], waterDuration: List[int]) -> int:
        land_water = self.solve(landStartTime, landDuration, waterStartTime, waterDuration)
        water_land = self.solve(waterStartTime, waterDuration, landStartTime, landDuration)
        return min(land_water, water_land)
''',
    call='Solution().earliestFinishTime([2,8,5], [4,1,3], [6,1,9], [3,2,1])',
    expect=7,
    views=[
        dict(type='array', var='landStartTime', label='先玩一类 · 开始时间', h=125, cell=70, index=False),
        dict(type='array', var='landDuration', label='先玩一类 · 时长', h=125, cell=70, index=False),
        dict(type='array', var='waterStartTime', label='后玩一类 · 开始时间', h=125, cell=70, index=False),
        dict(type='array', var='waterDuration', label='后玩一类 · 时长', h=125, cell=70, index=False),
        dict(type='text', h=90, size=28, fn=_phase),
    ],
    watch=[('min_finish', 'min_finish', 'blue'), ('land_water', 'land_water', 'green'), ('water_land', 'water_land', 'pink')],
    captions={
        'min_finish = min': '先玩的一类，==结束越早越好==：最早结束时间 `min_finish = {min_finish}`',
        'return min(max': '后玩的一类：每个设施 `max(start, {min_finish}) + duration`，取最小 = ==`{ret}`==',
        'land_water =': '先陆地后水上，最早完成时间 `land_water = {land_water}`',
        'water_land =': '先水上后陆地，最早完成时间 `water_land = {water_land}`',
        'return min(land_water': '两种顺序取较小：`min({land_water}, {water_land})` = =={ret}==',
    },
    cards=dict(
        one_liner='先玩的一类，挑结束最早的；后玩的一类，等它开放',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['陆地、水上设施各选一个，顺序不限，求最早完成两个设施的时间',
                 '设施 `i` 只能在 `startTime[i]` 及之后开始，持续 `duration[i]`',
                 '示例：陆地 `[2,8]/[4,1]`，水上 `[6]/[3]` → `9`'],
        quote='贪心地，完成陆地游乐设施的时间越早越好（这样能玩的水上设施越多，玩完的时间越早）',
        quote_src='—— 灵茶山艾府题解',
        idea=['假设先玩陆地：只看它的结束时间，取最小 `min_finish`',
              '再玩水上：每个设施开始时间 `max(start, min_finish)`，加时长取最小',
              '先玩水上同理，把参数对调再调一次 `solve`'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '易错点：先玩的一类选「结束最早」，不是「开始最早」或「时长最短」',
                 '后玩的一类要 `max(start, min_finish)`，不能忘了等待开放',
                 '两种顺序都要算，取较小值'],
    ),
)
