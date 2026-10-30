CONFIG = dict(
    num=4049, title='统计等间距出现整数数目 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + pairwise 判等差',
    code='''
class Solution:
    def countSpecialIntegers(self, nums: list[int]) -> int:
        pos = defaultdict(list)
        for i, x in enumerate(nums):
            pos[x].append(i)

        ans = 0
        for p in pos.values():
            if len(p) < 3:
                continue
            d = p[1] - p[0]
            if all(y - x == d for x, y in pairwise(p)):
                ans += 1
        return ans
''',
    call='Solution().countSpecialIntegers([1,8,1,5,1,5,8,5,8,3,3,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=170, cell=70,
             color=lambda S, k, v: 'green' if 'i' in S and k == S['i'] else None),
        dict(type='map', var='pos', label='pos[x] = x 的所有出现下标', fmt=lambda k, v: f'{k}: {v}', h=260, font=32),
        dict(type='text', size=30, h=70, fn=lambda S: (
            f"`p = {S['p']}`，公差 `d = {S['d']}`" if 'p' in S and 'd' in S and len(S['p']) >= 3 else
            (f"`p = {S['p']}`：不足 3 次，排除" if 'p' in S and len(S['p']) < 3 else '先收集位置，再逐个检查'))),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('p', 'p', 'orange'), ('d', 'd', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'pos = defaultdict': '`pos[x]` 存数 x 出现过的全部下标',
        'for i, x in enumerate': lambda S, B, ret: (f'看 `nums[{S.i}] = {S.x}`' if 'i' not in B or S.i != B.i else '位置都收集完了'),
        'pos[x].append': '把下标 `{i}` 记到 `pos[{x}]`：现在是 `{pos[x]}`',
        'ans = 0': '位置收集完毕，逐个检查是否等间隔',
        'for p in pos.values()': lambda S, B, ret: ('所有数都检查完了' if 'p' in B and S.p == B.p else f'检查下一个数的位置列表 `p = {S.p}`'),
        'if len(p) < 3': lambda S, B, ret: (f'`len(p) = {len(S.p)} < 3` → 不满足“至少三次”，跳过' if len(S.p) < 3 else f'`len(p) = {len(S.p)}`，至少三次，继续检查间隔'),
        'continue': '直接看下一个数',
        'd = p[1] - p[0]': '第一个间隔就是公差：`d = {p[1]} - {p[0]} = {d}`',
        'if all(': lambda S, B, ret: (
            f'`p` 中每相邻两项的差都等于 `{S.d}` → ==等间隔，特别整数==' if all(b - a == S.d for a, b in zip(S.p, S.p[1:])) else f'有相邻差 ≠ `{S.d}` → 不等间隔，排除'),
        'ans += 1': '又找到一个特别整数 → `ans = {ans}`',
        'return ans': '返回特别整数的个数 =={ret}==',
    },
    cards=dict(
        one_liner='位置列表的相邻差全部等于第一个差',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['特别整数：在 `nums` 中==至少出现三次==，且所有出现下标等间隔',
                 '返回不同的特别整数个数',
                 '本视频：`[1,8,1,5,1,5,8,5,8,3,3,3]` → `3`（1、5、3）'],
        quote='先统计每个元素 x 的所有出现位置，记在 pos[x] 中。然后遍历每个 pos[x]，判断是否等间隔。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和 I 题一样先把下标按顺序收集起来',
              '出现不足 3 次的直接 `continue`',
              '取 `d = p[1] - p[0]`，用 `pairwise(p)` 看每对相邻下标的差是否都是 `d`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：至少三次，不是恰好；`[8,8,8,8]` 的公差为 1，算特别',
                 '`pairwise` 来自 itertools，相邻两两配对',
                 '本视频示例中 8 的下标是 1、6、8，间隔 5 与 2 不同，被排除'],
    ),
)
