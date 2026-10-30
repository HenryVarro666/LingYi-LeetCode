Q = [11, 6]
N = 6


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'green'
    return None


def _segs(S):
    if 'mx' in S and S['_line'] in (4, 5, 6, 7):
        m = S['mx']
        return [(q + m - 1) // m for q in Q]
    return []


def _top(S):
    line = S['_line']
    if 'mx' in S and line in (4, 5, 6, 7):
        m = S['mx']
        sg = [(q + m - 1) // m for q in Q]
        return f"每段至多 `{m}`：各根木棍切 `{' + '.join(map(str, sg))}` = `{sum(sg)}` 段，要求 `≤ n = {N}`"
    if 'left' not in S:
        return f'`n = {N}` 间商店：上限 mx 越大越容易分完 → ==二分猜答案=='
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：里面 `{r - l - 1}` 个 mx 还==不知道==行不行'
    return f'`left + 1 == right`：`{l}` 不行，`{r}` 可以 → 答案 =={r}=='


def _ret(S, B, ret):
    if ret:
        return f'`cnt = {S.cnt} ≤ n = {S.n}` → ==可以==，商店够用'
    return f'`cnt = {S.cnt} > n = {S.n}` → ==不行==，商店不够'


CONFIG = dict(
    num=2064, title='分配给商店的最多商品的最小值', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 最小化最大值',
    tags=['灵神题单·二分算法', '难度分 1886'],
    code='''
class Solution:
    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        def check(mx: int) -> bool:
            cnt = 0
            for q in quantities:
                cnt += (q + mx - 1) // mx
            return cnt <= n

        left, right = 0, max(quantities)
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().minimizedMaximum({N}, {Q})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(max(Q) + 1)),
             label='候选上限 mx（红 = 不行，绿 = 可以，灰 = 未知）',
             cell=70, index=False, color=_color, pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, h=240),
        dict(type='array', var='quantities', label='quantities：每种商品（木棍）的数量', cell=100, h=170),
        dict(type='array', var=_segs, label='每种商品至少占的商店数 ceil(q / mx)', cell=100, index=False, h=170),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'cyan'), 'n'],
    captions={
        'cnt = 0': '`cnt` 统计需要的商店总数，从 0 开始',
        'cnt += (q': '`q = {q}`：每间店至多 `{mx}` 件，至少要 `ceil({q}/{mx}) = {(q + mx - 1) // mx}` 间店 → `cnt` = =={cnt}==',
        'return cnt <= n': _ret,
        'left, right = 0': '`left = 0`：上限 0 不可能，==恒为 False==；`right = max = {right}`：每种商品占一间店，`m ≤ n` 一定够，==恒为 True==',
        'while left + 1': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                          else f'`left + 1 == right = {S.right}`：开区间为空，==每个 mx 都有结论=='),
        'mid = (left': '猜一个上限：`mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': '调用 `check({mid})`：每间店至多 `{mid}` 件，够不够分？',
        'right = mid': '`mid` 够用，答案 ==≤ mid==：`right = {right}`，右端点仍==恒为 True==',
        'left = mid': '`mid` 不够用，答案 ==> mid==：`left = {left}`，左端点仍==恒为 False==',
        'return right': '`right` 是==最小的可行上限== → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='把商品看成木棍切成 n 段，最长段越短越苛刻 → 二分猜最长段',
        complexity='时间 `O(m log U)`，空间 `O(1)`，`U = max(quantities)`',
        problem=['`n` 间商店，`quantities[i]` 是第 `i` 种商品的件数',
                 '一间店至多放一种商品，所有商品都要分完，求店里最大件数 `x` 的==最小值==',
                 '示例：`n = 6, [11, 6]` → `3`（11 → 2,3,3,3；6 → 3,3）'],
        quote='把 quantities[i] 视作木棍的长度，你有 m 根木棍，要切分成 n 段（长度可以是 0），让最长的那根木棍尽量短。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最长段不能是 2，就更不能是 1：==苛刻方向单调== → 二分答案',
              '判定：每段至多 `mx`，长 `q` 的木棍要切 `ceil(q/mx)` 段，总段数 `≤ n`？',
              '开区间 `(0, max)`：left 恒 False，right 恒 True，`check` 为真就更新 right'],
        summary=['时间 `O(m log U)`，空间 `O(1)`',
                 '上取整：`ceil(a/b) = (a + b − 1) // b`，不用浮点数',
                 '开区间写法不用想加一减一：`check` 为真更新谁，最后就返回谁',
                 '另有 `bisect_left(range(...), True, key=check)` 的库函数写法'],
    ),
)
