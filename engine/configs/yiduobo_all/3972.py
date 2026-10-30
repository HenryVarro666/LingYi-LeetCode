def _win(S):
    if 'p' not in S or 'right' not in S or S.get('_inner', S).get('p') is None:
        return '前缀和 `s` 单调递增：每个位数 `p` 各维护一个窗口 + 个位计数表'
    p = S['p']
    r, l = S['right'][p], S['left'][p]
    s = S['s']
    return (f"`p = {p}`（差是 {p + 1} 位数）：下标 `[{l}, {r - 1}]` 的前缀和与 `s[-1] = {s[-1]}` 之差在"
            f" `[{S['x'] * S['p10'][p]}, {(S['x'] + 1) * S['p10'][p] - 1}]`，首位恰为 {S['x']}")


def _col(S, i, v):
    if 'p' not in S or 'right' not in S or S.get('p') is None or S['p'] >= len(S['right']):
        return None
    p = S['p']
    if S['left'][p] <= i < S['right'][p]:
        return 'green'
    return None


CONFIG = dict(
    num=3972, title='求和后首尾数字相同的有效子数组 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='前缀和 · 按位数滑动窗口 + 个位哈希计数', tags=[],
    code='''
class Solution(object):
    def countValidSubarrays(self, nums, x):

        n = len(nums)

        p10 = [1]
        while p10[-1] <= n * (10 ** 9):
            p10.append(p10[-1] * 10)

        m = len(p10)
        left = [0] * m
        right = [0] * m
        f = [[0] * 10 for _ in range(m)]
        s = [0]

        res = 0
        for v in nums:
            s.append(s[-1] + v)
            p = 0
            while p < m and p10[p] * x <= s[-1]:
                while s[-1] - s[right[p]] >= x * p10[p]:
                    f[p][s[right[p]] % 10] += 1
                    right[p] += 1
                while s[-1] - s[left[p]] >= (x + 1) * p10[p]:
                    f[p][s[left[p]] % 10] -= 1
                    left[p] += 1
                
                target = s[-1] % 10 - x
                if target < 0:
                    target += 10
                res += f[p][target]
                p += 1

        return res
''',
    call='Solution().countValidSubarrays([1, 5, 5, 1], 1)',
    expect=4,
    max_steps=110,
    skip=['p10.append', 'while p10[-1]', 'left = [0]', 'right = [0]', 'f = [[0]', 's = [0]', 'if target < 0', 'target += 10', 'right[p] += 1', 'left[p] += 1', 'p = 0', 'p += 1', 'n = len', 'target = s[-1]'],
    views=[
        dict(type='text', fn=_win, size=24),
        dict(type='array', var='nums', label='nums', cell=84, pointers={'len(s) - 2': 'blue'}, pointer_labels={'len(s) - 2': 'v'}, h=200),
        dict(type='array', var='s', label='前缀和 s（绿 = 当前位数 p 的窗口）', cell=84, color=_col, h=200),
        dict(type='text', fn=lambda S: (f"累计 `res = {S['res']}`" if 'res' in S else ''), size=28),
    ],
    watch=[('x', 'x', 'yellow'), ('p', 'p', 'blue'), ('s[-1]', 's[-1]', 'pink'), ('target', 'target', 'orange'), ('res', 'res', 'green')],
    captions={
        'p10 = [1]': '`p10[k] = 10^k`，用来给每个位数划界',
        'while p10[-1]': '前缀和最大不超过 `n * 10^9`，造够 10 的幂',
        'm = len': '`m = {m}` 种位数，每种位数各一组窗口 `left[p]`、`right[p]` 和计数表 `f[p]`',
        'left = [0]': '每个位数的窗口左端点',
        'right = [0]': '每个位数的窗口右端点',
        'f = [[0]': '`f[p][d]`：窗口内前缀和个位是 `d` 的个数',
        's = [0]': '前缀和从 `s[0] = 0` 开始',
        'res = 0': '`res` 统计有效子数组数',
        'for v in nums': lambda S, B, ret: (f'取 `v = {S.v}`' if S.get('v') is not None and S.v != B.get('v') else '遍历完了'),
        's.append': '新的前缀和 `s[-1] = {s[-1]}`：以它为右端点，向左数有多少个前缀和作差后首尾都是 `x`',
        'p = 0': '从 1 位数的差开始：`p = 0`',
        'while p < m': lambda S, B, ret: (f'`p = {S.p}`：`10^p * x = {S.p10[S.p] * S.x} <= s[-1] = {S.s[-1]}`，差有可能是 {S.p + 1} 位数，继续'
                                         if S.p < S.m and S.p10[S.p] * S.x <= S.s[-1] else '差已经不可能再多一位了，这个 `v` 处理完'),
        'while s[-1] - s[right[p]]': lambda S, B, ret: (f'`s[-1] - s[{S.right[S.p]}] = {S.s[-1] - S.s[S.right[S.p]]}` >= `x*10^p = {S.x * S.p10[S.p]}`：差首位 ≥ x，右端收进它'
                                                      if S.s[-1] - S.s[S.right[S.p]] >= S.x * S.p10[S.p] else '右端不再扩大了'),
        'f[p][s[right[p]]': '把 `s[right[p]]` 的个位 `{s[right[p]] % 10}` 计入 `f[p]`',
        'right[p] += 1': '`right[p]` → {right[p]}',
        'while s[-1] - s[left[p]]': lambda S, B, ret: (f'`s[-1] - s[{S.left[S.p]}] = {S.s[-1] - S.s[S.left[S.p]]}` >= `(x+1)*10^p = {(S.x + 1) * S.p10[S.p]}`：首位已超过 x，左端丢掉它'
                                                     if S.s[-1] - S.s[S.left[S.p]] >= (S.x + 1) * S.p10[S.p] else '左端不再收缩了，窗口里的差首位都恰好是 x'),
        'f[p][s[left[p]]': '把 `s[left[p]]` 的个位从 `f[p]` 里减掉',
        'left[p] += 1': '`left[p]` → {left[p]}',
        'target = s[-1] % 10': '差的个位要等于 `x`：窗口里前缀和的个位 = `(s[-1] % 10 - x) mod 10`',
        'if target < 0': lambda S, B, ret: ('个位相减不够减，借位：+10' if S.target < 0 else '`target >= 0`，不用借位'),
        'target += 10': '`target` → {target}',
        'res += f[p]': '个位要等于 `(s[-1] % 10 - x) mod 10 = {target}`：窗口内有 `{f[p][target]}` 个 → `res` = {res}',
        'p += 1': '换下一个位数 `p` → {p}',
        'return res': '所有位数、所有右端点累计 = =={ret}==',
    },
    cards=dict(
        one_liner='前缀和单调递增：按位数各开一个滑动窗口，个位用计数表',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['正整数数组 `nums` 和一位数 `x`；子数组和的==最高位和最低位都等于 x== 才算有效',
                 '数出有效子数组的个数；`n` 到 `10^5`，元素到 `10^9`',
                 '本视频：`nums = [1,5,5,1]`，`x = 1` → `4`'],
        quote='满足小于等于 s[index] - x * 10^k，同时大于 s[index] - (x + 1) * 10^k 的元素在 s 中必然是连续的一段，同时随着 index 的向右移动，这一段也会跟着向右移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['子数组和 = 两个前缀和之差；差的最低位用「模 10 的余数」哈希计数就能查',
              '最高位：`nums` 全是正数，`s` 递增，差落在 `[x·10^k, (x+1)·10^k)` 的前缀和是连续一段 → 滑动窗口',
              '差有 1 位、2 位、…各种位数：每种位数 `p` 各维护一个窗口和计数表'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`：位数只有 `log U` 种',
                 '只算「窗口内个位恰为 `s % 10 - x`」，借位用 `+ 10`',
                 '`p10[p] * x <= s[-1]` 才可能有 p+1 位的差，否则提前结束内层循环',
                 '原文已是 Python 3 可运行的写法，只是 `(10 ** 9)` 等未改',
                 '这一版只在一位数 `x` 时成立：首位和末位都等于 `x`'],
    ),
)
