def _bits(S, v, w=6):
    return format(v, f'0{w}b')


CONFIG = dict(
    num=2869, title='收集元素的最少操作次数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='倒序遍历 + 位集合',
    tags=[],
    code='''
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        u = (2 << k) - 2  # 1~k
        s, n = 0, len(nums)
        for i in range(n - 1, -1, -1):
            s |= 1 << nums[i]
            if (s & u) == u:
                return n - i
''',
    call='Solution().minOperations([3,1,5,4,2], 2)',
    expect=4,
    views=[
        dict(type='text', size=28, fn=lambda S: f"目标集合 `u` = =={_bits(S, S['u'])}== （第 1 ~ {S['k']} 位为 1）" if 'u' in S else ''),
        dict(type='text', size=28, fn=lambda S: f"已收集 `s`  = =={_bits(S, S['s'])}== （第 x 位为 1 表示收集到了 x）" if 's' in S and isinstance(S['s'], int) else ''),
        dict(type='text', size=26, fn=lambda S: f"`s & u` = `{_bits(S, S['s'] & S['u'])}`，{'==等于 u，齐了==' if (S['s'] & S['u']) == S['u'] else '还不等于 u，继续'}" if 'u' in S and isinstance(S.get('s'), int) and S['_line'] >= 7 else ''),
        dict(type='array', var='nums', label='nums（从右往左删：蓝 = 当前 i，灰 = 已删除）', pointers={'i': 'blue'}, h=260,
             color=lambda S, j, v: 'blue' if S.get('i') == j else None,
             dim=lambda S, j, v: 'i' in S and j > S['i']),
    ],
    watch=[('i', 'i', 'blue'), ('u', 'u'), ('s', 's', 'green'), ('n', 'n')],
    captions={
        'u = (2 << k) - 2': '`u = (2 << {k}) - 2 = {u}`，二进制 `{u:b}`：==第 1 到 {k} 位都是 1== → 目标集合 {{1..{k}}}',
        's, n = 0, len(nums)': '`s` 是已收集的集合，初始为空；`n = {n}`',
        'for i in range': '倒序遍历：从最后一个元素往前「删」，`i = {i}`',
        's |= 1 << nums[i]': '把 `{nums[i]}` 加入集合：第 `{nums[i]}` 位置 1 → `s = {s:b}`',
        'if (s & u) == u': lambda S, B, r: (f'`s & u = {S.s & S.u:b}` 等于 `u = {S.u:b}` → ==1 到 {S.k} 都收集齐了== ，不用再删'
                                           if (S.s & S.u) == S.u else f'`s & u = {S.s & S.u:b}` ≠ `u = {S.u:b}` → 还缺元素，继续往前删'),
        'return n - i': '删掉了下标 `{i}` 到 `{n - 1}` 共 `{n} − {i}` = =={ret}== 个元素',
    },
    cards=dict(
        one_liner='倒着数，用一个整数的位当集合，齐了就返回',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作删除数组最后一个元素，加入集合', '求收集齐 `1, 2, …, k` 的最少操作次数',
                 '示例：`[3,1,5,4,2]`，`k = 2` → `4`', '删掉 2、4、5、1 后集合里有 1 和 2，不必再删 3'],
        quote='倒序遍历。由于元素范围在 [1,50]，我们可以用一个 64 位整数表示集合，只要集合中有 1 到 k 就立刻返回。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删最后一个 = 从右往左遍历，第一次凑齐 `1~k` 时的 `n - i` 就是答案',
              '元素 ≤ 50，用整数 `s` 的第 `x` 位表示「收集到了 x」，`s |= 1 << x`',
              '目标 `u = (2 << k) - 2` 是第 1 到 k 位全为 1；`(s & u) == u` 判断是否收集齐'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`(2 << k) - 2` = `2^(k+1) - 2`：低 k+1 位全 1，再去掉第 0 位',
                 '易错：判断要写 `(s & u) == u`，括号不能省（`==` 优先级高于 `&`）',
                 '大于 k 的元素也会被 `1 << x` 记进 `s`，但 `& u` 会把它们过滤掉',
                 '题目保证能收集齐，所以循环里一定会 `return`'],
    ),
)
