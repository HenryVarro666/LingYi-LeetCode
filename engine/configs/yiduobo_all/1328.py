def _top(S):
    n = S['n']
    if n == 1:
        return '只有一个字符：怎么改都是回文'
    if 'index' not in S:
        return f'回文串：前半部分 `0 ~ {n // 2 - 1}` 就够了，后半部分与它镜像'
    c = S['palindrome'][S['index']]
    if c == 'a':
        return f"`palindrome[{S['index']}] = 'a'` 已是最小，继续向后扫描"
    return f"`palindrome[{S['index']}] = '{c}'` 不是 a → 把它改成 ==a=="


CONFIG = dict(
    num=1328, title='破坏回文串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='从高位扫描前半部分',
    tags=['灵神题单', '贪心算法', '难度分 1474'],
    code='''
class Solution(object):
    def breakPalindrome(self, palindrome):

        n = len(palindrome)

        if n == 1:
            return ""
        
        for index in range(n // 2):
            if palindrome[index] != 'a':
                return palindrome[:index] + 'a' + palindrome[index + 1:]
        
        return palindrome[:n - 1] + 'b'
''',
    call='Solution().breakPalindrome("aaabaaa")',
    expect='aaabaab',
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='palindrome', label='palindrome（亮 = 要扫描的前半部分，中间字符不能改）', cell=84,
             pointers={'index': 'blue'},
             color=lambda S, k, v: ('blue' if S.get('index') == k else ('yellow' if k == S['n'] // 2 and S['n'] % 2 else None)),
             dim=lambda S, k, v: k > S['n'] // 2 or (k == S['n'] // 2 and S['n'] % 2 == 0)),
        dict(type='text', fn=lambda S: '示例 `"aaabaaa"`：前半 `aaa` 全是 a → 中心之外全是 a → 最后一个改成 b', size=24),
    ],
    watch=[('n', 'n'), ('index', 'index', 'blue')],
    captions={
        'n = len': '`n = {n}`',
        'if n == 1': '`n = {n}`：不止一个字符，继续',
        'for index in range': lambda S, B, r: ('从高位向低位扫，只看前半：`index = %d`（后半与前半镜像）' % S.index
                                               if 'index' not in B or S.index != B.index or S.index == 0 and B.get('index') is None
                                               else '前半部分扫完了，没有找到非 a 的字符'),
        'if palindrome[index]': lambda S, B, r: (f"`palindrome[{S.index}] = '{S.palindrome[S.index]}'` ≠ 'a' → 改成 a 即得最小答案"
                                                 if S.palindrome[S.index] != 'a'
                                                 else f"`palindrome[{S.index}] = 'a'` 本来就是 a，改了没收益 → 看下一位"),
        'return palindrome[:index]': '把 `index` 位改成 a：`{ret}`',
        'return palindrome[:n - 1]': '前半全是 a，后半也必然全是 a（奇数长度时除中心外）→ 把最后一个改成 b：`{ret}`',
    },
    cards=dict(
        one_liner='从高位扫前半部分，遇到非 a 就改成 a；全是 a 就把末位改成 b',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把回文串恰好改一个字符，使它不再是回文串，且字典序最小',
                 '无法做到返回空串',
                 '示例：`"abccba"` → `"aaccba"`；`"a"` → `""`'],
        quote='为了使得新串字典序最小，因此我们应当从高位向下扫描，若当前字符不是a，那么就将其修改成a，否则继续向后扫描。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数长度的回文串，正中间的字符不能改（改了仍是回文）；其余任意位置都行',
              '字典序最小：高位尽量变小，所以从高位找第一个不是 a 的字符改成 a',
              '原串是回文，只需检查前半部分；前半全是 a，后半也全是 a，此时把最后一个字符改成 b'],
        summary=['时间 `O(n)`，空间 `O(n)`（切片拼接）',
                 '原文为 Python 2 写法，`range(n / 2)` 已改为 `range(n // 2)`',
                 '易错：`n == 1` 要单独返回空串',
                 '易错：循环只到 `n // 2`，不碰奇数长度的中心字符',
                 '对比灵神：思路相同，灵神用 `s[:-1] + "b"` 收尾，yiduobo 写成 `palindrome[:n - 1]`'],
    ),
)
