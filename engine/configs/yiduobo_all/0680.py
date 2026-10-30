S0 = 'abcdxfdcba'


def _txt(S):
    l, r = S.get('l'), S.get('r')
    if l is None or r is None:
        return f'`s = "{S0}"`：最多删一个字符，能否变成回文串？'
    if 'new_l' in S:
        return f"试删后检查剩下的：`new_l = {S['new_l']}`，`new_r = {S['new_r']}`（相遇说明剩下是回文）"
    return f"两端扫描：`s[{l}] = {S0[l]}`，`s[{r}] = {S0[r]}`"


def _color(S, k, v):
    if 'l' not in S or 'r' not in S:
        return None
    if k < S['l'] or k > S['r']:
        return 'green'
    return None


CONFIG = dict(
    num=680, title='验证回文串 II', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='双指针 · 失配后试删一边再检查',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def validPalindrome(self, s):

        l = 0
        r = len(s) - 1
        while l < r:
            if s[l] != s[r]:
                new_l = l + 1
                new_r = r
                while new_l < new_r and s[new_l] == s[new_r]:
                    new_l += 1
                    new_r -= 1
                if new_l >= new_r:
                    return True

                new_l = l
                new_r = r - 1
                while new_l < new_r and s[new_l] == s[new_r]:
                    new_l += 1
                    new_r -= 1
                if new_l >= new_r:
                    return True

                return False

            else:
                l += 1
                r -= 1

        return True
''',
    call=f'Solution().validPalindrome({S0!r})',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='string', var=lambda S: S0, label='s（蓝 = l，粉 = r，绿 = 已配对相等）', h=260, cell=84,
             pointers={'l': 'blue', 'r': 'pink', 'new_l': 'cyan', 'new_r': 'orange'}, color=_color),
    ],
    watch=['l', 'r', ('new_l', 'new_l', 'cyan'), ('new_r', 'new_r', 'orange')],
    captions={
        'l = 0': '`l` 从左端出发',
        'r = len': '`r = len(s) - 1 = {r}`，从右端出发',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`，继续往中间扫' if S.l < S.r else '指针相遇：全部配对成功'),
        'if s[l] != s[r]': lambda S, B, r_: (f"`s[{S.l}] = {S.s[S.l]}` 和 `s[{S.r}] = {S.s[S.r]}` ==不同== → 要试着删掉一个" if S.s[S.l] != S.s[S.r]
                                             else f"`s[{S.l}] = s[{S.r}] = {S.s[S.l]}` 相同 → 继续向内"),
        'new_l = l + 1': '先试==删掉左边==的 `s[l]`：从 `l + 1` 开始检查',
        'while new_l < new_r': lambda S, B, r_: (f"检查剩下的：`s[{S.new_l}] = {S.s[S.new_l]}` 和 `s[{S.new_r}] = {S.s[S.new_r]}` 相同，继续向内"
                                                 if S.new_l < S.new_r and S.s[S.new_l] == S.s[S.new_r] else
                                                 ('剩下的两头相遇了 → 是回文' if S.new_l >= S.new_r else
                                                  f"`s[{S.new_l}] = {S.s[S.new_l]}` ≠ `s[{S.new_r}] = {S.s[S.new_r]}`：这样删不行")),
        'new_l += 1': '`new_l` → {new_l}',
        'new_r -= 1': '`new_r` → {new_r}',
        'if new_l >= new_r': lambda S, B, r_: (f'`new_l = {S.new_l} >= new_r = {S.new_r}`：剩下的串是回文 → 返回 `True`' if S.new_l >= S.new_r
                                               else '没扫完就停了：删这一边不行'),
        'new_l = l\n': '再试==删掉右边==的 `s[r]`：`new_l = l`，`new_r = r - 1`',
        'return False': '删左边、删右边都不行 → `False`',
        'l += 1': '两端相同，`l` → {l}',
        'r -= 1': '两端相同，`r` → {r}',
        'return True': lambda S, B, r_: '`s` 本身就是回文串 → `True`' if S.l >= S.r and 'new_l' not in S else '删一个字符后能成回文 → `True`',
    },
    cards=dict(
        one_liner='两端向内扫，遇到不同就试删一个再检查',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定字符串 `s`，==最多==删除一个字符',
                 '判断能否得到回文串',
                 '示例：`"abca"` → `true`；`"abc"` → `false`；本视频：`"abcdxfdcba"` → `true`'],
        quote='两个指针从两端开始往中间扫描，若当前的两侧字符相同，那么向内继续扫描，若当前的两侧字符不同，就尝试删去其中一个，然后检测剩下的字符串是否是回文串。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l`、`r` 从两端向内，相同就继续',
              '不同时：先删 `s[l]`，用 `new_l`、`new_r` 手动检查 `s[l+1..r]` 是不是回文',
              '不行再删 `s[r]`，检查 `s[l..r-1]`；都不行才是 `False`'],
        result='`l = 4`、`r = 5` 不同：删 `x`，剩 `f`，检查直接通过 → `True` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`：不切片，只用下标检查',
                 '检查结束条件是 `new_l >= new_r`（相遇或交错）',
                 '只有第一次失配才试删；检查完无论成败都直接返回',
                 '原文本来就能在 Python 3 运行，代码未改动',
                 '对比灵神：灵神用切片 + `s == s[::-1]` 判回文，这里手写指针检查'],
    ),
)
