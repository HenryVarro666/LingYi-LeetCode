NUMS = [10, 5, 2, 6, 3]
K = 100


def _color(S, i, v):
    if 'right' not in S:
        return None
    if S['left'] <= i <= S['right']:
        return 'green' if S['_line'] == 13 else 'blue'
    return None


def _top(S):
    if 'right' not in S:
        return f'`k = {K}`：子数组越长乘积越大 → ==越短越合法=='
    l, r = S['left'], S['right']
    if S['_line'] == 10:
        return f"移出 `nums[{l}] = {NUMS[l]}` 后 `prod = {S['prod']}`，接着 left 右移"
    win = NUMS[l:r + 1]
    expr = ' × '.join(map(str, win)) if win else '空'
    ok = S['prod'] < K
    return f"窗口 `[{l}, {r}]`：`{expr} = {S['prod']}` {'<' if ok else '≥'} `{K}` → {'==合法==' if ok else '不合法，要缩小'}"


def _subs(S):
    if 'right' not in S or S['_line'] != 13:
        return ''
    l, r = S['left'], S['right']
    parts = ['[' + ','.join(map(str, NUMS[i:r + 1])) + ']' for i in range(l, r + 1)]
    return f"右端点固定在 {r}：{'、'.join(parts)} → 共 =={r - l + 1}== 个"


def _while(S, B, ret):
    if S.prod >= S.k:
        return f'`prod = {S.prod} ≥ {S.k}`：窗口乘积太大，==不满足要求== → 缩小窗口'
    return f'`prod = {S.prod} < {S.k}`：窗口 `[{S.left}, {S.right}]` 合法，停止缩小'


CONFIG = dict(
    num=713, title='乘积小于 K 的子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 越短越合法',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0
        ans = left = 0
        prod = 1
        for right, x in enumerate(nums):
            prod *= x
            while prod >= k:  # 不满足要求
                prod //= nums[left]
                left += 1  # 缩小窗口
            # 对于固定的 right，有 right-left+1 个合法的左端点
            ans += right - left + 1
        return ans
''',
    call=f'Solution().numSubarrayProductLessThanK({NUMS}, {K})',
    expect=11,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, right]，绿 = 本轮计入答案的左端点）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_color, cell=120, h=300),
        dict(type='text', fn=_subs, size=26, h=80),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'x', ('prod', 'prod', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'if k <= 1': '`nums[i] ≥ 1`，乘积至少是 1；`k = {k} > 1`，不用特判返回',
        'ans = left = 0': '`ans = 0`，窗口左端点 `left = 0`',
        'prod = 1': '`prod`：窗口内元素的乘积，空窗口为 1',
        'for right, x': lambda S, B, r: ('右端点枚举完毕，结束循环' if 'right' in B and B.right == S.right
                                         else f'枚举右端点 `right = {S.right}`，新元素 `x = {S.x}` 进入窗口'),
        'prod *= x': '`prod = {B.prod} × {x} = {prod}`',
        'while prod >= k': _while,
        'prod //= nums[left]': '移出左端元素 `nums[{left}]`：`prod = {B.prod} // {B.prod // prod} = {prod}`',
        'left += 1': '`left` → {left}：窗口变短，乘积变小',
        'ans += right': '左端点取 `{left}..{right}` 都合法：`ans += {right} − {left} + 1` → =={ans}==',
        'return ans': '共有 =={ret}== 个乘积小于 {k} 的子数组',
    },
    cards=dict(
        one_liner='枚举右端点，缩小左端点；right 固定时有 right−left+1 个合法子数组',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`（元素 ≥ 1）和整数 `k`',
                 '求==乘积严格小于 k== 的连续子数组个数',
                 '示例：`[10,5,2,6], k = 100` → `8`；本视频 `[10,5,2,6,3], k = 100` → `11`'],
        quote='由于子数组越长，乘积越大，越不能满足题目要求；反之，子数组越短，乘积越小，越能满足题目要求。有这种性质的题目，可以用==滑动窗口==解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['内层循环结束后 `[left, right]` 合法，==更短的 `[left+1, right]`…`[right, right]` 也合法==',
              '所以右端点固定在 right 时，一次加上 `right − left + 1` 个',
              '保留「枚举右端点」的暴力思路，左端点只右移，均摊 `O(1)`'],
        summary=['时间 `O(n)`：`left` 总共最多右移 n 次；空间 `O(1)`',
                 '`k ≤ 1` 要特判：否则 `prod >= k` 恒成立，left 会越界',
                 '不特判也行：内层条件改成 `left <= right and prod >= k`',
                 '同类：越短越合法的「求子数组个数」都是 `ans += right − left + 1`'],
    ),
)
