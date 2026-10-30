def _rot(S):
    s, k = S['s'], S['k']
    return f"`s[{k}:]` = =={s[k:]}==　+　`s[:{k}]` = =={s[:k]}==　→　`{s[k:] + s[:k]}`"


CONFIG = dict(
    num=3210, title='找出加密后的字符串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='循环左移 · 切片拼接',
    code='''
class Solution:
    def getEncryptedString(self, s: str, k: int) -> str:
        k %= len(s)
        return s[k:] + s[:k]
''',
    call='Solution().getEncryptedString("dartxy", 8)',
    expect='rtxyda',
    views=[
        dict(type='string', var='s', pointers={'k': 'blue'}, h=260, label='s（箭头 = 切开的位置 k）',
             color=lambda S, i, v: 'green' if i >= S['k'] else 'pink'),
        dict(type='text', fn=lambda S: f"`k` = {S['k']}，`n` = {len(S['s'])}" if S['_line'] <= 3 and S['k'] >= 0 else ''),
        dict(type='text', fn=lambda S: _rot(S) if S['_line'] >= 4 else '先把 k 缩到 0 ~ n−1 之内', size=34),
    ],
    watch=['s', 'k'],
    captions={
        'k %=': '往后数 `k` 个，转一整圈等于没动 → `k` 取模：`{B.k} % {len(s)} = {k}`',
        'return s[k:]': '加密 = ==循环左移 k 位==：`s[{k}:]` 放前面（{s[k:]}），`s[:{k}]` 接到后面（{s[:k]}）→ ==`{s[k:] + s[:k]}`==',
    },
    cards=dict(
        before=[dict(heading='先看一个例子', lines=['`s = "dart", k = 3`：每个字符换成后面第 3 个', '`d→t`，`a→d`，`r→a`，`t→r`，结果 `tdar`', '对比 `dart` 和 `tdar`：==整串向左转了 3 格==', '所以不用逐字符模拟，直接切两段拼起来'])],
        one_liner='每个字符换成后面第 k 个，就是整串循环左移 k 位',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符 `s[i]` 换成它后面（循环）第 `k` 个字符，求加密后的字符串',
                 '示例：`s = "dart", k = 3` → `"tdar"`',
                 '本视频：`s = "dartxy", k = 8` → `"rtxyda"`'],
        quote='根据题意，我们相当于把 s 循环左移 k 位，所以答案为 s[k:] + s[:k]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新串第 `i` 位 = 原串第 `(i+k) mod n` 位，正好是循环左移',
              '`k` 可能比 `n` 大，先 `k %= n`',
              '切片：后半段 `s[k:]` 在前，前半段 `s[:k]` 在后'],
        summary=['时间 `O(n)`；空间 `O(n)`（不计返回值则 `O(1)`）',
                 '易错点：==先取模==，否则 `k > n` 时切片结果不对',
                 '同类：旋转数组、旋转字符串，都是“切一刀再换位”'],
    ),
)
