CONFIG = dict(
    num=2150, title='找出数组中的所有孤独数字', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def findLonely(self, nums: List[int]) -> List[int]:
        ans = []
        cnt = Counter()
        for v in nums:
            cnt[v] += 1
        for v, c in cnt.items():
            if c == 1 and cnt[v + 1] == 0 and cnt[v - 1] == 0:
                ans.append(v)
        return ans
''',
    call='Solution().findLonely([10, 6, 5, 8, 3, 3])',
    expect=[10, 8],
    views=[
        dict(type='array', var='nums', h=170, label='nums',
             color=lambda S, i, v: 'yellow' if 'v' in S and S['v'] == v and 'c' not in S else None),
        dict(type='map', var='cnt', h=270, label='cnt（出现次数）', fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var='ans', label='ans（孤独数字）', h=150),
    ],
    watch=['v', 'c', ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 存放孤独数字，`cnt` 记录每个数出现的次数',
        'cnt = Counter': '用哈希表 `cnt` 统计次数',
        'cnt[v] += 1': '`{v}` 的出现次数变成 `{cnt[v]}`',
        'for v, c in': lambda S, B, r: (f'检查 `{S.v}`：它出现了 `{S.c}` 次' if 'c' in S else '统计完毕，逐个检查哈希表里的数'),
        'if c == 1': lambda S, B, r: (
            f"`{S.v}`：次数 `{S.c}`，`{S.v+1}` 出现 `{S.cnt.get(S.v+1, 0)}` 次，`{S.v-1}` 出现 `{S.cnt.get(S.v-1, 0)}` 次 → "
            + ('==三个条件都满足，是孤独数字==' if S.c == 1 and S.cnt.get(S.v+1, 0) == 0 and S.cnt.get(S.v-1, 0) == 0
               else '重复或有相邻数字，不是孤独数字')),
        'ans.append': '`{v}` 加入答案',
        'return ans': '孤独数字：`{ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='次数为 1，且 x-1、x+1 都没出现过',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数 `x` 只出现一次，且 `x-1`、`x+1` 都不在数组里，就是孤独数字',
                 '返回所有孤独数字，顺序任意',
                 '示例：`[10,6,5,8]` → `[10,8]`；本视频：`[10,6,5,8,3,3]`'],
        quote='cnt[v+1] == 0 && cnt[v-1] == 0，且 c == 1',
        quote_src='—— 灵茶山艾府题解代码条件',
        idea=['先用哈希表数出每个数的出现次数',
              '遍历哈希表：次数必须为 `1`，重复的数直接排除',
              '再查 `v+1`、`v-1` 的次数是否为 `0`，两侧都没有邻居才是孤独数字'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 'Go 的 `map` 读不存在的键得 `0`，Python 里用 `defaultdict(int)` 对应',
                 '遍历时查 `cnt[v+1]` 会往 `defaultdict` 里插入键，所以用 `cnt.items()` 取快照遍历（Go 原文无此问题）',
                 '时间 `O(n)`，空间 `O(n)`；返回顺序任意'],
    ),
)
