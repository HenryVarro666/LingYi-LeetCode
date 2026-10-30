CONFIG = dict(
    num=3784, title='使所有字符相等的最小删除代价', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分组求和 + 保留最大组',
    code='''
class Solution:
    def minCost(self, s: str, cost: List[int]) -> int:
        group_cost_sum = defaultdict(int)
        for ch, x in zip(s, cost):
            group_cost_sum[ch] += x
        return sum(group_cost_sum.values()) - max(group_cost_sum.values())
''',
    call='Solution().minCost("aabaac", [1,2,3,4,1,10])',
    expect=11,
    views=[
        dict(type='string', var='s', h=170, label='s',
             color=lambda S, i, v: ('yellow' if S.get('ch') == v else None)),
        dict(type='array', var='cost', h=170, label='cost'),
        dict(type='map', var='group_cost_sum', h=260, label='group_cost_sum：每个字母的代价和'),
        dict(type='text', size=30, fn=lambda S: (f"总代价 ==" + str(sum(S['group_cost_sum'].values())) + "==，保留最大组 ==" + str(max(S['group_cost_sum'].values())) + "==") if 'group_cost_sum' in S and S['group_cost_sum'] else ''),
    ],
    watch=['ch', 'x'],
    captions={
        'group_cost_sum = ': '建一个哈希表：key 是字母，value 是这个字母所有位置的删除代价之和',
        'group_cost_sum[ch] += x': '字母 `{ch}` 的代价和加上 `{x}` → =={group_cost_sum[ch]}==',
        'return sum': '总代价 =={sum(group_cost_sum.values())}==，保留代价和最大的组 =={max(group_cost_sum.values())}==，其余全删：==差 = {ret}==',
    },
    cards=dict(
        one_liner='保留代价和最大的那一组，其余全删',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（字符集大小 26）',
        problem=['`cost[i]` 是删除 `s[i]` 的代价，删掉若干字符，使剩下非空且字符全相同',
                 '求最小总删除代价',
                 '示例：`s="aabaac"`, `cost=[1,2,3,4,1,10]` → `11`（只留 `c`）'],
        quote='按照相同字母分组，每一组累加代价。贪心地，保留代价和最大的那一组，其余组全部删除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最终只剩一种字母，保留它的所有字符，删除其他字母',
              '删除代价 = 总代价 − 保留那个字母的代价和',
              '要让删得最少，就选代价和最大的字母'],
        summary=['先按字母分组求和，再用总代价减去最大组',
                 '时间 `O(n)`，空间 `O(|Σ|)`',
                 '易错点：必须保留非空，所以至少保留一组；最大组的代价和一定 >0',
                 '`defaultdict(int)` 免去判断 key 是否存在'],
    ),
)
