W = [2, 1, 3, 2]
D = 2


def _inner(S):
    return S.get('_line') in range(18, 37)


def _wcolor(S, i, v):
    if 'now' not in S or 'w' not in S:
        return None
    if i <= S['now']:
        return 'green'
    return None


def _scolor(S, i, v):
    if 'offset' not in S or 'w' not in S:
        return None
    if i <= S['now']:
        return None
    if v - S['offset'] <= S['w']:
        return 'cyan'
    return None


def _cand(S, i, v):
    if 'min_w' not in S:
        return None
    if v < S['min_w']:
        return 'red'
    if 'max_w' in S and v > S['max_w']:
        return 'green'
    return None


def _top(S):
    if 'min_w' not in S:
        return f'前缀和 `s`：`s[i] − offset` 就是这一船从上次停下处装到 i 的总重'
    if 'w' not in S or S['_line'] in (11, 46):
        return f"运力答案在 `[{S['min_w']}, {S.get('max_w', '?')}]` 里"
    w, off = S['w'], S.get('offset', 0)
    return f"运力 `w = {w}`：第 `{S.get('step', 0)}` 船，已运到下标 `{S['now']}`，`offset = {off}`，找最大 pos 使 `s[pos] − {off} ≤ {w}`"


def _fast(S, B, ret):
    r = S.r if S.r is not None else len(S.weights) - 1
    rem = S.s[len(S.weights) - 1] - S.offset
    if S.w >= rem:
        return f'剩下的总重 `{rem} ≤ w = {S.w}`：==这一船全部装完=='
    return f'剩下的总重 `{rem} > w = {S.w}`：一船装不完，二分找这一船最远装到哪'


def _bin(S, B, ret):
    v = S.s[S.mid] - S.offset
    if S.w >= v:
        return f'装到下标 {S.mid} 共 `{S.s[S.mid]} − {S.offset} = {v} ≤ {S.w}`：装得下 → `next = {S.mid}`，`l = {S.mid + 1}` 往右找'
    return f'装到下标 {S.mid} 共 `{S.s[S.mid]} − {S.offset} = {v} > {S.w}`：超重 → `r = {S.mid - 1}` 往左找'


def _judge(S, B, ret):
    n = len(S.weights)
    if S.now < n - 1:
        return f'有包裹一船都装不下：运力 `{S.w}` ==不可行== → `min_w = w + 1`'
    if S.step > S.D:
        return f'要 `{S.step}` 天 > `D = {S.D}`：运力 `{S.w}` 太小 → `min_w = w + 1`'
    return f'只要 `{S.step}` 天 ≤ `D = {S.D}`：运力 `{S.w}` 可行 → `max_w = w`'


CONFIG = dict(
    num=1011, title='在 D 天内送达包裹的能力', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分运力 + 前缀和上再二分',
    tags=['labuladong', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def shipWithinDays(self, weights, D):

        s = [weights[0]]
        for num in weights[1:]:
            s.append(s[-1] + num)
        
        min_w = s[0]
        max_w = s[-1]
        while min_w < max_w:
            w = (max_w + min_w) >> 1
            now = -1
            step = 0
            offset = 0
            while now < len(weights):
                step += 1
                l = now + 1
                r = len(weights) - 1
                next = None
                if w >= s[r] - offset:
                    now = r
                    break
                while l <= r:
                    mid = (l + r) >> 1
                    if w >= s[mid] - offset:
                        next = mid
                        l = mid + 1
                    else:
                        r = mid - 1
                
                if next is None:
                    break

                now = next
                offset = s[now]

                
            
            if now < len(weights) - 1 or step > D:
                min_w = w + 1
            else:
                max_w = w
            
        return min_w
''',
    call=f'Solution().shipWithinDays({W}, {D})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=25, h=80),
        dict(type='array', var=lambda S: list(range(sum(W) + 1)), label='候选运力（红 = 已排除，绿 = 可行但不是最小）',
             cell=64, index=False, dim=lambda S, i, v: i == 0, color=_cand,
             pointers={'min_w': 'blue', 'w': 'yellow', 'max_w': 'pink'}, h=200),
        dict(type='array', var='weights', label='weights（绿 = 已经运走）', color=_wcolor,
             pointers={'now': 'green'}, cell=90, h=180),
        dict(type='array', var=lambda S: S.get('s', []), label='前缀和 s（青 = 这一船能装到的位置）', color=_scolor,
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, cell=90, h=260),
    ],
    watch=[('w', 'w', 'yellow'), ('step', 'step', 'purple'), 'offset', ('next', lambda S: None if callable(S.get('next')) else S.get('next'), 'cyan'), 'D'],
    captions={
        's = [weights[0]]': '先求前缀和：`s[i]` = 前 i+1 个包裹的总重',
        'for num in': lambda S, B, r: ('前缀和求完' if B.get('num') == S.get('num') and 'num' in B else f'`num = {S.num}`'),
        's.append': '`s = {s}`',
        'min_w = s[0]': '运力下界 `min_w = s[0] = {min_w}`',
        'max_w = s[-1]': '运力上界 `max_w = {max_w}`：所有包裹一天运完',
        'while min_w < max_w': lambda S, B, r: (f'`[{S.min_w}, {S.max_w}]` 里不止一个候选，继续二分'
                                                if S.min_w < S.max_w else f'`min_w == max_w = {S.min_w}`，二分结束'),
        'w = (max_w': '试运力 `w = ({max_w} + {min_w}) >> 1 = {w}`；`now = -1`、`step = 0`、`offset = 0` 从头模拟',
        'now = -1': '`now`：已运到的最后一个下标，还没运为 -1',
        'step = 0': '`step`：用了几天',
        'offset = 0': '`offset = s[now]`：已运走的总重',
        'while now < len': '还有包裹没运，开一船',
        'step += 1': '第 `{step}` 天',
        'l = now + 1': '在 `s[{l}..{len(weights) - 1}]` 里二分这一船的终点',
        'r = len(weights) - 1': '`r = {r}`',
        'next = None': '`next`：这一船能装到的最远下标',
        'if w >= s[r] - offset': _fast,
        'now = r': '`now = {now}`：全部运完',
        'break': '结束这一轮模拟',
        'while l <= r': lambda S, B, r: ('`l ≤ r`，继续二分' if S.l <= S.r else f'二分结束，`next = {S.next}`'),
        'mid = (l + r)': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'if w >= s[mid] - offset': _bin,
        'next = mid': '`next = {next}`',
        'l = mid + 1': '`l` → {l}',
        'r = mid - 1': '`r` → {r}',
        'if next is None': lambda S, B, r: ('`next` 为空：下一个包裹单独都超重' if S.next is None
                                           else f'这一船最远装到下标 `{S.next}`'),
        'now = next': '`now = {now}`：这一船运走到下标 {now}',
        'offset = s[now]': '`offset = s[{now}] = {offset}`',
        'if now < len(weights) - 1 or step > D': _judge,
        'min_w = w + 1': '`min_w` → {min_w}',
        'max_w = w': '`max_w` → {max_w}',
        'return min_w': '最小运力 =={ret}==',
    },
    skip=['for num in', 'now = -1', 'step = 0', 'offset = 0', 'r = len(weights) - 1', 'next = None',
          'next = mid', 'l = mid + 1', 'r = mid - 1', 'min_w = w + 1', 'max_w = w'],
    max_steps=80,
    cards=dict(
        one_liner='运力越大天数越少：二分运力，每一船在前缀和上二分找最远能装到哪',
        complexity='时间 `O(D log n · log S)`，空间 `O(n)`',
        problem=['传送带上的包裹 `weights[i]` 必须==按顺序==装船，每天运一船',
                 '每船总重不能超过运力；求 `D` 天内运完的==最低运力==',
                 '示例：`[1,2,3,4,5,6,7,8,9,10], D = 5` → `15`',
                 '本视频：`[1,2,3,1,1], D = 4` → `3`'],
        quote='每一批次都尽可能地上船……区间和问题的经典处理方法是前缀和，而前缀和是单调递增的，也就是说==我们在这里又可以在前缀和数组prefix中二分==。',
        quote_src='—— yiduobo 题解原文',
        idea=['运力 `w` 越大，天数单调不增 → 二分 `w`',
              '贪心：每船尽量多装；装到 pos 的重量是 `s[pos] − s[now]`',
              '前缀和递增 → 用二分找满足 `≤ w` 的最大 pos，每船 `O(log n)`'],
        summary=['外层二分 `log S` 次，每次最多 D 船、每船 `O(log n)`',
                 '`next is None`：下一个包裹单独就超重，运力不可行',
                 '下界取 `s[0]` 也对，不可行的运力会被 `now < n − 1` 排除',
                 '更常见写法：下界 `max(weights)`，线性扫描数天数',
                 '原文为 Python 2 风格，代码无需修改'],
    ),
)
