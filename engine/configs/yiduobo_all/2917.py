def _tab(S):
    return [[x >> b & 1 for b in (3, 2, 1, 0)] for x in S['nums']]


def _col(S, r, c, v):
    if 'pow2' not in S or S['pow2'].bit_length() > 4:
        return None
    if c == 4 - S['pow2'].bit_length():
        if 'v' in S and S['nums'][r] == S['v'] and S['_line'] in (9, 10):
            return 'yellow'
        return 'green' if v else 'blue'
    return None


def _info(S):
    if 'pow2' not in S:
        return ''
    s = f'`pow2 = {S["pow2"]}`'
    if 'cnt' in S:
        s += f'，已数到 `cnt = {S["cnt"]}`，k = {S["k"]}'
    return s + f'；`res = {S.get("res", 0)}`'


CONFIG = dict(
    num=2917, title='找出数组中的 K-or 值', difficulty='Easy', category='位运算',
    author='yiduobo', technique='枚举 2 的幂 · 与运算计数',
    tags=['灵神题单', '位运算', '难度分 1389'],
    code='''
class Solution(object):
    def findKOr(self, nums, k):

        ma = max(nums)
        pow2 = 1
        res = 0
        while pow2 <= ma:
            cnt = 0
            for v in nums:
                if v & pow2 == pow2:
                    cnt += 1
            
            if cnt >= k:
                res += pow2
            
            pow2 += pow2
        
        return res
''',
    call='Solution().findKOr([7,15,9,8], 3)',
    expect=9,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='table', var=_tab, rows=lambda S: [str(x) for x in S['nums']], cols=['bit3', 'bit2', 'bit1', 'bit0'],
             color=_col, cell=80, h=420, label='nums 的二进制（当前 pow2 对应的那一列）'),
    ],
    watch=[('pow2', 'pow2', 'blue'), ('v', 'v', 'cyan'), ('cnt', 'cnt', 'yellow'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'ma = max': '`ma = {ma}`：枚举到 pow2 超过最大值就停（更高位全是 0）',
        'while pow2 <= ma': lambda S, B, r: (f'`pow2 = {S.pow2} <= ma = {S.ma}` → 检测这一位' if S.pow2 <= S.ma
                                             else f'`pow2 = {S.pow2} > ma = {S.ma}` → 所有位都检测完了'),
        'cnt = 0': '换到新的一位 `{pow2}`，计数清零',
        'for v in nums': lambda S, B, r: ('这一位的 4 个数都数完了' if 'v' in B and S.v == B.v else f'取下一个数 `v = {S.v}`'),
        'if v & pow2': lambda S, B, r: (f'`{S.v} & {S.pow2} = {S.v & S.pow2}` == pow2 → 这个数这一位是 1' if S.v & S.pow2 == S.pow2
                                        else f'`{S.v} & {S.pow2} = {S.v & S.pow2}` ≠ pow2 → 这一位是 0'),
        'cnt += 1': '这一位的 1 多了一个：`cnt = {cnt}`',
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} >= k = {S.k}` → 这一位算进答案' if S.cnt >= S.k
                                        else f'`cnt = {S.cnt} < k = {S.k}` → 这一位不够，不加'),
        'res += pow2': '`res += {pow2}` → `res = {res}`',
        'pow2 += pow2': '`pow2` 翻倍，换到下一位：`pow2 = {pow2}`',
        'return res': 'K-or = `{res}`',
    },
    cards=dict(
        one_liner='枚举每个 2 的幂，数有几个数这一位是 1',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['K-or：某一位上 ==至少有 k 个数是 1==，结果的这一位才是 1',
                 '例：`[7,12,9,8,9,15], k = 4` → `9`',
                 '本视频：`[7,15,9,8], k = 3` → `9`'],
        quote='直接枚举所有2的幂次pow2，然后对于当前枚举到的pow2，一趟遍历检测数组中有多少个数在这一位上为1。若存在至少k个数在这一位上为1，就将pow2累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pow2` 从 1 开始翻倍，代表第 0、1、2…位',
              '`v & pow2 == pow2` 判断 v 的这一位是不是 1',
              '数够 k 个就 `res += pow2`，直到 pow2 超过最大值'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`pow2 <= ma` 作为终止条件，不必固定枚举 31 位',
                 '`v & pow2 == pow2` 里 `==` 优先级低于 `&`，写法没问题',
                 '对比灵神：灵神用 `x >> i & 1` 取位并 `sum` 计数，思路相同'],
    ),
)
