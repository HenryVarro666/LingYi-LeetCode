def _txt(S):
    if 'miles' not in S or 'position' not in S:
        return '汽车最多能开到的位置 `miles`；每个加油站是一个==待用的油桶=='
    pos, miles = S['position'], S['miles']
    if miles >= pos:
        return f'`miles = {miles}` ≥ 下一站 `{pos}`：能开到，不用加油'
    return f'`miles = {miles}` < 下一站 `{pos}`：==开不到==，要从油桶里选最大的加油'


CONFIG = dict(
    num=871, title='最低加油次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='反悔贪心 + 最大堆（油桶）',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2074'],
    code='''
class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:
        stations.append((target, 0))
        ans, miles = 0, startFuel
        fuel_heap = []  # 下面把堆中元素取反，当作最大堆用
        for position, fuel in stations:
            while fuel_heap and miles < position:  # 没有足够的油到达 position
                miles -= heappop(fuel_heap)  # 选油量最多的油桶
                ans += 1
            if miles < position:  # 无法到达
                return -1
            heappush(fuel_heap, -fuel)  # 留着后面加油
        return ans
''',
    call='Solution().minRefuelStops(100, 10, [[10,60],[20,30],[30,30],[60,40]])',
    expect=2,
    views=[
        dict(type='table', var='stations', label='stations（位置, 油量；末尾追加了终点）', h=300, cell=64,
             rows=lambda S: [f'站{k}' for k in range(len(S['stations']))], cols=['位置', '油量'],
             color=lambda S, r, c, v: 'blue' if 'position' in S and S['stations'][r][0] == S['position'] else None),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='heap', var='fuel_heap', label='fuel_heap（显示成正的油量）', h=240,
             fmt=lambda x: str(-x)),
    ],
    watch=[('position', 'position', 'blue'), ('miles', 'miles', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'stations.append': '把终点当成一个油量为 0 的虚拟加油站 `({target}, 0)`，最后一段路也能用同样的代码处理',
        'ans, miles = 0, startFuel': '`ans = 0` 次加油；`miles = {miles}`：现在最远能开到第 `{miles}` 英里',
        'fuel_heap = []': '油桶堆：经过的加油站不急着加，把油==先收进堆里==，没油时再选最大的',
        'for position, fuel in stations': lambda S, B, r: (f'下一站在 `{S.position}` 英里，有 `{S.fuel}` 升油' if S.get('position') != B.get('position') else '所有站（含终点）处理完'),
        'while fuel_heap and miles <': lambda S, B, r: (f'`miles = {S.miles}` < `position = {S.position}`，堆里有油桶 → ==必须加油== ' if S.miles < S.position and S.fuel_heap else f'要么够开（`{S.miles} ≥ {S.position}`），要么堆空，不再加油'),
        'miles -= heappop': '从油桶里选==油量最多==的一桶倒进车里（堆里是负数，减负数 = 加）：`miles` {B.miles} → =={miles}==',
        'ans += 1': '用了一个油桶 = 加了一次油：`ans` = =={ans}==',
        'if miles < position': lambda S, B, r: (f'堆已空，`miles = {S.miles}` 仍 < `{S.position}` → 到不了' if S.miles < S.position else f'`miles = {S.miles}` ≥ `{S.position}`，能到达'),
        'return -1': '油桶全用完还开不到下一站 → ==返回 -1==',
        'heappush(fuel_heap, -fuel)': '到了这一站，把它的 `{fuel}` 升油==当作油桶留着==：以后没油了可以反悔，回头在这站加油',
        'return ans': '到达终点，最少加油次数 `ans` = =={ret}==',
    },
    cards=dict(
        one_liner='经过的加油站当成油桶，没油时再反悔选最大的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['汽车从起点开往 `target` 英里外，初始油量 `startFuel`，每英里耗 1 升',
                 '沿途加油站 `[位置, 油量]`，到站可以把站里的油全部加入车中',
                 '求到终点的==最少加油次数==，到不了返回 `-1`。示例：`target=100, startFuel=10` → `2`'],
        quote='当汽车行驶到第 i 个加油站时，视作获取了一个装有 fuel_i 升汽油的油桶。在后续的行驶过程中，可以在没油时，把油桶中的油加到汽车中。为了让加油次数尽量少，贪心地选油量多的油桶。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每经过一站就收一个油桶入堆，先不加',
              '要到下一站却 `miles < position`：从堆里取==最大==的油桶加',
              '终点当作虚拟站 `(target, 0)`，最后一段也走同样流程'],
        summary=['时间 `O(n log n)`：每个油桶最多入堆、出堆各一次，双重循环总共 `O(n)` 次',
                 '易错：Python 只有最小堆，入堆存 `-fuel`，出堆时 `miles -= 负数`',
                 '写法一：用 `cur_fuel` 记剩余油量，每站先扣去行驶耗油；本视频用写法二，记「能开到的距离 miles」',
                 '同类：反悔贪心题单 §1.9（如 630. 课程表 III）'],
    ),
)
