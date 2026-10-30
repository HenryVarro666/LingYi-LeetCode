def _color(S, i, v):
    if 'j' not in S:
        return None
    if i == S['i']:
        return 'blue'
    if i == S['j']:
        return 'pink'
    if (i < S['i'] or i > S['j']) and v.isalnum():
        return 'green'
    return None


def _dim(S, i, v):
    return 'j' in S and (i < S['i'] or i > S['j']) and not v.isalnum()


def _text(S):
    if 'j' not in S:
        return ''
    i, j, s = S['i'], S['j'], S['s']
    if i >= j:
        return '`i ≥ j`：两指针相遇，所有有效字符都配对成功'
    a, b = s[i], s[j]
    if not a.isalnum():
        return f'`s[{i}] = "{a}"` 不是字母数字 → 跳过'
    if not b.isalnum():
        return f'`s[{j}] = "{b}"` 不是字母数字 → 跳过'
    ok = a.lower() == b.lower()
    return f'比较 `"{a}".lower()` 和 `"{b}".lower()`：' + ('==相等==' if ok else '==不相等==')


def _cap_while(S, B, ret):
    if B.i < B.j:
        return f'`i = {B.i} < j = {B.j}`：还没相遇，继续'
    return f'`i = {B.i} ≥ j = {B.j}`：相遇了，所有有效字符都配对成功'


def _cap_left(S, B, ret):
    c = S.s[S.i]
    if not c.isalnum():
        return f'`s[{S.i}] = "{c}"` ==不是字母也不是数字== → 无关字符，要跳过'
    return f'`s[{S.i}] = "{c}"` 是有效字符 → 再看右边'


def _cap_right(S, B, ret):
    c = S.s[S.j]
    if not c.isalnum():
        return f'`s[{S.j}] = "{c}"` ==不是字母也不是数字== → 要跳过'
    return f'`s[{S.j}] = "{c}"` 也是有效字符 → 两边可以比较了'


def _cap_cmp(S, B, ret):
    a, b = S.s[S.i], S.s[S.j]
    if a.lower() == b.lower():
        return f'`"{a}"` 和 `"{b}"` 转成小写后==相等== → 这一对配对成功'
    return f'`"{a}"` ≠ `"{b}"` → 对称位置不一样，==不是回文=='


CONFIG = dict(
    num=125, title='验证回文串', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='相向双指针，边走边跳过',
    tags=['热题173', '面试经典150'],
    code='''
class Solution:
    def isPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1
        while i < j:
            if not s[i].isalnum():
                i += 1
            elif not s[j].isalnum():
                j -= 1
            elif s[i].lower() == s[j].lower():
                i += 1
                j -= 1
            else:
                return False
        return True
''',
    call='Solution().isPalindrome("Race a car")',
    expect=False,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='string', var='s', label='s（绿 = 已配对，灰 = 跳过的无关字符）', cell=92,
             pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'), color=_color, dim=_dim, h=260),
        dict(type='string', var=lambda S: ''.join(c.lower() for c in S['s'] if c.isalnum()) if 's' in S else None,
             label='等价于判断它是否回文（只是示意，代码并不生成它）', cell=80, h=170),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s[i]', 's[i]', 'blue'), ('s[j]', 's[j]', 'pink')],
    captions={
        'i, j = 0': '相向双指针：`i = 0` 从左往右，`j = len(s) - 1 = {j}` 从右往左',
        'while i < j': _cap_while,
        'if not s[i].isalnum()': _cap_left,
        6: '左指针右移：`i` → {i}',
        'elif not s[j].isalnum()': _cap_right,
        8: '右指针左移：`j` → {j}',
        'elif s[i].lower() ==': _cap_cmp,
        10: '两个指针同时往中间走：`i` → {i}',
        11: '`j` → {j}',
        'return False': '有一对对不上，直接返回 ==False==，后面不用再看',
        'return True': '全部配对成功 → 返回 ==True==',
    },
    cards=dict(
        one_liner='两个指针从两端往中间走，跳过无关字符，逐对比较',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['大写转小写、去掉所有==非字母数字==字符后，正读反读都一样 → 回文串',
                 '示例 1：`"A man, a plan, a canal: Panama"` → `true`',
                 '示例 2：`"race a car"` → `false`（`"raceacar"` 不是回文）',
                 '演示：`"Race a car"`（示例 2 首字母改成大写，看 `.lower()` 的作用）'],
        quote='如果 s[i] 既不是字母也不是数字，右移左指针……否则，如果 s[i] 和 s[j] ==转成小写后相等==，那么把 i 加一，把 j 减一，继续判断。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用先拼出新字符串：==边走边跳过==无关字符，空间 `O(1)`',
              '每轮只做一件事：跳左、跳右、或比较一对',
              '一对不相等立刻 `return False`；`i ≥ j` 说明全部配对成功'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：比较前要 `.lower()`；==数字也是有效字符==（`"0P"` → false）',
                 '`while i < j`：最中间剩一个字符时不用比',
                 '原文另附库函数写法：`filter(str.isalnum)` 后与反串比较，空间 `O(n)`'],
    ),
)
