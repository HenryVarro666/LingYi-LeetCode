def _tab(S):
    return [[x >> b & 1 for b in (3, 2, 1, 0)] for x in S['nums']]


def _col(S, r, c, v):
    if 'i' not in S:
        return None
    if c == 3 - S['i']:
        return 'green' if v else 'blue'
    return None


def _info(S):
    if 'i' not in S:
        return ''
    i = S['i']
    s = f'第 `{i}` 位（值 {1 << i}）'
    if 'cnt1' in S and S['_line'] != 4:
        s += f'：有 ==%d== 个数这一位是 1，k = {S["k"]}' % S['cnt1']
    ans = S.get('ans', 0)
    return s + f'；`ans = {ans:04b}`'


CONFIG = dict(
    num=2917, title='找出数组中的 K-or 值', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='枚举比特位 · 统计 1 的个数',
    tags=['灵神题单', '位运算', '难度分 1389'],
    code='''
class Solution:
    def findKOr(self, nums: List[int], k: int) -> int:
        ans = 0
        for i in range(max(nums).bit_length()):
            cnt1 = sum(x >> i & 1 for x in nums)
            if cnt1 >= k:
                ans |= 1 << i
        return ans
''',
    call='Solution().findKOr([7,12,9,8,9,15], 4)',
    expect=9,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='table', var=_tab, rows=lambda S: [str(x) for x in S['nums']], cols=['bit3', 'bit2', 'bit1', 'bit0'],
             color=_col, cell=70, h=520, label='nums 的二进制（每行一个数，每列一个比特位）'),
    ],
    watch=[('i', 'i', 'blue'), ('cnt1', 'cnt1', 'cyan'), ('k', 'k', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'for i in range': lambda S, B, r: ('`max(nums) = 15` 有 4 个比特位，所以只枚举 `i = 0..3`（更高位全是 0，不可能 >= k）' if 'i' not in B
                                           else '4 个比特位都枚举完了，退出循环' if S.i == B.i else f'换到第 `{S.i}` 位'),
        'cnt1 = sum': '看第 `{i}` 位这一列：1 的个数 `cnt1 = {cnt1}`',
        'if cnt1 >= k': lambda S, B, r: (f'`cnt1 = {S.cnt1} >= k = {S.k}` → 这一位够多，K-or 的这一位是 ==1==' if S.cnt1 >= S.k
                                         else f'`cnt1 = {S.cnt1} < k = {S.k}` → 这一位不够多，K-or 的这一位是 0，跳过'),
        'ans |= 1 << i': '把 `2^{i}` 加进答案：`ans |= 1 << {i}` → `ans = {ans}`（二进制 {bin(ans)[2:]}）',
        'return ans': '各位拼起来：K-or = `{ans}`',
    },
    cards=dict(
        one_liner='拆位：每个比特位单独数 1 的个数，够 k 个就置位',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['K-or：某一位上 ==至少有 k 个数是 1==，结果的这一位才是 1',
                 'k = 1 时就是普通的按位或；k = n 时就是按位与',
                 '本视频：`[7,12,9,8,9,15], k = 4` → `9`'],
        quote='由于数组元素值 < 2^31，我们枚举 0 到 30 的每个比特位。遍历数组，如果第 i 个比特位上的 1 的个数 ≥ k，则把 2^i 加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['各个比特位互不影响，所以可以一位一位单独算',
              '`x >> i & 1` 取出 x 的第 i 位，`sum` 就是这一位 1 的个数',
              '上界用 `max(nums).bit_length()`，比固定枚举 31 位更省'],
        summary=['时间 `O(n log U)`，U 为 `max(nums)`；空间 `O(1)`',
                 '`x >> i & 1` 的优先级：先移位再与，不用加括号',
                 '用 `ans |= 1 << i` 置位，不要写成 `ans += i`',
                 '同类：拆位思想可用于很多位运算题'],
    ),
)
