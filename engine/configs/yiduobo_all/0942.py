CONFIG = dict(
    num=942, title='增减字符串匹配', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='贪心 · 剩余最小/最大值',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def diStringMatch(self, S):

        res = []
        l = 0
        r = len(S)

        for char in S:
            if char == 'I':
                res.append(l)
                l += 1
            else:
                res.append(r)
                r -= 1

        res.append(l)
        return res
''',
    call="Solution().diStringMatch('IDIDDI')",
    expect=[0, 6, 1, 5, 4, 2, 3],
    views=[
        dict(type='text', fn=lambda S: (f"剩下的数是 `{S['l']} .. {S['r']}`" if 'r' in S else '')),
        dict(type='string', var='S', pointers={'len(res)': 'blue'}, h=170,
             color=lambda S, i, v: ('green' if v == 'I' else 'pink') if 'res' in S and i < len(S['res']) else None),
        dict(type='array', var='res', h=220, label='res'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'char', 'res'],
    captions={
        'l = 0': '`l` 是剩下的最小值，初始 0',
        'r = len': '`r = len(S) = {r}`：剩下的最大值，数字 `0 .. {r}` 共 `n+1` 个',
        'for char': '处理第 `{len(res)+1}` 个字符 `{char}`',
        "if char == 'I'": lambda S, B, r: (f"字符 `I`：要求后一个更大 → 当前取剩下的 ==最小值== 最安全" if S.char == 'I' else f"字符 `D`：要求后一个更小 → 当前取剩下的 ==最大值== 最安全"),
        'res.append(l)': lambda S, B, r: (f'放入最小值 `{S.res[-1]}`，后面剩下的都比它大，I 必然成立' if len(S.res) <= len(S.S) else f'最后剩下 `l = r = {S.res[-1]}`，放进末尾'),
        'l += 1': '最小值变为 `l = {l}`',
        'res.append(r)': '放入最大值 `{res[-1]}`，后面剩下的都比它小，D 必然成立',
        'r -= 1': '最大值变为 `r = {r}`',
        'return res': '最后 `l = r`，只剩一个数放末尾 → `{res}`',
    },
    cards=dict(
        one_liner='I 取剩下的最小值，D 取剩下的最大值',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['字符串 `S` 只含 `I`（上升）和 `D`（下降），长度 `n`',
                 '返回 `0..n` 的一个排列，使 `S[i]=I` 时 `A[i] < A[i+1]`，`S[i]=D` 时 `A[i] > A[i+1]`',
                 '本视频：`S = "IDIDDI"`'],
        quote='从头开始扫描S，若当前字符为I，那么就将当前剩下的最小值加入答案，否则将当前剩下的最大值加入答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l`、`r` 维护还没用的数字范围 `[l, r]`',
              '遇到 `I`：取 `l`，此后全比它大，上升必成立',
              '遇到 `D`：取 `r`，此后全比它小，下降必成立',
              '扫完后 `l == r`，把最后一个数补在末尾'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '易错：循环后还要再 `res.append(l)`，共 `n+1` 个数',
                 '作者说本题像「低配版」的某个同类题'],
    ),
)
