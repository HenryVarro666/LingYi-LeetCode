C = [1, 2, 3, 3, 5, 7, 9]
N = len(C)


def _cand(S, i, v):
    if 'left' not in S or 'right' not in S:
        return None
    if v < S['left']:
        return 'green'
    if v > S['right']:
        return 'red'
    return None


def _paper(S, i, v):
    if 'mid' not in S or S['_line'] not in (11, 12, 13, 14, 16):
        return None
    m = S['mid']
    if i == N - m:
        return 'yellow'
    if i > N - m:
        return 'cyan'
    return None


def _top(S):
    if 'right' not in S:
        return '二分 h：验证==从大到小第 h 篇==的引用次数是否 ≥ h'
    l, r = S['left'], S['right']
    if 'mid' in S and S['_line'] in (11, 12):
        m = S['mid']
        return f"从大到小第 `{m}` 篇 = 下标 `n − mid = {N} − {m} = {N - m}`，引用 `{C[N - m]}` 次"
    if l <= r:
        return f'闭区间 `[{l}, {r}]` 待验证；`res = {S["res"]}` 是目前验证通过的最大 h'
    return f'`left > right`：区间验证完毕，`res = {S["res"]}`'


def _if(S, B, ret):
    m = S.mid
    v = S.citations[len(S.citations) - m]
    if v >= m:
        return f'第 {m} 大的引用 `{v} ≥ {m}`：前 {m} 篇都 ≥ {m} 次 → h = {m} ==成立==，再试更大的'
    return f'第 {m} 大的引用 `{v} < {m}`：凑不出 {m} 篇 → h = {m} ==不成立==，往小找'


CONFIG = dict(
    num=275, title='H 指数 II', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分 h · 下标 n−mid 转换',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def hIndex(self, citations):

        if not citations:
            return 0

        left = 1
        right = len(citations)
        res = 0
        while left <= right:
            mid = (left + right) // 2
            if citations[len(citations) - mid] >= mid:
                res = mid
                left = mid + 1
            else:
                right = mid - 1

        return res
''',
    call=f'Solution().hIndex({C})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(1, N + 1)),
             label='候选 h ∈ [1, n]（绿 = 已确认可行，红 = 已确认不可行）', cell=84, index=False, color=_cand,
             pointers={'left': 'blue', 'mid': 'yellow', 'right': 'pink'}, h=240),
        dict(type='array', var='citations', label='citations（黄 = 下标 n−mid，即从大到小第 mid 篇；青 = 比它引用多的）',
             cell=90, color=_paper, h=200),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('res', 'res', 'green')],
    captions={
        'if not citations': '没有论文时 h 指数为 0；这里 `n = {len(citations)}`',
        'left = 1': '从 `1` 到 `n` 二分 h：`left = 1`',
        'right = len': '`right = n = {right}`',
        'res = 0': '`res` 记录验证通过的最大 h，先为 0',
        'while left <= right': lambda S, B, r: (f'`[{S.left}, {S.right}]` 不为空，继续' if S.left <= S.right
                                                 else f'`left = {S.left} > right = {S.right}`，结束'),
        'mid = (left': '`mid = ({left} + {right}) // 2 = {mid}`：试 h = {mid}',
        'if citations[len': _if,
        'res = mid': '`res = {res}`：h = {res} 可行，先记下',
        'left = mid + 1': '`left = {left}`：看看更大的 h 行不行',
        'right = mid - 1': '`right = {right}`',
        'return res': 'h 指数 =={ret}==',
    },
    cards=dict(
        one_liner='二分 h，用下标 n−mid 取从大到小第 mid 篇来验证',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`citations` 升序排列，`citations[i]` 是第 i 篇论文被引用次数',
                 '求 h 指数：==至少有 h 篇==论文各被引用==至少 h 次==，要求对数时间',
                 '示例：`[0,1,3,5,6]` → `3`；本视频 `[1,2,3,3,5,7,9]` → `3`'],
        quote='二分h时，需要验证的是==从大到小第h篇文章的引用次数是否超过了h==……从1到n开始进行二分，那么数组下标为n-mid的数就是数组中从大到小的第mid个数了。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组有序 + 要求对数时间 → 自然想到==二分==',
              '`mid` 是 h 的候选值，不是下标；从大到小第 mid 个数在下标 `n − mid`',
              '验证通过就记 `res = mid` 并往大找，否则往小找'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：二分的是 h，要把「第 mid 大」换成下标 `n − mid`',
                 '用 `res` 单独记录答案，闭区间 `while left <= right` 不用纠结返回 left 还是 right',
                 '原文为 Python 2 写法，`(left + right) / 2` 已改为 `(left + right) // 2`'],
    ),
)
