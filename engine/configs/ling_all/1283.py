NUMS = [1, 2, 5, 9]
TH = 6


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'green'
    return None


def _terms(S):
    if 'mid' not in S or S['_line'] not in (6, 7, 8, 9, 10):
        return []
    m = S['mid']
    return [(x - 1) // m for x in NUMS]


def _top(S):
    n = len(NUMS)
    if 'mid' in S and S['_line'] in (6, 7, 9):
        m = S['mid']
        ts = _terms(S)
        tot = sum(ts)
        ok = tot <= TH - n
        return f"除数 `{m}`：`Σ (x−1)//{m}` = `{' + '.join(map(str, ts))}` = `{tot}` {'≤' if ok else '>'} `{TH} − {n} = {TH - n}` → {'==满足==' if ok else '不满足'}"
    if 'left' not in S:
        return f'除数越大，和越小 → ==二分答案==；`threshold = {TH}`'
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：里面的除数还==不知道==是否满足'
    return f'`left + 1 == right`：`{l}` 不满足，`{r}` 满足 → 答案 =={r}=='


def _if(S, B, ret):
    m = S.mid
    t = sum((x - 1) // m for x in S.nums)
    lim = S.threshold - len(S.nums)
    if t <= lim:
        return f'`Σ (x−1)//{m} = {t} ≤ {lim}`：除数 `{m}` 满足 → 答案 ==≤ {m}==，`right = mid`'
    return f'`Σ (x−1)//{m} = {t} > {lim}`：除数 `{m}` 太小 → 答案 ==> {m}==，`left = mid`'


CONFIG = dict(
    num=1283, title='使结果不超过阈值的最小除数', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 开区间',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1542'],
    code='''
class Solution:
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        left, right = 0, max(nums)
        while left + 1 < right:
            mid = (left + right) // 2
            if sum((x - 1) // mid for x in nums) <= threshold - len(nums):
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().smallestDivisor({NUMS}, {TH})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(max(NUMS) + 1)),
             label='候选除数（红 = 不满足 False，绿 = 满足 True，灰 = 未知）', cell=80, index=False, color=_color,
             pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, h=240),
        dict(type='array', var='nums', label='nums', cell=100, h=170),
        dict(type='array', var=_terms, label='每项 (x − 1) // mid（= ceil(x / mid) − 1）', cell=100, index=False, h=170),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow'),
           ('threshold − n', lambda S: S['threshold'] - len(S['nums']) if 'threshold' in S else None, 'cyan')],
    captions={
        'left, right = 0': '开区间 `(0, {right})`：除数 0 ==一定不满足==；除数 `max(nums) = {right}` 时每项都是 1，和 `n ≤ threshold` ==一定满足==',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                                  else f'`left + 1 == right = {S.right}`：开区间为空，==每个除数都有了结论=='),
        'mid = (left': '猜一个除数：`mid = ({left} + {right}) // 2 = {mid}`',
        'if sum(': _if,
        'right = mid': '`right = {right}`：右端点仍然满足',
        'left = mid': '`left = {left}`：左端点仍然不满足',
        'return right': '`right` 是==最小的满足要求的除数== → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='除数越大和越小，有单调性 → 二分答案',
        complexity='时间 `O(n log U)`，空间 `O(1)`，`U = max(nums)`',
        problem=['选一个正整数除数，`nums` 每个数除以它并==向上取整==后求和',
                 '求使和 `≤ threshold` 的==最小==除数，保证有解',
                 '示例：`nums = [1,2,5,9], threshold = 6` → `5`（除数 4 时和为 7，除数 5 时和为 5）'],
        quote='由于 m 越大，上式越小，有==单调性==，可以二分答案。……最小的满足 Σ ceil(nums[i]/m) ≤ threshold 的 m 就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['上取整：`ceil(a/b) = floor((a−1)/b) + 1`，求和后两边减去 `n`',
              '判定变成 `Σ (x−1)//m ≤ threshold − n`，全是整数运算',
              '开区间 `(0, max(nums))`：左端点恒不满足，右端点恒满足'],
        summary=['时间 `O(n log U)`：二分 `log U` 次，每次 `O(n)`；空间 `O(1)`',
                 '右端点取 `max(nums)`：此时和为 `n`，题目保证 `n ≤ threshold`',
                 '开区间：`check(mid)` 为真时更新谁（right），最后就返回谁',
                 '另有 `bisect_left(range(max(nums)), True, 1, key=check)` 的库函数写法'],
    ),
)
