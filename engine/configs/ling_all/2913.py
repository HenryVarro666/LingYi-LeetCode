CONFIG = dict(
    num=2913, title='子数组不同元素数目的平方和 I', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='按右端点分组 + lazy 线段树',
    tags=[],
    code='''
class Solution:
    def sumCounts(self, nums: List[int]) -> int:
        n = len(nums)
        sum = [0] * (n * 4)
        todo = [0] * (n * 4)

        def do(o: int, l: int, r: int, add: int) -> None:
            sum[o] += add * (r - l + 1)
            todo[o] += add

        # o=1  [l,r] 1<=l<=r<=n
        # 把 [L,R] 加一，同时返回加一之前的区间和
        def query_and_add1(o: int, l: int, r: int, L: int, R: int) -> int:
            if L <= l and r <= R:
                res = sum[o]
                do(o, l, r, 1)
                return res

            m = (l + r) // 2
            add = todo[o]
            if add:
                do(o * 2, l, m, add)
                do(o * 2 + 1, m + 1, r, add)
                todo[o] = 0

            res = 0
            if L <= m: res += query_and_add1(o * 2, l, m, L, R)
            if m < R:  res += query_and_add1(o * 2 + 1, m + 1, r, L, R)
            sum[o] = sum[o * 2] + sum[o * 2 + 1]
            return res

        ans = s = 0
        last = {}
        for i, x in enumerate(nums, 1):
            j = last.get(x, 0)
            s += query_and_add1(1, 1, n, j + 1, i) * 2 + i - j
            ans += s
            last[x] = i
        return ans % 1_000_000_007
''',
    call='Solution().sumCounts([1,2,1])',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums（线段树里的 i = 下标 + 1，是右端点）', pointers={}, h=110,
             color=lambda S, i, v: 'pink' if S.get('i') == i + 1 and S['_line'] >= 34 else None),
        dict(type='array', var=lambda S: S.get('sum'), label='sum（线段树：区间内「不同计数」之和）', h=110, cell=56,
             color=lambda S, i, v: 'yellow' if S.get('o') == i else None),
        dict(type='array', var='todo', label='todo（lazy 标记）', h=110, cell=56,
             color=lambda S, i, v: 'cyan' if v else None),
        dict(type='text', size=30, h=60, fn=lambda S: f"右端点 `i = {S['i']}`：`s` = 右端点为 i 的子数组「不同计数平方」之和 = =={S['s']}==，`ans` = =={S['ans']}==" if 'i' in S and 's' in S else ''),
        dict(type='calls', h=130),
    ],
    watch=['i', 'x', 'j', ('s', 's', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'j = last.get': '`{x}` 上次出现在 `j = {j}`（0 = 没出现过）→ 只有左端点在 `[{j+1}, {i}]` 的子数组会多一个新元素',
        'j + 1, i) * 2': '这些子数组的「不同计数」都 +1，平方和增加 `2x+1`，累加得 `s` = =={s}==',
        'if L <= m': '左半 `[{B.l},{B.m}]` 与要加的 `[{B.L},{B.R}]`：{"有交集 → 递归进左儿子" if B.L <= B.m else "无交集 → 跳过"}',
        'if m < R': '右半 `[{B.m+1},{B.r}]` 与要加的 `[{B.L},{B.R}]`：{"有交集 → 递归进右儿子" if B.m < B.R else "无交集 → 跳过"}',
        'do(o * 2, l': '把标记下推给左儿子：它的 `sum` 和 `todo` 都加上',
        'do(o * 2 + 1': '同样下推给右儿子',
        'ans += s': '右端点为 `{i}` 的所有子数组都算完了，`ans += s` → =={ans}==',
        'last[x] = i': '记下 `{x}` 最近出现的位置是 `{i}`',
        'res = sum[o]': '这一段整个落在 `[L,R]` 内：先取出旧的区间和 `{res}`',
        'do(o, l, r, 1)': '整段打 lazy 标记：这一段每个子数组的不同计数 +1',
        'sum[o] += add': '`sum[{o}]` 增加 `{add} × {r-l+1}`，变成 {sum[o]}',
        'zzz': '`todo[{o}] = {add}`：有没下推的标记 → {"先下推给左右儿子" if add else "没有标记，直接往下走"}',
        'sum[o] = sum[o * 2]': '回溯合并：`sum[{o}] = sum[{o*2}] + sum[{o*2+1}]` = {sum[o]}',
        'return ans': '答案对 `10^9+7` 取模，返回 =={ans % 1_000_000_007}==',
    },
    skip=['m = (l + r)', 'add = todo[o]', 'res = 0', 'todo[o] = 0', 'todo[o] += add', 'if add:'],
    max_steps=120,
    cards=dict(
        one_liner='右端点相同的分一组，每组的增量用线段树区间加一求出',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['子数组的「不同计数」= 里面不同值的个数，求所有子数组不同计数的平方和',
                 '示例：`[1,2,1]` → `15`',
                 '（本题 n 只有 100，灵神给的是能直接扩展到 II 的线段树做法）'],
        quote='右端点为 i 的子数组，可以看成是右端点为 i-1 的子数组，在末尾添加上 a[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['某个子数组不同计数从 x 变成 x+1，平方增量是 `(x+1)^2 - x^2 = 2x+1`',
              '`a[i]` 上次出现在 j，则左端点在 `[j+1, i]` 的子数组不同计数都 +1，其余不变',
              '线段树维护「每个左端点的不同计数」：区间加一，同时返回加一前的区间和'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '==线段树下标从 1 开始==，区间 `[j+1, i]` 与 `last` 默认值 0 对应',
                 '查询和更新同一个区间，所以一次递归同时完成',
                 '同类题：2262 字符串的总引力（简单版）；本题 n 小，也可以暴力枚举子数组'],
    ),
)
