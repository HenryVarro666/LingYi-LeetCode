CONFIG = dict(
    num=2960, title='统计已测试设备', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='差分思想 · 只记减一次数',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution:
    def countTestedDevices(self, batteryPercentages: List[int]) -> int:
        dec = 0
        for x in batteryPercentages:
            if x > dec:
                dec += 1
        return dec
''',
    call='Solution().countTestedDevices([1,1,2,1,3])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"当前电量 `x = {S['x']}`，前面已让它减了 `dec = {S['dec']}` 次，实际电量 `max(0, {S['x']} − {S['dec']})` → =={max(0, S['x'] - S['dec'])}==" if 'x' in S and 'dec' in S else '`dec`：后面每个设备都要被减一的次数')),
        dict(type='array', var='batteryPercentages', h=200, label='batteryPercentages'),
        dict(type='text', fn=lambda S: (f"已测试设备数 = `dec` = =={S['dec']}==" if 'dec' in S else '')),
    ],
    watch=['x', ('dec', 'dec', 'green')],
    captions={
        'dec = 0': '`dec` 记录「后面设备要减一的次数」，同时也是已测试设备数',
        'if x > dec': lambda S, B, r: f'实际电量 `max(0, {S.x} − {S.dec})` = {max(0, S.x - S.dec)}' + ('，大于 0 → 这个设备会被测试' if S.x > S.dec else '，不大于 0 → 跳过，不测试'),
        'dec += 1': '测试了一个设备：后面所有设备都要减一，差分上只需 `dec += 1` → =={dec}==',
        'return dec': '每次 `x > dec` 都 `dec += 1`，正好就是测试过的设备数 → `{dec}`',
    },
    cards=dict(
        one_liner='「后面全部减一」不用真减，记一个次数 dec 就够',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['按顺序测试设备：电量 `> 0` 就计数，并让后面所有设备电量减 1（最低为 0）',
                 '返回被测试的设备数',
                 '示例：`[1,1,2,1,3]` → `3`'],
        quote='如果 x - dec > 0，即 x > dec，那么后面的数都要减一，根据差分数组的思想，把 dec 加一即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['区间 `[i+1, n-1]` 整体减一，是差分数组的典型场景',
              '因为区间一直延伸到末尾，差分的前缀和就是一个累计值 `dec`',
              '实际电量 `x − dec`，大于 0 就测试，`dec` 同时是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '不用真的去减后面的元素（那样是 `O(n^2)`）',
                 '判断用 `x > dec`，等价于 `x − dec > 0`',
                 '同类题：差分数组 §2.1 一维差分'],
    ),
)
