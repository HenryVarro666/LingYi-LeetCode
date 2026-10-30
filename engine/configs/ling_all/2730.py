STR = '5223343'


def _pairs(S):
    """窗口内相邻相等的右端下标集合"""
    if 'right' not in S:
        return set()
    s, l, r = S['s'], S['left'], S['right']
    return {i for i in range(l + 1, r + 1) if s[i] == s[i - 1]}


def _color(S, i, v):
    if 'right' not in S:
        return None
    p = _pairs(S)
    if i in p or (i + 1) in p:
        return 'orange'
    if S['left'] <= i <= S['right']:
        return 'blue'
    return None


def _dim(S, i, v):
    return 'right' in S and not (S['left'] <= i <= S['right'])


def _top(S):
    if 'right' not in S:
        return '半重复：==至多一对==相邻字符相等'
    s, l, r = S['s'], S['left'], S['right']
    ps = ['`' + s[i - 1] + s[i] + '`' for i in sorted(_pairs(S))]
    return f"窗口 `{s[l:r + 1]}` 中相等相邻对：{'、'.join(ps) if ps else '无'}（cnt = {S['cnt']}）"


def _while(S, B, ret):
    if S.cnt > 1:
        return f'`cnt = {S.cnt} > 1`：窗口里有两对相邻相等，==不再半重复== → 移动左端'
    return f'`cnt = {S.cnt} ≤ 1`：窗口是半重复的'


def _ifl(S, B, ret):
    s, l = S.s, S.left
    if s[l] == s[l + 1]:
        return f'`s[{l}] = s[{l + 1}] = {s[l]}`：left 离开后==这一对被拆开=='
    return f'`s[{l}] = {s[l]} ≠ s[{l + 1}] = {s[l + 1]}`：离开不影响 cnt'


CONFIG = dict(
    num=2730, title='找到最长的半重复子字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 统计相邻相等对',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def longestSemiRepetitiveSubstring(self, s: str) -> int:
        ans = 1
        cnt = left = 0
        for right in range(1, len(s)):
            if s[right] == s[right - 1]:
                cnt += 1
            while cnt > 1:
                if s[left] == s[left + 1]:
                    cnt -= 1  # left 离开窗口后，和 left+1 断开
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call=f'Solution().longestSemiRepetitiveSubstring({STR!r})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（框 = 窗口，橙 = 窗口内相邻相等的一对）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_color, dim=_dim, cell=110, h=320),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cnt', 'cnt', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '单个字符一定是半重复的：`ans = 1`',
        'cnt = left = 0': '`cnt`：窗口内相邻相等的对数；`left = 0`',
        'for right in': lambda S, B, r: ('右端点枚举完毕' if 'right' in B and B.right == S.right
                                         else f'`s[{S.right}] = {S.s[S.right]}` 进入窗口'),
        'if s[right] == s[right - 1]': lambda S, B, r: (f'`s[{S.right}] = s[{S.right - 1}] = {S.s[S.right]}`：新增一对相邻相等'
                                                        if S.s[S.right] == S.s[S.right - 1]
                                                        else f'`{S.s[S.right - 1]} ≠ {S.s[S.right]}`：没有新增相等对'),
        'cnt += 1': '`cnt` → {cnt}',
        'while cnt > 1': _while,
        'if s[left] == s[left + 1]': _ifl,
        'cnt -= 1': '和 left+1 断开：`cnt` → {cnt}',
        'left += 1': '`left` → {left}',
        'ans = max': '窗口 `[{left}, {right}]` 长 `{right - left + 1}`：`ans = max({B.ans}, {right - left + 1})` = =={ans}==',
        'return ans': '最长半重复子串长 =={ret}==',
    },
    cards=dict(
        one_liner='窗口里维护相邻相等的对数 cnt，超过 1 就缩左端',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==半重复==：至多一对相邻字符相等',
                 '求 `s` 中最长半重复子串的长度',
                 '示例：`"52233"` → `4`；本视频 `"5223343"` → `5`'],
        quote='本题维护的是窗口中的==相邻字符相等的次数 cnt==。……s[left] 离开窗口前，如果其等于 s[left+1]，则把 cnt 减少 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s[right]` 进入：若等于 `s[right−1]`，cnt 加一',
              '`cnt > 1` 时右移 left；离开的 `s[left]` 若等于 `s[left+1]` 就拆掉一对',
              '每次用 `right − left + 1` 更新答案'],
        summary=['时间 `O(n)`：left 只增不减；空间 `O(1)`',
                 'right 从 1 开始，`ans` 初始为 1（长度为 1 的情况）',
                 '判断「离开」看的是 `s[left]` 和 `s[left+1]`，不是 `s[left−1]`',
                 '同类：统计窗口内「某种对」的个数，进出时只看相邻元素'],
    ),
)
