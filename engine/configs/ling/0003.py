def _win_text(S):
    if 'right' not in S:
        return '窗口 `[left, right]`：右端点进，重复了就从左边出'
    s, l, r = S['s'], S['left'], S['right']
    w = s[l:r + 1]
    dup = any(v > 1 for v in S['cnt'].values())
    tag = '==有重复==' if dup else '无重复'
    return f"窗口 `s[{l}..{r}]` = `\"{w}\"`，长度 `{r - l + 1}`，{tag}"


def _color(S, i, v):
    if 'right' not in S:
        return None
    if S['cnt'][S['c']] > 1 and v == S['c'] and S['left'] <= i <= S['right']:
        return 'red'
    return None


def _while(S, B, ret):
    c, k = S.c, S.cnt[S.c]
    if k > 1:
        return f'`cnt["{c}"] = {k} > 1`：==窗口内有重复字母==，而且只可能是刚进来的 `"{c}"`'
    return f'`cnt["{c}"] = 1`：窗口内没有重复'


CONFIG = dict(
    num=3, title='无重复字符的最长子串', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='不定长滑动窗口 · 哈希表计数',
    code='''
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        ans = left = 0
        cnt = defaultdict(int)  # 维护从下标 left 到下标 right 的字符及其出现次数
        for right, c in enumerate(s):
            cnt[c] += 1
            while cnt[c] > 1:  # 窗口内有重复字母
                cnt[s[left]] -= 1  # 移除窗口左端点字母
                left += 1  # 缩小窗口
            ans = max(ans, right - left + 1)  # 更新窗口长度最大值
        return ans
''',
    call='Solution().lengthOfLongestSubstring("pwwkew")',
    expect=3,
    views=[
        dict(type='text', fn=_win_text),
        dict(type='string', var='s', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             color=_color, cell=100, h=270, label='s'),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k}: {v}', font=30, h=150,
             label='cnt：窗口内每个字母出现的次数'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('c', 'c', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans` 记录最长长度，`left` 是窗口左端点',
        'cnt = defaultdict': '`cnt`：维护窗口 `[left, right]` 内每个字母的出现次数',
        'for right, c in': lambda S, B, r: ('枚举结束' if 'right' in B and B.right == S.right
                                            else f'右端点 `right = {S.right}`：`"{S.c}"` 进入窗口'),
        'cnt[c] += 1': '`cnt["{c}"]` → {cnt[c]}',
        'while cnt[c] > 1': _while,
        'cnt[s[left]] -= 1': '移除窗口左端点字母 `"{s[left]}"`：`cnt["{s[left]}"]` → {cnt[s[left]]}',
        'left += 1': '缩小窗口：`left` → {left}，窗口变成 `"{s[left:right + 1]}"`',
        'ans = max': '窗口 `"{s[left:right + 1]}"` 合法，长度 `{right - left + 1}`：`ans = max({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '最长无重复子串长度 `{ans}`',
    },
    cards=dict(
        one_liner='右端点进，重复了就从左边出：窗口里永远没有重复字母',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['给定字符串 `s`，找出其中==不含重复字符==的最长子串的长度',
                 '示例：`"abcabcbb"` → `3`（`"abc"`）',
                 '本视频：`"pwwkew"` → `3`（`"wke"`；`"pwke"` 是子序列，不是子串）'],
        quote='`cnt[c] > 1`：==窗口内有重复字母== → 移除窗口左端点字母，缩小窗口。……注意 left 至多增加 n 次，所以整个二重循环至多循环 O(n) 次。',
        quote_src='—— 灵茶山艾府题解（代码注释与复杂度分析）',
        idea=['枚举右端点 `right`：`s[right]` 进入窗口，计数 +1',
              '只可能是刚进来的 `c` 重复 → 不断移出左端点，直到 `cnt[c] == 1`',
              '每轮循环结束时窗口一定合法 → 用窗口长度更新 `ans`'],
        summary=['时间 `O(n)`：`left`、`right` 都只增不减，各至多移动 n 次',
                 '`while` 只判断刚进来的 `c`：之前的窗口已经没有重复',
                 '写法二：哈希集合，先把窗口内的 `c` 移出，再加入 `c`',
                 '滑窗三步：右端进 → `while` 不合法就左端出 → 更新答案'],
    ),
)
