CONFIG = dict(
    num=3675, title='转换字符串的最小操作次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='找最小非 a 字符',
    tags=['贪心算法', '思维题', '难度分 1414'],
    code='''
class Solution(object):
    def minOperations(self, s):
        
        mi = None
        for c in s:
            if c != 'a' and (mi is None or mi > c):
                mi = c
        
        if mi is None:
            return 0
        return 123 - ord(mi)
''',
    call="Solution().minOperations('yazyd')",
    expect=23,
    views=[
        dict(type='string', var='s', h=200, label='s',
             color=lambda S, i, v: 'blue' if 'c' in S and 'mi' in S and S.get('mi') == v and v == S['c'] else ('yellow' if 'c' in S and 'mi' in S and S['c'] == v else None),
             dim=lambda S, i, v: v == 'a'),
        dict(type='text', h=120, fn=lambda S: (f"当前最小的非 a 字符：`mi = {S['mi']}`" if S.get('mi') else '还没遇到非 a 字符：`mi = None`')),
    ],
    watch=[('c', 'c', 'yellow'), ('mi', 'mi', 'blue')],
    captions={
        'mi = None': '`mi` 记录字符串中不为 `a` 的最小字符，开始时还没有',
        'if c != ': lambda S, B, r: (f"`c = {S.c}` 是 `a` → 不用转换，跳过" if S.c == 'a' else
                                     (f"`c = {S.c}` 不是 a 且 `mi` 还是 None → 记下它" if B.mi is None else
                                      (f"`c = {S.c}`，`mi = {B.mi}`：{B.mi} > {S.c} → ==更小，更新 mi==" if B.mi > S.c else f"`c = {S.c}`，`mi = {B.mi}`：{B.mi} 不比 {S.c} 大 → 保持"))),
        'mi = c': '`mi` 更新为 `{mi}`',
        'if mi is None': '`mi` 是 None 吗？→ {mi is None}（None 说明全是 a）',
        'return 0': '全是 `a`，一次操作都不用',
        'return 123': "`123 - ord('{mi}')` = `123 - {ord(mi)}` = =={ret}==：`mi` 走到 `z`（122）再多一步变成 `a`",
    },
    cards=dict(
        one_liner='转换顺序固定为 b→c→…→z→a，只看最小的非 a 字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选一个字符 `c`，把串中所有 `c` 换成字母表里的下一个（`z` 的下一个是 `a`）',
                 '求 `s` 变成全 `a` 的最少操作次数',
                 '示例：`"yz"` → `2`；本视频：`"yazyd"` → `23`'],
        quote='只需要找出字符串中不为\'a\'的最小字符mi，然后逐步将mi转换为\'z\'再转换为\'a\'即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['最终都要变成 `a`，转换路径只能是 `b → c → … → z → a`',
              '路径前面的字母如果不存在，直接跳过；从最小的 `mi` 出发，后面的字母会一起被带走',
              '没有 `mi` 就是全 `a`，答案 0；否则是 `ord(\'z\') - ord(mi)` 再加 1，即 `123 - ord(mi)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`mi` 初值用 `None`，要先判断是否为空，再和 `c` 比较',
                 '`123 = ord(\'z\') + 1`，别忘了最后 `z → a` 这一步',
                 '对比灵神：灵神把字母摆在数轴上，用 `{` 作为 `z+1`；yiduobo 手动找最小值并分类讨论',
                 '原文为 Python 2 风格，除类型说明外代码无需改动'],
    ),
)
