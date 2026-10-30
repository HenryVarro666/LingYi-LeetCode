def _win_left(S):
    if S.get('_line') in (10, 11) and 't' in S and S['t'] in S['pos'] and S['pos'][S['t']] < S['i']:
        return S['pos'][S['t']] + 1
    return None


def _parity_color(S, i, v):
    if 'i' not in S or i > S['i']:
        return None
    return 'orange' if v % 2 else 'blue'


def _txt(S):
    if 'i' not in S:
        return '`xor` = 前缀异或和，`diff` = 奇数个数 − 偶数个数；两个都相同的两个前缀，夹住的子数组就合法'
    ln = S['_line']
    head = f"`x = {S['x']}`（=={'奇' if S['x'] % 2 else '偶'}数==）"
    if ln <= 6:
        return head
    if ln in (7,):
        return head + f"：`xor = {S['xor']}`"
    if ln == 8:
        return head + f"：`xor = {S['xor']}`，`diff = {S['diff']}`"
    t = S['t']
    pos = S['pos']
    if ln == 13:
        return f'`t = {t}` 记入哈希表，首次出现下标 ==`{S["i"]}`=='
    if t in pos and pos[t] < S['i']:
        return f"`t = {t}` 在下标 {pos[t]} 出现过 → 子数组 `nums[{pos[t] + 1}..{S['i']}]` 异或为 0、奇偶个数相等"
    return f'`t = {t}`：哈希表里还没有这个二元组'


def _t_cap(S, B, ret):
    t, pos = S.t, S.pos
    if t in pos:
        return f'`{t}` 已在哈希表中（首次在下标 {pos[t]}）→ 前后两个前缀的 xor 和 diff ==都相同==，夹住的子数组合法'
    same_x = [k for k in pos if k[0] == t[0]]
    same_d = [k for k in pos if k[1] == t[1]]
    if same_x:
        return f'`{t}` 不在表里：虽然 xor 和 `{same_x[0]}` 相同，但 diff 不同 → ==两个条件缺一不可==，不算'
    if same_d:
        return f'`{t}` 不在表里：虽然 diff 和 `{same_d[0]}` 相同，但 xor 不同 → 不算'
    return f'`{t}` 第一次出现，不在哈希表里'


CONFIG = dict(
    num=3755, title='最大平衡异或子数组的长度', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表 · 二元组做 key',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def maxBalancedSubarray(self, nums: List[int]) -> int:
        ans = 0
        pos = {(0, 0): -1}  # 空前缀的位置视作 -1
        xor = diff = 0
        for i, x in enumerate(nums):
            xor ^= x
            diff += 1 if x % 2 else -1
            t = (xor, diff)
            if t in pos:
                ans = max(ans, i - pos[t])
            else:
                pos[t] = i
        return ans
''',
    call='Solution().maxBalancedSubarray([3,1,3,2,0])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（橙 = 奇数，蓝 = 偶数；框 = 当前找到的子数组）', cell=96, pointers={'i': 'blue'},
             window=(_win_left, 'i'), color=_parity_color, h=190),
        dict(type='map', var='pos', label='pos：(xor, diff) → 首次出现的下标', fmt=lambda k, v: f'{k} → {v}', h=190, font=30),
        dict(type='text', h=110, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('xor', 'xor', 'cyan'), ('diff', 'diff', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans = 0`：找不到合法子数组就返回 0',
        'pos = {': '`pos` 记录二元组 ==(xor, diff)== 首次出现的下标；空前缀 `(0, 0)` 位置视作 `-1`，这样从下标 0 开始的子数组也能算',
        'xor = diff = 0': '`xor`：前缀异或和；`diff`：奇数个数减偶数个数，都从空前缀的 0 开始',
        'for i, x': lambda S, B, r: (f'枚举下标 `i = {S.i}`，`x = {S.x}`' if 'i' in S and ('i' not in B or S.i != B.i)
                                     else '遍历完所有元素'),
        'xor ^= x': '`xor = {B.xor} ^ {x}` → =={xor}==：异或为 0 等价于两个前缀异或和相等',
        'diff += 1': lambda S, B, r: (f"`{S.x}` 是{'奇' if S.x % 2 else '偶'}数，视作 `{'+1' if S.x % 2 else '-1'}`："
                                      f"`diff` {B.diff} → =={S.diff}==（奇偶个数相等 ⇔ 前缀 diff 相等）"),
        't = (xor, diff)': '合成二元组 `t = ({xor}, {diff})`：两个条件要同时满足，所以整个二元组当 key',
        'if t in pos': _t_cap,
        'ans = max': '子数组长度 = `i − pos[t]` = `{i} − {pos[t]}` = `{i - pos[t]}`，`ans = max({B.ans}, {i - pos[t]})` → =={ans}==',
        'pos[t] = i': '首次出现：`pos[{t}] = {i}`。只记==第一次==的下标，以后用它算出来的子数组最长',
        'return ans': '遍历结束，最长平衡子数组长度为 =={ans}==',
    },
    cards=dict(
        one_liner='哈希表的 key 从 int 换成二元组 (异或和, 奇偶差)',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求最长子数组：异或和 ==等于 0==，且奇数、偶数个数 ==相等==',
                 '示例：`[3,1,3,2,0]` → `4`',
                 '`[1,3,2,0]`：`1^3^2^0 = 0`，2 个奇数 2 个偶数'],
        quote='本题有两个要求，把哈希表的 key 从 int 改成 pair 即可。为了计算子数组长度，用一个哈希表记录二元组 (xor, diff) 首次出现的位置。',
        quote_src='—— 灵茶山艾府题解（公式符号为引用时改写）',
        idea=['异或为 0：前缀异或和相等，`s[r] == s[l]`',
              '奇偶相等：奇数记 +1、偶数记 −1，前缀和 `diff` 相等（先做 525 连续数组）',
              '两个前缀量同时相等 → 二元组 `(xor, diff)` 当 key，保留首次下标'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '空前缀 `(0, 0)` 要先放进哈希表，位置记 `-1`',
                 '已有的 key ==不覆盖==：保留首次出现的下标，子数组才最长',
                 '只对上一个条件也不行：xor 相同但 diff 不同的前缀不能配对',
                 '相似题：3728、3714、2949（同样是多个状态拼成 key）'],
    ),
)
