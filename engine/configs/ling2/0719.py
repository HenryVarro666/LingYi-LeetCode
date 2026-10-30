NUMS, K = [6, 1, 3], 2
U = max(NUMS) - min(NUMS)
CANDS = list(range(U + 1))


def _in_check(S):
    return 'mx' in S


def _cand_color(S, i, v):
    if 'left' not in S:
        return None
    if _in_check(S) and v == S['mx']:
        return 'yellow'
    if v <= S['left']:
        return 'red'
    if v >= S['right']:
        return 'blue'
    return None


def _nums_color(S, k, v):
    if not _in_check(S) or 'j' not in S:
        return None
    if k == S['j']:
        return 'blue'
    if S['i'] <= k < S['j']:
        return 'cyan'
    return None


def _text(S):
    if 'left' not in S:
        return '第 k 小 ⇔ 最小的 x，使得 ==绝对差 ≤ x 的数对至少有 k 个=='
    if _in_check(S) and 'j' in S:
        return f"check(`mx = {S['mx']}`)：右端点 `j = {S['j']}`，`cnt = {S['cnt']}`，目标 `k = {K}`"
    return f"开区间 `({S['left']}, {S['right']})`：红 = check 为 false，蓝 = check 为 true"


def _while_ij(S, B, ret):
    d = B.x - B.nums[B.i]
    if d > B.mx:
        return f'`{B.x} − {B.nums[B.i]} = {d} > mx = {B.mx}`：`i` 太靠左 → 右移'
    return f'`{B.x} − {B.nums[B.i]} = {d} ≤ mx = {B.mx}`：`i` 满足要求了'


def _ret_check(S, B, ret):
    op = '≥' if ret else '<'
    return f'`cnt = {S.cnt} {op} k = {S.k}` → `check({S.mx}) = {ret}`'


CONFIG = dict(
    num=719, title='找出第 K 小的数对距离', difficulty='Hard', category='二分查找',
    author='灵茶山艾府', technique='二分答案（开区间）+ 同向双指针计数',
    tags=['字节30天'],
    code='''
class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        nums.sort()

        def check(mx: int) -> bool:
            cnt = i = 0
            for j, x in enumerate(nums):
                while x - nums[i] > mx:
                    i += 1
                cnt += j - i
            return cnt >= k

        left, right = -1, nums[-1] - nums[0]
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().smallestDistancePair({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='array', var=lambda S: CANDS, label='答案候选 x（红 = check(x) 为 false，蓝 = true，黄 = 正在 check）',
             cell=84, h=250, pointers={'left': 'red', 'right': 'blue', 'mid': 'yellow'}, color=_cand_color),
        dict(type='array', var='nums', label='nums（排序后；蓝 = 右端点 j，青 = 能和 j 配对的 i..j−1）', cell=96, h=210,
             pointers={'i': 'pink', 'j': 'blue'}, color=_nums_color),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'), 'cnt', 'k'],
    captions={
        'nums.sort()': '先排序：`nums = {nums}`（绝对差和下标顺序无关）',
        'left, right = -1': '开区间 `(left, right)`：`-1` 时 0 个数对，一定 false；`{right}` 时所有数对都满足，一定 true',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({B.left}, {B.right})` 不为空 → 继续二分' if B.left + 1 < B.right
                                                   else f'`left + 1 == right`：区间空了，`right = {B.right}` 就是答案'),
        'mid = (left + right) // 2': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': lambda S, B, r: f'判定：绝对差 `≤ {B.mid}` 的数对，==至少==有 `k = {B.k}` 个吗？',
        'cnt = i = 0': '`cnt` 统计绝对差 `≤ {mx}` 的数对；`i` 是左指针',
        'for j, x in enumerate(nums)': lambda S, B, r: (f'枚举右端点 `j = {S.j}`，`x = {S.x}`'
                                                       if 'j' not in B or B.j != S.j else f'所有右端点枚举完：`cnt = {S.cnt}`'),
        'while x - nums[i] > mx': _while_ij,
        'i += 1': '`i` → `{i}`',
        'cnt += j - i': lambda S, B, r: (f'`i = j = {S.j}`：左边没有能和它配对的，`cnt` 不变' if S.j == S.i else
                                         f'`i` 越大越满足：`i, i+1, …, j−1` 都行，共 `{S.j} − {S.i}` 个 → `cnt = {S.cnt}`'),
        'return cnt >= k': _ret_check,
        'right = mid': '`check({mid})` 为 true → 答案 `≤ {mid}`：`right = {right}`（蓝色扩大）',
        'left = mid': '`check({mid})` 为 false → 答案 `> {mid}`：`left = {left}`（红色扩大）',
        'return right': 'check 为 true 时更新的是 `right`，最后就返回它 → =={ret}==',
    },
    cards=dict(
        one_liner='第 k 小 ⇔ 最小的 x，使绝对差 ≤ x 的数对至少有 k 个',
        complexity='时间 `O(n log n + n log U)`，空间 `O(1)`',
        problem=['数对 `(nums[i], nums[j])`（`i < j`）的距离 = 两数之差的绝对值',
                 '返回所有数对距离中==第 k 小==的那个',
                 '示例：`nums = [1,3,1], k = 1` → `0`；`nums = [1,6,1], k = 3` → `5`',
                 '本视频：`nums = [6,1,3], k = 2` → `3`（距离从小到大 `2,3,5`）'],
        quote='第 k 小等价于：求最小的 x，满足==绝对差 ≤ x 的数对至少有 k 个==。（注意是至少不是恰好）',
        quote_src='—— 灵茶山艾府题解「第 k 小/大问题的通用转化方法」',
        idea=['x 越大越能找到 k 个数对 → 有单调性，==二分猜答案==',
              '判定：排序后枚举右端点 `j`，最小的合法 `i` 只会右移（同向双指针），`cnt += j − i`',
              '开区间写法：check 为 true 时更新的是谁，最后就返回谁'],
        summary=['时间 `O(n log n + n log U)`，`U = max − min`；空间 `O(1)`（忽略排序）',
                 '易错：是“==至少== k 个”，不是“恰好 k 个”',
                 '答案一定是某两数之差：否则 `check(ans − 1)` 也为 true，与循环不变量矛盾',
                 '库函数写法：`bisect_left(range(U), True, key=check)`',
                 '同类：二分题单 §2.6 第 K 小/大'],
    ),
)
