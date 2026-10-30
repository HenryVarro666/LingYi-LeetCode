TIME, M = [1, 2, 3, 3], 2


def _day(S, i, v):
    # 按当前 mid 重新模拟，给已完成的题按天交替上色（青 / 紫），正在加入的题为黄
    if 'p' not in S or 'mid' not in S or S['_line'] in (7, 8, 9):
        return None
    p, mid = S['p'], S['mid']
    if i == p and S['_line'] in range(13, 25):
        return 'yellow'
    if i >= p:
        return None
    day, s, ma, q = 0, 0, 0, 0
    days = []
    while q < p:
        ma, s = max(ma, TIME[q]), s + TIME[q]
        if s - ma > mid:
            day, s, ma = day + 1, 0, 0
            continue
        days.append(day)
        q += 1
    return 'cyan' if days[i] % 2 == 0 else 'purple'


def _top(S):
    if 'mid' not in S:
        return '每天做题时间上限 `T` 越大，需要的天数越少 → ==二分 T=='
    s, ma = S.get('s', 0), S.get('ma', 0)
    return (f"上限 `mid = {S['mid']}`：第 `{min(S.get('cnt', 0) + 1, M)}` 天已做总耗时 `s = {s}`，最难一题 `ma = {ma}`，"
            f"求助后耗时 `s − ma = {s - ma}`")


def _cand(S, i, v):
    if 'l' not in S or 'r' not in S:
        return None
    if v < S['l']:
        return 'red'
    if v >= S['r']:
        return 'green'
    return None


def _if(S, B, ret):
    if S.s - S.ma > S.mid:
        return f'`s − ma = {S.s - S.ma} > {S.mid}`：求助最难的也超时 → ==这题留到下一天=='
    return f'`s − ma = {S.s - S.ma} ≤ {S.mid}`：最难的一题求助，今天做得完'


CONFIG = dict(
    num='LCP 12', title='小张刷题计划', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 每天求助最难的题',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def minTime(self, time, m):

        l = 0
        r = sum(time)

        while l < r:
            mid = (l + r) // 2
            p = 0
            ma = 0
            s = 0
            cnt = 0
            while p < len(time):
                ma = max(ma, time[p])
                s += time[p]
                if s - ma > mid:
                    cnt += 1
                    if cnt == m:
                        break
                    ma = 0
                    s = 0
                    continue
                p += 1
            
            if p == len(time):
                r = mid
            else:
                l = mid + 1
        
        return l
''',
    call=f'Solution().minTime({TIME}, {M})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=25, h=100),
        dict(type='array', var=lambda S: list(range(sum(TIME) + 1)), label='候选每日上限 T（红 = 不可行，绿 = 可行）',
             cell=70, index=False, color=_cand, pointers={'l': 'red', 'mid': 'yellow', 'r': 'green'}, h=200),
        dict(type='array', var='time', label=f'time（按顺序做，共 m = {M} 天；青 / 紫 = 各天做完的题，黄 = 正在加入）', cell=110, h=200,
             color=_day,
             pointers={'p': 'blue'}),
    ],
    watch=[('l', 'l', 'red'), ('mid', 'mid', 'yellow'), ('r', 'r', 'green'), ('p', 'p', 'blue'),
           's', 'ma', ('cnt', 'cnt', 'purple')],
    captions={
        'l = 0': '二分每天的做题时间上限：下界 `l = 0`（每天只做一题且求助）',
        'r = sum': '上界 `r = sum(time) = {r}`：一天做完也够',
        'while l < r': lambda S, B, rr: (f'区间 `[{S.l}, {S.r}]` 还有多个候选，继续二分' if S.l < S.r else f'`l = r = {S.l}`，二分结束'),
        'mid = (l + r)': '猜每天上限 `mid = ({l} + {r}) // 2 = {mid}`，模拟一遍看要几天',
        'p = 0': '模拟：`p` 指向下一道要做的题，`s`/`ma`/`cnt` 清零',
        'cnt = 0': '`cnt`：已经做满的天数',
        'while p < len(time)': lambda S, B, rr: (f'还有题没做：第 `{S.p}` 题' if S.p < len(S.time) else '所有题都做完了'),
        'ma = max(': '当天最难的一题 `ma = {ma}`（留给场外求助）',
        's += time[p]': '当天总耗时 `s = {s}`',
        'if s - ma > mid': lambda S, B, r: f'加入第 `{S.p}` 题：`s = {S.s}`，最难 `ma = {S.ma}`；' + _if(S, B, r),
        'cnt += 1': '今天结束：`cnt = {cnt}` 天',
        'if cnt == m': lambda S, B, rr: (f'`cnt = {S.cnt} = m`：天数用完了，还有题没做 → ==不可行==' if S.cnt == S.m else f'`cnt = {S.cnt} < m = {S.m}`，开始新的一天'),
        'break': '提前结束模拟',
        20: '新的一天：`ma`、`s` 清零，==从第 {p} 题重新开始==',
        'p += 1': '第 `{B.p}` 题今天做完，`p` → {p}',
        'if p == len(time)': lambda S, B, rr: (f'`{S.m}` 天内做完了全部题 → 上限 `{S.mid}` ==可行==' if S.p == len(S.time) else f'没做完 → 上限 `{S.mid}` ==不可行=='),
        'r = mid': '可行，还可能更小：`r = {r}`',
        'l = mid + 1': '不可行，必须更大：`l = {l}`',
        'return l': '每天最少需要 =={ret}== 的时间',
    },
    skip=[10, 11, 12, 13, 14, 15, 21, 22],
    max_steps=80,
    cards=dict(
        one_liner='二分每天的做题时间，每天把场外求助留给当天最难的题',
        complexity='时间 `O(n log S)`，空间 `O(1)`，`S = sum(time)`',
        problem=['`time[i]` 是第 `i` 题的耗时，必须==按顺序==做，要在 `m` 天内做完',
                 '每天可以用一次「场外求助」，直接解决一道题（不耗时）',
                 '求每天做题时间 `T` 的最小值；示例：`time = [1,2,3,3], m = 2` → `3`'],
        quote='T越大，每天能刷的题只会多不会少……最直观的想法就是==将求助机会留给当天做的题中最难的那个==，这样节省的时间就会更多。',
        quote_src='—— yiduobo 题解原文',
        idea=['二分上限 `mid`，贪心模拟：当天不断加题，记总耗时 `s` 和最难 `ma`',
              '`s − ma > mid`：求助最难的也超了，这题留给下一天（`p` 不动）',
              '`m` 天内做完 → `r = mid`，否则 `l = mid + 1`'],
        summary=['时间 `O(n log S)`，空间 `O(1)`',
                 '超限时不要 `p += 1`：当前题要放到下一天重新计算',
                 '每天的最难题一直在变，所以要实时维护 `ma`',
                 '原文为 Python 2 写法，整数除法 `(l + r) / 2` 已改为 `//`'],
    ),
)
