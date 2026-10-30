def _b8(c):
    return format(ord(c), '08b')


def _info(S):
    s = S.get('s')
    if s is None or 'left' not in S:
        return ('先看 ASCII：小写字母 97~122 的二进制都以 `011` 开头；反转后要还是合法字母，末尾就得是 `110`' if s else '')
    l, r = S['left'], S['right']
    if l >= len(s) or r < 0:
        return ''
    if l == r:
        return f"`left == right`：中间字符 `'{s[l]}'` = `{_b8(s[l])}`，自己和自己对称，反转后必须不变"
    return f"`'{s[l]}'` = `{_b8(s[l])}`　`'{s[r]}'` = `{_b8(s[r])}`（右边反转看是否等于左边）"


def _lc(S, i, v):
    if 'left' not in S:
        return None
    if i == S['left']:
        return 'blue'
    if i == S['right']:
        return 'pink'
    if i < S['left'] or i > S['right']:
        return 'green'
    return None


CONFIG = dict(
    num=4030, title='判断 ASCII 值回文', difficulty='Easy', category='位运算',
    author='yiduobo', technique='ASCII 规律 · 只有 f / n / v 可用',
    tags=['灵神题单', '位运算', '难度分 1165'],
    code='''
class Solution(object):
    def isPalindromic(self, s):
        
        left = 0
        right = len(s) - 1
        # a-z => 97-122 => 011XXXXX
        # 01100110 <=> 01100110  f <=> f
        # 01101110 <=> 01110110  n <=> v
        while left < right:
            if s[left] == 'n':
                if s[right] != 'v':
                    return False
            elif s[left] == 'v':
                if s[right] != 'n':
                    return False
            elif s[left] == 'f':
                if s[right] != 'f':
                    return False
            else:
                return False
            
            left += 1
            right -= 1
        
        if left == right:
            return s[left] == "f"
        return True
''',
    call='Solution().isPalindromic("fnfvf")',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=24, h=90),
        dict(type='string', var='s', label='s（蓝 = left，粉 = right，绿 = 已配对通过）', cell=100,
             pointers={'left': 'blue', 'right': 'pink'}, color=_lc, h=300),
        dict(type='text', fn=lambda S: '字母只能是 `f`（`01100110`）、`n`（`01101110`）、`v`（`01110110`）；`n` 必须对 `v`，`f` 必须对 `f`', size=22, h=80),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'left = 0': '`left` 指向字符串开头',
        'right = len': '`right` 指向末尾：`right = {right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，还有成对的字符要核对' if S.left < S.right
                                                else f'`left = {S.left}`，`right = {S.right}`：成对的核对完了，看中间还剩什么'),
        "if s[left] == 'n'": lambda S, B, r: (f"`s[left] = '{S.s[S.left]}'` " + ("是 `n`（`01101110`）：反转后是 `01110110` = `v`，右边必须是 `v`" if S.s[S.left] == 'n' else '不是 `n`，看看是不是 `v`')),
        "elif s[left] == 'v'": lambda S, B, r: (f"`s[left] = 'v'`（`01110110`）：反转后是 `01101110` = `n`，右边必须是 `n`" if S.s[S.left] == 'v' else '不是 `v`，看看是不是 `f`'),
        "elif s[left] == 'f'": lambda S, B, r: (f"`s[left] = 'f'`（`01100110`）：反转后还是 `f`，右边必须也是 `f`" if S.s[S.left] == 'f' else f"`'{S.s[S.left]}'` 既不是 n、v 也不是 f：反转后不是小写字母 → 不可能回文"),
        "if s[right] != 'v'": lambda S, B, r: f"右边是 `'{S.s[S.right]}'`" + ('，不是 `v` → 返回 `False`' if S.s[S.right] != 'v' else '，正好是 `v` ✓'),
        "if s[right] != 'n'": lambda S, B, r: f"右边是 `'{S.s[S.right]}'`" + ('，不是 `n` → 返回 `False`' if S.s[S.right] != 'n' else '，正好是 `n` ✓'),
        "if s[right] != 'f'": lambda S, B, r: f"右边是 `'{S.s[S.right]}'`" + ('，不是 `f` → 返回 `False`' if S.s[S.right] != 'f' else '，正好是 `f` ✓'),
        'return False': '这一对不满足 → 返回 `False`',
        'left += 1': '这一对没问题，`left` → {left}',
        'right -= 1': '`right` → {right}，继续往中间走',
        'if left == right': lambda S, B, r: (f'`left == right = {S.left}`：长度是奇数，中间还剩一个字符' if S.left == S.right else '`left > right`：长度是偶数，没有中间字符'),
        'return s[left] == "f"': '中间字符自己对自己，只有 `f` 反转后不变 → `s[{left}] == "f"` 为 `{s[left] == "f"}`',
        'return True': '所有字符对都通过 → `True`',
    },
    cards=dict(
        one_liner='小写字母里只有 f、n、v 能凑回文，直接双指针',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个小写字母换成 8 位 ASCII 二进制并拼接，判断是否回文',
                 '示例：`"ff"` → `true`；`"leet"` → `false`',
                 '本视频：`"fnfvf"` → `true`（中间还有一个 `f`）'],
        quote='a到z的ascii码占据了97到123，……开头的三位一定是011。而题目需要构成回文串，因此……这些ascii码的后三位必须是110。',
        quote_src='—— yiduobo 题解原文',
        idea=['字母都以 `011` 开头，回文要求它们的结尾 3 位是 `110`',
              '只剩 `f`（`01100110`）、`n`（`01101110`）、`v`（`01110110`）；`01111110` 是 126，超出范围',
              '`n` 和 `v` 要成对出现在对称位置，`f` 对 `f`，奇数长度的正中心只能是 `f`'],
        result='`f↔f`、`n↔v` 通过，中心是 `f` → 返回 `True` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：奇数长度要单独检查正中心，只有 `f` 可以',
                 '易错：偶数长度不能漏掉 `return True`（`left > right` 时直接通过）',
                 '原文是 Python 2 风格的类写法，在 Python 3 可直接运行，代码未改动',
                 '对比灵神：灵神用位运算反转每个字符，这里直接用规律把字符限制成 f / n / v'],
    ),
)
