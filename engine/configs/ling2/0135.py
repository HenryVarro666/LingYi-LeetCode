RATINGS = [1, 2, 3, 4, 2, 1, 4, 5, 2]

CODE = '''
class Solution:
    def candy(self, ratings: List[int]) -> int:
        ans = n = len(ratings)  # 先给每人分一个
        i = 0
        while i < n:
            start = i - 1 if i > 0 and ratings[i - 1] < ratings[i] else i

            # 找严格递增段
            while i + 1 < n and ratings[i] < ratings[i + 1]:
                i += 1
            top = i  # 峰顶

            # 找严格递减段
            while i + 1 < n and ratings[i] > ratings[i + 1]:
                i += 1

            inc = top - start  # start 到 top 严格递增
            dec = i - top      # top 到 i 严格递减
            ans += (inc * (inc - 1) + dec * (dec - 1)) // 2 + max(inc, dec)
            i += 1
        return ans
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(s, k=0):
    return [i + 1 for i, t in enumerate(_LINES) if s in t][k]


L_UP_I, L_DOWN_I, L_OUT_I = _ln('i += 1', 0), _ln('i += 1', 1), _ln('i += 1', 2)
L_START, L_TOP, L_ANS = _ln('start = '), _ln('top = i'), _ln('ans += (')
L_OUTER, L_RET = _ln('while i < n'), _ln('return ans')


def _extras(r):
    """按灵神的分组规则，算出每个孩子在分组循环里分到的糖果（不含先给的 1 颗）"""
    n, out, i = len(r), [0] * len(r), 0
    while i < n:
        start = i - 1 if i > 0 and r[i - 1] < r[i] else i
        while i + 1 < n and r[i] < r[i + 1]:
            i += 1
        top = i
        while i + 1 < n and r[i] > r[i + 1]:
            i += 1
        inc, dec = top - start, i - top
        for k in range(start, top):
            out[k] = k - start
        for k in range(top + 1, i + 1):
            out[k] = i - k
        out[top] = max(inc, dec)
        i += 1
    return out


EXTRA = _extras(RATINGS)
TOP_EXPR = 'top if _line >= %d and _line not in (%d, %d) else None' % (L_TOP, L_OUT_I, L_OUTER)


def _done(S):
    line = S.get('_line')
    if 'start' not in S:
        return -1
    if line == L_RET:
        return len(RATINGS) - 1
    if line == L_ANS:
        return S['i']
    if line in (L_OUT_I, L_OUTER, L_START):
        return S['i'] - 1
    st = S['start']
    shared = st > 0 and RATINGS[st - 1] > RATINGS[st]
    return st if shared else st - 1


def _bar_color(S, i, v):
    if 'start' not in S:
        return None
    line = S.get('_line')
    if line in (L_OUT_I, L_OUTER):
        return 'green' if i <= S['i'] - 1 else None
    st, cur = S['start'], S['i']
    top = S['top'] if ('top' in S and line >= L_TOP) else None
    if top is None:
        if st <= i <= cur:
            return 'blue'
        return 'green' if i < st else None
    if i == top:
        return 'orange'
    if st <= i < top:
        return 'blue'
    if top < i <= cur:
        return 'pink'
    return 'green' if i < st else None


def _formula(S):
    line = S.get('_line')
    if line == L_ANS:
        inc, dec = S['inc'], S['dec']
        a, b = inc * (inc - 1) // 2, dec * (dec - 1) // 2
        return f"递增段 `{a}` + 递减段 `{b}` + 峰顶 `max({inc},{dec}) = {max(inc, dec)}` → `ans` = =={S['ans']}=="
    if 'start' in S and line not in (L_OUT_I, L_OUTER):
        return '蓝 = 严格递增段，橙 = 峰顶，粉 = 严格递减段（绿 = 已结算的组）'
    if 'ans' in S:
        return f"先给每人 1 颗：`ans` 从 `n = {len(RATINGS)}` 开始，下面每个孩子最少可以分 0 颗"
    return ''


def _up(S, B, ret):
    i = B.i
    if i + 1 < B.n and B.ratings[i] < B.ratings[i + 1]:
        return f'`{B.ratings[i]} < {B.ratings[i + 1]}`：还在上坡 → `i` 右移'
    if i + 1 >= B.n:
        return '到数组末尾了，上坡结束'
    return f'`{B.ratings[i]} ≥ {B.ratings[i + 1]}`：上坡结束，`i = {i}` 就是峰顶'


def _down(S, B, ret):
    i = B.i
    if i + 1 < B.n and B.ratings[i] > B.ratings[i + 1]:
        return f'`{B.ratings[i]} > {B.ratings[i + 1]}`：还在下坡 → `i` 右移'
    if i + 1 >= B.n:
        return f'到数组末尾了，下坡结束于 `i = {i}`'
    return f'`{B.ratings[i]} ≤ {B.ratings[i + 1]}`：下坡结束于 `i = {i}`'


def _start(S, B, ret):
    i = S.i
    if S.start == i - 1:
        return f'`ratings[{i - 1}] = {S.ratings[i - 1]} < ratings[{i}]`：`{i - 1}` 是谷底，==被两组共享== → `start = {S.start}`'
    return f'新的一组从 `start = {S.start}` 开始'


CONFIG = dict(
    num=135, title='分发糖果', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='分组循环 · 一座山一座山地算',
    tags=['字节30天', '热题173', '面试经典150'],
    code=CODE,
    call=f'Solution().candy({RATINGS})',
    expect=19,
    skip=[L_UP_I, L_DOWN_I, 'i = 0'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='bars', var='ratings', label='ratings（每个孩子的评分）', h=330, vmax=5,
             pointers={'start': 'cyan', TOP_EXPR: 'orange', 'i': 'blue'}, pointer_labels={TOP_EXPR: 'top'}, color=_bar_color),
        dict(type='array', var=lambda S: [EXTRA[k] if k <= _done(S) else None for k in range(len(RATINGS))],
             label='已结算的组里，每人额外分到的糖果（不含先给的 1 颗）', cell=88, h=150),
    ],
    watch=[('start', 'start', 'cyan'), ('top', 'top', 'orange'), ('i', 'i', 'blue'), 'inc', 'dec', ('ans', 'ans', 'green')],
    captions={
        'ans = n = len': '==先给每人分一个==：`ans = n = {n}`，之后每人最少分 0 颗就行',
        'while i < n': lambda S, B, r: (f'`i = {B.i} < n`：开始找下一座「山」' if B.i < B.n else f'`i = {B.i} = n`：所有组都处理完了'),
        'start = ': _start,
        'while i + 1 < n and ratings[i] < ratings[i + 1]': _up,
        'top = i': '峰顶 `top = {top}`（评分 {ratings[top]}）',
        'while i + 1 < n and ratings[i] > ratings[i + 1]': _down,
        'inc = top - start': '`inc = top - start = {inc}`：递增段分 `0, 1, …, inc-1` 颗',
        'dec = i - top': '`dec = i - top = {dec}`：递减段从右往左分 `0, 1, …, dec-1` 颗',
        'ans += (': '等差数列求和 + 峰顶 `max(inc, dec)`：`ans` 加上 `{ans - B.ans}` → =={ans}==',
        L_OUT_I: '`i` 加一，找下一组',
        'return ans': '一共需要 =={ret}== 颗糖果',
    },
    cards=dict(
        one_liner='先给每人一颗，再把数组拆成「上坡 + 峰顶 + 下坡」的山，逐座求和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 个孩子站成一排，`ratings[i]` 是评分',
                 '每人==至少 1 颗==糖果；相邻两人中评分==更高==的糖果更多',
                 '求最少需要多少颗糖果',
                 '示例：`[1,0,2]` → `5`；`[1,2,2]` → `4`',
                 '本视频（题解里的例子）：`[1,2,3,4,2,1,4,5,2]` → `19`'],
        quote='我们==先给每个孩子 1 颗糖果==，下面就不用考虑这个要求了，可以给孩子最少 0 颗糖果。……把严格递增段 + 峰顶 + 严格递减段叫做一座山。',
        quote_src='—— 灵茶山艾府题解：分组循环，把困难题变成简单题',
        idea=['递增段从左往右分 `0,1,2,…`；递减段从右往左分 `0,1,2,…`',
              '峰顶要比两边都多：分 `max(inc, dec)` 颗',
              '分组循环：外层记 start、更新答案，内层找这组到哪结束'],
        summary=['时间 `O(n)`：`i` 只增不减，二重循环一共只走 n 步',
                 '==谷底被两组共享==：`ratings[i-1] < ratings[i]` 时 `start = i - 1`',
                 '谷底在两组里都分到 0 颗，所以不会重复统计',
                 '相邻评分相等时自然断开成两组，如 `[1,2,2,3]` 分 `0,1,0,1`',
                 '分组循环不需要特判最后一组，是最不容易出 bug 的写法'],
    ),
)
