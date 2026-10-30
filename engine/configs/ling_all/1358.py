S_IN = 'abcabc'


def _r(S):
    if 'cnt' not in S or 'c' not in S:
        return None
    # 窗口长度 = cnt 的总数；第 9–11 行 out 已减掉但 left 还没右移
    return S['left'] + sum(S['cnt'].values()) - 1 + (1 if S.get('_line') in (9, 10, 11) else 0)


def _color(S, i, v):
    if 'left' not in S or 'c' not in S:
        return None
    if S['_line'] == 13 and i < S['left']:
        return 'green'
    return None


def _top(S):
    if 'c' not in S:
        return '子串越长越可能包含 abc → ==越长越合法=='
    l = S['left']
    if S['_line'] == 13:
        if l == 0:
            return '左端点 `0..left−1` 为空：以当前字母结尾的合法子串 ==0== 个'
        return f"左端点取 `0..{l - 1}` 都合法 → 本轮 =={l}== 个"
    kinds = sum(1 for v in S['cnt'].values() if v > 0)
    return f"窗口里有 {kinds} 种字母" + ('，==abc 齐了==，缩小左端点' if kinds == 3 else '')


def _while(S, B, ret):
    r = _r(S)
    if len(S.cnt) == 3:
        return f'`len(cnt) == 3`：窗口 `{S.s[S.left:r + 1]}` 含 abc，==合法== → 右移左端点'
    if S.left > 0 and len(set(S.s[S.left - 1:r + 1])) == 3:
        return f'`len(cnt) = {len(S.cnt)}`：窗口 `{S.s[S.left:r + 1]}` ==恰好不合法==，停止缩小'
    return f'`len(cnt) = {len(S.cnt)}`：窗口还没凑齐 abc，不用缩小'


CONFIG = dict(
    num=1358, title='包含所有三种字符的子字符串数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 越长越合法',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1646'],
    code='''
class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        cnt = defaultdict(int)
        ans = left = 0
        for c in s:
            cnt[c] += 1
            while len(cnt) == 3:
                out = s[left]  # 离开窗口的字母
                cnt[out] -= 1
                if cnt[out] == 0:
                    del cnt[out]
                left += 1
            ans += left
        return ans
''',
    call=f'Solution().numberOfSubstrings({S_IN!r})',
    expect=10,
    setup='',
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（绿 = 本轮计入答案的左端点 0..left−1）', pointers={'left': 'blue', _r: 'pink'}, pointer_labels={_r: 'right'}, window=('left', _r),
             color=_color, cell=110, h=280),
        dict(type='map', var='cnt', label='cnt（窗口内每种字母的次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
    ],
    watch=[('left', 'left', 'blue'), 'c', 'out', ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 统计窗口内每种字母的出现次数',
        'ans = left = 0': '`ans = 0`，窗口左端点 `left = 0`',
        'for c in s': lambda S, B, r: ('右端点枚举完毕' if 'c' in B and _r(B) == len(S.s) - 1
                                       else f'枚举右端点：字母 `{S.c!r}` 进入窗口'),
        'cnt[c] += 1': '`cnt[{c!r}]` → {cnt[c]}',
        'while len(cnt)': _while,
        'out = s[left]': '左端字母 `{out!r}` 离开窗口',
        'cnt[out] -= 1': '`cnt[{out!r}]` → {cnt[out] if out in cnt else 0}',
        'if cnt[out] == 0': lambda S, B, r: (f'`cnt[{S.out!r}]` 变成 0：窗口里==没有== {S.out!r} 了' if S.cnt[S.out] == 0
                                             else f'窗口里还有 {S.cnt[S.out]} 个 {S.out!r}，种数不变'),
        'del cnt[out]': '删掉键 `{out!r}` → 种数变成 {len(cnt)}',
        'left += 1': '`left` → {left}',
        'ans += left': lambda S, B, r: (f'`left = 0`：还没有合法子串，`ans` 不变' if S.left == 0 else f'`[{S.left - 1}, {_r(S)}]` 合法，左端点更靠左的也合法 → `ans += {S.left}` = =={S.ans}=='),
        'return ans': '一共 =={ret}== 个包含 abc 的子串',
    },
    max_steps=75,
    cards=dict(
        one_liner='枚举右端点，把左端点推到“恰好不合法”，左边的 left 个都合法',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（|Σ| = 3）',
        problem=['字符串 `s` 只含 a、b、c',
                 '求 ==a、b、c 都至少出现一次== 的子串个数',
                 '示例：`"abcabc"` → `10`；`"aaacb"` → `3`'],
        quote='当右端点固定在 right 时，左端点在 0,1,2,…,left−1 的所有子串都是符合要求的，这一共有 left 个，加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['窗口含 abc 就右移 left，直到==恰好不合法==',
              '此时 `[left−1, right]` 合法，更长的 `[0..left−2, right]` ==也合法==',
              '保留“外层枚举右端点”的暴力思路，所以不重不漏'],
        summary=['时间 `O(n)`：`left` 总共最多右移 n 次',
                 '`cnt[out]` 减到 0 要 `del`，否则 `len(cnt)` 不会变小',
                 '越长越合法：`ans += left`；越短越合法：`ans += right − left + 1`',
                 '写法二用长为 3 的数组 + `cnt[0] and cnt[1] and cnt[2]`',
                 '改成“每种至少 k 次”，只需把判断换成 `>= k`'],
    ),
)
