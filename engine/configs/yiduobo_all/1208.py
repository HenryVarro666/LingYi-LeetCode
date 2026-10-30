S_, T_ = 'abcdef', 'bdcfff'
MAXC = 4


def _right(S):
    return S['r'] - 1 if 'r' in S else None


def _top(S):
    if 'cost_list' not in S or 'now' not in S:
        return f'预算 `maxCost = {MAXC}`：找代价和 ≤ 预算的==最长连续段=='
    l, r, c = S['l'], S['r'], S['cost_list']
    seg = ' + '.join(map(str, c[l:r])) or '空'
    ok = S['now'] <= MAXC
    return f"窗口 `[{l}, {r})`：`{seg} = {S['now']}` {'≤' if ok else '>'} `{MAXC}` → {'==合法==' if ok else '超预算，l 右移'}"


def _init_while(S, B, ret):
    r, n = S.r, S.n
    if r >= n:
        return '整个数组都放得下'
    c = S.cost_list[r]
    if c + S.now <= S.maxCost:
        return f'`cost_list[{r}] + now = {c} + {S.now} = {c + S.now} ≤ {S.maxCost}`：还放得下 → r 后移'
    return f'`{c} + {S.now} = {c + S.now} > {S.maxCost}`：放不下了，==从 0 开始最远到 r = {r}=='


def _shrink(S, B, ret):
    if S.now > S.maxCost and S.l < S.r:
        return f'`now = {S.now} > {S.maxCost}`：超预算 → 把 `cost_list[{S.l}]` 移出窗口'
    return f'`now = {S.now} ≤ {S.maxCost}`：窗口合法，l 不用再动'


CONFIG = dict(
    num=1208, title='尽可能使字符串相等', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='代价数组 + 变长滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def equalSubstring(self, s, t, maxCost):

        n = len(s)
        cost_list = [abs(ord(s[index]) - ord(t[index])) for index in range(n)]
        l = 0
        r = 0
        now = 0
        while r < n and cost_list[r] + now <= maxCost:
            now += cost_list[r]
            r += 1

        res = r - l
        while r < n:
            now += cost_list[r]
            r += 1
            while l < r and now > maxCost:
                now -= cost_list[l]
                l += 1
            res = max(res, r - l)

        return res
''',
    call=f'Solution().equalSubstring({S_!r}, {T_!r}, {MAXC})',
    expect=4,
    views=[
        dict(type='string', var='s', label='s', cell=96, h=140),
        dict(type='string', var='t', label='t', cell=96, h=175),
        dict(type='array', var=lambda S: S.get('cost_list') or [], label='cost_list（框 = 窗口 [l, r)，r 指向下一个要加入的位置）',
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', _right), cell=96, h=230),
        dict(type='text', fn=_top, size=28, h=80),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len(s)': '`n = {n}`',
        'cost_list = [': '先扫一趟：每个位置的变换代价 `|s[i] − t[i]|` = `{cost_list}`',
        'l = 0': '答案起点先设为 `l = 0`',
        'r = 0': '`r`：窗口右端（开区间）',
        'now = 0': '`now`：窗口内代价之和',
        'while r < n and': _init_while,
        'now += cost_list[r]': lambda S, B, ret: f'加入 `cost_list[{B.r}] = {S.cost_list[B.r]}`：`now = {S.now}`',
        'r += 1': '`r` → {r}',
        'res = r - l': '从 0 开始最长 `{res}` 个，作为初始答案',
        'while r < n:': lambda S, B, ret: (f'`r = {S.r} < n`：尝试把 r 再后移一位' if S.r < S.n else 'r 到头了，结束'),
        'while l < r and': _shrink,
        'now -= cost_list[l]': '`now = {B.now} − {cost_list[l]} = {now}`',
        'l += 1': '`l` → {l}',
        'res = max': '窗口长 `{r} − {l} = {r - l}`：`res = max({B.res}, {r - l})` = =={res}==',
        'return res': '最长可以转化 =={ret}== 个字符',
    },
    cards=dict(
        one_liner='先算出每个位置的代价，再找和不超过预算的最长连续段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['等长字符串 `s`、`t`，把 `s[i]` 改成 `t[i]` 的代价是 `|s[i] − t[i]|`（ASCII 差）',
                 '总代价不超过 `maxCost`，求能改成和 t 相同的==最长子串==长度',
                 '示例：`"abcd", "bcdf", 3` → `3`；本视频 `"abcdef", "bdcfff", 4` → `4`'],
        quote='我们就得到了一个代价数组，而目标则是从中间选择出==尽可能长的连续的一段==，而这一段数组中各个数字之和必须小于等于最大预算。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一步：`cost_list[i] = |ord(s[i]) − ord(t[i])|`',
              '先从 `l = 0` 向后扫，找到最大的 r 作为初始答案',
              '之后每轮 r 后移一位，超预算就把 l 往右推'],
        summary=['时间 `O(n)`：l、r 都只往右走；空间 `O(n)` 存代价数组',
                 '`r` 是开区间右端，窗口长度是 `r − l`',
                 '缩窗条件 `now > maxCost`，等于预算仍然合法',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动'],
    ),
)
