PILES = [5, 8, 3, 9]
H = 6


def _top(S):
    if 'l' not in S:
        return f'`H = {H}`：K 越大，吃完所需时间==单调不增== → 二分 K'
    l, r = S['l'], S['r']
    if 'mid' in S and S['_line'] in (8, 10, 11, 12, 13, 14, 16):
        return f"试速度 `mid = {S['mid']}`：已累计 `cnt = {S['cnt']}` 小时（上限 `H = {H}`）"
    if l < r:
        return f'答案在闭区间 `[{l}, {r}]` 里'
    return f'`l == r = {l}`：区间只剩一个数，就是答案'


def _while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：区间里不止一个候选，继续二分'
    return f'`l == r = {S.l}`：区间缩成一个点，结束'


def _mod(S, B, ret):
    p, m = S.pile, S.mid
    if p % m != 0:
        return f'`{p} % {m} = {p % m} ≠ 0`：剩下的 {p % m} 根还要==再吃一小时=='
    return f'`{p} % {m} = 0`：正好吃完，不用多一小时'


def _cmp(S, B, ret):
    if S.cnt > S.H:
        return f'`cnt = {S.cnt} > H = {S.H}`：速度 {S.mid} 太慢 → 答案在 `mid` 右边'
    return f'`cnt = {S.cnt} ≤ H = {S.H}`：速度 {S.mid} 够用 → 答案 ==≤ mid=='


CONFIG = dict(
    num=875, title='爱吃香蕉的珂珂', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分 K · 逐堆累计小时',
    tags=['labuladong', '灵神题单·二分算法', '难度分 1766'],
    code='''
class Solution(object):
    def minEatingSpeed(self, piles, H):

        l = 1
        r = max(piles)
        while l < r:
            cnt = 0
            mid = (l + r) >> 1
            for pile in piles:
                cnt += pile // mid
                if pile % mid != 0:
                    cnt += 1
            if cnt > H:
                l = mid + 1
            else:
                r = mid
        
        return l
''',
    call=f'Solution().minEatingSpeed({PILES}, {H})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(max(PILES) + 1)), dim=lambda S, i, v: i == 0,
             label='候选速度 K（0 不可能；红 = 已排除的太慢速度，绿 = 已知够用但不是最小）',
             cell=80, index=False, color=lambda S, i, v: ('red' if 'l' in S and v < S['l'] else
                                                         'green' if 'l' in S and v > S['r'] else None),
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'},
             h=240),
        dict(type='array', var='piles', label='piles（黄 = 正在算的这一堆）', cell=100, h=180,
             color=lambda S, i, v: 'yellow' if 'pile' in S and S['_line'] in (10, 11, 12)
             and v == S['pile'] else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), 'pile', ('cnt', 'cnt', 'orange'), 'H'],
    captions={
        'l = 1': '下界 `l = 1`：至少每小时吃一根',
        'r = max': '上界 `r = max(piles) = {r}`：比它更大的 K ==没有意义==',
        'while l < r': _while,
        'cnt = 0': '`cnt`：以速度 mid 吃完需要的小时数',
        'mid = (l + r)': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'cnt += pile // mid': '整小时：`{pile} // {mid} = {pile // mid}` → `cnt = {cnt}`',
        'if pile % mid': _mod,
        'cnt += 1': '`cnt` → {cnt}',
        'if cnt > H': _cmp,
        'l = mid + 1': '`l = mid + 1 = {l}`：mid 本身也不行，排除',
        'r = mid': '`r = mid = {r}`：mid 可能就是答案，保留',
        'return l': '返回 `l` = =={ret}==：最小的够用速度',
    },
    skip=['for pile in', 'cnt = 0'],
    cards=dict(
        one_liner='K 越大越快吃完：二分 K，每次逐堆算要几小时',
        complexity='时间 `O(n log max)`，空间 `O(1)`',
        problem=['`n` 堆香蕉，第 `i` 堆 `piles[i]` 根，`H` 小时后警卫回来',
                 '每小时选一堆吃 `K` 根，不足 K 根就吃完这一堆',
                 '求 H 小时内吃完的最小 `K`；示例 `[3,6,7,11], H = 8` → `4`',
                 '本视频：`[5,8,3,9], H = 6` → `5`'],
        quote='K的增大，吃完所有香蕉所需的时间必然是单调递减的，因此在这里可以二分K……下界自然是1，而上界则是max(piles)，因此==更大的K相比max(piles)是没有意义的==。',
        quote_src='—— yiduobo 题解原文',
        idea=['二分区间 `[1, max(piles)]`，每轮取 `mid`',
              '一堆要 `pile // mid` 小时，==有余数再加 1==',
              '`cnt > H` 说明太慢：`l = mid + 1`；否则 `r = mid`'],
        summary=['时间 `O(n log max(piles))`，空间 `O(1)`',
                 '`l < r` + `r = mid` / `l = mid + 1`：最后 l 就是最小可行速度',
                 '上取整也可写成 `(pile + mid − 1) // mid`',
                 '原文为 Python 2 写法，`pile / mid` 已改为 `pile // mid`'],
    ),
)
