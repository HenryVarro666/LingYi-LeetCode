_P_LINES = '21 <= _line <= 31'


def _row(S):
    if 'f' not in S:
        return None
    p = S.get('p', 0)
    return S['f'][p] if p < len(S['f']) else S['f'][0]


def _scolor(S, i, v):
    if S.get('_line') is not None and 18 <= S['_line'] <= 31 and i == len(S['s']) - 1:
        return 'orange'
    return None


def _fcolor(S, i, v):
    if v < 0:
        return 'red'
    if 'target' in S and S.get('_line') in (29, 30, 31) and i == S['target'] % 10:
        return 'green'
    return 'cyan' if v > 0 else None


def _txt(S):
    if 'm' not in S:
        return '和的位数不同，首位的判断方式也不同 → 每种位数（档）各用一个滑动窗口'
    ln = S['_line']
    if ln < 19 or ln > 32 or 'p' not in S or S['p'] >= S['m']:
        return f"一共 `m = {S['m']}` 档，档 `p` 管「和是 `p+1` 位数、首位是 x」的子数组"
    x, p = S['x'], S['p']
    lo, hi = x * S['p10'][p], (x + 1) * S['p10'][p] - 1
    t = f"；末位要找 `target = {S['target']}`" if ln in (29, 30, 31) and 'target' in S else ''
    return f'档 `p = {p}`：差 ∈ `[{lo}, {hi}]`（首位是 {x} 的 {p + 1} 位数）' + t


def _top(S, B, ret):
    if S.p < S.m and S.p10[S.p] * S.x <= S.s[-1]:
        return f'档 `p = {S.p}`：`x·10^p = {S.p10[S.p] * S.x} ≤ s[-1] = {S.s[-1]}`，这档的和可能存在 → 处理'
    return f'`x·10^p = {S.p10[S.p] * S.x} > s[-1] = {S.s[-1]}`：更高位的和不可能出现 → 这个右端点处理完'


def _w_right(S, B, ret):
    d = B.s[-1] - B.s[B.right[B.p]]
    need = B.x * B.p10[B.p]
    if d >= need:
        return f'`s[-1] − s[{B.right[B.p]}] = {d} ≥ x·10^p = {need}`：差够大 → ==进窗口=='
    return f'`s[-1] − s[{B.right[B.p]}] = {d} < {need}`：差还不够，后面的更不够'


def _w_left(S, B, ret):
    d = B.s[-1] - B.s[B.left[B.p]]
    need = (B.x + 1) * B.p10[B.p]
    if d >= need:
        return f'`s[-1] − s[{B.left[B.p]}] = {d} ≥ (x+1)·10^p = {need}`：首位超过 x → ==出窗口=='
    return f'`s[-1] − s[{B.left[B.p]}] = {d} < {need}`：首位还是 x，留在窗口里'


def _in(S, B, ret):
    R = B.right[B.p]
    d = B.s[R] % 10
    return f'`s[{R}] = {B.s[R]}` 末位 {d} 入窗口：`f[{B.p}][{d}]` → `{S.f[B.p][d]}`，`right[{B.p}]` 右移'


def _out(S, B, ret):
    L = B.left[B.p]
    d = B.s[L] % 10
    return f'`s[{L}] = {B.s[L]}` 末位 {d} 出窗口：`f[{B.p}][{d}]` → `{S.f[B.p][d]}`，`left[{B.p}]` 右移'


CONFIG = dict(
    num=3969, title='求和后首尾数字相同的有效子数组 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 按位数分层的滑动窗口',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
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
    call='Solution().countValidSubarrays([1, 10], 1)',
    expect=2,
    skip=['while p10[-1]', 'p10.append', 'right[p] += 1', 'left[p] += 1'],
    views=[
        dict(type='array', var='s', label='s 前缀和（框 = 当前档的窗口 s[left[p] .. right[p]-1]，橙 = 右端点 s[-1]）', cell=96,
             pointers={f'left[p] if {_P_LINES} else None': 'pink', f'right[p] if {_P_LINES} else None': 'blue'},
             pointer_labels={f'left[p] if {_P_LINES} else None': 'left[p]', f'right[p] if {_P_LINES} else None': 'right[p]'},
             window=(f'left[p] if {_P_LINES} else None', f'right[p] - 1 if {_P_LINES} else None'), color=_scolor, h=235),
        dict(type='array', var=_row, label='f[p][d]：当前档窗口里，前缀和末位是 d 的个数（绿 = 要查的 target）', cell=64, min_slots=10,
             color=_fcolor, h=130),
        dict(type='text', h=120, size=28, fn=_txt),
    ],
    watch=[('p', 'p', 'cyan'), ('s[-1]', 's[-1]', 'orange'), ('target', 'target', 'green'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`：每个数 ≤ 10^9，前缀和不会超过 `n × 10^9`',
        'p10 = [1]': '`p10` 存 10 的各次幂，预处理到超过和的上界 `n × 10^9`',
        'm = len(p10)': '`p10` 备好：`10^0` 到 `10^{m - 1}`，共 `m = {m}` 档；每档对应和的一种位数',
        'left = [0] * m': '每档一对窗口指针：`left[p]` 是左边界',
        'right = [0] * m': '`right[p]` 是右边界（不含），窗口 = `[left[p], right[p])`',
        'f = [[0] * 10': '`f[p][d]`：档 `p` 窗口里，前缀和末位为 `d` 的个数',
        's = [0]': '`s`：前缀和数组，先放一个空前缀 0',
        'res = 0': '`res`：有效子数组个数',
        'for v in nums': lambda S, B, r_: (f'读入 `v = {S.v}`' if 'v' not in B or S.v != B.v else '数组读完了'),
        's.append': '前缀和追加：当前右端点 `s[-1] = {s[-1]}`',
        'p = 0': '从最低的一档 `p = 0` 开始，逐档往上处理',
        'while p < m and': _top,
        'while s[-1] - s[right[p]]': _w_right,
        'f[p][s[right[p]] % 10] += 1': _in,
        'while s[-1] - s[left[p]]': _w_left,
        'f[p][s[left[p]] % 10] -= 1': _out,
        'target = s[-1] % 10 - x': '末位要对上：`target = {s[-1] % 10} − {x}` = `{target}`（差的末位是 x ⇔ 左边前缀末位为 target）',
        'if target < 0': lambda S, B, r_: ('`target < 0`：加 10 拉回 0~9' if S.target < 0 else f'`target = {S.target} ≥ 0`，不用调整（为负时要加 10）'),
        'target += 10': '`target` → `{target}`',
        'res += f[p][target]': '档 {p} 窗口里末位是 `{target}` 的有 `{f[p][target]}` 个 → `res` = =={res}==',
        'p += 1': '换到下一档 `p = {p}`',
        'return res': '返回 =={res}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='末位用哈希计数，首位用滑窗框出：每种位数一个窗口',
        complexity='时间 `O(n log S)`，空间 `O(n + 10 log S)`',
        problem=['`nums` 是正整数。子数组和的 ==首位== 与 ==末位== 都等于 `x`，就是有效子数组',
                 '求有效子数组个数；示例：`[1,100,1], x=1` → `4`',
                 '本视频：`[1,10], x=1` → `2`（`[1]` 和 `[1,10]`，和 1、11）'],
        quote='使用s[index]减去其中的元素，得到的差必然在x*10^k到(x + 1) * 10^k - 1之间，即最高位恰好为x。',
        quote_src='—— yiduobo 题解原文',
        idea=['拆成前缀和：每个右端点 `s[-1]`，数左边有多少个 `s[ℓ]` 让差的首位、末位都是 `x`',
              '末位：差模 10 为 `x` ⇔ `s[ℓ] % 10 = s[-1] % 10 − x`，用 `f[p][d]` 记次数',
              '首位：`s` 递增，差 ∈ `[x·10^p, (x+1)·10^p)` 的 `ℓ` 连成一段 → 每一档 `p` 一个窗口'],
        summary=['每个右端点最多处理 `log S` 档，指针只右移，总体 `O(n log S)`',
                 '先让 `right[p]` 放入够大的，再让 `left[p]` 踢出太大的，计数不会变负',
                 '`target = s[-1] % 10 − x` 可能为负，要加 10 回到 0~9',
                 '`p10` 预处理到超过 `n × 10^9`，保证覆盖最大的和',
                 '代码与原文一致，Python 3 可直接运行；同一思路也解 3972（II，数据范围更大）'],
    ),
)
