def _nums(S):
    return S.get('nums') or []


def _col(S, i, v):
    mx = S.get('mx')
    if mx is None or '_inner' not in S or 'x' not in S['_inner']:
        return None
    return 'green' if v <= mx else None


def _dim(S, i, v):
    mx = S.get('mx')
    return mx is not None and v > mx


def _txt(S):
    mx = S.get('mx')
    if mx is None:
        return ''
    return f"最大金额 `mx = {mx}`：绿色 = 能偷（`≤ {mx}`），灰色 = 不能偷。目前最多偷 ==`{S.get('f1', 0)}`== 间"


CONFIG = dict(
    num=2560, title='打家劫舍 IV', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 打家劫舍 DP',
    tags=['二分答案', '难度分 2081'],
    code='''
class Solution:
    def minCapability(self, nums: List[int], k: int) -> int:
        # solve(mx) 返回最大金额为 mx 时，最多可以偷多少间房子
        def solve(mx: int) -> int:
            f0 = f1 = 0
            for x in nums:
                if x > mx:
                    f0 = f1
                else:
                    f0, f1 = f1, max(f1, f0 + 1)
            return f1
        return bisect_left(range(max(nums)), k, key=solve)
''',
    call='Solution().minCapability([2,7,9,3,1], 2)',
    expect=2,
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='nums', label='nums（每间房的现金）', h=250,
             color=_col, dim=_dim),
        dict(type='text', fn=lambda S: (f"`f0 = {S['f0']}`（偷到上上间时的最大数），`f1 = {S['f1']}`（偷到当前间时的最大数）" if 'f1' in S else '')),
    ],
    watch=['mx', ('f0', 'f0', 'cyan'), ('f1', 'f1', 'green'), 'x', 'k'],
    max_steps=90,
    captions={
        'f0 = f1 = 0': '还没看任何房子：`f0 = f1 = 0`。`f1` 是已看的房子里最多能偷几间',
        'for x in nums': '`x = {x}`：考虑这间房偷不偷',
        'if x > mx': lambda S, B, r: (f"`x = {S.x} > mx = {S.mx}` → 超过能力上限，==不能偷==" if S.x > S.mx
                                      else f"`x = {S.x} ≤ mx = {S.mx}` → ==可以偷=="),
        'f0 = f1': '不能偷：`f[i] = f[i-1]`，滚动后 `f0 = f1 = {f1}`',
        'f0, f1 = f1, max': '选或不选取大：`max(不选 {B.f1}, 选 {B.f0} + 1)` = =={f1}==',
        'return f1': lambda S, B, r: (f"`mx = {S.mx}` 时最多偷 =={S.f1}== 间 ≥ `k = {S.k}` → 够用，答案 ≤ {S.mx}，往小的猜" if S.f1 >= S.k
                                      else f"`mx = {S.mx}` 时最多偷 =={S.f1}== 间 < `k = {S.k}` → 不够，答案 > {S.mx}，往大的猜"),
        'return bisect_left': '二分答案：`bisect_left` 用 `solve(mx)` 判定，找第一个偷得到 `k = {k}` 间的 `mx`。下面逐个试 `mx`',
    },
    cards=dict(
        one_liner='最小化最大值：二分答案，再用打家劫舍 DP 判定',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['不能偷相邻的房子，至少偷 `k` 间；窃取能力 = 偷过的最大金额',
                 '求窃取能力的最小值',
                 '示例：`nums=[2,7,9,3,1], k=2` → `2`（偷下标 0 和 4）'],
        quote='看到「最大化最小值」或者「最小化最大值」就要想到二分答案，这是一个固定的套路。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`mx` 越大，能偷的房子越多，有单调性 → 二分猜 `mx`',
              '`solve(mx)`：只有 `≤ mx` 的房子能偷，套 198 打家劫舍：`f[i] = max(f[i-1], f[i-2] + 1)`',
              '`bisect_left(range(max(nums)), k, key=solve)` 找最小的、能偷满 `k` 间的 `mx`'],
        summary=['时间 `O(n log U)`，`U = max(nums)`；两个变量滚动，空间 `O(1)`',
                 '`bisect_left` 的 `key` 要求 `solve` 单调不降，这里成立',
                 '二分出的答案一定在 `nums` 中，否则 `ans-1` 也满足，与二分矛盾',
                 '题解方法二：从左往右能偷就偷（贪心），把 DP 换成 `cnt`、`i += 2` 跳过下一间',
                 '同类题：2439、2616、1552、2517'],
    ),
)
