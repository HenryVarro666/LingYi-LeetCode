CONFIG = dict(
    num=4048, title='统计等间距出现整数数目 I', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表记录出现位置',
    code='''
class Solution:
    def countSpecialIntegers(self, nums: list[int]) -> int:
        pos = defaultdict(list)
        for i, x in enumerate(nums):
            pos[x].append(i)

        ans = 0
        for p in pos.values():
            if len(p) == 3 and p[1] - p[0] == p[2] - p[1]:
                ans += 1
        return ans
''',
    call='Solution().countSpecialIntegers([1,8,1,5,1,5,8,5])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=170,
             color=lambda S, k, v: 'green' if 'i' in S and k == S['i'] else None),
        dict(type='map', var='pos', label='pos[x] = x 的所有出现下标', fmt=lambda k, v: f'{k}: {v}', h=260, font=34),
        dict(type='text', size=30, h=70, fn=lambda S: (
            f"`p = {S['p']}`：`{S['p'][1]} − {S['p'][0]}` 对比 `{S['p'][2]} − {S['p'][1]}`"
            if 'p' in S and len(S['p']) == 3 else
            (f"`p = {S['p']}`：不是恰好 3 个，直接排除" if 'p' in S else '先收集位置，再逐个检查'))),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('p', 'p', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'pos = defaultdict': '`pos[x]` 用来存数 x 出现过的全部下标，缺省是空列表',
        'for i, x in enumerate': lambda S, B, ret: (f'看 `nums[{S.i}] = {S.x}`' if 'i' not in B or S.i != B.i else '位置都收集完了'),
        'pos[x].append': '把下标 `{i}` 记到 `pos[{x}]`：现在是 `{pos[x]}`',
        'ans = 0': '位置收集完毕，接下来逐个数检查是否等间隔；`ans` 从 0 开始',
        'for p in pos.values()': lambda S, B, ret: ('所有数都检查完了' if 'p' in B and S.p == B.p else f'检查下一个数的位置列表 `p = {S.p}`'),
        'if len(p) == 3': lambda S, B, ret: (
            (f'恰好 3 次，且 `{S.p[1]} − {S.p[0]} = {S.p[1]-S.p[0]}`，`{S.p[2]} − {S.p[1]} = {S.p[2]-S.p[1]}` → ==等间隔，特别整数==' if S.p[1]-S.p[0] == S.p[2]-S.p[1]
             else f'恰好 3 次，但间隔 {S.p[1]-S.p[0]} ≠ {S.p[2]-S.p[1]} → 不是特别整数')
            if len(S.p) == 3 else f'出现 {len(S.p)} 次，不是恰好 3 次 → 不是特别整数'),
        'ans += 1': '又找到一个特别整数 → `ans = {ans}`',
        'return ans': '返回特别整数的个数 =={ret}==',
    },
    cards=dict(
        one_liner='先记下每个数的所有位置，再看是否恰好三个且等差',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['特别整数：在 `nums` 中==恰好出现三次==，且三个下标等间隔',
                 '返回不同的特别整数个数',
                 '示例：`[1,8,1,5,1,5,8,5]` → `2`（1 和 5）'],
        quote='先统计每个元素 x 的所有出现位置，记在 pos[x] 中。然后遍历每个 pos[x]，判断是否等间隔。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一遍遍历，把每个值的下标按顺序追加进列表',
              '第二步只看长度恰好为 3 的列表',
              '三个下标 `p[0] < p[1] < p[2]` 等间隔 ⇔ `p[1]-p[0] == p[2]-p[1]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：必须恰好 3 次，出现 4 次的数不算（II 题才放宽为至少 3 次）',
                 '下标是追加进去的，天然递增，不用排序',
                 '同类：II 题把判断改成 `all(y - x == d ...)`'],
    ),
)
