S0, K0 = '100011001', 3


def _color(S, i, v):
    if 'right' not in S:
        return None
    if S['left'] <= i <= S['right']:
        if S['_line'] in (12, 13, 14, 15) and S.get('cnt1') == K0:
            return 'green'
        return 'blue'
    return None


def _top(S):
    if 'right' not in S:
        return f'`k = {K0}`：答案恰好含 k 个 1；`ans` 先设为整个 `s`'
    l, r = S['left'], S['right']
    t = S0[l:r + 1]
    return f"窗口 `[{l}, {r}] = {t!r}`，1 的个数 `cnt1 = {S['cnt1']}`；当前 `ans = {S['ans']!r}`"


def _while(S, B, ret):
    if S.cnt1 > S.k:
        return f'`cnt1 = {S.cnt1} > {S.k}`：1 太多 → ==缩小窗口=='
    if S.left <= S.right and S.s[S.left] == '0':
        return f"`s[{S.left}] = '0'`：左端是 0，去掉它窗口更短、1 的个数不变 → ==缩小=="
    return f"`cnt1 = {S.cnt1} ≤ {S.k}` 且左端是 '1'：停止缩小"


def _cmp(S, B, ret):
    t, a = S.t, S.ans
    if len(t) < len(a):
        return f'`{t!r}` 长 {len(t)}，比 `ans` 的 {len(a)} ==更短== → 更新'
    if len(t) == len(a) and t < a:
        return f'长度相同，`{t!r} < {a!r}`：==字典序更小== → 更新'
    if len(t) == len(a):
        return f'长度相同，但 `{t!r}` 字典序不比 `{a!r}` 小 → 不更新'
    return f'`{t!r}` 比 `ans` 长，不更新'


CONFIG = dict(
    num=2904, title='最短且字典序最小的美丽子字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 求最短',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def shortestBeautifulSubstring(self, s: str, k: int) -> str:
        if s.count('1') < k:
            return ''
        ans = s
        cnt1 = left = 0
        for right, c in enumerate(s):
            cnt1 += int(c)
            while cnt1 > k or s[left] == '0':
                cnt1 -= int(s[left])
                left += 1
            if cnt1 == k:
                t = s[left: right + 1]
                if len(t) < len(ans) or len(t) == len(ans) and t < ans:
                    ans = t
        return ans
''',
    call=f'Solution().shortestBeautifulSubstring({S0!r}, {K0})',
    expect='11001',
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='string', var='s', label="s（框 = 窗口 [left, right]，绿 = 恰好 k 个 1 的候选）",
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_color, cell=100, h=300),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cnt1', 'cnt1', 'orange'), 't', ('ans', 'ans', 'green')],
    captions={
        "if s.count('1') < k": "`s` 中有 {s.count('1')} 个 1，不少于 `k = {k}` → ==一定有解==",
        'ans = s': '`ans` 先设为整个 `s`（最长的候选）',
        'cnt1 = left = 0': '`cnt1`：窗口内 1 的个数；`left = 0`',
        'for right, c in': lambda S, B, r: ('右端点枚举完毕' if 'right' in B and B.right == S.right
                                            else f"右端点 `right = {S.right}`，`{S.c!r}` 进入窗口"),
        'cnt1 += int(c)': '`cnt1` → {cnt1}',
        'while cnt1 > k or': _while,
        'cnt1 -= int(s[left])': "移出 `s[{left}] = {s[left]!r}`：`cnt1` → {cnt1}",
        'left += 1': '`left` → {left}',
        'if cnt1 == k': lambda S, B, r: (f'`cnt1 == {S.k}`：窗口 `{S.s[S.left:S.right + 1]!r}` 是==美丽子串==，左端是 1，已是以 right 结尾最短的'
                                         if S.cnt1 == S.k else f'`cnt1 = {S.cnt1} < {S.k}`：1 不够，继续扩'),
        't = s[left': '候选 `t = {t!r}`',
        'if len(t) < len(ans)': _cmp,
        'ans = t': '`ans` → =={ans!r}==',
        'return ans': '答案：=={ret!r}==',
    },
    cards=dict(
        one_liner='1 太多或左端是 0 就缩窗口，恰好 k 个 1 时比较长度和字典序',
        complexity='时间 `O(n^2)`（比较字典序要 `O(n)`），空间 `O(n)`',
        problem=['二进制串 `s`，==恰好含 k 个 1== 的子串叫美丽子串',
                 '返回==最短==的美丽子串中字典序最小的那个；没有就返回空串',
                 '示例：`s = "100011001", k = 3` → `"11001"`'],
        quote='由于答案中恰好有 k 个 1，我们也可以用滑动窗口找最短的答案。如果窗口内的 1 的个数==超过 k==，或者窗口==端点是 0==，就可以缩小窗口。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`s` 里 1 不足 k 个直接返回 `\'\'`，否则一定有解',
              '左端是 0 时去掉它更短且 1 不变 → 窗口左端总停在 1 上',
              '`cnt1 == k` 时窗口就是以 right 结尾的最短美丽子串'],
        summary=['时间 `O(n^2)`：每次比较字典序 `O(n)`；用字符串哈希可降到 `O(n log n)`',
                 '方法一：从 k 开始枚举长度 size，找到就返回，`O(n^3)`',
                 '易错：比较时要==先比长度==，长度相同再比字典序',
                 '`ans` 初始为 `s`，它恰好是最长的候选'],
    ),
)
