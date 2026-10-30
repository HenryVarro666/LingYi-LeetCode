def _oi(S):
    if 'f_inc' not in S:
        return None
    return sum(1 for v in S['f_inc'] if v) - (1 if S.get('_line', 0) >= 44 else 0)


def _fml(S):
    i = _oi(S)
    if i is None or i >= len(S['nums']):
        return '`f_inc[i]`：以 `nums[i]` 结尾、最后两项==递增==的最大和；`f_dec[i]` 同理递减'
    x, k = S['nums'] and S.get('x'), S['k']
    if S.get('_line', 0) < 56:
        return f'`i = {i}`，`x = {x}`：只能接在下标 `≤ i−k = {i - k}` 的元素后面'
    return f'`f_inc[{i}] = max f_dec[j] + {x}`（`nums[j] < {x}`）　`f_dec[{i}] = max f_inc[j] + {x}`（`nums[j] > {x}`）'


def _cap_fi(S, B, ret):
    v = B.dec.pre_max(B.j)
    return (f'在 `dec` 里查值域前缀 `[0, {B.j})`（即值小于 `{B.x}` 的位置）的 `f_dec` 最大值 = `{v}`'
            f' → `f_inc[{B.i}] = {v} + {B.x}` = =={v + B.x}==')


def _cap_fd(S, B, ret):
    v = B.inc.pre_max(B.m - 1 - B.j)
    return (f'后缀变前缀：值大于 `{B.x}` 的 `f_inc` 最大值 = `{v}`（查前缀 `{B.m - 1 - B.j}`）'
            f' → `f_dec[{B.i}] = {v} + {B.x}` = =={v + B.x}==')


OI = 'sum(1 for v in f_inc if v) - (_line >= 44)'


CONFIG = dict(
    num=3915, title='距离至少为 K 的交替子序列的最大和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='值域树状数组优化 DP', tags=['动态规划', '常用数据结构', '难度分 2288'],
    code='''
class Fenwick:
    def __init__(self, n: int):
        self.f = [0] * n

    def update(self, i: int, val: int) -> None:
        f = self.f
        while i < len(f):
            f[i] = max(f[i], val)
            i += i & -i

    def pre_max(self, i: int) -> int:
        f = self.f
        res = 0
        while i > 0:
            res = max(res, f[i])
            i &= i - 1
        return res

class Solution:
    def maxAlternatingSum(self, nums: list[int], k: int) -> int:
        # 离散化 nums
        sorted_nums = sorted(set(nums))

        n = len(nums)
        f_inc = [0] * n  # f_inc[i] 表示以 nums[i] 结尾且最后两项递增的交替子序列的最大和
        f_dec = [0] * n  # f_dec[i] 表示以 nums[i] 结尾且最后两项递减的交替子序列的最大和

        # 值域树状数组
        m = len(sorted_nums)
        inc = Fenwick(m + 1)  # 维护 f_inc[i] 的最大值
        dec = Fenwick(m + 1)  # 维护 f_dec[i] 的最大值

        for i, x in enumerate(nums):
            if i >= k:
                # 在这个时候才把 f_inc[i-k] 和 f_dec[i-k] 添加到值域树状数组中，从而保证转移来源的下标 <= i-k
                j = nums[i - k]
                inc.update(m - j, f_inc[i - k])  # m-j 可以把后缀变成前缀
                dec.update(j + 1, f_dec[i - k])

            j = bisect_left(sorted_nums, x)
            nums[i] = j  # 注意这里修改了 nums[i]，这样上面的 nums[i-k] 无需二分

            f_inc[i] = dec.pre_max(j) + x          # 计算满足 nums[i'] < x 的 f_dec[i'] 的最大值
            f_dec[i] = inc.pre_max(m - 1 - j) + x  # 计算满足 nums[i'] > x 的 f_inc[i'] 的最大值

        return max(max(f_inc), max(f_dec))  # 枚举子序列以 nums[i] 结尾
''',
    call='Solution().maxAlternatingSum([3, 5, 4, 2, 4], 2)',
    expect=9,
    skip=['nums[i] = j', 'while i < len(f)', 'i += i & -i', 'while i > 0', 'res = max(res, f[i])', 'i &= i - 1', 'return res', 'def __init__', 'self.f = ', 'f = self.f', 'res = 0', 'sorted_nums = sorted', 'n = len', 'f_inc = [0]', 'f_dec = [0]', 'm = len'],
    max_steps=100,
    views=[
        dict(type='text', fn=_fml, size=22, h=50),
        dict(type='array', var='nums', label='nums（处理过的被改成排名）', h=105, cell=70, pointers={OI: 'blue'}, pointer_labels={OI: 'i'}),
        dict(type='array', var='f_inc', label='f_inc', h=105, cell=70, pointers={OI: 'blue'}, pointer_labels={OI: 'i'}),
        dict(type='array', var='f_dec', label='f_dec', h=105, cell=70, pointers={OI: 'blue'}, pointer_labels={OI: 'i'}),
        dict(type='array', var=lambda S: S['inc'].f, label='inc', h=105, cell=70),
        dict(type='array', var=lambda S: S['dec'].f, label='dec', h=105, cell=70),
    ],
    watch=[('i', OI, 'blue'), ('x', 'x', 'pink'), ('j', 'j', 'cyan'), ('sorted', 'sorted_nums', 'green')],
    captions={
        'for i, x in enumerate': '枚举以 `nums[{i}] = {x}` 结尾的子序列',
        'if i >= k': lambda S, B, r: (f'`i = {S.i} ≥ k = {S.k}`：`nums[{S.i - S.k}]` 现在才有资格作转移来源' if S.i >= S.k else f'`i = {S.i} < k = {S.k}`：前面还没有距离够的元素，`f` 只能是自己'),
        'j = nums[i - k]': '`j` = `nums[{i-k}]` 的排名（已被改成排名）= =={j}==',
        'inc.update': '把 `f_inc[{B.i-B.k}] = {B.f_inc[B.i-B.k]}` 放进 `inc` 的位置 `m−j = {B.m-B.j}`：==后缀变前缀==',
        'dec.update': '把 `f_dec[{B.i-B.k}] = {B.f_dec[B.i-B.k]}` 放进 `dec` 的位置 `j+1 = {B.j+1}`',
        'j = bisect_left': '`x = {x}` 在 `sorted_nums` 里的排名 `j` = =={j}==；顺手把 `nums[{i}]` 改成排名（以后取 `nums[i-k]` 不用再二分）',
        'nums[i] = j': '`nums[{i}]` 改成排名 `{j}`，之后取 `nums[i-k]` 不用再二分',
        'f_inc[i] = dec.pre_max': _cap_fi,
        'f_dec[i] = inc.pre_max': _cap_fd,
        'return max': '以每个位置结尾的最大和取最大：=={ret}==',
        'while i < len(f)': lambda S, B, r: f'`update`：树状数组往上爬，`i = {S.i}`' if S.i < len(S.f) else '越界，结束',
        'f[i] = max(f[i], val)': lambda S, B, r: (f'树状数组位置 `{B.i}`：`max({B.f[B.i]}, {B.val})` = =={max(B.f[B.i], B.val)}==，' + (f'然后 `i += lowbit` 往上爬到 `{B.i + (B.i & -B.i)}`' if B.i + (B.i & -B.i) < len(B.f) else '再往上就越界了，结束')),
    },
    cards=dict(
        one_liner='f_inc / f_dec 两个 DP + 值域树状数组：每个 i 才放入 i−k，保证距离',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选下标间距 `≥ k` 的子序列，值严格交替（升降相间），求元素和最大',
                 '示例：`[3,5,4,2,4]`，`k=1` → `14`',
                 '本视频：`[3,5,4,2,4]`，`k=2` → `9`'],
        quote='对下标的限制，可以在遍历到 nums[i] 时，才把 f_inc[i-k] 和 f_dec[i-k] 添加到值域树状数组中，从而保证转移来源的下标 <= i-k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['类似 376 摆动序列：`f_inc[i]` 要接在「更小的 `f_dec[j]`」后面',
              '`f_dec` 的值域前缀最大值、`f_inc` 的值域后缀最大值 → 两个值域树状数组（后缀用 `m−j` 变前缀）',
              '先离散化；`i ≥ k` 时才把 `i−k` 放进树状数组'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '转移没有负数，树状数组维护前缀最大值就够用（不需要线段树）',
                 '代码把 `nums[i]` 原地改成排名，注意 `nums` 被修改',
                 '易错：`i−k` 延迟插入；`< x` 查前缀 `j`，`> x` 查 `m−1−j`'],
    ),
)
