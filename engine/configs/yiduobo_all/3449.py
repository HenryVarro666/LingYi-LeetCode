def _top(S):
    if 'cnt' in S and 'mid' in S and 'nxt' in S:
        return f"试探 `mid = {S['mid']}`：累计操作 `cnt = {S['cnt']}`（上限 `m = {S['m']}`），上一个顺带到达当前下标的次数 `nxt = {S['nxt']}`"
    if 'mid' in S:
        return f"二分 `[{S['left']}, {S['right']}]`，试探 `mid = {S['mid']}`"
    if 'left' in S:
        return f"二分区间 `[{S['left']}, {S['right']}]`"
    return '最大化最小值 → 二分答案 `mid`'


def _need(S):
    if 'need' not in S or 'index' not in S:
        return ''
    need, nxt = S['need'], S['nxt']
    return f"下标 `{S['index']}`：要到达 `need = {need}` 次；之前顺带到达过的次数见 `nxt`，累计 `cnt = {S['cnt']}`"


CONFIG = dict(
    num=3449, title='最大化游戏分数的最小值', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 010101 往返贪心',
    tags=['二分算法', '贪心与思维', '难度分 2748'],
    code='''
class Solution(object):
    def maxScore(self, points, m):
        
        if m < len(points):
            return 0

        mi = min(points)

        left = mi
        right = mi * m
        while left < right:
            mid = (left + right + 1) // 2
            cnt = 0
            nxt = 0

            for index, v in enumerate(points):
                need = (mid - 1) // v + 1
                if need > nxt:
                    cnt += (need - nxt) * 2 - 1
                    nxt = need - nxt - 1
                elif index != len(points) - 1:
                    cnt += 1
                    nxt = 0
            
            if cnt > m:
                right = mid - 1
            else:
                left = mid
        
        return left
''',
    call='Solution().maxScore([1,2,3], 5)',
    expect=2,
    max_steps=70,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='array', var='points', label='points（黄 = 当前下标）', h=220, pointers={'index': 'blue'},
             color=lambda S, i, v: 'yellow' if S.get('index') == i and 'need' in S else None,
             dim=lambda S, i, v: 'index' in S and 'need' in S and i < S['index']),
        dict(type='text', fn=_need, size=24, h=80),
    ],
    watch=['mid', 'index', 'v', 'need', 'nxt', 'cnt', 'm', 'left', 'right'],
    captions={
        'if m < len(points)': lambda S, B, r: ('`m < n`：连每个游戏都走不到 → 答案 0' if S.m < len(S.points) else f'`m = {S.m} ≥ n = {len(S.points)}`：至少能走一遍，进入二分'),
        'mi = min(points)': '`mi = {mi}`：一路向右走，每个得分至少是自己的 points',
        9: '下界 `left = {left}`：一路向右，必可行',
        10: '上界 `right = mi × m = {right}`：设得大一点',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，继续' if S.left < S.right else f'`left = right = {S.left}`，答案确定'),
        'mid = (left': '试探 `mid = {mid}`（取上中位数，配合 `left = mid`）',
        13: '`cnt`：达到 `mid` 至少要多少次操作',
        14: '`nxt`：前面的往返顺带到了当前下标几次',
        16: lambda S, B, r: (f'看下标 `{S.index}`，`v = {S.v}`' if not (B.get('index') == S.get('index') and 'need' in B) else '遍历结束，数完所需操作'),
        'need = (mid - 1)': '得分 ≥ `{mid}`，要到达 `need = ({mid}-1)//{v}+1 = {need}` 次',
        'if need > nxt': lambda S, B, r: (f'`need = {S.need} > nxt = {S.nxt}`：之前顺带的不够，还得往返 `{S.need - S.nxt}` 次' if S.need > S.nxt else f'`need = {S.need} ≤ nxt = {S.nxt}`：之前顺带的已经够了'),
        'cnt += (need - nxt)': '往返 `{need - B.nxt}` 次：形如 `i, i+1, i, ...` 共 `({need} - {B.nxt})×2 - 1 = {(need - B.nxt) * 2 - 1}` 步，`cnt = {cnt}`',
        'nxt = need - nxt - 1': '往返中到过下一个下标 `{nxt}` 次：`nxt = {nxt}`',
        'elif index != len': lambda S, B, r: (f'不是最后一个下标：还得走 1 步到下一格' if S.index != len(S.points) - 1 else '已是最后一个下标，且分数够了，不用再走'),
        'cnt += 1': '只需 1 步走过去：`cnt = {cnt}`',
        23: '这一步没往返，下一个下标没有顺带次数：`nxt = 0`',
        'if cnt > m': lambda S, B, r: (f'`cnt = {S.cnt} > m = {S.m}`：步数不够 → `mid` ==不可行==' if S.cnt > S.m else f'`cnt = {S.cnt} ≤ m = {S.m}`：够用 → `mid` 可行'),
        26: '`right = {right}`',
        28: '`left = {left}`',
        'return left': '答案 `{left}`',
    },
    cards=dict(
        one_liner='二分答案，每个位置先往返凑够次数，再带着余量往后走',
        complexity='时间 `O(n log(m·min))`，空间 `O(1)`',
        problem=['从下标 -1 出发，每步 ±1，把落脚处的 `points[i]` 加进得分',
                 '至多 `m` 步，使 `gameScore` 的==最小值最大==',
                 '本视频：`points=[1,2,3], m=5` → `2`'],
        quote='对于index = 0这个位置，……需要走出形如010101...010的操作，其中有need个0，因此一共需要need * 2 - 1次操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['`m < n` 走不完，答案直接 0；否则二分 `mid`，下界 `min(points)`',
              '位置 i 需要到达 `need` 次：在 i 与 i+1 间往返，花 `(need-nxt)×2-1` 步',
              '往返顺带到达 i+1 共 `need-nxt-1` 次，记在 `nxt`；够了就只走 1 步'],
        summary=['时间 `O(n log(m·min))`，空间 `O(1)`',
                 '原文已使用 `//`，是 Python 3 可直接运行的写法，无需修改',
                 '易错：`m < n` 要先特判返回 0',
                 '最后一个下标满足后不用再走，所以 `elif index != len(points) - 1`',
                 '对比灵神：灵神 `left` 从 0 开始、用 `pre` 和 `rem` 倒扣步数；yiduobo 从 `min(points)` 起，用 `nxt` 和 `cnt` 累计步数'],
    ),
)
