CODE = '''
class Solution:
    def countOfSubstrings(self, word: str, k: int) -> int:
        cnt_vowel1 = defaultdict(int)
        cnt_vowel2 = defaultdict(int)
        cnt_consonant1 = cnt_consonant2 = 0
        ans = left1 = left2 = 0
        for b in word:
            if b in "aeiou":
                cnt_vowel1[b] += 1
                cnt_vowel2[b] += 1
            else:
                cnt_consonant1 += 1
                cnt_consonant2 += 1

            while len(cnt_vowel1) == 5 and cnt_consonant1 >= k:
                out = word[left1]
                if out in "aeiou":
                    cnt_vowel1[out] -= 1
                    if cnt_vowel1[out] == 0:
                        del cnt_vowel1[out]
                else:
                    cnt_consonant1 -= 1
                left1 += 1

            while len(cnt_vowel2) == 5 and cnt_consonant2 > k:
                out = word[left2]
                if out in "aeiou":
                    cnt_vowel2[out] -= 1
                    if cnt_vowel2[out] == 0:
                        del cnt_vowel2[out]
                else:
                    cnt_consonant2 -= 1
                left2 += 1

            ans += left1 - left2
        return ans
'''
_L = CODE.strip('\n').split('\n')


def _ln(txt, nth=0):
    return [i + 1 for i, s in enumerate(_L) if txt in s][nth]


_BEFORE = {_ln('for b in word'), _ln('if b in "aeiou"')}
_PEND1 = {_ln('cnt_vowel1[out] -= 1'), _ln('if cnt_vowel1[out] == 0'), _ln('del cnt_vowel1[out]'), _ln('cnt_consonant1 -= 1')}
_PEND2 = {_ln('cnt_vowel2[out] -= 1'), _ln('if cnt_vowel2[out] == 0'), _ln('del cnt_vowel2[out]'), _ln('cnt_consonant2 -= 1')}


class _Named:
    def __init__(self, f, name):
        self.f, self.name = f, name

    def __call__(self, S):
        return self.f(S)

    def __str__(self):
        return self.name

    __repr__ = __str__


def _live(S):
    return 'left2' in S and 'ans' in S and 'b' in S


def _right(S):
    if not _live(S):
        return None
    ln = S['_line']
    size1 = sum(S['cnt_vowel1'].values()) + S['cnt_consonant1']
    r = S['left1'] + size1 - 1
    if ln in _BEFORE:
        r += 1
    if ln in _PEND1:
        r += 1
    return min(r, len(S['word']) - 1)


def _l1(S):
    return S['left1'] if _live(S) else None


def _l2(S):
    return S['left2'] if _live(S) else None


def _txt(S):
    if 'ans' not in S:
        return '窗口 1：元音齐 5 种且辅音 `>= k`（至少 k）；窗口 2：元音齐 5 种且辅音 `> k`（至少 k+1）'
    return (f"窗口1 `[{S['left1']}, right]`：元音 {len(S['cnt_vowel1'])} 种，辅音 {S['cnt_consonant1']}；"
            f"窗口2 `[{S['left2']}, right]`：元音 {len(S['cnt_vowel2'])} 种，辅音 {S['cnt_consonant2']}")


CONFIG = dict(
    num=3306, title='元音辅音字符串计数 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='恰好型滑窗 · 三指针 f(k) − f(k+1)',
    tags=['难度分 2200'],
    code=CODE,
    call='Solution().countOfSubstrings("aeiouqeb", 1)',
    expect=2,
    views=[
        dict(type='string', var='word', label='word（框 = 窗口1 [left1, right]；left2 是“至少 k+1 个辅音”的左端点）', cell=100, h=240,
             pointers={'left1': 'blue', 'left2': 'cyan', _Named(_right, 'right'): 'pink'}, window=(_l1, _right)),
        dict(type='map', var='cnt_vowel1', label='cnt_vowel1（窗口1 元音次数）', fmt=lambda k, v: f"'{k}': {v}", h=110, font=30),
        dict(type='map', var='cnt_vowel2', label='cnt_vowel2（窗口2 元音次数）', fmt=lambda k, v: f"'{k}': {v}", h=110, font=30),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('b', 'b', 'pink'), ('left1', 'left1', 'blue'), ('left2', 'left2', 'cyan'), ('ans', 'ans', 'green')],
    skip=['cnt_vowel2 = defaultdict', 'cnt_consonant1 = cnt_consonant2 = 0'],
    max_steps=100,
    captions={
        'cnt_vowel1 = defaultdict': '两个窗口：窗口 1 对应 f(k)（至少 k 个辅音），窗口 2 对应 f(k+1)（至少 k+1 个辅音）；各自记元音次数、辅音个数',
        'ans = left1 = left2 = 0': '两个左端点 `left1`、`left2`：==恰好 k 个辅音的起点 = left1 − left2 个==',
        'for b in word': lambda S, B, ret: ('遍历结束，所有右端点都枚举完了' if S.left1 + sum(S.cnt_vowel1.values()) + S.cnt_consonant1 == len(S.word)
                                            else f'枚举右端点：`b = {S.b!r}` 移入两个窗口'),
        'if b in "aeiou"': lambda S, B, ret: (f'`{S.b!r}` 是元音' if S.b in 'aeiou' else f'`{S.b!r}` 是辅音'),
        'cnt_vowel1[b] += 1': '元音 `{b!r}` 进入窗口 1',
        'cnt_vowel2[b] += 1': '元音 `{b!r}` 进入窗口 2',
        'cnt_consonant1 += 1': '辅音进入窗口 1：`cnt_consonant1 = {cnt_consonant1}`',
        'cnt_consonant2 += 1': '辅音进入窗口 2：`cnt_consonant2 = {cnt_consonant2}`',
        'while len(cnt_vowel1) == 5': lambda S, B, ret: (
            f'窗口 1：元音 `{len(S.cnt_vowel1)}` 种、辅音 `{S.cnt_consonant1} >= k = {S.k}` → ==合法==，缩左端点'
            if len(S.cnt_vowel1) == 5 and S.cnt_consonant1 >= S.k else
            f'窗口 1：元音 `{len(S.cnt_vowel1)}` 种、辅音 `{S.cnt_consonant1}`（k = {S.k}）→ 不合法，停止缩小'),
        'while len(cnt_vowel2) == 5': lambda S, B, ret: (
            f'窗口 2：元音 `{len(S.cnt_vowel2)}` 种、辅音 `{S.cnt_consonant2} > k = {S.k}` → 辅音==多于 k== ，缩左端点'
            if len(S.cnt_vowel2) == 5 and S.cnt_consonant2 > S.k else
            f'窗口 2：元音 `{len(S.cnt_vowel2)}` 种、辅音 `{S.cnt_consonant2}`（要 > {S.k}）→ 不满足，停止缩小'),
        'out = word[left1]': '窗口 1 左端点 `word[{left1}] = {out!r}` 准备移出',
        'out = word[left2]': '窗口 2 左端点 `word[{left2}] = {out!r}` 准备移出',
        'if out in "aeiou"': lambda S, B, ret: (f'`{S.out!r}` 是元音：减少它的次数' if S.out in 'aeiou' else f'`{S.out!r}` 是辅音：减少辅音个数'),
        'cnt_vowel1[out] -= 1': '`cnt_vowel1[{out!r}]` → `{cnt_vowel1[out]}`',
        'cnt_vowel2[out] -= 1': '`cnt_vowel2[{out!r}]` → `{cnt_vowel2[out]}`',
        'if cnt_vowel1[out] == 0': lambda S, B, ret: ('次数变 0：这种元音不在窗口 1 里了，==元音种类少一种==' if S.cnt_vowel1[S.out] == 0 else '这种元音还有，种类不变'),
        'if cnt_vowel2[out] == 0': lambda S, B, ret: ('次数变 0：这种元音不在窗口 2 里了，==元音种类少一种==' if S.cnt_vowel2[S.out] == 0 else '这种元音还有，种类不变'),
        'del cnt_vowel1[out]': '从 `cnt_vowel1` 删掉 `{out!r}`，`len` 变成 `{len(cnt_vowel1)}`',
        'del cnt_vowel2[out]': '从 `cnt_vowel2` 删掉 `{out!r}`，`len` 变成 `{len(cnt_vowel2)}`',
        'cnt_consonant1 -= 1': '窗口 1 辅音 → `{cnt_consonant1}`',
        'cnt_consonant2 -= 1': '窗口 2 辅音 → `{cnt_consonant2}`',
        'left1 += 1': '`left1` → `{left1}`',
        'left2 += 1': '`left2` → `{left2}`',
        'ans += left1 - left2': lambda S, B, ret: (
            f'`left1 − left2 = {S.left1} − {S.left2} = {S.left1 - S.left2}`：起点在 `[{S.left2}, {S.left1 - 1}]` 的子串，辅音==恰好 k 个== → `ans = {S.ans}`'
            if S.left1 > S.left2 else f'`left1 − left2 = 0`：这个右端点没有恰好 k 个辅音的子串'),
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='恰好 = 至少 k − 至少 k+1：两个窗口合成三指针',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['求 `word` 的子串中：==5 个元音都至少出现一次==，且==恰好含 k 个辅音==的个数',
                 '示例：`word = "aeiou", k = 0` → `1`',
                 '本视频：`word = "aeiouqeb", k = 1` → `2`（`aeiouq`、`aeiouqe`）'],
        quote='“至少 20 岁”可以分成“恰好 20 岁”和“至少 21 岁”，所以“至少 20 岁”的人数减去“至少 21 岁”的人数，就是“恰好 20 岁”的人数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f(k)`：元音齐全且辅音==至少== k 个的子串数；答案 = `f(k) − f(k+1)`',
              '子串越长越满足“至少”，两个都能用“枚举右端点、`ans += left`”的滑窗',
              '优化二：两个窗口共用一次遍历，`ans += left1 - left2`'],
        summary=['时间 `O(n)`，空间 `O(1)`（元音至多 5 种）',
                 '“至少 k” 与 “至少 k+1” 用的是 `>= k` 与 `> k`，别写反',
                 '`left1 >= left2` 恒成立：窗口 1 的条件更宽松，所以缩得更远',
                 '原文还给出“优化前”两次调用 `f(k) − f(k+1)` 的写法，本视频用三指针版本'],
    ),
)
