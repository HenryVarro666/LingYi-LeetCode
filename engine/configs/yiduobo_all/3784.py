CONFIG = dict(
    num=3784, title='使所有字符相等的最小删除代价', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='哈希表统计 + 总代价减最大值',
    code='''
class Solution(object):
    def minCost(self, s, cost):
        
        su = {}
        tot = 0
        for ch, co in zip(s, cost):
            su[ch] = su.get(ch, 0) + co
            tot += co
        
        return tot - max(su.values())
''',
    call='Solution().minCost("aabaac", [1,2,3,4,1,10])',
    expect=11,
    views=[
        dict(type='string', var='s', h=170, label='s',
             color=lambda S, i, v: ('yellow' if S.get('ch') == v else None)),
        dict(type='array', var='cost', h=170, label='cost'),
        dict(type='map', var='su', h=260, label='su：删除每种字符的代价'),
        dict(type='text', size=30, fn=lambda S: f"删除所有字符的总代价 `tot = {S['tot']}`" if 'tot' in S else ''),
    ],
    watch=['ch', 'co', ('tot', 'tot', 'green')],
    captions={
        'su = {}': '`su` 记录删掉每种字符需要的代价',
        'tot = 0': '`tot` 记录删掉所有字符的总代价',
        'su[ch] =': '字符 `{ch}` 的删除代价累计为 =={su[ch]}==',
        'tot += co': '总代价加上 `{co}` → `tot = {tot}`',
        'return tot': '保留 `su` 里代价最大的字符（=={max(su.values())}==），其余都删：`{tot} - {max(su.values())}` = =={ret}==',
    },
    cards=dict(
        one_liner='选一种字符保留，其余全删，总代价减去它的代价',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['`cost[index]` 是删除 `s[index]` 的代价',
                 '删去一些字符，使剩下的非空且全部相同，求最小总代价',
                 '示例：`"aabaac"`, `[1,2,3,4,1,10]` → `11`'],
        quote='最优的处理方法必然选择一种字符，保留所有的该字符，然后删掉其他的字符，那么总的删除代价就是删除所有字符的总代价，减去删除保留的字符的总代价。',
        quote_src='—— yiduobo 题解',
        idea=['一趟遍历：哈希表记录每种字符的代价，变量记录总代价',
              '答案 = 总代价 − 哈希表 value 的最大值'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '保留的字符，其所有出现位置都不删，所以减的是它的整组代价',
                 '易错点：`su.get(ch, 0)` 处理第一次出现的字符'],
    ),
)
