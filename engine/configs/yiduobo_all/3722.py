def _cand(S):
    if 'k' not in S:
        return ''
    s, k = S['s'], S['k']
    return f"k = {k}：反转前 {k} 个 → ==`{s[:k][::-1] + s[k:]}`==；反转后 {len(s)-k} 个 → ==`{s[:k] + s[k:][::-1]}`=="


CONFIG = dict(
    num=3722, title='反转后字典序最小的字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举 k · 同时算两种拆分',
    tags=['灵神题单', '字符串', '字符串哈希', '后缀数组'],
    code='''
class Solution(object):
    def lexSmallest(self, s):
        
        res = s
        for k in range(1, len(s) + 1):
            rl = s[:k][::-1]
            res = min(res, rl + s[k:])
            rr = s[k:][::-1]
            res = min(res, s[:k] + rr)
        
        return res
''',
    call='Solution().lexSmallest("dcab")',
    expect='acdb',
    views=[
        dict(type='text', fn=_cand, size=24, h=90),
        dict(type='string', var='s', label='s（粉 = s[:k]，青 = s[k:]）', cell=110, h=210,
             color=lambda S, i, v: None if 'k' not in S else ('pink' if i < S['k'] else 'cyan')),
        dict(type='string', var='res', label='res：目前最小的结果', cell=110, h=190),
    ],
    watch=[('k', 'k', 'blue'), ('rl', 'rl', 'pink'), ('rr', 'rr', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = s': '`res` 先取 `s` 自己，后面遇到更小的再替换',
        'for k in': lambda S, B, r: (f'枚举 `k = {S.k}`：`s[:k]` 与 `s[k:]` 两种情况一起算' if S.k != B.get('k') else 'k 枚举完毕'),
        'rl = ': '`rl` = 前 `{k}` 个字符反转 = `{rl}`',
        'res = min(res, rl': '反转前缀：`{rl}` + `{s[k:]}` = `{rl + s[k:]}`，与 `res` 取小 → =={res}==',
        'rr = ': '`rr` = 后 `{len(s) - k}` 个字符反转 = `{rr}`',
        'res = min(res, s[:k]': '反转后缀：`{s[:k]}` + `{rr}` = `{s[:k] + rr}`，与 `res` 取小 → =={res}==',
        'return res': '`k` 枚举完，最小的是 `{res}`',
    },
    cards=dict(
        one_liner='k 从 1 到 n，前缀反转和后缀反转两种情况一起算',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['长度为 `n` 的小写字符串 `s`，`n ≤ 1000`',
                 '选 `k`（1 到 n），反转前 `k` 个字符，或反转后 `k` 个字符',
                 '示例：`"dcab"` → `"acdb"`'],
        quote='由于n的规模不大，因此可以直接暴力枚举这个k，然后按照题目要求，分别计算两种情况构成的字符串，取其中的最小值即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['反转后 `k` 个，等价于把 `s[k:]` 反转，所以 `s[:k]` 与 `s[k:]` 能一起计算',
              '同一个 `k`：`rl + s[k:]` 是反转前缀，`s[:k] + rr` 是反转后缀',
              '每次都与 `res` 取最小值'],
        summary=['时间 `O(n^2)`：每个 `k` 拼接、比较都是 `O(n)`',
                 '`k = n` 时反转前缀 = 整串反转；反转后缀的 `s[n:]` 为空，结果是 `s` 本身',
                 '原文已是 Python 3 写法，未做修改',
                 '对比灵神：灵神 `k = 1` 单独当初值，yiduobo 从 `k = 1` 起，用 `s[k:]` 的反转统一表示后缀'],
    ),
)
