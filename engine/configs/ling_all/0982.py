def _w(S):
    return max(1, (S['u'] - 1).bit_length()) if 'u' in S else 2


def _bin(S):
    if 'u' not in S:
        return ''
    w = _w(S)
    u = S['u']
    if 'm' in S and 'x' in S and S['_line'] >= 11:
        m = S['m']
        out = f"全集 `{u - 1:0{w}b}`：补集 `m` = `{m:0{w}b}`"
        if 's' in S and S['_line'] >= 13:
            out += f'，当前子集 `s` = ==`{S["s"]:0{w}b}`=='
        return out
    return f"全集 `u - 1` = `{u - 1:0{w}b}`（`nums` 最大值的位数）"


def _sp(S):
    return S.get('s') if S['_line'] >= 12 else None


CONFIG = dict(
    num=982, title='按位与为零的三元组', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='枚举补集的子集 + 计数',
    tags=['位运算'],
    code='''
class Solution:
    def countTriplets(self, nums: List[int]) -> int:
        u = 1
        for x in nums:
            while u <= x:
                u <<= 1
        cnt = [0] * u
        cnt[0] = len(nums)  # 直接统计空集
        for m in nums:
            m ^= u - 1
            s = m
            while s:  # 枚举 m 的非空子集
                cnt[s] += 1
                s = (s - 1) & m
        return sum(cnt[x & y] for x in nums for y in nums)
''',
    call='Solution().countTriplets([2, 1, 3])',
    expect=12,
    views=[
        dict(type='text', fn=_bin, size=28, h=70),
        dict(type='array', var='nums', label='nums', cell=84, h=150),
        dict(type='array', var='cnt', label='cnt[v]：有多少个 nums[k]，其补集包含 v 作为子集', cell=84, h=190,
             pointers={_sp: 'blue'}, pointer_labels={_sp: 's'},
             color=lambda S, i, v: 'green' if v > 0 else None),
    ],
    watch=[('u', 'u', 'cyan'), ('m', 'm', 'purple'), ('s', 's', 'blue')],
    captions={
        'u = 1': '`u` 是大于所有 `nums[i]` 的最小 2 的幂，全集就是 `u - 1`，不用开 `2^16` 那么大',
        'while u <= x': lambda S, B, r: (f'`u = {S.u} <= x = {S.x}`：位数不够，`u` 左移' if S.u <= S.x else f'`u = {S.u} > x = {S.x}`：够了，看下一个数'),
        'u <<= 1': '`u` 翻倍 → `{u}`',
        'cnt = [0] * u': '`cnt` 长 `{u}`，`cnt[v]` 记「有多少个 `nums[k]` 与 `v` 按位与为 0」',
        'cnt[0] = len': '`v = 0` 与任何数 AND 都是 0：`cnt[0] = {len(nums)}`',
        'for m in nums': '枚举每个 `nums[k]`：取下一个（取完则结束）',
        'm ^= u - 1': '`m` = `nums[k]` 的补集：`{B.m} ^ {u - 1} = {m}`。`x & y` 要与 `nums[k]` 无交集，必须是 `m` 的子集',
        's = m': '从 `m` 自己开始枚举子集：`s = {s}`',
        'while s': lambda S, B, r: (f'`s = {S.s} != 0`：还有非空子集' if S.s else '`s = 0`：子集枚举完（空集已在 `cnt[0]` 里统计）'),
        'cnt[s] +=': '`s = {s}` 是 `m` 的子集：`cnt[{s}]` 加一 → {cnt[s]}',
        's = (s - 1) & m': '`s - 1` 把最低位 1 变成 0、低位补 1，再 `& m` 直接跳到下一个子集：`s = {s}`',
        'return sum': '枚举 `x & y`（9 对），累加 `cnt[x & y]`：每个 `x & y` 能配多少个 `k` → ==`{ret}`== 个三元组',
    },
    cards=dict(
        one_liner='三个数 AND 为 0：先算两个，再数第三个的补集子集',
        complexity='时间 `O(n(n+U))`，空间 `O(U)`（`U` 为 `max(nums)`）',
        problem=['数组 `nums`，数有多少下标三元组 `(i, j, k)`（可重复）满足 `nums[i] & nums[j] & nums[k] == 0`',
                 '示例：`[2,1,3]` → `12`；`[0,0,0]` → `27`',
                 '`n ≤ 1000`，`nums[i] < 2^16`，暴力 `O(n^3)` 不行'],
        quote='把二进制数看成集合……`a AND b = 0` 相当于集合 A 和集合 B 没有交集，也可以理解成 B 是 A 补集的子集。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums[k]` 只关心「`x & y` 与它 AND 是否为 0」，所以只需知道 `x & y` 的值',
              '反过来：对每个 `nums[k]`，把它补集的所有子集 `s` 的 `cnt[s]` 加一',
              '子集枚举：`s = (s - 1) & m`，直接跳到下一个子集；最后对每个 `x & y` 查 `cnt`'],
        summary=['时间 `O(n(n+U))`：枚举 `x, y` 是 `n^2`，枚举子集总数不超过 `n·U`',
                 '易错点：`s = 0`（空集）要单独算：`cnt[0] = len(nums)`，循环里写 `while s`',
                 '全集用 `u - 1`（最大数的位数），比固定 `0xffff` 快很多',
                 '题解还给了：哈希表计数 `x & y` 再枚举 key，和固定 `2^16` 的子集枚举写法'],
    ),
)
