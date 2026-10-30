CONFIG = dict(
    num=594, title='最长和谐子序列', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数 · 枚举 x 和 x+1',
    tags=[],
    code='''
class Solution:
    def findLHS(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = 0
        for x, c in cnt.items():
            if x + 1 in cnt:
                ans = max(ans, c + cnt[x + 1])
        return ans
''',
    call='Solution().findLHS([1,3,2,2,5,2,3,7])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', h=170),
        dict(type='map', var='cnt', label='cnt（数值 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=200, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"候选：`cnt[{S['x']}] + cnt[{S['x']+1}]` = {S['c']} + {S['cnt'][S['x']+1]} = =={S['c'] + S['cnt'][S['x']+1]}==" if 'x' in S and S['x'] + 1 in S['cnt'] else (f"`{S['x']+1}` 不在 cnt 中，没有候选" if 'x' in S else ''))),
    ],
    watch=[('x', 'x', 'blue'), ('c', 'c', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '值域很大，用哈希表 `cnt` 统计每个数的次数：`{dict(cnt)}`',
        'ans = 0': '`ans = 0`：找不到相差 1 的两个数时答案就是 0',
        'for x, c in cnt.items()': lambda S, B, r: ('枚举完所有键，结束' if B.get('x') == S.x else f'枚举键 `x = {S.x}`（出现 `{S.c}` 次），看看有没有 `x + 1`'),
        'if x + 1 in cnt': lambda S, B, r: (f'`{S.x + 1}` 在 cnt 中：子序列可以==恰好由 {S.x} 和 {S.x + 1} 两种数组成==' if S.x + 1 in S.cnt
                                            else f'`{S.x + 1}` 不在 cnt 中：{S.x} 没有伙伴，跳过'),
        'ans = max': '两种数全取：`{c} + {cnt[x + 1]} = {c + cnt[x + 1]}`，`ans = max({B.ans}, {c + cnt[x + 1]}) = {ans}`',
        'return ans': '最长和谐子序列长度为 =={ans}==',
    },
    cards=dict(
        one_liner='和谐子序列 = 恰好两种数 x 和 x+1，全取',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['和谐数组：最大值与最小值之差==正好是 1==',
                 '求 `nums` 的最长和谐==子序列==的长度（不要求连续）',
                 '示例：`[1,3,2,2,5,2,3,7]` → `5`（`[3,2,2,2,3]`）'],
        quote='「最大值和最小值之间的差别正好是 1」意味着子序列必须恰好包含 x 和 x+1 两种元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子序列不要求连续，所以==只看每个数出现几次==，顺序无关',
              '值域很大，用哈希表 `cnt` 计数，遍历键 `x`',
              '若 `x+1` 也在表里，两种数全取：`cnt[x] + cnt[x+1]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：必须==恰好两种数==，`[1,1,1,1]` 答案是 0，不是 4',
                 '只往 `x+1` 方向找，不用再看 `x-1`，每对相邻数只算一次',
                 '同类：计数哈希表题，如 1 两数之和的思路'],
    ),
)
