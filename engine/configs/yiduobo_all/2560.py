def _col(S, i, v):
    if 'mid' not in S:
        return None
    return 'green' if v <= S['mid'] else None


def _dim(S, i, v):
    return 'mid' in S and v > S['mid']


def _range(S):
    if 'left' not in S:
        return ''
    s = f"二分范围 `[{S['left']}, {S['right']}]`"
    if 'mid' in S:
        s += f"，猜 `mid = {S['mid']}`：绿色 = 小于等于 mid 的房子"
    return s


def _state(S):
    if 'cnt' not in S or 'pre' not in S:
        return ''
    return f"上一间{'偷了' if S['pre'] else '没偷'}（`pre = {S['pre']}`），已偷 ==`{S['cnt']}`== 间，目标 `k = {S['k']}`"


CONFIG = dict(
    num=2560, title='打家劫舍 IV', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分能力值 + 贪心偷',
    tags=['二分答案', '难度分 2081'],
    code='''
class Solution(object):
    def minCapability(self, nums, k):

        left = min(nums)
        right = max(nums)
        while left < right:
            mid = (left + right) // 2
            pre = False
            cnt = 0
            for v in nums:
                if v <= mid and not pre:
                    pre = True
                    cnt += 1
                else:
                    pre = False
            
            if cnt >= k:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().minCapability([2,3,5,9], 2)',
    expect=5,
    views=[
        dict(type='text', fn=_range),
        dict(type='array', var='nums', label='nums', h=230, color=_col, dim=_dim),
        dict(type='text', fn=_state),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), 'pre', ('cnt', 'cnt', 'green'), 'k'],
    max_steps=80,
    captions={
        'left = min': '能力值最低也得是最小的那间：`left = {left}`',
        'right = max': '能力值取最大金额一定够：`right = {right}`',
        'while left < right': lambda S, B, r: (f"`left = {S.left} < right = {S.right}`：答案还在 `[{S.left}, {S.right}]` 里，继续猜" if S.left < S.right
                                               else f"`left = right = {S.left}`：范围缩成一个数，就是答案"),
        'mid = ': '猜能力值 `mid = ({left} + {right}) // 2 = {mid}`：能不能只偷 `≤ {mid}` 的房子凑够 `{k}` 间',
        8: '`pre` 记录上一间有没有偷，先设为没偷',
        'cnt = 0': '`cnt` 统计偷了几间，从 0 开始',
        'for v in nums': '看下一间：金额 `v = {v}`',
        'if v <= mid and not pre': lambda S, B, r: (f"`{S.v} <= {S.mid}` 且上一间没偷 → ==偷这间==" if S.v <= S.mid and not B.pre
                                                    else (f"`{S.v} <= {S.mid}` 但上一间偷了（相邻）→ ==不能偷==" if S.v <= S.mid
                                                          else f"`{S.v} > {S.mid}`，超过能力值 → ==不能偷==")),
        'pre = True': '偷了：`pre = True`',
        'cnt += 1': '已偷 `cnt = {cnt}` 间',
        15: '没偷这间：`pre = False`，下一间就可以偷了',
        'if cnt >= k': lambda S, B, r: (f"`cnt = {S.cnt} >= k = {S.k}` → mid 够用，答案可能更小 → 收缩上界" if S.cnt >= S.k
                                        else f"`cnt = {S.cnt} < k = {S.k}` → mid 不够，答案必须更大 → 抬高下界"),
        'right = mid': '`right = mid = {right}`：mid 本身可能就是答案，所以不减 1',
        'left = mid + 1': '`left = mid + 1 = {left}`：mid 已经不行，排除掉',
        'return left': '二分结束，最小窃取能力 `{left}`',
    },
    cards=dict(
        one_liner='能力值越大越容易成功：二分，每次贪心地能偷就偷',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['不能偷相邻房子，至少偷 `k` 间，窃取能力 = 偷过的最大金额',
                 '求最小的窃取能力',
                 '本视频：`nums=[2,3,5,9], k=2` → `5`'],
        quote='由于本题并不在意窃取的总金额，而是只需要保证窃取的房子数量，因此在这里可以使用贪心法来进行窃取，也就是一趟遍历，若当前的房子可以窃取，那么就执行窃取。',
        quote_src='—— yiduobo 题解原文',
        idea=['窃贼能力越高，越容易偷够 `k` 间，所以能二分',
              '二分的范围：房屋金额的最小值到最大值',
              '每个 `mid` 扫一遍：`v <= mid` 且上一间没偷就偷，用 `pre` 防相邻'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`(left + right) / 2` 已改为 `//`',
                 '`cnt >= k` 时 `right = mid`（不减 1），否则 `left = mid + 1`',
                 '`pre` 在偷不了时必须清成 `False`，否则会永远隔着跳',
                 '对比灵神：他用 DP 或同样的贪心配 `bisect_left`，这里手写二分'],
    ),
)
