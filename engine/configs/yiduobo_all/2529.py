NUMS = [-4, -3, -3, -1, 0, 0, 2, 5, 7]


def _phase(S):
    if 'pos' in S:
        return 3
    if 'neg' in S:
        return 2
    return 1


def _color(S, i, v):
    ph = _phase(S)
    if ph >= 2 and i < S['neg']:
        return 'red'
    if ph == 3 and i > len(NUMS) - 1 - S['pos']:
        return 'green'
    return None


def _top(S):
    ph = _phase(S)
    if 'left' not in S:
        return '边界：首元素为正 / 末元素为负 → 全是同号，答案就是 `n`'
    l, r = S['left'], S['right']
    if ph == 1:
        return f'第一次二分：找==最小的非负数下标== p，候选 `[{l}, {r}]`'
    if ph == 2:
        return f"第二次二分：找==最大的非正数下标== q，候选 `[{l}, {r}]`（已知负数 `{S['neg']}` 个）"
    return f"`neg = {S['neg']}`，`pos = n − 1 − q = {S['pos']}`"


def _if1(S, B, ret):
    m, v = S.mid, S.nums[S.mid]
    if v >= 0:
        return f'`nums[{m}] = {v} ≥ 0`：非负 → p 在 `mid` 或它左边，`right = mid`'
    return f'`nums[{m}] = {v} < 0`：负数 → p 一定在 `mid` 右边'


def _if2(S, B, ret):
    m, v = S.mid, S.nums[S.mid]
    if v <= 0:
        return f'`nums[{m}] = {v} ≤ 0`：非正 → q 在 `mid` 或它右边，`left = mid`'
    return f'`nums[{m}] = {v} > 0`：正数 → q 一定在 `mid` 左边'


def _while(S, B, ret):
    if S.left < S.right:
        return f'`left = {S.left} < right = {S.right}`：还没收缩到一个点 → 继续'
    return f'`left == right = {S.left}`：找到了'


CONFIG = dict(
    num=2529, title='正整数和负整数的最大计数', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='特判边界 + 两次闭区间二分',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def maximumCount(self, nums):

        n = len(nums)
        if nums[0] > 0 or nums[-1] < 0:
            return n

        left, right = 0, n - 1
        while left < right:
            mid = (left + right) >> 1
            if nums[mid] >= 0:
                right = mid
            else:
                left = mid + 1

        neg = left

        left, right = 0, n - 1
        while left < right:
            mid = (left + right + 1) >> 1
            if nums[mid] <= 0:
                left = mid
            else:
                right = mid - 1

        pos = n - 1 - left

        return max(neg, pos)
''',
    call=f'Solution().maximumCount({NUMS})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='array', var='nums', label='nums（红 = 已确定的负数，绿 = 已确定的正数）', color=_color,
             window=('left', 'right'), pointers={'left': 'blue', 'mid': 'yellow', 'right': 'pink'}, cell=96, h=330),
    ],
    watch=['n', ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('neg', 'neg', 'red'), ('pos', 'pos', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'if nums[0] > 0': lambda S, B, r: ('首元素为正或末元素为负 → 全部同号，直接返回 `n`'
                                           if S.nums[0] > 0 or S.nums[-1] < 0 else
                                           f'`nums[0] = {S.nums[0]} ≤ 0` 且 `nums[-1] = {S.nums[-1]} ≥ 0`：不是全同号 → ==一般情况，要二分=='),
        8: '`left, right = 0, {right}`：在闭区间 `[{left}, {right}]` 里找',
        18: '重新从 `[{left}, {right}]` 开始第二次二分',
        'while left < right': _while,
        'mid = (left + right) >> 1': '`mid = ({left} + {right}) >> 1 = {mid}`：==下取整==，配合 `left = mid + 1`',
        'if nums[mid] >= 0': _if1,
        12: '`right = {right}`',
        22: '`left = {left}`：`mid` 非正，它自己仍可能是 q',
        'left = mid + 1': '`left = {left}`：跳过负数 `mid`',
        'neg = left': '`p = {neg}`：下标 `0 … p−1` 都是负数 → `neg = {neg}`',
        'mid = (left + right + 1) >> 1': '`mid = ({left} + {right} + 1) >> 1 = {mid}`：==上取整==，否则 `left = mid` 会死循环',
        'if nums[mid] <= 0': _if2,
        'right = mid - 1': '`right = {right}`：跳过正数 `mid`',
        'pos = n - 1 - left': '`q = {left}`：下标 `q+1 … n−1` 都是正数 → `pos = {n} − 1 − {left} = {pos}`',
        'return max': '`max({neg}, {pos})` = =={ret}==',
    },
    cards=dict(
        one_liner='先特判全同号，再二分找最小非负数 p 和最大非正数 q',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`nums` 非递减有序，返回 ==正整数个数和负整数个数的较大值==；`0` 不算',
                 '示例：`[-2,-1,-1,1,2,3]` → `3`；`[5,20,66,1314]` → `4`',
                 '本视频：`[-4,-3,-3,-1,0,0,2,5,7]` → 负 4、正 3 → `4`'],
        quote='可以通过二分法找到数组中==最小的非负数下标==，不妨记为p，那么下标在0到p - 1之间的数就都是负数；同样的，也可以通过二分法找到数组中==最大的非正数下标==，不妨记为q',
        quote_src='—— yiduobo 题解原文',
        idea=['边界：`nums[0] > 0` 全为正，`nums[-1] < 0` 全为负 → 答案是 `n`',
              '否则一定有非负数和非正数，`p`、`q` 都存在',
              '负数个数 = `p`，正数个数 = `n − 1 − q`，取较大者'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '找最大的满足条件的下标时，`mid` 要==上取整==：`(left + right + 1) >> 1`',
                 '特判保证了 p、q 一定存在，闭区间二分不会越界',
                 '对比灵神：灵神直接用 `bisect_left / bisect_right` 两行搞定'],
    ),
)
