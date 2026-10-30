BD = [1, 10, 3, 10, 2]
M, K = 3, 1


def _col(S, i, v):
    if 'mid' not in S:
        return None
    return 'green' if v <= S['mid'] else None


def _top(S):
    if 'mid' not in S:
        return f'要 `{M}` 束花，每束 `{K}` 朵相邻的花；开花天数越晚，能做的越多 → ==二分天数=='
    mid = S['mid']
    bl = ''.join('●' if v <= mid else '○' for v in BD)
    return f'第 `{mid}` 天开花情况 `{bl}`（● 已开），已做 `{S.get("deal", 0)}` 束 / 需要 `{M}` 束'


def _while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：答案还在 `[{S.l}, {S.r}]` 内 → 继续二分'
    return f'`l = r = {S.l}`：区间收缩到一个点 → 它就是最少天数'


def _chk(S, B, ret):
    if S.deal >= M:
        return f'`deal = {S.deal} >= {M}`：第 `{S.mid}` 天够做 → 答案 ==<= {S.mid}==，`r = mid`'
    return f'`deal = {S.deal} < {M}`：第 `{S.mid}` 天不够 → 答案 ==> {S.mid}==，`l = mid + 1`'


CONFIG = dict(
    num=1482, title='制作 m 束花所需的最少天数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 扫描统计连续盛开',
    tags=['灵神题单·二分算法'],
    code='''
class Solution(object):
    def minDays(self, bloomDay, m, k):

        if m * k > len(bloomDay):
            return -1
        
        l = None
        r = None
        for day in bloomDay:
            if l is None or day < l:
                l = day
            if r is None or day > r:
                r = day
        
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            deal = 0
            for day in bloomDay:
                if day <= mid:
                    cnt += 1
                    if cnt == k:
                        deal += 1
                        cnt = 0
                else:
                    cnt = 0
            
            if deal >= m:
                r = mid
            else:
                l = mid + 1
        
        return l
''',
    call=f'Solution().minDays({BD}, {M}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='array', var='bloomDay', label='bloomDay（绿 = 到第 mid 天已经开花）', cell=110, color=_col, h=300),
        dict(type='text', fn=lambda S: f"连续盛开计数 `cnt = {S['cnt']}`，满 `k = {K}` 朵就成一束，`deal = {S['deal']}`" if 'cnt' in S else '', size=26, h=80),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), 'cnt', ('deal', 'deal', 'green')],
    captions={
        'if m * k > len': '总共要 `m * k = {m * k}` 朵，花只有 `{len(bloomDay)}` 朵：不够就直接 `-1`',
        'l = None': '`l` 用来记最早开花的天数',
        'r = None': '`r` 用来记最晚开花的天数',
        'if l is None or day < l': '`day = {day}` 对比当前最小值 `{l}`：{"更小（或还没有最小值）→ 更新" if l is None or day < l else "不更小，跳过"}',
        'if r is None or day > r': '`day = {day}` 对比当前最大值 `{r}`：{"更大（或还没有最大值）→ 更新" if r is None or day > r else "不更大，跳过"}',
        'while l < r': _while,
        'mid = (l + r) >> 1': '猜一个天数：`mid = ({l} + {r}) >> 1 = {mid}`，数它能做几束',
        17: '`cnt` 记当前连续盛开的花数，从 0 开始数',
        24: '这一束已凑好，`cnt` 清零，下一束重新数',
        26: '这朵没开 → 连续被打断，`cnt` 清零（必须相邻）',
        'deal = 0': '`deal` 记第 `{mid}` 天一共能做几束',
        'if day <= mid': '`day = {day}` {"<=" if day <= mid else ">"} `mid = {mid}`：{"这朵花已开" if day <= mid else "这朵还没开"}',
        'cnt += 1': '连续盛开的花 `cnt = {cnt}`',
        'if cnt == k': '`cnt = {cnt}`，{"凑够 k 朵" if cnt == k else "还不够 k 朵"}',
        'deal += 1': '凑成一束：`deal = {deal}`',
        'if deal >= m': _chk,
        'r = mid': '`r = {r}`：`mid` 天够用，上界缩到 mid',
        'l = mid + 1': '`l = {l}`：`mid` 天不够，下界抬到 mid + 1',
        'return l': '二分结束，最少天数 =={ret}==',
    },
    cards=dict(
        one_liner='天数越多开的花越多：二分天数，扫一遍数连续花束',
        complexity='时间 `O(n log(max−min))`，空间 `O(1)`',
        problem=['`bloomDay[i]` 是第 `i` 朵花开放的天数，要做 `m` 束花，每束用 `k` 朵==相邻==的花',
                 '求最少等几天，做不出来返回 `-1`',
                 f'本视频：`bloomDay = {BD}, m = {M}, k = {K}` → `3`'],
        quote='由于时间越晚开的花就越多，因此在这里是符合二分的要求的。那么此时只需要二分答案，然后对于当前二分的日期mid，每次都进行一趟扫描……',
        quote_src='—— yiduobo 题解原文',
        idea=['先判 `m*k` 超过花的总数就直接 `-1`',
              '`l`、`r` 取最早、最晚的开花日；对 `mid` 扫一遍，连续 `k` 朵开了就成一束',
              '遇到没开的花要把 `cnt` 清零，因为必须相邻'],
        summary=['时间 `O(n log(max−min))`，空间 `O(1)`',
                 '`cnt` 凑够 `k` 后也要清零，下一束重新数',
                 '没开的花要打断连续，别忘了 `else: cnt = 0`',
                 '原文还提到“离散化 + 线段树”做法 `O(m log m)`，作者认为二分更简单',
                 '`m*k` 超过总数时先返回 `-1`，否则二分一定有解'],
    ),
)
