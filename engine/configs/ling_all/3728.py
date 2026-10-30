def _r(S):
    if 'x' not in S or 'last' not in S:
        return None
    a = S['capacity']
    for r in range(1, len(a)):
        if a[r] == S['x'] and a[r - 1] == S['last'] and sum(a[:r]) in (S['s'], S['s'] - S['x']):
            return r
    return None


CONFIG = dict(
    num=3728, title='边界与内部和相等的稳定子数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表（二元组计数）',
    tags=['灵神题单·常用数据结构', '难度分 1909'],
    code='''
class Solution:
    def countStableSubarrays(self, capacity: List[int]) -> int:
        cnt = defaultdict(int)
        s = capacity[0]  # 前缀和
        ans = 0
        for last, x in pairwise(capacity):
            ans += cnt[(x, s)]
            cnt[(last, last + s)] += 1
            s += x
        return ans
''',
    call='Solution().countStableSubarrays([9,3,3,3,9])',
    expect=2,
    views=[
        dict(type='array', var='capacity', label='capacity（蓝 = 右端点 r，粉 = 刚加入哈希表的 l）', h=190,
             color=lambda S, i, v: 'blue' if i == _r(S) else ('pink' if _r(S) is not None and i == _r(S) - 1 else None),
             pointers={_r: 'blue'}, pointer_labels={_r: 'r'}),
        dict(type='map', var='cnt', label='cnt：左端点的 (capacity[l], capacity[l]+s[l+1]) → 个数',
             fmt=lambda k, v: f'{k}: {v}', h=250, font=30),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"右端点 `r={_r(S)}`：要找 `(x, s) = ({S['x']}, {S['s']})`" if _r(S) is not None else '')),
    ],
    watch=['s', 'last', 'x', ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 统计左端点的二元组 `(capacity[l], capacity[l] + s[l+1])` 出现次数',
        's = capacity[0]': '`s` 是前缀和，先放入 `capacity[0]` = {s}；之后循环里 `s` 始终是 `capacity[0..r-1]` 的和',
        'ans +=': '右端点是 `{x}`：找有多少个左端点的二元组等于 `({x}, {s})` → 加 `{cnt[(x, s)]}`，`ans` = =={ans}==',
        'cnt[(last': '再把 `last = {last}` 当作后面右端点的左端点：存入 `({last}, {last + s})`，现在这个键出现 `{cnt[(last, last + s)]}` 次',
        's += x': '前缀和包含进 `x`：`s = {s}`（先查询再入表，保证长度至少是 3）',
        'return ans': '共 =={ans}== 个稳定子数组',
    },
    cards=dict(
        one_liner='首尾相等 + 中间和等于首元素 → 二元组配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组长度至少 3，首尾元素都等于中间所有元素的和，叫“稳定”',
                 '数一共有多少个稳定子数组',
                 '示例：`[9,3,3,3,9]` → 2（整个数组和 `[3,3,3]`）'],
        quote='枚举 r，用哈希表维护左边的 (capacity[l], capacity[l]+s[l+1]) 的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['式子等价于 `capacity[l] = capacity[r]` 且 `capacity[l] + s[l+1] = s[r]`',
              '枚举右端点 `r`，哈希表里存左端点的二元组，直接查 `(capacity[r], s[r])`',
              '先查询再把 `r−1` 入表，自然保证长度 ≥ 3'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：查询在前、入表在后，否则会把长度 2 的子数组也算进来',
                 '易错点：`s` 的含义随循环变化，进循环时是 `capacity[0..r-1]` 的和',
                 '思考：最小长度改成 k，只需延迟 k−2 步入表',
                 '前置题：560 和为 K 的子数组'],
    ),
)
