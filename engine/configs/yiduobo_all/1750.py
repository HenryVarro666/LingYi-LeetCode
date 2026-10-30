def _top(S):
    if 'l' not in S:
        return ''
    l, r, s = S['l'], S['r'], S['s']
    if l > r:
        return ''
    return f"剩余区间 `s[{l}..{r}]` = =={s[l:r+1]}==，长度 {r - l + 1}"


CONFIG = dict(
    num=1750, title='删除字符串两端相同字符后的最短长度', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='相向双指针 · 两端删干净',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def minimumLength(self, s):

        l = 0
        r = len(s) - 1
        while l < r and s[l] == s[r]:
            while l < r and s[l] == s[r]:
                l += 1
            
            if l == r:
                return 0
            
            while s[r] == s[l - 1]:
                r -= 1
            
        return r - l + 1
''',
    call='Solution().minimumLength("aabccabba")',
    expect=3,
    views=[
        dict(type='text', fn=_top, h=60),
        dict(type='string', var='s', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), h=300,
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= i <= S['r'])),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'l = 0': '`l` 从最左边出发',
        'r = len': '`r = len(s) - 1 = {r}`，从最右边出发',
        'while l < r and s[l] == s[r]:': lambda S, B, ret: (
            f"两端 `s[{S.l}] = '{S.s[S.l]}'`，`s[{S.r}] = '{S.s[S.r]}'` 相同 → ==还能删=="
            if S.l < S.r and S.s[S.l] == S.s[S.r] else
            f"两端 `s[{S.l}]` 与 `s[{S.r}]` 不同（或指针相遇）→ 不能再删了"),
        'l += 1': '`s[l]` 与右端相同，==整段删掉==：`l` → {l}',
        'if l == r': lambda S, B, ret: ('`l == r`：整串都是同一个字符，==全删光== → 返回 0' if S.l == S.r
                                        else '`l != r`：中间还有别的字符，左侧已删完，接着删右侧'),
        'while s[r] == s[l - 1]': lambda S, B, ret: (
            f"`s[{S.r}] = '{S.s[S.r]}'` 等于刚删掉的字符 `'{S.s[S.l-1]}'` → 右侧也要删干净"
            if S.s[S.r] == S.s[S.l - 1] else
            f"`s[{S.r}] = '{S.s[S.r]}'` 不等于 `'{S.s[S.l-1]}'` → 右侧删完了"),
        'r -= 1': '右侧同字符删掉：`r` → {r}',
        'return r - l + 1': '不能再删：剩下 `{r} - {l} + 1` = =={r - l + 1}==',
    },
    cards=dict(
        one_liner='能删就两端删干净，删到删不动为止',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选一个非空前缀和后缀，要求它们字符全相同且互不重叠，把它们删掉',
                 '反复操作，求字符串最短能剩多长',
                 '示例：`"aabccabba"` → 删 `aa|a`、`b|b` 后剩 `"cca"`，答案 `3`'],
        quote='为了尽可能多的删除字符，在可以删除的时候就应该将两端的字符都删除干净',
        quote_src='—— yiduobo 题解原文',
        idea=['若一端删不干净，另一端删光了，剩下的两端字符就不同，再也删不动',
              '所以每轮都把两端那个字符删干净：先移 `l`，再移 `r`',
              '`l == r` 说明整串同字符，全删光，返回 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先删左侧，再用 `s[l-1]` 当作被删字符去删右侧',
                 '内层 `while l < r` 保证左右不会交叉；`l == r` 要单独返回 0',
                 '原文为 Python 2 写法，仅删去了类型说明，无需其它修改'],
    ),
)
