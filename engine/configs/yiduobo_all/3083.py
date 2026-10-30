def _color(S, i, v):
    if 'index' not in S:
        return None
    k = S['index']
    if S['_line'] >= 8:
        return 'pink' if i == k else ('blue' if i == k - 1 else None)
    return 'blue' if i == k else ('pink' if i == k + 1 else None)


CONFIG = dict(
    num=3083, title='字符串及其反转中是否存在同一子字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='先收集所有子串，再反向遍历查集合',
    tags=[],
    code='''
class Solution(object):
    def isSubstringPresent(self, s):

        sub_set = set()
        for index in range(len(s) - 1):
            sub_set.add(s[index] + s[index + 1])
        
        for index in range(len(s) - 1, 0, -1):
            if s[index] + s[index - 1] in sub_set:
                return True

        return False
''',
    call="Solution().isSubstringPresent('abcdbaf')",
    expect=True,
    views=[
        dict(type='string', var='s', h=200, cell=70, color=_color),
        dict(type='set', var='sub_set', h=240, label='sub_set（正向的长为 2 的子串）'),
    ],
    watch=['index', ('sub_set', 'sorted(sub_set)', 'blue')],
    captions={
        'sub_set = set': '准备集合 `sub_set`，存放正向读到的所有长为 2 的子串',
        'for index in range(len(s) - 1)': lambda S, B, ret: ('第一趟结束：所有正向子串都在集合里了' if getattr(B, 'index', None) == S.index else f'第一趟（正向）：下标 `index = {S.index}`'),
        'sub_set.add': '加入子串 `{s[index] + s[index+1]}`',
        'for index in range(len(s) - 1, 0, -1)': '第二趟（反向）：`index = {index}`，反向读到的是 `s[{index}] + s[{index-1}]`',
        'if s[index] + s[index - 1]': '反向子串 `{s[index] + s[index-1]}` 在 `sub_set` 里吗？→ {"==在=="  if (s[index] + s[index-1] in sub_set) else "不在"}',
        'return True': '反向子串在正向集合里 → 它也出现在反转串中，返回 True',
        'return False': '反向子串都不在集合里，返回 False',
    },
    cards=dict(
        one_liner='正着收集一遍，反着查一遍',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断 `s` 的某个长为 2 的子串，是否也在 `s` 反转后出现',
                 '示例：`leetcode` → `True`；`abcd` → `False`',
                 '本例演示：`abcdbaf`，`ab` 与 `ba` 互为反向'],
        quote='题目需要判断的子串长度仅为 2，那么只需一趟遍历，将所有长度为 2 的子串加入到集合中，然后再一趟反向遍历，检测所有长度为 2 的反向子串是否出现在集合中即可。',
        quote_src='—— yiduobo 题解',
        idea=['第一趟：所有 `s[i]s[i+1]` 放进集合',
              '第二趟：从后往前读，读到的 `s[i]s[i-1]` 就是反转串里的子串',
              '这个子串在集合里，说明它在原串里也出现过'],
        summary=['时间 `O(n)`，空间 `O(n)`（集合最多 `n-1` 个子串）',
                 '反向循环 `range(len(s)-1, 0, -1)` 到 1 为止，因为要读 `s[index-1]`',
                 '和灵神「边遍历边查」不同，这里是==两趟==：先全部收集再查询',
                 '长度只有 1 的字符串两趟循环都不会执行，返回 False']),
)
