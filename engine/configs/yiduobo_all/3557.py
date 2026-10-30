CONFIG = dict(
    num=3557, title='不相交子字符串的最大数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · 哈希表记首次位置',
    tags=['贪心算法', '划分型贪心', '难度分 1720'],
    code='''
class Solution(object):
    def maxSubstrings(self, word):
        
        pre = {}
        res = 0
        for index, c in enumerate(word):
            if c not in pre:
                pre[c] = index
            elif index - pre[c] + 1 >= 4:
                res += 1
                pre = {}
        
        return res
''',
    call="Solution().maxSubstrings('abcdeafdef')",
    expect=2,
    views=[
        dict(type='string', var='word', pointers={'index': 'blue'}, h=250,
             color=lambda S, k, v: 'green' if 'pre' in S and S['pre'].get(v) == k else None),
        dict(type='map', var='pre', fmt=lambda k, v: f'{k} → {v}', h=230, label='pre：字母 → 首次出现的位置'),
        dict(type='text', fn=lambda S: (f"`index − pre[c] + 1` = `{S['index']} − {S['pre'][S['c']]} + 1` = =={S['index'] - S['pre'][S['c']] + 1}==，要 ≥ 4"
                                         if 'c' in S and S.get('pre') and S['c'] in S['pre'] and S['pre'][S['c']] != S['index'] else ''), h=70),
    ],
    watch=[('index', 'index', 'blue'), ('c', 'c', 'pink'), ('res', 'res', 'green')],
    captions={
        'pre = {}': lambda S, B, r: ('`pre` 清空：本次分离后，前面的字符都不能再用了' if 'index' in S
                                      else '哈希表 `pre`：每种字母第一次出现的位置'),
        'res = 0': '`res` 记分离出的子串数',
        'if c not in pre': lambda S, B, r: (f"`{S.c!r}` 还没出现过 → 先记下它的位置" if S.c not in S.pre
                                             else f"`{S.c!r}` 在 `pre` 里（位置 {S.pre[S.c]}），准备判断长度"),
        'pre[c] = index': '`pre[{c!r}] = {index}`：只记==第一次==出现的位置，这样子串最长',
        'elif index': lambda S, B, r: (f"子串 `{S.pre[S.c]}~{S.index}` 长 `{S.index} − {S.pre[S.c]} + 1 = {S.index - S.pre[S.c] + 1}` ≥ 4 → ==可以分离=="
                                        if S.index - S.pre[S.c] + 1 >= 4
                                        else f"子串 `{S.pre[S.c]}~{S.index}` 长只有 `{S.index - S.pre[S.c] + 1}` < 4，不够长，继续往后"),
        'res += 1': '立刻分离出去：剩下的字符串越长，后面能分的越多 → `res` = =={res}==',
    },
    cards=dict(
        one_liner='一碰到能分离的子串就立刻分离，剩得越长越好',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 26 个键）',
        problem=['求首尾字母相同、长度 ≥ 4 的不相交子串最多有几个',
                 '子串==不需要铺满==整个字符串，只要彼此不重叠',
                 '示例：`abcdeafdef` → `abcdea`、`fdef`，答案 `2`'],
        quote='由于不需要用到字符串中的每个字符，那么就可以从左向右一趟遍历，当碰到可以分离的子串时就立马分离出去，因为剩下的字符串越长，可能分离出去的子串数量就越多。',
        quote_src='—— yiduobo 题解原文',
        idea=['用哈希表 `pre` 记每种字母第一次出现的位置',
              '再次遇到同一字母，若 `index - pre[c] + 1 >= 4` 就分离，`res` 加 1',
              '分离后 `index` 之前的字符都不能再用 → ==清空 `pre`=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只记首次出现位置，否则子串会变短而凑不够 4',
                 '分离后必须清空 `pre`，否则下一个子串会和上一个重叠',
                 '对比灵神：灵神用位运算压缩，只看下标 ≤ i−3 的字母；本解直接比较长度'],
    ),
)
