CAND = [4, 7, 5]
K = 4


def _cand(S, i, v):
    if 'r' not in S:
        return None
    if v <= S['l']:
        return 'green'
    if v > S['r']:
        return 'red'
    return None


def _parts(S):
    if 'mid' not in S or 'cnt' not in S or S['_line'] not in (11, 13):
        return []
    m = S['mid']
    upto = len(CAND) if S['_line'] == 13 else CAND.index(S['candy']) + 1
    return [c // m if j < upto else '?' for j, c in enumerate(CAND)]


def _top(S):
    if 'r' not in S:
        return '每人分得越多，能分的份数越少 → ==二分答案=='
    if 'mid' in S and 'cnt' in S and S['_line'] in (10, 11, 13):
        return f"每人 `mid = {S['mid']}` 颗：已分出 `cnt = {S['cnt']}` 份，要满足 `k = {K}` 个小朋友"
    if S['l'] < S['r']:
        return f"答案在 `[{S['l']}, {S['r']}]` 里"
    return f"`l == r = {S['l']}`：就是答案"


def _if(S, B, ret):
    if S.cnt >= S.k:
        return f'`cnt = {S.cnt} ≥ k = {S.k}`：每人 {S.mid} 颗==够分== → 答案 ≥ {S.mid}'
    return f'`cnt = {S.cnt} < k = {S.k}`：每人 {S.mid} 颗==不够分== → 答案 ≤ {S.mid - 1}'


CONFIG = dict(
    num=2226, title='每个小孩最多能分到多少糖果', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 上取中点',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1646'],
    code='''
class Solution(object):
    def maximumCandies(self, candies, k):

        l = 0
        r = max(candies)

        while l < r:
            mid = (l + r + 1) >> 1
            cnt = 0
            for candy in candies:
                cnt += candy // mid
            
            if cnt >= k:
                l = mid
            else:
                r = mid - 1
        
        return l
''',
    call=f'Solution().maximumCandies({CAND}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(max(CAND) + 1)),
             label='候选答案（绿 = 确认够分，红 = 确认不够分，灰 = 未知）', cell=84, index=False, color=_cand,
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, h=240),
        dict(type='array', var='candies', label='candies（黄 = 当前这堆 candy）', cell=110, h=170,
             color=lambda S, i, v: 'yellow' if 'candy' in S and S['_line'] in (10, 11) and S['candies'].index(S['candy']) == i else None),
        dict(type='array', var=_parts, label='每堆能分给几个小朋友：candy // mid', cell=110, index=False, h=170,
             color=lambda S, i, v: 'cyan' if isinstance(v, int) and v else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'green'), 'candy', 'k'],
    skip=['for candy in'],
    captions={
        'l = 0': '下界 `l = 0`：一颗都不分总是可以的',
        'r = max': '上界 `r = max(candies) = {r}`：一堆不能合并，多于最大堆的不可能',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，继续二分' if S.l < S.r else f'`l == r = {S.l}`，结束'),
        'mid = (l + r + 1)': '`mid = ({l} + {r} + 1) >> 1 = {mid}`：==取上中点==，否则 `l = mid` 会死循环',
        'cnt = 0': '每人 {mid} 颗，数一数能分给几个小朋友',
        'cnt += candy': '`{candy}` 颗这堆分出 `{candy} // {mid} = {candy // mid}` 份 → `cnt = {cnt}`',
        'if cnt >= k': _if,
        'l = mid': '`l = {l}`',
        'r = mid - 1': '`r = {r}`',
        'return l': '每个小孩最多分到 =={ret}== 颗',
    },
    cards=dict(
        one_liner='老题型：每人分得越多份数越少，直接二分答案',
        complexity='时间 `O(n log max)`，空间 `O(1)`',
        problem=['`candies[i]` 是一堆糖果，可以拆成子堆但==不能合并==',
                 '分给 `k` 个小孩，每人数量相同且==至多拿一堆==，求每人最多几颗',
                 '示例：`[5,8,6], k = 3` → `5`；本视频 `[4,7,5], k = 4` → `3`'],
        quote='虽然每个小孩分的糖果数变多，==可以分的份数必然是变少的==，反过来也一样，因此满足使用二分的条件。二分的下界自然是0，而上界则是candies中的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['二分范围 `[0, max(candies)]`',
              '每堆能分给 `candy // mid` 个小朋友，累加看是否 `≥ k`',
              '够分就 `l = mid`，不够就 `r = mid - 1`；中点要==向上取=='],
        summary=['时间 `O(n log max)`，空间 `O(1)`',
                 '易错：`l = mid` 的写法中点必须 `(l + r + 1) >> 1`',
                 'mid 至少为 1，不会出现除以 0',
                 '原文为 Python 2 写法，`candy / mid` 已改为 `candy // mid`'],
    ),
)
