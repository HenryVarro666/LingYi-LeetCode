def _blk(S):
    s, k = S.get('s'), S.get('k')
    if s is None or 'i' not in S:
        return None
    return S['i'] // k


CONFIG = dict(
    num=3271, title='哈希分割字符串', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='按题意模拟 · 分块求和',
    tags=[],
    code='''
class Solution:
    def stringHash(self, s: str, k: int) -> str:
        ans = []
        for i in range(0, len(s), k):
            total = sum(ord(c) for c in s[i: i + k]) - ord('a') * k
            ans.append(ascii_lowercase[total % 26])
        return ''.join(ans)
''',
    call='Solution().stringHash("abcxyzmno", 3)',
    expect='dun',
    views=[
        dict(type='text', fn=lambda S: (f"第 `{S['i']//S['k']}` 块 `s[{S['i']}:{S['i']+S['k']}]` = =={S['s'][S['i']:S['i']+S['k']]}==" + (f"，字母和 `{S['total']}` → 取余 `{S['total']%26}`" if 'total' in S and S['_line'] >= 6 else '')) if 'i' in S else '', size=28),
        dict(type='string', var='s', label='s（每 k 个字符一块）', cell=84,
             color=lambda S, idx, v: ('blue' if S['i'] <= idx < S['i'] + S['k'] else None) if 'i' in S else None,
             dim=lambda S, idx, v: 'i' in S and idx < S['i'],
             ),
        dict(type='array', var='ans', label='ans（每块一个字母）', cell=84),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k'), ('total', 'total', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'for i in range': lambda S, B, ret: ('循环结束：所有块都处理完了' if 'i' in B and S.i == B.i else f'`i = {S.i}`：处理第 `{S.i // S.k}` 块，也就是 `s[{S.i}:{S.i + S.k}]`'),
        'total =': '块内字符 ASCII 之和减去 `ord(\'a\') * k`，等价于每个字母减 `a` 再求和：`total = {total}`',
        'ans.append': '`{total} % 26 = {total % 26}` → 字母表第 `{total % 26}` 个：==`{ascii_lowercase[total % 26]}`==，追加到 ans',
        'return': '全部块处理完，拼接 `ans` 得到 `"{ret}"`',
    },
    cards=dict(
        one_liner='按题意模拟：每 k 个字符一块，求和取余转字母',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['把长度为 `n` 的 `s` 切成 `n / k` 块，每块长 `k`',
                 '块内字母下标求和，对 26 取余，转回字母，依次拼成结果',
                 '示例：`s = "abcd"`，`k = 2` → `"bf"`'],
        quote='考察编程基本功，按照题目要求写代码即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`range(0, len(s), k)` 以 `k` 为步长枚举每块起点',
              '先把 ASCII 码全加起来，再一次性减去 `ord(\'a\') * k`，省掉逐个相减',
              '`ascii_lowercase[total % 26]` 直接取到对应的小写字母'],
        summary=['时间 `O(n)`；空间 `O(1)`，Python 切片空间忽略不计',
                 '易错：别忘了减去 `ord(\'a\') * k`，否则余数会整体偏移',
                 '切片 `s[i: i + k]` 左闭右开，刚好 `k` 个字符'],
    ),
)
