CONFIG = dict(
    num=2138, title='将字符串拆分为若干长度为 k 的组', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 满 k 个开新组',
    tags=[],
    code='''
class Solution(object):
    def divideString(self, s, k, fill):

        res = [[]]
        for char in s:
            res[-1].append(char)
            if len(res[-1]) == k:
                res.append([])
        
        if len(res[-1]) == 0:
            res.pop()

        if len(res[-1]) < k:
            res[-1].extend([fill] * (k - len(res[-1])))
        
        return [''.join(part) for part in res]
''',
    call='Solution().divideString("abcdefghij", 3, "x")',
    expect=['abc', 'def', 'ghi', 'jxx'],
    views=[
        dict(type='string', var='s', label='s', cell=84, h=150),
        dict(type='array', var='res', label='res（每组一个列表）', cell=150, h=260),
        dict(type='text', size=28, h=100, fn=lambda S: (f"最后一组 `res[-1]` 长度 {len(S['res'][-1])}，k = {S['k']}" if 'res' in S and S['res'] else '')),
    ],
    watch=[('char', 'char', 'blue'), ('k', 'k'), ('fill', 'fill')],
    captions={
        'res = [[]]': '`res` 里先放一个空组，字符都往最后一组里放',
        'for char in s': lambda S, B, ret: (f"取字符 `{S.char}`" if S.char != B.get('char') else '遍历完了'),
        'res[-1].append': '`{char}` 放进最后一组 → `{res[-1]}`',
        'if len(res[-1]) == k': lambda S, B, ret: (f"最后一组已有 `{len(S.res[-1])}` 个 == k → ==这一组满了，开新的一组==" if len(S.res[-1]) == S.k
                                                   else f"最后一组有 `{len(S.res[-1])}` 个 < k，继续放"),
        'res.append([])': '新开一个空组',
        'if len(res[-1]) == 0': lambda S, B, ret: ('最后一组是空的（刚好整除时多开的）→ ==要删掉==' if not S.res[-1] else '最后一组非空，保留'),
        'res.pop()': '删掉多余的空组',
        'if len(res[-1]) < k': lambda S, B, ret: (f"最后一组只有 `{len(S.res[-1])}` 个 < k = {S.k} → ==需要补 fill==" if len(S.res[-1]) < S.k else '最后一组正好 k 个，不用补'),
        'extend': lambda S, B, ret: f'补 `{len(S.res[-1]) - len(B.res[-1])}` 个 `{S.fill}` 补齐 → `{S.res[-1]}`',
        'return': '每组拼成字符串：`{ret}`',
    },
    cards=dict(
        one_liner='边遍历边放，放满 k 个就开新组，最后补 fill',
        complexity='时间 `O(n + k)`，空间 `O(n)`',
        problem=['把 `s` 每 `k` 个字符分为一组，最后一组不足用 `fill` 补满',
                 '示例：`s="abcdefghij"`，`k=3`，`fill="x"` → `["abc","def","ghi","jxx"]`'],
        quote='直接一趟遍历，每k个字符一组添加到答案中，然后对最后一组用fill补足到长度k即可。需要注意字符串长度恰好为k的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`res[-1]` 永远是正在填的那一组，满 `k` 个就 `append([])` 开新组',
              '字符串长度恰好整除 k 时，最后会多出一个空组，要先 `pop` 掉',
              '最后一组不足 k 个，用 `fill` 补齐，再把每组 `join` 成字符串'],
        summary=['时间 `O(n + k)`，空间 `O(n)`',
                 '易错：长度是 k 的倍数时末尾多出空组，必须 `pop`，否则会补出一整组 fill',
                 '作者也提到：用字符串切片可以更短（灵神写法）',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
