def _txt(S):
    if 'now' not in S:
        return ''
    return f"已覆盖到 `now = {S['now']}`　　本轮最远 `next = {S['next'] if isinstance(S.get('next'), int) else '-'}`　　已选 `res = {S['res']}`"


def _cur(S):
    seq = S.get('intervals')
    p = S.get('p')
    if not seq or p is None or isinstance(seq, list) and seq and not isinstance(seq[0], list):
        return None
    return p if p < len(seq) else None


CONFIG = dict(
    num=1326, title='灌溉花园的最少水龙头数目', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='区间排序 + 每轮选右端最远', tags=['贪心算法', '区间贪心', '难度分 1885'],
    code='''
class Solution(object):
    def minTaps(self, n, ranges):

        intervals = []
        for index, r in enumerate(ranges):
            l = max(index - r, 0)
            r = min(index + r, n)
            intervals.append([l, r])
        
        intervals = sorted(intervals, key=lambda d:d[0])
        now = 0
        p = 0
        res = 0
        while now < n:            
            next = now
            while p <= n and intervals[p][0] <= now:
                next = max(next, intervals[p][1])
                p += 1

            if now == next:
                return -1

            res += 1
            now = next
            

        return res
''',
    call='Solution().minTaps(6, [1, 2, 1, 0, 2, 1, 0])',
    expect=2,
    views=[
        dict(type='text', fn=_txt),
        dict(type='intervals', var='intervals', pointer=_cur, label='数轴：每个水龙头的灌溉区间（排序后，黄 = p 指向的下一个）', h=470),
    ],
    watch=[('now', 'now', 'blue'), ('next', lambda S: S['next'] if isinstance(S.get('next'), int) else '-', 'pink'), ('p', 'p', 'yellow'), ('res', 'res', 'green')],
    captions={
        'intervals = []': '把每个水龙头变成一个区间，装进 `intervals`',
        'for index, r in enumerate': lambda S, B, r_: ('所有水龙头都转成区间了' if B.get('index') == S.index and 'index' in B else f'水龙头 `{S.index}`，半径 `{S.ranges[S.index]}`'),
        'l = max': '左端点 `max({index} - {ranges[index]}, 0) = {l}`：花园从 0 开始，负的不算',
        'r = min': '右端点 `min({index} + {ranges[index]}, {n}) = {r}`',
        'intervals.append': '加入区间 `{intervals[-1]}`',
        'sorted(intervals': '按左边界排序：`{intervals}`',
        'now = 0': '`now`：目前已经覆盖到的位置',
        'p = 0': '`p`：下一个还没考虑的区间下标',
        'res = 0': '`res`：已经选的区间数',
        'while now < n': lambda S, B, r_: (f'`now = {S.now} < n = {S.n}`：还没覆盖到末尾，再选一个' if S.now < S.n else f'`now = {S.now} ≥ n = {S.n}`：覆盖完成'),
        'next = now': '新一轮：从 `now` 出发，先令 `next = now`（不扩展）',
        'while p <= n and': lambda S, B, r_: (f'`intervals[{S.p}][0] = {S.intervals[S.p][0]}` ≤ `now = {S.now}`：==左边界够得着，可选==' if S.p <= S.n and S.intervals[S.p][0] <= S.now else ('区间用完了，本轮结束' if S.p > S.n else f'`intervals[{S.p}][0] = {S.intervals[S.p][0]}` > `now = {S.now}`：接不上，本轮结束')),
        'next = max': '右边界尽量大：`next = max({B.next}, {intervals[p][1]}) = {next}`',
        'p += 1': '`p` → {p}',
        'if now == next': lambda S, B, r_: (f'`now == next = {S.now}`：没有区间能把右边界推过去 → ==无法覆盖，返回 -1==' if S.now == S.next else f'`next = {S.next}` > `now = {S.now}`：本轮选到了更远的区间'),
        'res += 1': '选下这个区间：`res = {res}`',
        'now = next': '`now` 推进到 =={now}==',
        'return res': '最少需要 `{ret}` 个水龙头',
    },
    cards=dict(
        one_liner='水龙头就是区间：每一轮选能接上、右端最远的那个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n + 1` 个水龙头在 `0..n`，水龙头 `i` 灌溉 `[i - ranges[i], i + ranges[i]]`',
                 '求覆盖 `[0, n]` 的最少水龙头数；覆盖不了返回 `-1`',
                 '本视频：`n = 6, ranges = [1,2,1,0,2,1,0]` → `2`'],
        quote='我们都选择左边界在l到r之间，右边界最大的区间，设这个右边界为r\'，那么此时我们将l更新为r + 1，将r更新为r\'，然后重复这个操作，直到可以覆盖整个区间，或者无法继续扩展区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['先选覆盖 0 且右边界最大的区间，设右边界为 `r`',
              '后面只能从左边界 ≤ `r` 的区间里选，仍然挑==右边界最大==的',
              '`l`、`r` 单调递增 → 区间按左边界排序后，一趟扫描解决'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先把区间裁到 `[0, n]`：`max(index - r, 0)` 与 `min(index + r, n)`',
                 '`now == next` 说明这一轮一点都扩展不了 → `-1`',
                 '`p <= n` 防止 `p` 越界，区间共 `n + 1` 个',
                 '同类题：1024. 视频拼接（思路几乎一样）'],
    ),
)
