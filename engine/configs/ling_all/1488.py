CONFIG = dict(
    num=1488, title='避免洪水泛滥', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='并查集 · 找最早的空闲抽水日',
    tags=['灵神题单', '常用数据结构', '难度分 1974'],
    code='''
class Solution:
    def avoidFlood(self, rains: List[int]) -> List[int]:
        n = len(rains)
        # 非递归并查集
        fa = list(range(n + 1))
        def find(x: int) -> int:
            rt = x
            while fa[rt] != rt:
                rt = fa[rt]
            while fa[x] != rt:
                fa[x], x = rt, fa[x]
            return rt

        ans = [-1] * n
        full_day = {}  # lake -> 装满日
        for i, lake in enumerate(rains):
            if lake == 0:
                ans[i] = 1  # 先随便选一个湖抽干
                continue
            if lake in full_day:
                j = full_day[lake]
                # 必须在 j 之后，i 之前把 lake 抽干
                # 选一个最早的未被使用的抽水日，如果选晚的，可能会导致其他湖没有可用的抽水日
                dry_day = find(j + 1)
                if dry_day >= i:
                    return []  # 无法阻止洪水
                ans[dry_day] = lake
                fa[dry_day] = find(dry_day + 1)  # 删除 dry_day
            fa[i] = i + 1  # 删除 i
            full_day[lake] = i  # 插入或更新装满日
        return ans
''',
    call='Solution().avoidFlood([1,2,0,0,2,1])',
    expect=[-1, -1, 2, 1, -1, -1],
    views=[
        dict(type='array', var='rains', pointers={'i': 'blue'}, label='rains（黄 = 晴天）', h=170,
             color=lambda S, i, v: 'blue' if i == S.get('i') else ('yellow' if v == 0 else None)),
        dict(type='array', var='fa', pointers={'dry_day': 'green'}, label='fa（并查集，灰 = 已不可用）', h=170,
             dim=lambda S, i, v: v != i,
             color=lambda S, i, v: 'green' if v == i and i < len(S['rains']) and S['rains'][i] == 0 else None),
        dict(type='array', var='ans', label='ans', h=130,
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='map', var='full_day', label='full_day：湖 → 最近装满日', h=130),
    ],
    watch=['i', 'lake', 'j', ('dry_day', 'dry_day', 'green')],
    captions={
        'fa = list': '并查集 `fa[x]` 指向「>= x 的最早可用日」，`fa[x]==x` 说明第 x 天还可用',
        'ans[i] = 1': '晴天先==随便==抽湖 1；第 `{i}` 天留作候选抽水日（`fa[{i}]` 仍指自己 = 可用）',
        'if lake in full_day': lambda S, B, r: (f'湖 `{S.lake}` 已在 full_day 中（第 `{S.full_day[S.lake]}` 天装满）→ 再下雨会洪水，必须在两天之间抽干'
                                                if S.lake in S.full_day else f'湖 `{S.lake}` 之前是空的，直接装满，没有风险'),
        'j = full_day[lake]': '上次装满日 `j = {j}`，抽水日必须落在 `({j}, {i})` 之间',
        'dry_day = find(j + 1)': '`find({j + 1})`：从 j 之后沿并查集找==最早==的可用晴天 → `{dry_day}`。选最早的，把晚的留给更晚装满的湖',
        'if dry_day >= i': lambda S, B, r: (f'`dry_day = {S.dry_day} >= i = {S.i}`：区间内没有可用晴天 → 洪水无法避免，返回空'
                                            if S.dry_day >= S.i else f'`dry_day = {S.dry_day} < i = {S.i}`：区间内有可用晴天，可行'),
        'ans[dry_day] = lake': '第 `{dry_day}` 天抽干湖 `{lake}`：`ans[{dry_day}] = {lake}`',
        'fa[dry_day] = find': '删除这个抽水日：`fa[{dry_day}]` 改指向后一个可用日，下次查找==直接跳过==它',
        'fa[i] = i + 1': '第 `{i}` 天是雨天，不能抽水，也从并查集删除：`fa[{i}] = {i + 1}`',
        'full_day[lake] = i': '记下湖 `{lake}` 的最近装满日 `{i}`',
        'return ans': '没有洪水，返回方案 `{ans}`',
    },
    cards=dict(
        one_liner='抽水日要选「装满日之后最早的晴天」，并查集帮你找并删除',
        complexity='时间 `O(n)`（并查集均摊），空间 `O(n)`',
        problem=['`rains[i] > 0`：第 i 天湖 `rains[i]` 下雨；`0`：可以抽干任一个湖',
                 '湖已满时再下雨就会洪水；要给出每个晴天抽哪个湖，无解返回 `[]`',
                 '示例：`[1,2,0,0,2,1]` → `[-1,-1,2,1,-1,-1]`'],
        quote='越晚的抽水日，灵活性越大，可以用于更晚装满的湖。所以越晚的抽水日越应该留到后面再使用。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遇到要再次下雨的湖，在它上次装满日 `j` 之后选==最早==的空闲晴天',
              '有序集合写法用二分；并查集写法删除 `x` 就让 `x` 指向 `x+1`，`find(j+1)` 一步跳到答案',
              '晴天没被指定时随便抽湖 `1`（编号从 1 起，抽空湖不影响）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：不能用栈顶/任意晴天，必须在 `j` 之后的==最早==晴天',
                 '易错：没被指定的晴天也要抽水，填 `1` 即可',
                 '题解还给了有序集合 `SortedList` 的写法（`O(n log n)`），本视频演示并查集写法'],
    ),
)
