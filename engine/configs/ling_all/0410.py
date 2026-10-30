NUMS = [3, 1, 4, 2]
K = 2


def _ncolor(S, i, v):
    # check 内部：之前的元素按所在段交替染色（青 / 紫），当前元素黄色
    if 'mx' not in S or 'x' not in S or S['_line'] not in range(6, 14):
        return None
    idx = NUMS.index(S['x'])
    if i == idx:
        return 'yellow'
    if i > idx:
        return None
    cnt, s = 1, 0
    seg = []
    for x in NUMS[:idx]:
        if s + x <= S['mx']:
            s += x
        else:
            cnt += 1
            s = x
        seg.append(cnt)
    return 'cyan' if seg[i] % 2 else 'purple'


def _top(S):
    if 'left' not in S:
        if 'mx' in S:
            return f"贪心：每段尽量装，和超过 `mx = {S['mx']}` 就新开一段（最多 `k = {K}` 段）"
        return f'`k = {K}`：「最大段和」越小，要划分的段数越多 → ==二分答案=='
    l, r = S['left'], S['right']
    if S['_line'] in (4, 5, 6, 7, 8, 9, 10, 11, 12) and 'mx' in S:
        return f"check(`{S['mx']}`)：第 `{S.get('cnt', 1)}` 段当前和 `s = {S.get('s', 0)}`，上限 `{S['mx']}`"
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：`{l}` 一定不行（False），`{r}` 一定行（True）'
    return f'`left + 1 == right`：`{l}` 不行、`{r}` 行 → 答案 =={r}=='


def _cand(S, i, v):
    if 'left' not in S:
        return None
    if v <= S['left']:
        return 'red'
    if v >= S['right']:
        return 'green'
    return None


def _if_add(S, B, ret):
    if B.s + S.x <= S.mx:
        return f'`s + x = {B.s} + {S.x} = {B.s + S.x} ≤ {S.mx}`：放进当前段'
    return f'`s + x = {B.s} + {S.x} = {B.s + S.x} > {S.mx}`：当前段装不下 `{S.x}`，==必须新开一段=='


def _if_k(S, B, ret):
    if S.cnt == S.k:
        return f'已经有 `cnt = {S.cnt} = k` 段，不能再分 → ==返回 False=='
    return f'`cnt = {S.cnt} < k = {S.k}`，还可以再分一段'


CONFIG = dict(
    num=410, title='分割数组的最大值', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 贪心划分',
    tags=['labuladong', '灵神题单·二分算法'],
    code='''
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def check(mx: int) -> bool:
            cnt = 1
            s = 0
            for x in nums:
                if s + x <= mx:
                    s += x
                    continue
                if cnt == k:  # 不能继续划分
                    return False
                cnt += 1  # 新划分一段
                s = x
            return True

        left = max(nums) - 1
        right = sum(nums)
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().splitArray({NUMS}, {K})',
    expect=6,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(sum(NUMS) + 1)),
             label='候选最大和（红 = 不可行 False，绿 = 可行 True）', cell=72, index=False,
             dim=lambda S, i, v: v < max(NUMS) - 1, color=_cand,
             pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, h=230),
        dict(type='array', var='nums', label='nums（黄 = 当前 x；青 / 紫 = 已划分的各段）', cell=110, h=190, color=_ncolor),
        dict(type='calls', h=150),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow'),
           ('mx', 'mx'), ('cnt', 'cnt', 'purple'), ('s', 's', 'cyan'), 'x'],
    captions={
        'cnt = 1': '贪心划分：`cnt = 1`，先开第一段',
        's = 0': '`s`：当前这一段的元素和',
        'for x in nums': lambda S, B, r: ('nums 遍历完了' if 'x' in B and B.x == S.x else f'看下一个元素 `x = {S.x}`'),
        'if s + x <= mx': _if_add,
        's += x': '`s = {s}`',
        'if cnt == k': _if_k,
        'return False': '段数超过 `k`：最大和 `{mx}` ==不可行==',
        'cnt += 1': '新划分一段：`cnt = {cnt}`',
        's = x': '新段从 `x` 开始：`s = {s}`',
        'return True': '划分不超过 `k` 段：最大和 `{mx}` ==可行==',
        'left = max': '`left = max(nums) − 1 = {left}`：比最大元素还小，==一定不可行==',
        'right = sum': '`right = sum(nums) = {right}`：不分割就行，==一定可行==',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                                   else f'`left + 1 == right`：开区间为空，结束'),
        'mid = (left': '猜最大和 `mid = ({left} + {right}) // 2 = {mid}`，用 check 验证',
        'if check(mid)': '调用 `check({mid})`：能否分成 ==至多 k 段==、每段和都 `≤ {mid}`？',
        'right = mid': '`right = {right}`：仍满足==恒为 True==',
        'left = mid': '`left = {left}`：仍满足==恒为 False==',
        'return right': '`right` 是最小的可行最大和 → =={ret}==',
    },
    skip=['continue'],
    cards=dict(
        one_liner='最大和越小越难满足：二分最大和，贪心算最少段数',
        complexity='时间 `O(n log U)`，空间 `O(1)`，`U = sum(nums)`',
        problem=['把非负整数数组 `nums` 分成 `k` 个非空连续子数组',
                 '使各段和的==最大值最小==，返回这个最小值',
                 '示例：`[7,2,5,10,8], k = 2` → `18`；本视频 `[3,1,4,2], k = 2` → `6`'],
        quote='「元素和的最大值」越小，需要划分出的段数就越多；「元素和的最大值」越大，需要划分出的段数就越少。……如果发现答案越小，越不能满足要求；答案越大，越能满足要求，就可以尝试==二分答案==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['check(mx)：贪心地往当前段里加，加不下就新开一段',
              '新开之前已经有 `k` 段 → 段数超了，返回 False',
              '开区间 `(max−1, sum)`：left 恒 False，right 恒 True'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '「恰好 k 段」等价于「至多 k 段」：段少了可以把长段再切开',
                 '二分结果一定是某段的真实和，否则 `check(ans−1)` 也为真，矛盾',
                 '另有 `bisect_left(range(...), True, key=check)` 写法；本题也可划分型 DP'],
    ),
)
