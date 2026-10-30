S0 = 'bcbbbcba'


def _color(S, i, v):
    if 'i' in S and 'left' in S and S['left'] <= i <= S['i'] and v == S['c'] and S['cnt'].get(v, 0) > 2:
        return 'red'
    return None


CONFIG = dict(
    num=3090, title='每个字符最多出现两次的最长子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口（求最长）',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        ans = left = 0
        cnt = defaultdict(int)
        for i, c in enumerate(s):
            cnt[c] += 1
            while cnt[c] > 2:
                cnt[s[left]] -= 1
                left += 1
            ans = max(ans, i - left + 1)
        return ans
''',
    call=f'Solution().maximumLengthSubstring({S0!r})',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口 [left, i]，红 = 超过 2 次的字母）', h=250, cell=100,
             pointers={'left': 'pink', 'i': 'blue'}, window=('left', 'i'), color=_color),
        dict(type='map', var='cnt', label='cnt（窗口内每个字母的出现次数）', h=170, font=36,
             fmt=lambda k, v: f"'{k}': {v}"),
        dict(type='text', h=80, size=28,
             fn=lambda S: f"窗口 `{S['s'][S['left']:S['i'] + 1]!r}` 长度 `{S['i'] - S['left'] + 1}`，`ans = {S['ans']}`" if 'i' in S else ''),
    ],
    watch=[('left', 'left', 'pink'), ('i', 'i', 'blue'), ('c', 'c'), ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`left`：窗口左端点；`ans`：最长长度',
        'cnt = defaultdict': '`cnt` 统计窗口内每个字母的出现次数',
        'for i, c in': lambda S, B, r: ('遍历结束' if B.get('i') == S.i else f'右端点 `i = {S.i}`，`{S.c!r}` 准备进入窗口'),
        'cnt[c] += 1': '`{c!r}` 进入窗口：`cnt[{c!r}] = {cnt[c]}`',
        'while cnt[c] > 2': lambda S, B, r: (f'`cnt[{S.c!r}] = {S.cnt[S.c]} > 2`：窗口==不合法==，要缩小左端点' if S.cnt[S.c] > 2
                                             else f'`cnt[{S.c!r}] = {S.cnt[S.c]} ≤ 2`：窗口合法'),
        'cnt[s[left]] -= 1': '`{s[left]!r}` 离开窗口：`cnt[{s[left]!r}]` → {cnt[s[left]]}',
        'left += 1': '`left` 右移到 {left}',
        'ans = max': '窗口 `[{left}, {i}]` 长 `{i - left + 1}` → `ans = max({B.ans}, {i - left + 1}) = {ans}`',
        'return ans': '最长 =={ans}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='第 3 题「无重复字符的最长子串」把 1 改成 2',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['求最长的子串，使得其中==每个字符最多出现两次==，返回长度',
                 '示例：`s = "bcbbbcba"` → `4`（`"bcba"`）',
                 '示例：`s = "aaaa"` → `2`'],
        quote='本题相当于把 3. 无重复字符的最长子串中的「出现次数不超过 1」改成「出现次数不超过 2」……把代码第 8 行的 1 改成 2 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右端点 `i`，`s[i]` 进入窗口',
              '只有刚进来的 `c` 可能超过 2 次 → `while cnt[c] > 2` 缩左端点',
              '窗口合法后，用 `i − left + 1` 更新答案'],
        summary=['`left` 只增不减，总共移动不超过 n 次 → `O(n)`',
                 '易错：`while` 只需检查 `cnt[c]`，其他字母不会超标',
                 '易错：长度是 `i − left + 1`',
                 '同类：3. 无重复字符的最长子串、1493、2958'],
    ),
)
