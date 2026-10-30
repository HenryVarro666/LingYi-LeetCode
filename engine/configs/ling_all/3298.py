CODE = '''
class Solution:
    def validSubstringCount(self, s: str, t: str) -> int:
        if len(s) < len(t):
            return 0

        # t 的字母出现次数与 s 的字母出现次数之差
        diff = defaultdict(int)  # 也可以用 Counter(t)，但是会慢很多
        for c in t:
            diff[c] += 1

        # 窗口内有 less 个字母的出现次数比 t 的少
        less = len(diff)

        ans = left = 0
        for c in s:
            diff[c] -= 1
            if diff[c] == 0:
                # c 移入窗口后，窗口内 c 的出现次数和 t 的一样
                less -= 1
            while less == 0:  # 窗口符合要求
                if diff[s[left]] == 0:
                    # s[left] 移出窗口之前，检查出现次数，
                    # 如果窗口内 s[left] 的出现次数和 t 的一样，
                    # 那么 s[left] 移出窗口后，窗口内 s[left] 的出现次数比 t 的少
                    less += 1
                diff[s[left]] += 1
                left += 1
            ans += left
        return ans
'''
_L = CODE.strip('\n').split('\n')


def _ln(txt):
    return [i + 1 for i, s in enumerate(_L) if txt in s][0]


class _Named:
    def __init__(self, f, name):
        self.f, self.name = f, name

    def __call__(self, S):
        return self.f(S)

    def __str__(self):
        return self.name

    __repr__ = __str__


def _live(S):
    return 'left' in S and 'ans' in S and 'c' in S


def _right(S):
    if not _live(S):
        return None
    w = len(S['t']) - sum(S['diff'].values())
    if S['_line'] in (_ln('for c in s'), _ln('diff[s[left]] += 1')):
        r = S['left'] + w
    else:
        r = S['left'] + w - 1
    return min(r, len(S['s']) - 1)


def _left(S):
    return S['left'] if _live(S) else None


def _txt(S):
    if 'less' not in S:
        return '`diff[x]` = t 里 x 的次数 − 窗口里 x 的次数；`diff[x] > 0` 表示 x ==还不够=='
    need = [k for k, v in S['diff'].items() if v > 0]
    show = '、'.join(need) if need else '无'
    if len(need) != S['less']:
        return f"`less = {S['less']}`：正在移出 `{S['s'][S['left']]}`，`diff` 马上同步更新"
    return f"`less = {S['less']}`：窗口里还不够的字母：{show}"


CONFIG = dict(
    num=3298, title='统计重新排列后包含另一个字符串的子字符串数目 II', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑窗 · 覆盖 t 的个数',
    tags=['难度分 1909'],
    code=CODE,
    call='Solution().validSubstringCount("abcabc", "abc")',
    expect=10,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口 [left, right]）', cell=100, h=230,
             pointers={'left': 'blue', _Named(_right, 'right'): 'pink'}, window=(_left, _right)),
        dict(type='map', var='diff', label='diff（t 的次数 − 窗口次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('c', 'c', 'pink'), ('left', 'left', 'blue'), ('less', 'less', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'if len(s) < len(t)': '`s` 比 `t` 短，肯定凑不出；这里不短，继续',
        'diff = defaultdict': '`diff[x]`：t 里 x 的次数 − 窗口里 x 的次数',
        'diff[c] += 1': '先把 `t` 的字母次数记下：`diff[{c!r}] = {diff[c]}`',
        'less = len(diff)': '`less`：窗口里次数==不够==的字母种数，一开始 = `{less}`',
        'ans = left = 0': '`left` 是窗口左端点，`ans` 累计答案',
        'for c in s': lambda S, B, ret: ('遍历结束' if S.left + len(S.t) - sum(S.diff.values()) == len(S.s) and S.get('ans', 0) > 0 and 'less' in B and S.c == B.c
                                         else f'枚举右端点：`s[right] = {S.c!r}` 移入窗口'),
        'diff[c] -= 1': '窗口里多了一个 `{c!r}` → `diff[{c!r}] = {diff[c]}`',
        'if diff[c] == 0': lambda S, B, ret: (f'`diff[{S.c!r}] == 0`：窗口里 {S.c!r} 的次数==刚好够了==' if S.diff[S.c] == 0
                                              else f'`diff[{S.c!r}] = {S.diff[S.c]}`：还不够或已经多了，less 不变'),
        'less -= 1': '少了一种“不够”的字母 → `less = {less}`',
        'while less == 0': lambda S, B, ret: (f'`less == 0`：窗口覆盖了 t，==合法==，缩左端点' if S.less == 0
                                              else f'`less = {S.less}`：窗口不再覆盖 t，停止缩小'),
        'if diff[s[left]] == 0': lambda S, B, ret: (f'`diff[{S.s[S.left]!r}] == 0`：{S.s[S.left]!r} 刚好够，移出去就==不够了==' if S.diff[S.s[S.left]] == 0
                                                    else f'`diff[{S.s[S.left]!r}] = {S.diff[S.s[S.left]]}`：{S.s[S.left]!r} 有富余，移出去也还够'),
        'less += 1': '又有一种字母不够了 → `less = {less}`',
        'diff[s[left]] += 1': '`{s[left]!r}` 移出窗口 → `diff[{s[left]!r}] = {diff[s[left]]}`',
        'left += 1': '`left` 右移到 `{left}`',
        'ans += left': lambda S, B, ret: (f'`left = 0`：这个右端点没有合法子串 → 贡献 `0`' if S.left == 0
                                          else f'退出循环时 `[left, right]` 不合法，但 `[left-1, right]` 合法 → 起点 `0 ~ {S.left - 1}` 都行，共 `{S.left}` 个 → `ans = {S.ans}`'),
        'return ans': '返回 `{ans}`',
    },
    max_steps=100,
    cards=dict(
        one_liner='重排不影响计数 → 就是“覆盖 t”的滑窗，统计个数',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['`x` 重新排列后 `t` 是它的前缀，`x` 就==合法==',
                 '统计 `s` 里合法子串的个数（`s` 最长 `10^6`，要线性）',
                 '示例：`s = "abcabc", t = "abc"` → `10`'],
        quote='由于子串可以重排，只要子串可以涵盖（见 76 题）字符串 t，那么子串就可以通过重排，使得 t 是子串的前缀。所以本题是 76. 最小覆盖子串 的求个数版本。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法 ⇔ 窗口里每种字母次数 ≥ t 的次数 → 子串越长越合法',
              '`diff` 记差值，`less` 记“还不够”的字母种数，`less == 0` 就覆盖了 t',
              '右端点固定时，合法起点是 `0 ~ left-1`，`ans += left`'],
        summary=['时间 `O(n)`，left 总共只右移 n 次；空间 `O(26)`',
                 '`diff` 用 defaultdict，比 Counter 快',
                 '易错：移出前先判断 `diff[s[left]] == 0`，再加一',
                 '和 76 题同一个滑窗，只是把“找最短”换成“数个数”'],
    ),
)
