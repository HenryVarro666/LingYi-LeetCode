def _cmp(S):
    if 'now' not in S:
        return ''
    return f"当前已覆盖到 `now = {S['now']}`　　目标 `T = {S['T']}`　　已选 `res = {S['res']}` 段"


CONFIG = dict(
    num=1024, title='视频拼接', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 每轮选右端点最大', tags=['贪心思维'],
    code='''
class Solution(object):
    def videoStitching(self, clips, T):

        if T == 0:
            return 0

        now = 0
        res = 0
        pos = 0
        sorted_clips = sorted(clips, key=lambda d:(d[0], d[1]))
        n = len(sorted_clips)
        while pos < n:
            next = 0
            while pos < n and sorted_clips[pos][0] <= now:
                next = max(next, sorted_clips[pos][1])
                pos += 1
            
            if next == 0:
                return -1

            now = next
            res += 1
            if now >= T:
                return res

        return -1
''',
    call='Solution().videoStitching([[0, 2], [4, 6], [8, 10], [1, 9], [1, 5], [5, 9]], 10)',
    expect=3,
    views=[
        dict(type='text', fn=_cmp),
        dict(type='intervals', var='sorted_clips', pointer='pos', label='数轴：按左端点排序的片段（黄 = pos 指向的下一个）', h=440),
    ],
    watch=[('now', 'now', 'blue'), ('next', lambda S: S['next'] if isinstance(S.get('next'), int) else '-', 'pink'), ('pos', 'pos', 'yellow'), ('res', 'res', 'green')],
    captions={
        'if T == 0': '`T = {T}`：目标长度不为 0，需要选片段',
        'now = 0': '`now` = 目前已经覆盖到的位置，从 0 开始',
        'res = 0': '`res` = 已选片段数',
        'pos = 0': '`pos` = 下一个还没看的片段下标',
        'sorted_clips = sorted': '按左端点排序：`{sorted_clips}`',
        'n = len': '共 `{n}` 个片段',
        'while pos < n:': lambda S, B, r: (f'还有片段没看，`pos = {S.pos} < {S.n}`，开始新一轮选择' if S.pos < S.n else '片段都看完了，没能覆盖到 T → 返回 -1'),
        'next = 0': '新一轮：在“左端点 ≤ now”的片段里找最大右端点，先记 `next = 0`',
        'while pos < n and': lambda S, B, r: (f'`sorted_clips[{S.pos}][0] = {S.sorted_clips[S.pos][0]}` ≤ `now = {S.now}`：==这个片段能接上==，纳入候选' if S.pos < S.n and S.sorted_clips[S.pos][0] <= S.now else ('片段已经用完，这一轮候选收集完毕' if S.pos >= S.n else '后面的片段左端点 > now，接不上了，这一轮候选收集完毕')),
        'next = max': '候选右端点取最大：`max({B.next}, {sorted_clips[pos][1]}) = {next}`',
        'pos += 1': '`pos` → {pos}，看下一个片段',
        'if next == 0': lambda S, B, r: ('`next = 0`：没有片段能接上 now → ==覆盖不了，返回 -1==' if S.next == 0 else f'`next = {S.next}` > 0：这一轮找到了能接上的片段'),
        'now = next': '选出右端点最大的片段：`now` 推进到 =={now}==',
        'res += 1': '多用了一个片段：`res = {res}`',
        'if now >= T': lambda S, B, r: (f'`now = {S.now}` ≥ `T = {S.T}`：已覆盖整个区间 → 返回 `res`' if S.now >= S.T else f'`now = {S.now}` < `T = {S.T}`：还没覆盖够，继续下一轮'),
        'return res': '最少需要 `{ret}` 个片段',
    },
    cards=dict(
        one_liner='每一轮在能接上的片段里，选右端点最远的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出若干视频片段 `[start, end]` 和目标时长 `T`',
                 '选出最少的片段，拼成覆盖 `[0, T]` 的整段视频；做不到返回 `-1`',
                 '示例：`[[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], T = 10` → `3`'],
        quote='每次都选择当前可选区间中右边界最大的，然后根据这个右边界更新当前可选区间的集合，重复此过程直到某一时刻右边界大于等于T，或者可选区间的集合为空。',
        quote_src='—— yiduobo 题解原文',
        idea=['首先必须选一个左边界为 0 的片段，代价都是 1，当然选==右边界最大==的',
              '设右边界为 `now`，下一步可选的是所有左边界 ≤ `now` 的片段，再选其中右边界最大的',
              '先按左边界排序，用 `pos` 一路往后扫，每个片段只看一次'],
        summary=['时间 `O(n log n)`，瓶颈在排序；双指针扫描 `O(n)`',
                 '`next == 0` 说明这一轮一个片段都接不上，直接 `-1`',
                 '`now >= T` 才算覆盖完，用 `>=` 因为片段可能超出 T',
                 '`T == 0` 要先特判返回 0',
                 '同类题：1326. 灌溉花园的最少水龙头数目、45. 跳跃游戏 II'],
    ),
)
