KEY = 'TTFTTFTT'
K = 1


def _color(S, i, v):
    if 'right' not in S:
        return None
    if S['left'] <= i <= S['right']:
        return 'blue' if v == 'T' else 'orange'
    return None


def _dim(S, i, v):
    return 'right' in S and not (S['left'] <= i <= S['right'])


def _top(S):
    if 'right' not in S:
        return f'合法子串：==T 不超过 k 个，或者 F 不超过 k 个==（k = {K}）'
    t, f = S['cnt']['T'], S['cnt']['F']
    bad = t > K and f > K
    return (f"窗口里 `T = {t}`、`F = {f}`：" +
            ('==两个都超过 k==，改不完 → 缩小' if bad else
             f"把 {'F' if f <= t else 'T'} 全改掉只需 `{min(t, f)}` 次 ≤ `{K}` → ==合法=="))


def _while(S, B, ret):
    t, f = S.cnt['T'], S.cnt['F']
    if t > S.k and f > S.k:
        return f'`T = {t} > {S.k}` 且 `F = {f} > {S.k}`：改成全 T 或全 F ==都不够次数== → 移出 `answerKey[{S.left}]`'
    return f'`T = {t}`、`F = {f}`，==至少一个 ≤ k== → 窗口合法'


CONFIG = dict(
    num=2024, title='考试的最大困扰度', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 至多 k 个 T 或 F',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def maxConsecutiveAnswers(self, answerKey: str, k: int) -> int:
        ans = left = 0
        cnt = defaultdict(int)
        for right, ch in enumerate(answerKey):
            cnt[ch] += 1
            while cnt['T'] > k and cnt['F'] > k:
                cnt[answerKey[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call=f'Solution().maxConsecutiveAnswers({KEY!r}, {K})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='answerKey', label='answerKey（框 = 窗口；蓝 = T，橙 = F）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_color, dim=_dim, cell=100, h=300),
        dict(type='map', var='cnt', label='cnt（窗口内 T / F 的个数）', fmt=lambda k, v: f"'{k}': {v}", font=34, h=150),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'ch', ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans = 0`，窗口左端 `left = 0`',
        'cnt = defaultdict': '`cnt` 统计窗口里 T 和 F 各有几个',
        'for right, ch in': lambda S, B, r: ('右端点枚举完毕' if 'right' in B and B.right == S.right
                                             else f'枚举右端点 `right = {S.right}`，`{S.ch!r}` 进入窗口'),
        'cnt[ch] += 1': "`cnt['{ch}']` → {cnt[ch]}",
        "while cnt['T']": _while,
        'cnt[answerKey[left]] -= 1': lambda S, B, r: f"`{S.answerKey[S.left]!r}` 离开窗口：`cnt[{S.answerKey[S.left]!r}]` → {S.cnt[S.answerKey[S.left]]}",
        'left += 1': '`left` → {left}',
        'ans = max': '窗口 `[{left}, {right}]` 长 `{right - left + 1}`：`ans = max({B.ans}, {right - left + 1})` = =={ans}==',
        'return ans': '最多 =={ret}== 个连续相同答案',
    },
    max_steps=60,
    cards=dict(
        one_liner='窗口里 T 和 F 只要有一个不超过 k，就能全改成另一个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `answerKey` 只含 T/F，最多修改 `k` 次',
                 '求修改后==最长的连续相同字符==个数',
                 '示例：`"TTFTTFTT", k = 1` → `5`'],
        quote='求 answerKey 的一个最长子串，包含==至多 k 个 T 或者至多 k 个 F==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子串越长越难满足要求 → 有单调性，用滑动窗口',
              '`T` 和 `F` 的次数==都==超过 k 时，必须右移 left',
              '一次遍历同时处理「全变 T」和「全变 F」两种情况'],
        summary=['时间 `O(n)`：left 总共右移不超过 n 次；空间 `O(1)`',
                 'while 条件是 `and`：两个都超才不合法',
                 '技巧：T、F 的 ASCII 除以 2 奇偶不同，可以只统计二进制次低位',
                 '思考题：把子串改成子序列怎么做？'],
    ),
)
