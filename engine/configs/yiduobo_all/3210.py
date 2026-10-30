CONFIG = dict(
    num=3210, title='找出加密后的字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='下标取模 · 一趟遍历',
    code='''
class Solution(object):
    def getEncryptedString(self, s, k):
        return ''.join([s[(index + k) % len(s)] for index in range(len(s))])
''',
    call='Solution().getEncryptedString("dartxy", 8)',
    expect='rtxyda',
    views=[
        dict(type='string', var='s', h=260, label='s（粉 = 被取走的字符，下标 (index+k)%n）',
             color=lambda S, i, v: 'pink' if i == (S['k'] % len(S['s'])) else None),
        dict(type='text', size=30, fn=lambda S: '　'.join(f"`{i}`←`s[{(i + S['k']) % len(S['s'])}]`=={S['s'][(i + S['k']) % len(S['s'])]}==" for i in range(len(S['s'])))),
        dict(type='text', size=34, fn=lambda S: f"每一位取 `s[(index + {S['k']}) % {len(S['s'])}]`，拼成 =={''.join(S['s'][(i + S['k']) % len(S['s'])] for i in range(len(S['s'])))}=="),
    ],
    watch=['s', 'k'],
    captions={
        'return': lambda S, B, r: f"一趟遍历：第 `index` 位填 `s[(index + {S.k}) % {len(S.s)}]`，取模负责绕回开头 → ==`{r}`==",
    },
    cards=dict(
        before=[dict(heading='先手算一位', lines=['`s = "dartxy"`，`k = 8`，`n = 6`', '`index = 0`：`(0 + 8) % 6 = 2` → 取 `s[2]` = `r`', '`index = 4`：`(4 + 8) % 6 = 0` → 绕回开头，取 `s[0]` = `d`', '每一位都这样算，就是答案'])],
        one_liner='第 index 位填 s[(index+k) % n]，取模负责“循环”',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把每个字符换成它后面（循环）第 `k` 个字符',
                 '示例：`s = "dart", k = 3` → `"tdar"`',
                 '本视频：`s = "dartxy", k = 8` → `"rtxyda"`'],
        quote='按照题目要求一趟遍历，对于当前遍历到的下标index，将s[(index + k) % len(s)]填充到答案的index位上即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐位照着题意做：第 `index` 位往后数 `k` 个',
              '数到末尾要绕回开头，所以对 `len(s)` 取模',
              '`k` 再大也只是多绕几圈，取模后位置不变'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文就是一行列表推导式，代码一字未改',
                 '易错点：别忘了对 `len(s)` 取模，否则越界',
                 '对比灵神：他看出这就是循环左移，直接切片 `s[k:] + s[:k]`'],
    ),
)
