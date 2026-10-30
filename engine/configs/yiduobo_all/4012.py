def _tail(S):
    if 'p' not in S or 'r' not in S or 's' not in S:
        return '前缀和 `s`（`s[0] = 0`）：`s[j] − s[i−1]` 就是任务 `i..j` 的总时长'
    p, r, s = S['p'], S['r'], S['s']
    need = s[-1] - s[p - 1]
    if 'v' in S and S['_line'] >= 11:
        return f"本班可用 `v = {S['v']}`；从任务 `{p - 1}` 起做完全部需要 `s[-1] − s[{p - 1}]` = =={need}=="
    return f"下一班从「任务 `{p - 1}` 已做了 `{r}` 分钟」继续 → 剩余总需 =={need - r}=="


def _color(S, i, v):
    if 'p' not in S or 'v' not in S or 'left' not in S or 'right' not in S:
        return None
    if S['_line'] >= 14 and i == S['p'] - 1:
        return 'cyan'
    return None


CONFIG = dict(
    num=4012, title='统计每个班次结束后的未完成任务数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='前缀和 + 手写二分 · 记录进度 (p, r)',
    tags=['二分查找', '进阶', '难度分 1736'],
    code='''
class Solution(object):
    def countTasks(self, tasks, shifts):
        
        s = [0]
        for t in tasks:
            s.append(s[-1] + t)
        
        p, r = 1, 0
        res = []
        for v in shifts:
            v += r
            if v >= s[-1] - s[p - 1]:
                res.append(0)
                p, r = 1, 0
            else:
                left = p
                right = len(s) - 1
                while left < right:
                    mid = (left + right) // 2
                    if s[mid] - s[p - 1] <= v:
                        left = mid + 1
                    else:
                        right = mid

                res.append(len(s) - left)
                r = v - (s[left - 1] - s[p - 1])
                p = left

        return res
''',
    call='Solution().countTasks([2,3,4,5], [4,3,6,20])',
    expect=[3, 2, 1, 0],
    views=[
        dict(type='text', size=24, fn=_tail),
        dict(type='array', var='s', label='s（前缀和，s[0] = 0；青 = 当前从哪个任务开始）', h=300,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             window=('left', 'right'),
             color=lambda S, i, v: 'cyan' if 'p' in S and S['_line'] >= 13 and i == S['p'] - 1 else None),
        dict(type='array', var='res', label='res（每班结束后的未完成数）', h=200, color=lambda S, i, v: 'green'),
    ],
    watch=[('p', 'p', 'cyan'), ('r', 'r', 'orange'), ('v', 'v'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        's.append(s[-1] + t)': '`s` 追加 `{s[-1]}`：前 `{len(s) - 1}` 个任务共需 `{s[-1]}`',
        'p, r = 1, 0': lambda S, B, r_: ('`p` = 下一班要接着做的任务（带 1 的偏移），`r` = 该任务已做的分钟数；初始 `p=1, r=0`' if S._line < 12
                                         else '全部做完 → ==进度重置== `p = 1, r = 0`'),
        'v += r': '本班可用时间 `{v}`（本班 `{B.v}` + 之前该任务已做的 `{r}`）',
        'if v >= s[-1] - s[p - 1]': lambda S, B, r_: (f"剩余总需 `s[-1] − s[p−1]` = `{S.s[-1]} − {S.s[S.p - 1]}` = {S.s[-1] - S.s[S.p - 1]}；`v = {S.v}` 够 → ==全做完=="
                                                      if S.v >= S.s[-1] - S.s[S.p - 1] else
                                                      f"剩余总需 `{S.s[-1] - S.s[S.p - 1]}`，`v = {S.v}` 不够 → 要二分找第一个做不完的任务"),
        'res.append(0)': '本班做完所有任务 → 答案 `0`',
        'left = p': '二分范围：下界 `left = p`',
        'right = len(s) - 1': '上界 `right = {right}`；在 `s` 里找第一个「做不完」的位置',
        'while left < right': lambda S, B, r_: (f'`{S.left} < {S.right}` 继续二分' if S.left < S.right
                                                 else f'`left = right = {S.left}`：首个做不完的位置'),
        'mid = (': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if s[mid] - s[p - 1] <= v': lambda S, B, r_: (f"任务 `{S.p - 1}..{S.mid - 1}` 共 `s[{S.mid}] − s[{S.p - 1}]` = {S.s[S.mid] - S.s[S.p - 1]}"
                                                       f" {'<=' if S.s[S.mid] - S.s[S.p - 1] <= S.v else '>'} `v = {S.v}`"
                                                       f" → {'做得完，==left = mid + 1==' if S.s[S.mid] - S.s[S.p - 1] <= S.v else '做不完，==right = mid=='}"),
        'left = mid + 1': '`left` → {left}',
        'right = mid': '`right` → {right}',
        'res.append(len(s) - left)': '`left` 偏移 1，做不完的是任务 `{left - 1}` → 未完成 `len(s) − left` = =={res[-1]}==',
        'r = v - (': '新进度：本班用掉 `s[{left - 1}] − s[{p - 1}]`，剩余 `r = {r}` 分钟已投入那个未完成任务',
        'p = left': '`p = {p}`：下班从这个任务继续',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='记下「做到哪个任务、已做了多久」，每班用前缀和二分',
        complexity='时间 `O(n + m log n)`，空间 `O(n)`',
        problem=['任务按序做，没做完的下一班接着做；某班做完所有任务则剩余时间丢弃、下一班从头来',
                 '求每个班次结束后的未完成任务数',
                 '示例：`tasks=[1,4,4], shifts=[9,1,4]` → `[0,2,1]`',
                 '本视频：`[2,3,4,5], [4,3,6,20]` → `[3,2,1,0]`'],
        quote='需要使用两个变量p和r，分别表示下一个班次将从已经执行了r分钟的任务p开始继续向后执行。',
        quote_src='—— yiduobo 题解原文',
        idea=['完成的任务越多用时越长 → 每班可以==二分==',
              '用 `p, r` 表示进度：下班从「已做了 r 分钟的任务 p」继续',
              '前缀和（`s[0]=0`）让区间和变成 `s[mid] − s[p−1]`，比较 `v = shifts + r`'],
        summary=['时间 `O(n + m log n)`，空间 `O(n)`',
                 '`s` 带 1 的偏移：`p` 初值与重置值都是 `1`，二分结束后 `left − 1` 才是做不完的任务',
                 '新的 `r = v − (s[left−1] − s[p−1])`，要把旧的 `r` 也算在 `v` 里',
                 '全做完时 `p, r` 一起重置；对比灵神：他把进度压成累计时间 `t`，不必维护 `p, r`'],
    ),
)
