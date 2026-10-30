def _txt(S):
    if 'index' not in S or 'res' not in S:
        return ''
    w = S['words']
    i = S['index']
    if w[i] == w[0]:
        return f"`words[{i}] = {w[i]!r}` 与 `words[0]` 相同，不能作为不同元素对的一端"
    return f"`words[{i}]` 与首元素不同：到左端 `{i + 1}`，到右端 `{len(w) - i}`"


CONFIG = dict(
    num=3696, title='不同单词间的最大距离 I', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='首尾端点 + 枚举中间', tags=[],
    code='''
class Solution(object):
    def maxDistance(self, words):
        
        if words[0] != words[-1]:
            return len(words)
        
        res = 0
        for index in range(1, len(words) - 1):
            if words[index] != words[0]:
                res = max(res, index + 1, len(words) - index)
        
        return res
''',
    call="Solution().maxDistance(['a','a','c','b','a'])",
    expect=4,
    views=[
        dict(type='array', var='words', label='words', pointers={'index': 'blue'}, cell=110, h=220,
             color=lambda S, i, v: ('green' if i in (0, len(S['words']) - 1) else None)),
        dict(type='text', h=80, size=30, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'if words[0] != words[-1]': lambda S, B, r: (
            f"首尾 `{S.words[0]!r}` 和 `{S.words[-1]!r}` "
            + ('不同 → 它们就是最远的一对，距离 = ==整个数组长度==' if S.words[0] != S.words[-1]
               else '相同 → 首尾不能配对，只能让其中一端和中间某个不同的元素配对')),
        'return len(words)': '直接返回 `{ret}`',
        'res = 0': '`res = 0`：万一所有元素都相同，答案就是 0',
        'for index': '检查中间元素 `index = {index}`（首尾已经相同，不用看）',
        'if words[index] != words[0]': '`words[{index}] = {words[index]!r}` vs `words[0] = {words[0]!r}` → {"不同，可以配对" if words[index] != words[0] else "相同，跳过"}',
        'res = max': '用它到两端的距离更新：`max({B.res}, {index + 1}, {len(words) - index})` = =={res}==',
        'return res': '最大距离 `{ret}`',
    },
    cards=dict(
        one_liner='最优解一定有一端是首元素或尾元素',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给字符串数组 `words`，找两个不同元素的最远距离',
                 '距离 = 下标之差 + 1；所有元素都相同则返回 0',
                 '本视频：`["a","a","c","b","a"]` → `4`'],
        quote='最终结果必然是words[0]或者words[-1]，与words中另一个不同于words[0]的元素构成的。',
        quote_src='—— yiduobo 题解原文',
        idea=['首尾不同：直接返回 `n`，这是数组里最远的一对',
              '首尾相同：一端若在某元素左边，换成 `words[0]` 只会更远；在右边则换成 `words[-1]`',
              '所以只枚举中间与 `words[0]` 不同的元素，用到两端的距离取最大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：距离是下标差 ==+1==，到左端是 `index + 1`，到右端是 `n - index`',
                 '首尾相同时，`words[index] != words[0]` 等价于不等于 `words[-1]`',
                 '全部相同时循环不更新，返回 0'],
    ),
)
