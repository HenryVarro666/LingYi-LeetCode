POS, M = [1, 2, 3, 4, 7], 3


def _pcol(S, i, v):
    if 'cnt' not in S or 'now' not in S or S['_line'] in (6, 7, 8):
        return None
    # 重新贪心一遍：已放球的篮子标绿
    pos, mid = S['position'], S['mid']
    placed, now = [0], 0
    for j in range(1, len(pos)):
        if len(placed) >= S['cnt']:
            break
        if pos[j] - pos[now] >= mid:
            placed.append(j)
            now = j
    if i in placed[:S['cnt']]:
        return 'green'
    if i < S['next'] and i > S['now']:
        return 'red'
    return None


def _top(S):
    if 'mid' not in S:
        return '最小间隔越大越难放下 `m` 个球 → ==二分答案=='
    if 'now' in S and 'next' in S and S['next'] < len(S['position']):
        return (f"`mid = {S['mid']}`：上一个球在 `position[{S['now']}] = {S['position'][S['now']]}`，"
                f"候选 `position[{S['next']}] = {S['position'][S['next']]}`，距离 `{S['position'][S['next']] - S['position'][S['now']]}`")
    return f"`mid = {S['mid']}`：已放 `cnt = {S.get('cnt', 0)}` 个球"


def _inner(S, B, ret):
    pos, now, nx, mid = S.position, S.now, S.next, S.mid
    if nx < S.n and pos[nx] - pos[now] < mid:
        return f'`{pos[nx]} − {pos[now]} = {pos[nx] - pos[now]} < {mid}`：离上一个球太近，跳过这个篮子'
    if nx >= S.n:
        return '`next` 走到末尾，没有篮子了'
    return f'`{pos[nx]} − {pos[now]} = {pos[nx] - pos[now]} ≥ {mid}`：找到==最靠前==的可放篮子 `next = {nx}`'


CONFIG = dict(
    num=1552, title='两球之间的磁力', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 贪心紧凑放球',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 2517'],
    code='''
class Solution(object):
    def maxDistance(self, position, m):

        position = sorted(position)
        l = 1
        r = position[-1] - position[0]
        n = len(position)
        while l < r:
            mid = (l + r + 1) >> 1
            cnt = 1
            now = 0
            next = 1

            while cnt < m:
                while next < n and position[next] - position[now] < mid:
                    next += 1
                if next == n:
                    break
            
                cnt += 1
                now = next
                next += 1

            if cnt == m:
                l = mid
            else:
                r = mid - 1
        
        return l
''',
    call=f'Solution().maxDistance({POS}, {M})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=25, h=90),
        dict(type='array', var=lambda S: list(range(POS[-1] - POS[0] + 1)) if 'l' in S and 'r' in S else [],
             label='候选最小磁力（绿 = 已确认可行，红 = 已确认不可行）', cell=80, index=False,
             dim=lambda S, i, v: v == 0,
             color=lambda S, i, v: None if v == 0 else ('green' if v <= S['l'] and S['l'] > 1 or (v == 1) else 'red' if v > S['r'] else None),
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, h=200),
        dict(type='array', var='position', label=f'排序后的篮子位置（绿 = 已放球，红 = 跳过；放 m = {M} 个球）', cell=110, h=220,
             color=_pcol, pointers={'now': 'green', 'next': 'orange'}),
    ],
    watch=[('l', 'l', 'blue'), ('mid', 'mid', 'yellow'), ('r', 'r', 'pink'), ('cnt', 'cnt', 'green'), 'now', 'next'],
    captions={
        'position = sorted': '先排序，才能从左到右贪心放球：`{position}`',
        'l = 1': '答案下界 `l = 1`（位置互不相同）',
        'r = position[-1]': '上界 `r = {position[-1]} − {position[0]} = {r}`：两端篮子的距离',
        'while l < r': lambda S, B, rr: (f'区间 `[{S.l}, {S.r}]` 还有多个候选，继续二分' if S.l < S.r else f'`l = r = {S.l}`，二分结束'),
        'mid = (l + r + 1)': '猜最小磁力 `mid = ({l} + {r} + 1) >> 1 = {mid}`：==上取整==，避免 `l = mid` 死循环',
        'cnt = 1': '贪心：第一个球==一定放在最左边==的篮子，`cnt = 1`',
        'while cnt < m': lambda S, B, rr: (f'已放 `{S.cnt}` 个，还要放 `{S.m - S.cnt}` 个' if S.cnt < S.m else f'`{S.m}` 个球都放好了'),
        'while next < n and': _inner,
        'if next == n': lambda S, B, rr: ('没有可放的篮子了 → 放不下 `m` 个球' if S.next == S.n else f'在篮子 `{S.next}` 放球'),
        'cnt += 1': '放下第 `{cnt}` 个球',
        'now = next': '`now = {now}`：上一个球的位置更新为 `{position[now]}`',
        'if cnt == m': lambda S, B, rr: (f'放下了 `{S.m}` 个球 → 最小磁力 `{S.mid}` ==可行==' if S.cnt == S.m else f'只放下 `{S.cnt}` 个 → `{S.mid}` ==不可行=='),
        'l = mid': '可行，答案 `≥ {mid}`：`l = {l}`',
        'r = mid - 1': '不可行，答案 `< {mid}`：`r = {r}`',
        'return l': '最大的最小磁力是 =={ret}==',
    },
    skip=[7, 11, 12, 16, 18, 22],
    max_steps=80,
    cards=dict(
        one_liner='二分最小磁力，从左到右尽量紧凑地放球',
        complexity='时间 `O(n log n + n log U)`，空间 `O(n)`',
        problem=['`n` 个篮子在 `position[i]`，放 `m` 个球，两球磁力为 `|x − y|`',
                 '让任意两球间的==最小磁力最大==，返回这个值',
                 '示例：`position = [1,2,3,4,7], m = 3` → `3`（放在 1、4、7）'],
        quote='当最终答案越大时，安排方案的难度显然是越高的，因此可以二分最终的答案……应该==尽可能将边界上的篮子利用起来==，于是可以从小到大一趟排序，然后从头开始尽可能紧凑地进行安排。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一个球放最左边，之后每次找==最靠前==的、距离 `≥ mid` 的篮子',
              '能放满 `m` 个 → `l = mid`；否则 `r = mid − 1`',
              '因为是 `l = mid`，`mid` 要==上取整== `(l + r + 1) >> 1`'],
        summary=['时间 `O(n log n + n log U)`，空间 `O(n)`',
                 '`l = mid` 的写法必须上取整，否则 `l + 1 == r` 时死循环',
                 '贪心正确性：越早放下一个球，后面剩余空间越大',
                 '原文为 Python 2 风格（已用 `>>`），代码无需改动即可在 Python 3 运行'],
    ),
)
