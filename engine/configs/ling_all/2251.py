CONFIG = dict(
    num=2251, title='花期内花的数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='差分 + 离线排序双指针',
    tags=['灵神题单', '常用数据结构', '难度分 2022'],
    code='''
class Solution:
    def fullBloomFlowers(self, flowers: List[List[int]], people: List[int]) -> List[int]:
        diff = Counter()
        for start, end in flowers:
            diff[start] += 1
            diff[end + 1] -= 1
        times = sorted(diff)

        j = s = 0
        for p, i in sorted(zip(people, range(len(people)))):
            while j < len(times) and times[j] <= p:
                s += diff[times[j]]  # 累加不超过 people[i] 的差分值
                j += 1
            people[i] = s  # 从而得到这个时刻花的数量
        return people
''',
    call='Solution().fullBloomFlowers([[1,4],[3,6],[7,9]], [4,3,8])',
    expect=[2, 2, 1],
    views=[
        dict(type='map', var='diff', label='diff（时刻 → 花的数量变化：开花 +1，凋谢后一刻 -1）',
             fmt=lambda k, v: f'{k}: {v:+d}', h=150, font=30),
        dict(type='array', var='times', label='times（有变化的时刻，排序；蓝 = j 下一个要累加的）', pointers={'j': 'blue'}, h=190,
             dim=lambda S, i, v: 'j' in S and i < S['j']),
        dict(type='array', var='people', label='people（来的时间；处理后原地改成花的数量）', pointers={'i': 'pink'}, h=190),
        dict(type='text', fn=lambda S: (f"累加到时刻 `{S['p']}` 为止，`s = {S['s']}` 朵花正开着" if 'p' in S and 's' in S else ''), h=50),
    ],
    watch=['p', 'i', 'j', ('s', 's', 'green')],
    captions={
        'diff = Counter': '`diff` 记录某个时刻花数的变化，时间很大，用哈希表代替数组',
        'diff[start] += 1': '花在 `{start}` 开：该时刻花数 +1',
        'diff[end + 1] -= 1': '花期含 `end`，所以到 `{end + 1}` 才凋谢：该时刻花数 -1',
        'times = sorted': '把有变化的时刻排序，之后用指针 `j` 往右累加',
        'j = s = 0': '`j` 指向下一个没累加的时刻，`s` 是当前花数',
        'for p, i in sorted': '把人按来的时间从小到大处理（`i` 是他在原数组里的位置）→ 前缀和只用往右扫一遍',
        'while j < len': lambda S, B, r: (f'`times[{S.j}] = {S.times[S.j]} <= p = {S.p}`：这个变化已经发生 → 累加' if S.j < len(S.times) and S.times[S.j] <= S.p else (f'`j = {S.j}` 已到末尾，没有更多变化' if S.j >= len(S.times) else f'`times[{S.j}] = {S.times[S.j]} > p = {S.p}`：还没发生，停')),
        's += diff': '加上 `diff[{times[j]}] = {diff[times[j]]}`，花数 `s = {s}`',
        'j += 1': '指针 `j` 右移，看下一个变化时刻',
        'people[i] = s': '时刻 `{p}` 的花数就是 `s` 为 =={s}== → 写到 `people[{i}]`',
        'return people': '`people` 已被改成答案：`{people}`',
    },
    cards=dict(
        one_liner='开花 +1、凋谢 -1，按时间累加就是当时的花数',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n+m)`',
        problem=['每朵花有花期 `[start, end]`（含两端），每个人在某个时刻来看花',
                 '返回每个人到达时正在开的花的数量',
                 '示例：`flowers=[[1,4],[3,6],[7,9]], people=[4,3,8]` → `[2,2,1]`'],
        quote='把 flowers[i] 看成是将区间 [start_i, end_i] 上的每个时间点都增加一朵花。……对于本题，由于元素值很大，需要把数组改成有序集合，或者用哈希表+排序。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['区间加一 → 差分：`diff[start] += 1`，`diff[end + 1] -= 1`',
              '时刻很大不能开数组，用 `Counter` + 排序的 `times`',
              '把人也按时间排序，一边累加差分一边回答，答案写回 `people[i]`'],
        summary=['时间 `O((n+m) log)`，空间 `O(n+m)`',
                 '凋谢写在 `end + 1`：花期包含 `end`',
                 '`times[j] <= p` 用小于等于：恰好在 `p` 时刻开的花也算',
                 '方法一：`bisect_right(starts, p) - bisect_left(ends, p)`，两次二分',
                 '原题解函数名被打码，这里写回 `fullBloomFlowers`'],
    ),
)
