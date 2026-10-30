S0, K0 = 'abacb', 2


def _R(S):
    return S['left'] + sum(S['cnt'].values()) - 1 if 'cnt' in S else None


def _txt(S):
    if 'cnt' not in S:
        return '右端点枚举每个字符；窗口 `[left, right]` 里没有字母出现 `k` 次'
    return f'`left = {S["left"]}`：右端点固定时，左端点 `0 ~ {S["left"] - 1}` 共 ==`{S["left"]}`== 个子串合法　`ans = {S["ans"]}`'


CONFIG = dict(
    num=3329, title='字符至少出现 K 次的子字符串 II', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='滑动窗口 · 越长越合法',
    tags=[],
    code='''
class Solution:
    def numberOfSubstrings(self, s: str, k: int) -> int:
        ans = left = 0
        cnt = defaultdict(int)
        for c in s:
            cnt[c] += 1
            while cnt[c] >= k:
                cnt[s[left]] -= 1
                left += 1
            ans += left
        return ans
''',
    call=f'Solution().numberOfSubstrings({S0!r}, {K0})',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口，里面没有字母出现 k 次）', cell=100, h=230,
             pointers={'left': 'blue'},
             window=('left', _R)),
        dict(type='map', var='cnt', label='cnt（窗口内各字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=[('k', 'k', 'yellow'), ('c', 'c', 'pink'), ('left', 'left', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans` 是答案，`left` 是窗口左端点',
        'cnt = defaultdict': '`cnt` 统计窗口里每个字母的出现次数',
        'for c in s': '枚举右端点，新字母 `c = {c}` 准备进窗口',
        'cnt[c] += 1': '`c` 进入窗口：`cnt[{c!r}]` → {cnt[c]}',
        'while cnt[c] >= k': lambda S, B, r: (f'`cnt[{S.c!r}] = {S.cnt[S.c]} >= k = {S.k}` → 窗口里有字母达到 k 次，需要收缩' if S.cnt[S.c] >= S.k
                                              else f'`cnt[{S.c!r}] = {S.cnt[S.c]} < k = {S.k}` → 窗口合法（没有字母出现 k 次），停止收缩'),
        'cnt[s[left]] -= 1': '左端点字母 `{s[left]}` 离开窗口：`cnt[{s[left]!r}]` → {cnt[s[left]]}',
        'left += 1': '`left` 右移到 {left}',
        'ans += left': lambda S, B, r: (f'右端点固定，左端点 `0 ~ {S.left - 1}` 的子串都合法 → 加 `{S.left}`，`ans = {S.ans}`' if S.left > 0
                                    else f'`left = 0`：还没有合法的左端点 → 加 `0`，`ans = {S.ans}`'),
        'return ans': '返回 =={ans}==',
    },
    cards=dict(
        one_liner='枚举右端点，窗口缩到刚好不合法，左边 left 个起点都合法',
        complexity='时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
        problem=['给定字符串 `s` 和整数 `k`，统计 `s` 的子串中，至少有一个字符出现 ==至少 k 次== 的子串个数',
                 '示例：`s = "abacb", k = 2` → `4`',
                 '本题 `n` 可达 `3×10^5`，要 `O(n)`'],
        quote='滑动窗口的内层循环结束时，右端点固定在 right，左端点在 0,1,2,…,left-1 的所有子串都是合法的，这一共有 left 个，加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['窗口 `[left, right]` 始终保持「没有字母出现 k 次」',
              '新字母 `c` 进窗口后若 `cnt[c] >= k`，不断移出左端点，直到不再达到 k',
              '此时 `[0..left-1]` 作为左端点都比窗口多包含一些字母，一定合法'],
        summary=['时间 `O(n+|Σ|)`：`left` 总共只右移 `n` 次',
                 '只需判断 `cnt[c] >= k`：只有 `c` 刚进窗口才可能让某字母达到 k，其余字母必然 `< k`',
                 '`>=` 写成 `==` 也可以',
                 '同类：滑动窗口「越长越合法」（题单 §2.3.1）'],
    ),
)
