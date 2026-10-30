C = [0, 1, 2, 4, 5, 6, 8, 9]
N = len(C)


def _cand(S, i, v):
    if 'left' not in S:
        return None
    if v <= S['left']:
        return 'green'
    if v >= S['right']:
        return 'red'
    return None


def _paper(S, i, v):
    if 'mid' not in S or S['_line'] not in (10, 12, 13, 15):
        return None
    m = S['mid']
    if i >= N - m:
        return 'yellow' if i == N - m else 'cyan'
    return None


def _top(S):
    if 'left' not in S or 'right' not in S:
        return '找最大的 `h`：引用最多的 `h` 篇论文==每篇都 ≥ h== 次'
    l, r = S['left'], S['right']
    if 'mid' in S and S['_line'] in (10, 12):
        m = S['mid']
        ok = C[-m] >= m
        return f"问：h = `{m}` 行吗？最多引用的 `{m}` 篇里最少的是 `citations[-{m}] = {C[-m]}` {'≥' if ok else '<'} `{m}` → {'==是==' if ok else '否'}"
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：左边都回答「是」，右边都回答「否」'
    return f'`left + 1 == right`：`{l}` 是最大的「是」 → h 指数 =={l}=='


def _if(S, B, ret):
    m = S.mid
    if S.citations[-m] >= m:
        return f'`citations[-{m}] = {S.citations[-m]} ≥ {m}`：引用最多的 {m} 篇都 ≥ {m} 次 → h ==至少是 {m}=='
    return f'`citations[-{m}] = {S.citations[-m]} < {m}`：凑不齐 {m} 篇 ≥ {m} 次 → h ==小于 {m}=='


CONFIG = dict(
    num=275, title='H 指数 II', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 开区间',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        # 在区间 (left, right) 内询问
        left = 0
        right = len(citations) + 1
        while left + 1 < right:  # 区间不为空
            # 循环不变量：
            # left 的回答一定为「是」
            # right 的回答一定为「否」
            mid = (left + right) // 2
            # 引用次数最多的 mid 篇论文，引用次数均 >= mid
            if citations[-mid] >= mid:
                left = mid  # 询问范围缩小到 (mid, right)
            else:
                right = mid  # 询问范围缩小到 (left, mid)
        # 根据循环不变量，left 现在是最大的回答为「是」的数
        return left
''',
    call=f'Solution().hIndex({C})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(N + 2)),
             label='候选 h（绿 = 回答「是」，红 = 回答「否」，灰 = 未知）', cell=80, index=False, color=_cand,
             pointers={'left': 'green', 'mid': 'yellow', 'right': 'red'}, h=240),
        dict(type='array', var='citations', label='citations（升序；青 = 引用最多的 mid 篇，黄 = 其中最少的 citations[-mid]）',
             cell=90, color=_paper, h=200),
    ],
    watch=[('left', 'left', 'green'), ('right', 'right', 'red'), ('mid', 'mid', 'yellow')],
    captions={
        'left = 0': '`left = 0`：h = 0 一定成立，回答==一定为「是」==',
        'right = len': '`right = n + 1 = {right}`：只有 {right - 1} 篇论文，h 不可能是 {right}，回答==一定为「否」==',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续询问' if S.left + 1 < S.right
                                                    else f'`left + 1 == right`：区间为空，每个 h 都有了答案'),
        'mid = (left': '二分的是==答案 h（引用次数）==，不是下标：`mid = ({left} + {right}) // 2 = {mid}`',
        'if citations[-mid]': _if,
        'left = mid': '`left = {left}`：{left} 的回答为「是」，询问 `({left}, {right})`',
        'right = mid': '`right = {right}`：{right} 的回答为「否」，询问 `({left}, {right})`',
        'return left': '`left` 是最大的回答为「是」的数 → h 指数 =={ret}==',
    },
    cards=dict(
        one_liner='h 越大越难满足：二分答案 h，看倒数第 h 篇够不够 h 次',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`citations` 已升序，`citations[i]` 是第 i 篇论文的引用次数',
                 'h 指数：==至少 h 篇==论文，每篇==至少被引用 h 次==；要求对数时间',
                 '示例：`[0,1,3,5,6]` → `3`；本视频 `[0,1,2,4,5,6,8,9]` → `4`'],
        quote='题意：找最大的 h，满足 `citations[n-h] >= h`。⚠注意：我们二分的是答案，是==引用次数==，不是 citations 的下标。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数组升序：引用最多的 h 篇就是最后 h 篇，其中最少的是 `citations[-h]`',
              '`citations[-h] ≥ h` 成立时，更小的 h 也成立 → ==单调，可二分==',
              '开区间 `(0, n+1)`：left 恒为「是」，right 恒为「否」，最后返回 left'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '二分的是 h（答案），用 `citations[-mid]` 取倒数第 mid 篇',
                 '`right = n + 1`：h 最大可以是 n，所以 n+1 才一定为「否」',
                 '题解还给了闭区间、半开区间写法，以及缩小初始范围的写法，结论相同'],
    ),
)
