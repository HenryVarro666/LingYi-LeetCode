S_IN, K = 'abacbab', 2


def _r(S):
    if 'cnt' not in S or 'c' not in S:
        return None
    # 窗口长度 = cnt 的总数；第 8 行 cnt 已减但 left 还没右移
    return S['left'] + sum(S['cnt'].values()) - 1 + (1 if S.get('_line') == 8 else 0)


def _color(S, i, v):
    if 'c' in S and S.get('_line') == 10 and i < S['left']:
        return 'green'
    return None


def _top(S):
    if 'c' not in S:
        return f'`k = {K}`：子串越长，越可能有字母出现 k 次 → ==越长越合法=='
    l, r = S['left'], _r(S)
    if S.get('_line') == 10:
        if l == 0:
            return '还没有合法的左端点：本轮 ==0== 个'
        return f"右端点 {r}：左端点取 `0..{l - 1}` 都合法 → 本轮 =={l}== 个"
    return f"窗口 `{S['s'][l:r + 1]}`"


def _while(S, B, ret):
    c, v = S.c, S.cnt[S.c]
    r = _r(S)
    if v >= S.k:
        return f'`cnt[{c!r}] = {v} ≥ {S.k}`：窗口 `{S.s[S.left:r + 1]}` ==合法== → 右移左端点'
    if S.left > 0 and S.s[S.left - 1] == c and S.cnt[c] == S.k - 1:
        return f'`cnt[{c!r}] = {v} < {S.k}`：窗口 `{S.s[S.left:r + 1]}` ==恰好不合法==，停'
    return f'`cnt[{c!r}] = {v} < {S.k}`：还没有字母到 k 次，不用缩小'


CONFIG = dict(
    num=3325, title='字符至少出现 K 次的子字符串 I', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 越长越合法',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
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
    call=f'Solution().numberOfSubstrings({S_IN!r}, {K})',
    expect=sum(1 for i in range(len(S_IN)) for j in range(i, len(S_IN))
               if max(S_IN[i:j + 1].count(ch) for ch in set(S_IN[i:j + 1])) >= K),
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（框 = 窗口，绿 = 本轮计入答案的左端点 0..left−1）',
             pointers={'left': 'blue', _r: 'pink'}, pointer_labels={_r: 'right'}, window=('left', _r),
             color=_color, cell=110, h=280),
        dict(type='map', var='cnt', label='cnt（窗口内每种字母的次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
    ],
    watch=[('left', 'left', 'blue'), 'c', ('k', 'k', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans = 0`，窗口左端点 `left = 0`',
        'cnt = defaultdict': '`cnt` 统计窗口内每种字母的次数',
        'for c in s': lambda S, B, r: ('右端点枚举完毕' if 'c' in B and _r(B) == len(S.s) - 1
                                       else f'枚举右端点：`{S.c!r}` 进入窗口'),
        'cnt[c] += 1': '`cnt[{c!r}]` → {cnt[c]}',
        'while cnt[c] >= k': _while,
        'cnt[s[left]] -= 1': '左端 `{s[left]!r}` 离开窗口：`cnt[{s[left]!r}]` → {cnt[s[left]]}',
        'left += 1': '`left` → {left}',
        'ans += left': lambda S, B, r: ('`left = 0`：还没有合法子串，`ans` 不变' if S.left == 0
                                        else f'`[{S.left - 1}, {_r(S)}]` 合法，更长的也合法 → `ans += {S.left}` = =={S.ans}=='),
        'return ans': '一共 =={ret}== 个合法子串',
    },
    max_steps=70,
    cards=dict(
        one_liner='枚举右端点，只盯刚进来的字母：它到 k 次就缩左端点',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（|Σ| = 26）',
        problem=['给字符串 `s` 和整数 `k`',
                 '求==至少有一个字符出现至少 k 次==的子串个数',
                 '示例：`s = "abacb", k = 2` → `4`',
                 f'本视频：`s = "{S_IN}", k = {K}`'],
        quote='因为只有 `cnt[c - \'a\']++` 导致了 `cnt[c - \'a\']` 达到 k，所以其余字母的出现次数必然小于 k，无需判断。',
        quote_src='—— 灵茶山艾府题解 · 答疑',
        idea=['窗口合法就右移 left；退出时 `[left−1, right]` 是==最后一个合法的==',
              '子串越长越合法 → 左端点 `0..left−1` 都合法，`ans += left`',
              '每次只有新字母 c 的次数变化，所以只判断 `cnt[c] >= k`'],
        summary=['时间 `O(n)`：`left` 总共最多右移 n 次',
                 '内层判断的是 `cnt[c]`，不是窗口里所有字母',
                 '`>=` 写成 `==` 也对：只有 c 会到达 k',
                 '和 1358、2799 同一个模板：越长越合法 → `ans += left`'],
    ),
)
