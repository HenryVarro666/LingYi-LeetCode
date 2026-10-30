CONFIG = dict(
    num=2109, title='向字符串添加空格', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双序列双指针',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1315'],
    code='''
class Solution:
    def addSpaces(self, s: str, spaces: List[int]) -> str:
        ans = []
        j = 0
        for i, c in enumerate(s):
            if j < len(spaces) and spaces[j] == i:
                ans.append(' ')
                j += 1
            ans.append(c)
        return ''.join(ans)
''',
    call='Solution().addSpaces("icodeinpython", [1,5,7,9])',
    expect='i code in py thon',
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, label='s', h=240, cell=60),
        dict(type='array', var='spaces', pointers={'j': 'pink'}, label='spaces（要加空格的下标，严格递增）', h=220),
        dict(type='text', fn=lambda S: ("ans = `" + ''.join(S['ans']).replace(' ', '␣') + "`" if 'ans' in S else ''), size=34),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'green'), ('j', 'j', 'pink')],
    captions={
        'ans = []': '`ans` 收集结果字符',
        'j = 0': '`j` 指向 `spaces` 中下一个要加空格的下标',
        'for i, c': '遍历 `s`：`i = {i}`，`c = {c!r}`',
        'if j < len(spaces)': lambda S, B, r: (f'`spaces[{S.j}] = {S.spaces[S.j]}` 等于当前下标 `i = {S.i}` → ==这个字符前要加空格==' if (S.j < len(S.spaces) and S.spaces[S.j] == S.i)
            else (f'`spaces[{S.j}] = {S.spaces[S.j]}` ≠ `i = {S.i}`：还没到，直接加字符' if S.j < len(S.spaces) else '`spaces` 已经用完，后面直接加字符')),
        "ans.append(' ')": '先加空格',
        'j += 1': '这个空格用掉了，`j` 指向下一个：`j` → {j}',
        'ans.append(c)': '加字符 `{c}`：`ans` = `{"".join(ans)}`',
        "return": '拼接 `ans` 得到 `{ret!r}`',
    },
    cards=dict(
        one_liner='两个指针各走各的：i 扫字符串，j 扫 spaces，对上了先加空格',
        complexity='时间 `O(n)`，空间 `O(n)` 或 `O(1)`',
        problem=['在 `s` 的下标 `spaces[k]` 处的字符之前各插入一个空格，`spaces` 严格递增',
                 '示例：`"icodeinpython"`，`[1,5,7,9]` → `"i code in py thon"`'],
        quote='初始化 j=0。遍历 s，把 s[i] 加到答案中。如果 spaces[j] 等于当前下标 i，那么先加空格，再加 s[i]，然后把 j 加一。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['`spaces` 严格递增，所以 `j` 只会往后走，不用回头',
              '`i == spaces[j]`：先加空格再加字符，然后 `j += 1`',
              '注意判断 `j < len(spaces)`，`spaces` 用完后不能再取 `spaces[j]`'],
        summary=['时间 `O(n)`，空间 `O(n)`（若不计返回值则 `O(1)`）',
                 '`j < len(spaces)` 必须放在 `and` 左边，防止越界',
                 '空格要加在字符之前：先 `append(\' \')` 再 `append(c)`',
                 '方法二：按空格位置切片再拼接（`pairwise`），写法更短'],
    ),
)
