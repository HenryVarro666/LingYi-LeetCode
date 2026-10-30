def _a(S):
    a = S.get('a')
    if a is None:
        return ''
    if not a:
        return '`a = []`（LCM 集合为空）'
    return '`a` = ' + '，'.join(f"[LCM ==`{p[0]}`==，右端点 `{p[1]}`]" for p in a)


CONFIG = dict(
    num=2470, title='最小公倍数等于 K 的子数组数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='LCM 集合 + 原地去重',
    tags=['灵神题单'],
    code='''
class Solution:
    def subarrayLCM(self, nums: List[int], k: int) -> int:
        ans = 0
        a = []  # [LCM，相同 LCM 区间的右端点]
        i0 = -1
        for i, x in enumerate(nums):
            if k % x:  # 保证后续求的 LCM 都是 k 的因子
                a = []
                i0 = i
                continue
            a.append([x, i])
            # 原地去重，因为相同的 LCM 都相邻在一起
            j = 0
            for p in a:
                p[0] = lcm(p[0], x)
                if a[j][0] != p[0]:
                    j += 1
                    a[j] = p
                else:
                    a[j][1] = p[1]
            del a[j + 1:]
            if a[0][0] == k:
                ans += a[0][1] - i0
        return ans
''',
    setup='from math import lcm',
    call='Solution().subarrayLCM([3, 6, 2, 7, 1], 6)',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（k = 6；红 = 不是 k 的因子）', pointers={'i': 'blue', 'i0': 'pink'}, h=170,
             color=lambda S, i, v: ('red' if 6 % v else None)),
        dict(type='text', fn=_a, size=32, h=110),
        dict(type='text', fn=lambda S: f"`i0 = {S['i0']}`：最近一个 ==不是 k 的因子== 的位置" if 'i0' in S else '', size=30, h=70),
    ],
    watch=['i', 'x', ('i0', 'i0', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'a = []  #': '`a` 里存 [LCM, 右端点]：以当前位置结尾的子数组，按 LCM 分组',
        'i0 = -1': '`i0` 记录最近的“非 k 因子”位置，这之后的子数组才可能合法',
        'if k % x': lambda S, B, r: (f'`k % x = {6 % S.x}`≠0：`{S.x}` 不是 `k` 的因子，含它的子数组 LCM 必定不是 k 的因子' if 6 % S.x
                                     else f'`{S.x}` 是 `k` 的因子，可以继续'),
        'a = []': '清空 `a`：之前的子数组都跨过了这个坏数',
        'i0 = i': '`i0 = {i}`：以后合法子数组的左端点必须在 `{i}` 右边',
        'continue': '跳过，处理下一个数',
        'a.append': '新增只含 `{x}` 的子数组，LCM = `{x}`，右端点 `{i}`',
        'j = 0': '`j` 是去重后的写指针：相同 LCM 都相邻，合并成一组',
        'p[0] = lcm': '每个子数组的 LCM 并入 `{x}`：`p[0] = {p[0]}`（LCM 要么不变，要么至少 ×2，所以组数 ≤ log k）',
        'if a[j][0] != p[0]': lambda S, B, r: (f'`a[{S.j}]` 的 LCM = `{S.a[S.j][0]}` 与当前 `{S.p[0]}` ' + ('不同 → 开新组' if S.a[S.j][0] != S.p[0] else '相同 → 合并到同一组')),
        'j += 1': '开新组：写指针 `j = {j}`',
        'a[j] = p': '把 `p` 放到第 `{j}` 组',
        'a[j][1] = p[1]': '同 LCM：右端点更新为更靠右的 `{p[1]}`',
        'del a[j + 1:]': '删掉合并后多余的尾部，`a` 只剩 `{j + 1}` 组',
        'if a[0][0] == k': lambda S, B, r: (f'`a[0]` 的 LCM = `{S.a[0][0]}`' + ('，等于 k' if S.a[0][0] == S.k else '，不等于 k') + '（最长的子数组 LCM 最小，所以只看第一组）'),
        'ans += a[0][1] - i0': '第一组左端点在 `({i0}, {a[0][1]}]` 内都合法：`ans += {a[0][1]} − {i0}` → {ans}',
    },
    cards=dict(
        one_liner='右端点固定，左端点按 LCM 分组：LCM 每次变化至少翻倍，组数 ≤ log k',
        complexity='时间 `O(n log k)`，空间 `O(log k)`',
        problem=['统计 `nums` 中 ==最小公倍数恰为 k== 的非空连续子数组个数',
                 '示例：`[3,6,2,7,1]`，`k = 6` → `4`'],
        quote='最小公倍数要么不变，要么至少 ×2，因此在遍历 nums 的同时，维护最小公倍数集合（数组），这至多有 O(log k) 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历右端点 `i`，维护“以 i 结尾的子数组的 LCM 分组”',
              '`x` 不是 `k` 的因子：之前的全部作废，记下 `i0`',
              '分组按 LCM 从小到大排，==第一组 LCM 最小==，等于 k 才有贡献',
              '贡献 = 第一组右端点 − `i0`'],
        summary=['时间 `O(n log k)`，空间 `O(log k)`',
                 '先判 `k % x`，保证所有 LCM 都是 k 的因子，不会过大',
                 '合并时同 LCM 的右端点取最右',
                 '方法一：双重循环枚举 + `k % res` 剪枝，`O(n(n+log k))`',
                 '同类题：2447 最大公因数等于 K 的子数组数目'],
    ),
)
