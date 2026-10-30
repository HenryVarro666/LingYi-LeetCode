CONFIG = dict(
    num=2332, title='坐上公交的最晚时间', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 双指针模拟 + 插队',
    tags=['灵神题单', '难度分 1841'],
    code='''
class Solution:
    def latestTimeCatchTheBus(self, buses: List[int], passengers: List[int], capacity: int) -> int:
        buses.sort()
        passengers.sort()

        # 模拟乘客上车
        j = 0
        for t in buses:
            c = capacity
            while c and j < len(passengers) and passengers[j] <= t:
                j += 1
                c -= 1

        # 寻找插队时机
        j -= 1
        ans = buses[-1] if c else passengers[j]
        while j >= 0 and ans == passengers[j]:  # 往前找没人到达的时刻
            ans -= 1
            j -= 1
        return ans
''',
    call='Solution().latestTimeCatchTheBus([20,30,10], [19,13,26,4,25,11,21], 2)',
    expect=20,
    views=[
        dict(type='array', var='buses', label='buses（发车时间）', h=200,
             color=lambda S, i, v: 'orange' if S.get('t') == v else None),
        dict(type='array', var='passengers', label='passengers（到达时间，绿 = 已上车）', h=260,
             pointers={'j': 'blue'},
             color=lambda S, i, v: 'green' if i < S.get('j', 0) and S.get('_line', 0) < 16 else None),
        dict(type='text', size=34, fn=lambda S: (f"这班车 `t = {S['t']}`，剩余座位 `c = {S['c']}`" if 't' in S and 'c' in S else '')),
    ],
    watch=['t', 'c', ('j', 'j', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'buses.sort()': '先把发车时间从小到大排好，方便按顺序模拟',
        'passengers.sort()': '乘客也按到达时间排序：先到的先上车',
        'for t in buses': '处理下一班车，发车时间 `t = {t}`',
        'c = capacity': '新来一班车，座位清零重算：`c = {c}`',
        'while c and': lambda S, B, r: (f'有座位 `c = {S.c}` 且乘客 `{S.passengers[S.j]}` ≤ 发车时间 `{S.t}` → ==上车=='
                                        if S.c and S.j < len(S.passengers) and S.passengers[S.j] <= S.t
                                        else '没座位了，或下一位乘客赶不上这班车 → 等下一班'),
        'j += 1': '乘客上车，`j` 指向下一位：{j}',
        'c -= 1': '座位少一个：`c = {c}`',
        15: '`j` 退一步，指向==最后一个上车的乘客== `passengers[{j}] = {passengers[j]}`',
        'ans = buses[-1]': lambda S, B, r: (f'最后一班车还有空位 `c = {S.c}` → 想在发车时 `{S.ans}` 到' if S.c
                                            else f'最后一班车满了 → 想挤掉最后上车的 `{S.ans}`，在它前一刻到'),
        'while j >= 0': lambda S, B, r: (f'`ans = {S.ans}` 已经有乘客在这一刻到 → 要继续往前找' if S.j >= 0 and S.ans == S.passengers[S.j]
                                         else f'`ans = {S.ans}` 没有人同时到 → 就在这一刻插队'),
        'ans -= 1': '这个时刻被占了，往前一刻：`ans = {ans}`',
        19: '同时看更早的乘客：`j = {j}`',
        'return ans': '最晚可以在 `{ans}` 时刻到达',
    },
    cards=dict(
        one_liner='先模拟上车，再顺着最后一名乘客往前找没人到的时刻插队',
        complexity='时间 `O(n log n + m log m)`，空间 `O(1)`',
        problem=['`buses` 是发车时间，`passengers` 是到达时间，每车最多载 `capacity` 人',
                 '先到先上车，求自己能赶上车的==最晚到站时间==，且不能和别人同时到',
                 '示例：`buses=[20,30,10]`，`passengers=[19,13,26,4,25,11,21]`，`capacity=2` → `20`'],
        quote='如果一个乘客上了车，那么他前面的乘客也肯定上了车。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最后一班车有空位：想在发车时到；没空位：想挤掉最后上车的乘客 A，在 A 前一刻到',
              '想到的时刻若已有人到，就==往前找第一个没人的时刻==，这样插队不会影响前面的人',
              '前面的人先上车，所以插队只可能挤掉后面的人，自己一定能上'],
        summary=['时间 `O(n log n + m log m)`，瓶颈是排序；双重循环里 `j` 总共只增加 `O(m)` 次',
                 '最后一班车 `c > 0` 才取 `buses[-1]`，否则从最后上车的乘客往前找',
                 '`j` 加一后要先 `j -= 1`，才是最后一个上车的人',
                 '所有乘客都上车时，最后几班车可能是空的，结论不变'],
    ),
)
