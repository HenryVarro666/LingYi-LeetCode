NUMS = [4, 6, 1, 2, 8, 5]
K = 2


def _live(S):
    return 'right' in S and 'left' in S


def _draw(cv, S, B, box, T):
    """每个数 x 画成闭区间 [x-k, x+k]；窗口内的区间蓝色，交集画黄色竖带"""
    x0, y0, x1, y1 = box
    a = S['nums']
    cv.text((x0 + 18, y0 + 4), f'每个数 x 看成闭区间 [x−k, x+k]（k = {K}）；黄带 = 窗口内区间的交集', 22, T['muted'], bold=True)
    lo, hi = min(a) - K, max(a) + K
    L, R = x0 + 70, x1 - 50

    def X(v):
        return L + (v - lo) / max(1, hi - lo) * (R - L)
    top = y0 + 50
    rowh = min(40, (y1 - top - 40) / len(a))
    live = _live(S)
    if live and S['left'] <= S['right']:
        l, r = S['left'], S['right']
        il, ir = a[r] - K, a[l] + K
        if il <= ir:
            cv.rect((X(il), top - 4, max(X(ir), X(il) + 8), top + rowh * len(a)), fill=T['yellow'], alpha=90)
    for i, v in enumerate(a):
        y = top + i * rowh
        inwin = live and S['left'] <= i <= S['right']
        c = T['pink'] if live and i == S['right'] else (T['blue'] if inwin else T['dim'])
        cv.rect((X(v - K), y + 8, X(v + K), y + rowh - 8), fill=c, r=8)
        cv.text((x0 + 20, y + rowh / 2), f'{v}', 22, T['text'] if inwin else T['dim'], anchor='lm', mono=True, bold=True)
    for v in range(lo, hi + 1):
        cv.text((X(v), y1 - 26), str(v), 16, T['dim'], anchor='mt')


def _top(S):
    if not _live(S):
        return '选出的区间==交集非空== ⇔ 最右 − 最左 ≤ `2k`'
    a, l, r = S['nums'], S['left'], S['right']
    d = a[r] - a[l]
    return f"`nums[{r}] − nums[{l}] = {a[r]} − {a[l]} = {d}` {'≤' if d <= 2 * K else '>'} `2k = {2 * K}`"


def _while(S, B, ret):
    a, l = S.nums, S.left
    d = S.x - a[l]
    if d > S.k * 2:
        return f'`{S.x} − {a[l]} = {d} > {S.k * 2}`：区间 `[{a[l] - S.k}, {a[l] + S.k}]` 与新区间==不相交== → left 右移'
    return f'`{S.x} − {a[l]} = {d} ≤ {S.k * 2}`：窗口内所有区间有公共点，可以变成同一个数'


CONFIG = dict(
    num=2779, title='数组的最大美丽值', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 滑动窗口（区间交集）',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def maximumBeauty(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = left = 0
        for right, x in enumerate(nums):
            while x - nums[left] > k * 2:
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call=f'Solution().maximumBeauty({NUMS}, {K})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=28, h=70),
        dict(type='array', var='nums', label='nums（排序后）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), cell=100, h=230),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'x', ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '子序列 + 元素都要相等 → ==顺序无关==，先排序：`{nums}`',
        'ans = left = 0': '`ans = 0`，窗口左端 `left = 0`',
        'for right, x in': lambda S, B, r: ('右端点枚举完毕' if 'right' in B and B.right == S.right
                                            else f'枚举 `x = nums[{S.right}] = {S.x}` 作为子数组最后一个数'),
        'while x - nums[left]': _while,
        'left += 1': '`left` → {left}',
        'ans = max': '`[{left}, {right}]` 都能变成同一个数：`ans = max({B.ans}, {right - left + 1})` = =={ans}==',
        'return ans': '最大美丽值 =={ret}==',
    },
    cards=dict(
        one_liner='每个数看成区间 [x−k, x+k]，找交集非空的最多区间',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每个下标至多操作一次：把 `nums[i]` 换成 `[nums[i]−k, nums[i]+k]` 中的数',
                 '美丽值 = 由==相等元素==组成的最长子序列长度，求最大值',
                 '示例：`[4,6,1,2], k = 2` → `3`；本视频 `[4,6,1,2,8,5], k = 2` → `4`'],
        quote='题目要求的「由相等元素组成的最长子序列」，相当于选出若干闭区间，这些区间的==交集不为空==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后选出的区间是连续的，只看最左 `[x−k, x+k]` 和最右 `[y−k, y+k]`',
              '交集非空 ⇔ `x + k ≥ y − k` ⇔ ==`y − x ≤ 2k`==',
              '变成：最长连续子数组，末尾减开头 `≤ 2k` → 滑动窗口'],
        summary=['时间 `O(n log n)`，瓶颈在排序；滑窗部分 `O(n)`',
                 '阈值是 `2k` 不是 `k`：两个数各自都能移动 k',
                 '子序列 → 顺序无关 → 可以排序；子数组就不行（思考题）',
                 '另一种写法：差分/计数后枚举目标值（yiduobo 的做法）'],
    ),
)
