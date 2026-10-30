CONFIG = dict(
    num=3980, title='变换二进制字符串的最少操作次数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='从左到右贪心 · 操作右边',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1846'],
    code='''
class Solution:
    def minOperations(self, s1: str, t: str) -> int:
        n = len(s1)
        if n == 1 and s1 == "1" and t == "0":
            return -1

        # 也可以用一个布尔变量表示 s1[i] 是否操作过，从而做到 O(1) 空间，见 Python3 写法二
        s = list(s1)
        ans = 0
        for i in range(n):
            if s[i] == t[i]:
                continue
            if s[i] == '0':
                ans += 1
            elif i < n - 1 and s[i + 1] == '1':
                ans += 1
                s[i + 1] = '0'
            else:
                ans += 2
        return ans
''',
    call="Solution().minOperations('0110100', '1001001')",
    expect=6,
    views=[
        dict(type='array', var='s', label='s（当前被改动的串）', h=200, cell=80, pointers={'i': 'blue'},
             color=lambda S, k, v: ('green' if 'i' in S and k < S['i'] else None)),
        dict(type='string', var='t', label='t（目标）', h=200, cell=80, pointers={'i': 'blue'}),
        dict(type='text', h=70, size=26, fn=lambda S: (
            f"`s[{S['i']}] = {S['s'][S['i']]}`，`t[{S['i']}] = {S['t'][S['i']]}`" + (' → ==相同，不用改==' if S['s'][S['i']] == S['t'][S['i']] else ' → ==不同，要操作==')) if 'i' in S and 's' in S and S['i'] < len(S['s']) else '从左到右，一位一位把 s 变成 t'),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'if n == 1': '只有 1 位且 `1 → 0`：操作二要两个相邻的 1，没法做 → 返回 -1；其余情况一定有解',
        's = list(s1)': '转成列表：后面会把 `s[i+1]` 改成 0',
        'if s[i] == t[i]': lambda S, B, r: (f'`s[{S.i}] = t[{S.i}] = {S.t[S.i]}` → ==不用改==，继续向右' if S.s[S.i] == S.t[S.i]
                                            else f'`s[{S.i}] = {S.s[S.i]}` ≠ `t[{S.i}] = {S.t[S.i]}` → 必须操作'),
        "if s[i] == '0'": lambda S, B, r: (f'`s[{S.i}]` 是 0、`t[{S.i}]` 是 1 → 操作一直接把它变 1，==1 次==' if S.s[S.i] == '0'
                                           else f'`s[{S.i}]` 是 1、要变成 0 → 只能靠操作二，需要一个相邻的 1'),
        "elif i < n - 1": lambda S, B, r: (f'`s[{S.i + 1}] = 1`：和右边这个 1 一起用操作二，==操作右边不操作左边== → 成立' if S.i < S.n - 1 and S.s[S.i + 1] == '1'
                                           else ('右边是 0，要先用操作一把它变成 1，再一起变 0 → 不成立，共 2 次' if S.i < S.n - 1
                                                 else '已经是最后一位，右边没有了，只能动左边 → 共 2 次')),
        'ans += 1': '`ans = {ans}`：操作 1 次',
        "s[i + 1] = '0'": '操作二把 `s[{i+1}]` 一并变成 0：下一轮它如果 ≠ `t[{i+1}]`，就是 0→1 再操作 1 次',
        'ans += 2': '`ans = {ans}`：操作 2 次（先造出一个相邻的 1，再一起清零）',
        'return ans': '最少操作次数 =={ret}==',
    },
    cards=dict(
        one_liner='从左到右贪心：要动就动右边，不动左边',
        complexity='时间 `O(n)`，空间 `O(n)`（可优化为 `O(1)`）',
        problem=['两个等长二进制串 `s1`、`t`，两种操作：',
                 '① 把一个 `0` 变 `1`；② 把相邻两个 `11` 一起变 `00`',
                 '求 `s1` 变成 `t` 的最少操作次数，不可能则 -1',
                 '示例：`s1 = "01"`, `t = "10"` → `3`'],
        quote='操作左边，必须操作 2 次，而且 s[i+1] 还没改。操作右边不比操作左边差，无脑操作右边即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右，`s[i] = t[i]` 不动；`0 → 1` 直接操作一',
              '`1 → 0` 且右边是 1：操作二一次搞定，顺便把 `s[i+1]` 改成 0',
              '右边是 0 或到末尾：补一次操作一再操作二，共 2 次'],
        summary=['时间 `O(n)`；用一个布尔变量记「`s[i]` 是否被前一步改过」可做到空间 `O(1)`（写法二）',
                 '易错：`n = 1` 且 `s = 1, t = 0` 要返回 -1（示例 3）',
                 '易错：操作二改了 `s[i+1]` 后，下一轮要按新值比较',
                 '为什么不操作左边：左边要 2 次，而且右边还没处理'],
    ),
)
