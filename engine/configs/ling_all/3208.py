CONFIG = dict(
    num=3208, title='交替组 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='环形数组 · 维护交替段长度', tags=[],
    code='''
class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], k: int) -> int:
        n = len(colors)
        ans = cnt = 0
        for i in range(n + k - 1):
            if colors[i % n] == colors[(i + 1) % n]:
                cnt = 0
            cnt += 1
            if cnt >= k:
                ans += 1
        return ans
''',
    call='Solution().numberOfAlternatingGroups([0,1,0,0,1,0,1], 4)',
    expect=4,
    views=[
        dict(type='array', var='colors', label='colors（环）：蓝箭头 = i % n，黄格 = (i+1) % n', h=250,
             pointers={'i % n': 'blue'},
             color=lambda S, i, v: 'yellow' if 'i' in S and 'n' in S and i == (S['i'] + 1) % S['n'] else ('blue' if v == 1 else 'pink')),
        dict(type='text', fn=lambda S: (f"以下标 `{S['i']}`（即 `{S['i'] % S['n']}` 号）为右端点的交替段长度 cnt = =={S['cnt']}==，需要 k = {S['k']}" if 'cnt' in S and 'i' in S else ''), size=28, h=60),
    ],
    watch=['i', ('cnt', 'cnt', 'blue'), 'k', ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`，数组是环，下标用 `i % n` 取',
        'ans = cnt = 0': '`ans` 记答案，`cnt` 记以当前位置结尾的交替段长度',
        'for i in range': '一共 `n` 个起点，最后一个窗口到 `n+k-2`，所以循环到 `n + k - 2` 为止，==不会重复统计，无需判断 i >= n==。现在 `i = {i}`',
        'if colors[i % n]': lambda S, B, r: (f"`colors[{S.i % S.n}] = {S.colors[S.i % S.n]}`，`colors[{(S.i + 1) % S.n}] = {S.colors[(S.i + 1) % S.n]}`："
                                             + ('相同 → 交替被打断，`cnt` 清零' if S.colors[S.i % S.n] == S.colors[(S.i + 1) % S.n] else '不同 → 交替段可以延续')),
        'cnt = 0': '`cnt = 0`：下一步再 +1，新交替段从 1 开始',
        'cnt += 1': '`cnt` → =={cnt}==',
        'if cnt >= k': lambda S, B, r: (f"`cnt = {S.cnt}` {'>=' if S.cnt >= S.k else '<'} `k = {S.k}`" + ('：==有一个长 k 的交替子数组以此结尾==' if S.cnt >= S.k else '：还不够长')),
        'ans += 1': '`ans` → =={ans}==',
        'return ans': '共 `{ans}` 个交替组',
    },
    cards=dict(
        one_liner='环形数组不拼接，循环到 n+k-2，用取模取值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['0/1 数组 `colors` 围成环，连续 `k` 块颜色交替算一个交替组',
                 '求交替组个数',
                 '示例：`[0,1,0,0,1,0,1], k = 6` → `2`；本视频取 `k = 4`'],
        quote='把数组复制一份拼接起来，和 3101 题一样，遍历数组的同时，维护以 i 为右端点的交替子数组的长度 cnt。代码实现时，不需要复制数组，而是用 i mod n 的方式取到对应的值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['维护以 `i` 为右端点的交替段长度 `cnt`：相邻同色就清零',
              '写法二：共 `n` 个窗口，右端点从 `k-1` 到 `n+k-2`，==循环到 n+k-2 就不重复==',
              '`cnt >= k` 说明以 `i` 结尾的长 k 窗口是交替的'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '写法一：循环 `2n` 次并判断 `i >= n` 避免重复；写法二改为循环到 `n+k-2`，更简洁',
                 '易错：比较的是 `colors[i % n]` 与 `colors[(i + 1) % n]`，相同时 `cnt` 清零后还要再 +1',
                 '相似题：503 下一个更大元素 II（同样用取模处理环）'],
    ),
)
