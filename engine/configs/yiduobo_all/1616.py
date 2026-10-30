CONFIG = dict(
    num=1616, title='分割两个字符串得到回文串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='中心扩展 + 两端匹配',
    tags=['灵神题单', '难度分 1868'],
    code='''
class Solution(object):
    def checkPalindromeFormation(self, a, b):

        n = len(a)
        if n & 1:
            l = r = n // 2
        else:
            l = n // 2 - 1
            r = n // 2
        
        flag1 = flag2 = True
        while l >= 0:
            if a[l] != a[r]:
                flag1 = False
            if b[l] != b[r]:
                flag2 = False
            if not flag1 and not flag2:
                break
            l -= 1
            r += 1
        
        if l == -1:
            return True

        flag1 = flag2 = True
        while l >= 0:
            if a[l] != b[r]:
                flag1 = False
            if a[r] != b[l]:
                flag2 = False
            if not flag1 and not flag2:
                return False
            l -= 1
            r += 1

        return True
''',
    call='Solution().checkPalindromeFormation("ulacfd", "jizalu")',
    expect=True,
    views=[
        dict(type='string', var='a', label='a', h=200, cell=80, pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='string', var='b', label='b', h=200, cell=80, pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='text', size=26, h=60, fn=lambda S: (f"阶段一（自身回文）：a 中心回文 `{S['flag1']}`，b 中心回文 `{S['flag2']}`" if S.get('_line', 0) < 25 and 'flag1' in S else (f"阶段二（a 头 + b 尾）`{S['flag1']}`；（b 头 + a 尾）`{S['flag2']}`" if 'flag1' in S else ''))),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('flag1', 'flag1', 'yellow'), ('flag2', 'flag2', 'cyan')],
    captions={
        'n = len(a)': '`n = {n}`',
        'if n & 1': lambda S, B, r: ('长度为奇数：正中间一个字符本身就是回文' if S.n & 1 else '长度为偶数：中心回文可能是空的'),
        'l = r = n // 2': '`l = r = {l}`：从正中间字符开始向外扩',
        'l = n // 2 - 1': '`l = {l}`：中心两个字符的左边',
        'r = n // 2': '`r = {r}`：中心两个字符的右边',
        11: '`flag1`/`flag2` 记录 ==a/b 的中心是否还保持回文==',
        'if a[l] != a[r]': '`a[{l}] = {a[l]}`，`a[{r}] = {a[r]}` → ' + '{"不等：a 的中心回文到此为止" if a[l] != a[r] else "相等，a 的中心回文继续"}',
        'if b[l] != b[r]': '`b[{l}] = {b[l]}`，`b[{r}] = {b[r]}` → ' + '{"不等：b 的中心回文到此为止" if b[l] != b[r] else "相等，b 的中心回文继续"}',
        'if not flag1 and not flag2:': lambda S, B, r: ('两个字符串的中心回文都断了 → 停，==此时 l、r 就是外层要匹配的位置==' if (not S.flag1 and not S.flag2) else '至少有一个还是回文，继续向外扩'),
        'l -= 1': '`l` → {l}',
        'r += 1': '`r` → {r}',
        'if l == -1': lambda S, B, r: ('`l == -1`：扩到头了，a 或 b 自己就是回文 → ==直接 True==' if S.l == -1 else '`l` 还没扩到头，要靠 a、b 的两端互相匹配'),
        25: '重新开始：这次看 ==a 头 + b 尾== 与 ==b 头 + a 尾==',
        'if a[l] != b[r]': '`a[{l}] = {a[l]}` 对 `b[{r}] = {b[r]}` → ' + '{"不匹配，a 头 + b 尾 这条路断了" if a[l] != b[r] else "匹配"}',
        'if a[r] != b[l]': '`a[{r}] = {a[r]}` 对 `b[{l}] = {b[l]}` → ' + '{"不匹配，b 头 + a 尾 这条路断了" if a[r] != b[l] else "匹配"}',
        'return False': '两条路都断了 → 无法构成回文，`False`',
        'return True': lambda S, B, r: ('扩到头了，至少一条路一直匹配 → ==能构成回文，True==' ),
    },
    cards=dict(
        one_liner='答案中间一定有一段原生回文，先找它，再向外匹配',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`a`、`b` 等长，在同一下标把两个串都切开',
                 '判断 `a前缀 + b后缀` 或 `b前缀 + a后缀` 能否是回文串',
                 '示例：`a="ulacfd"`, `b="jizalu"` → `True`（下标 3 切开得 `ulaalu`）'],
        quote='可以发现无论哪种情况，中间都存在一个原生的回文串。这个回文串可以来自a或者b，且越长越好。',
        quote_src='—— yiduobo 题解原文',
        idea=['拼出来的回文，中间一段只来自 a 或 b 其中一个',
              '先用中心扩展找 a、b 各自最长的中心回文',
              '再从它的两端出发，看 a 头 + b 尾、b 头 + a 尾能否一直匹配'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：长度奇数时中心至少 1 个字符；偶数时中心可以为空',
                 '`l == -1` 说明 a 或 b 自身是回文，直接 True',
                 '原文为 Python 2 风格，`n / 2` 已改为 `n // 2`，并删去类型说明',
                 '对比灵神：灵神先双指针匹配前后缀，再判断中间是否回文'],
    ),
)
