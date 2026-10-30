def _txt(S):
    if 'now' not in S:
        return '先走到走不动，再回头选「已经路过且油最多」的站加油'
    sp, n = S['station_pos'], S['n']
    seen = sp
    return f'`now = {S["now"]}`，目标 `{S["target"]}`；已路过前 `{seen}` 个站，其中没用的油在堆里'


CONFIG = dict(
    num=871, title='最低加油次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='最大堆：走不动了再选最多的站',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2074'],
    code='''
class Solution(object):
    def minRefuelStops(self, target, startFuel, stations):

        now = startFuel
        station_pos = 0
        heap = []
        n = len(stations)
        res = 0
        while now < target:
            while station_pos < n and now >= stations[station_pos][0]:
                heapq.heappush(heap, -stations[station_pos][1])
                station_pos += 1
            res += 1
            if heap:
                now += -heapq.heappop(heap)
            else:
                return -1
        
        return res
''',
    call='Solution().minRefuelStops(100, 10, [[10,60],[20,30],[30,30],[60,40]])',
    expect=2,
    views=[
        dict(type='table', var='stations', label='stations（位置, 油量；蓝 = 已路过并入堆）', h=300, cell=64,
             rows=lambda S: [f'站{k}' for k in range(len(S['stations']))], cols=['位置', '油量'],
             color=lambda S, r, c, v: 'blue' if 'station_pos' in S and r < S['station_pos'] else None),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='heap', var='heap', label='heap（显示成正的油量）', h=240, fmt=lambda x: str(-x)),
    ],
    watch=[('now', 'now', 'yellow'), ('target', 'target', 'blue'), ('station_pos', 'station_pos', 'pink'), ('res', 'res', 'green')],
    captions={
        'now = startFuel': '`now = {now}`：当前最远能开到第 `{now}` 英里（含已加的油）',
        'station_pos = 0': '`station_pos`：下一个还没考虑的加油站下标',
        'heap = []': '堆存==已经路过==、还没用的加油站油量（取负数当最大堆）',
        'while now < target': lambda S, B, r: (f'`now = {S.now}` < `{S.target}`：还到不了终点，需要加油' if S.now < S.target else f'`now = {S.now}` ≥ `{S.target}`：到终点了，结束'),
        'while station_pos < n': lambda S, B, r: (f'下一站在 `{S.stations[S.station_pos][0]}`，`now = {S.now}` ≥ 它 → ==路过得了，可以入堆==' if S.station_pos < S.n and S.now >= S.stations[S.station_pos][0] else '剩下的站都够不着了，停止入堆'),
        'heapq.heappush': '第 `{station_pos}` 站的油 `{stations[station_pos][1]}` 升入堆：留着以后需要时再用',
        'station_pos += 1': '`station_pos` → {station_pos}，看下一站',
        'res += 1': '走不动了，必须加一次油：`res` = =={res}==',
        'if heap': lambda S, B, r: ('堆里有油 → 选最多的那一站加油' if S.heap else '堆是空的，没有站可以加'),
        'now += -heapq.heappop(heap)': '弹出油量最多的站：`now` {B.now} → =={now}==',
        'return -1': '堆空仍到不了终点 → ==返回 -1==',
        'return res': '到达终点，最少加油次数 `res` = =={ret}==',
    },
    cards=dict(
        one_liner='先不急着加油，走不动了再回头选油最多的站',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['汽车从起点开往 `target` 英里外，初始油量 `startFuel`，每英里耗 1 升',
                 '沿途加油站 `[位置, 油量]`，油箱无限大，到站可以把油全加进去',
                 '求到终点的==最少加油次数==，到不了返回 `-1`。示例：`target=100, startFuel=10` → `2`'],
        quote='加油除了需要达到对应的加油站之外并没有任何额外的前置条件，因此并不需要在到达一个加油站时就急着判断是否需要加油，而是可以在无法继续前进时选择当前已经到达，且油最多的加油站进行加油。',
        quote_src='—— yiduobo 题解',
        idea=['`now` = 当前能开到的最远位置；`now < target` 就还得加油',
              '把 `now` 能到达的站全部入堆（负数当最大堆）',
              '堆空 → 无解；否则弹出油最多的站加油，`res + 1`，重复直到 `now ≥ target`'],
        summary=['时间 `O(n log n)`：每个站入堆一次、出堆至多一次',
                 '易错：入堆条件是 `now >= 站的位置`（油量恰好够到也可加油）',
                 '原文是 Python 2 写法，本题代码无需改动即可在 Python 3 运行',
                 '与灵神的区别：这里以「是否到达 target」为外层循环，不额外加虚拟终点站'],
    ),
)
