def _tgt(S):
    if 'start' not in S or 'n' not in S:
        return ''
    t = list(range(S['start'], S['n'], 2))
    return f"start = {S['start']}：车的目标下标 `{t}`，现在的车位 `{S['pos1']}`"


CONFIG = dict(
    num=3587, title='最小相邻交换至奇偶交替', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='奇数当车 · 按序配对目标位',
    tags=['灵神题单', '难度分 1548'],
    code='''
class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        pos1 = [i for i, x in enumerate(nums) if x % 2]  # 车（奇数）的下标

        n = len(nums)
        m = len(pos1)

        # start=0 表示车要去偶数下标，start=1 表示车要去奇数下标
        def calc(start: int) -> int:
            # (n-start+1)//2 表示偶数（奇数）下标的个数
            if (n - start + 1) // 2 != m:
                return inf
            return sum(abs(i - j) for i, j in zip(range(start, n, 2), pos1))

        ans = min(calc(0), calc(1))
        return -1 if ans == inf else ans
''',
    call='Solution().minSwaps([2,4,6,5,7])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 奇数 = 车，灰 = 偶数 = 空位）', h=200,
             color=lambda S, i, v: 'blue' if v % 2 else None),
        dict(type='array', var='pos1', label='pos1：车的下标', h=170, pointers={}),
        dict(type='text', fn=_tgt, size=26, h=90),
    ],
    watch=['n', 'm', 'start', ('ans', 'ans', 'green')],
    captions={
        'pos1 = [': '把奇数当==车==、偶数当空位，记下车的下标 `pos1 = {pos1}`',
        'n = len': '`n = {n}`',
        'm = len': '车一共 `m = {m}` 辆',
        'def calc': '`calc(start)`：车全部去 `start, start+2, ...` 这些下标，算总移动距离',
        '!= m': lambda S, B, r: (f'`(n-start+1)//2 = {(S.n-S.start+1)//2}` 个目标位，车有 `{S.m}` 辆 → '
                                 + ('数量不等，这种摆法不可能 → 返回 inf' if (S.n-S.start+1)//2 != S.m else '数量刚好，可以摆')),
        'return inf': '目标位个数和车数不同，无解 → `inf`',
        'return sum': lambda S, B, r: (f'最左的车去最左的目标位：`start = {S.start}`，目标 `{list(range(S.start, S.n, 2))}`，'
                                       f'距离和 = =={r}=='),
        'ans = min': '两种摆法取最小：`ans = min(calc(0), calc(1)) =` =={ans}==',
        'return -1': lambda S, B, r: ('两种都是 inf → 无解，返回 `-1`' if S.ans == inf else f'有解，答案 =={r}=='),
    },
    cards=dict(
        one_liner='奇数当车、偶数当空位，车按顺序去目标位',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次交换相邻两个数，让奇偶性交替出现，求最少交换次数；不可能则 `-1`',
                 '示例：`[2,4,6,5,7]` → `3`',
                 '`[4,5,6,8]` → `-1`'],
        quote='把偶数视作空位，奇数视作汽车。……贪心地，最左边的汽车移动到最左边的目标位置，比移动到其他位置更优。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只看车：全在偶数下标，或全在奇数下标，空位自然交替',
              '车的相对顺序不变（交换两辆车没意义），第 `i` 辆车去第 `i` 个目标位',
              '每辆车的移动距离 `|a[i]-b[i]|` 累加；两种目标取小，数量对不上就是 `inf`'],
        summary=['时间 `O(n)`，空间 `O(n)`（边遍历边算可 `O(1)`）',
                 '易错：目标位个数 `(n-start+1)//2` 必须等于车数，否则无解',
                 '长度为偶数时两种摆法都可行，要取最小',
                 '相似题：1864 构成交替字符串需要的最小交换次数'],
    ),
)
