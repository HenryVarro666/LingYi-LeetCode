V = 'aeiou'


def _L(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['k'] + 1)


def _enter(S, B, ret):
    if S.c in 'aeiou':
        return f'`s[{S.i}] = {S.c!r}` 是元音 → 进入窗口后要计数'
    return f'`s[{S.i}] = {S.c!r}` 不是元音，`vowel` 不变'


def _lt(S, B, ret):
    if S.left < 0:
        return f'`left = {S.left} < 0`：窗口只有 {S.i + 1} 个字母，==不足 k={S.k}==，先不更新答案'
    return f'`left = {S.left}`：窗口 `{S.s[S.left:S.i + 1]!r}` 长度刚好为 {S.k}'


def _out(S, B, ret):
    o = S.s[S.left]
    if o in 'aeiou':
        return f'左端点 `s[{S.left}] = {o!r}` 是元音，离开窗口要减掉'
    return f'左端点 `s[{S.left}] = {o!r}` 不是元音，离开窗口不影响计数'


CONFIG = dict(
    num=1456, title='定长子串中元音的最大数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑窗 · 入-更新-出',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1263'],
    code='''
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        ans = vowel = 0
        for i, c in enumerate(s):  # 枚举窗口右端点 i
            # 1. 右端点进入窗口
            if c in "aeiou":
                vowel += 1

            left = i - k + 1  # 窗口左端点
            if left < 0:  # 窗口长度不足 k，尚未形成第一个窗口
                continue

            # 2. 更新答案
            ans = max(ans, vowel)
            if ans == k:  # 答案已经等于理论最大值
                break  # 无需再循环

            # 3. 左端点离开窗口，为下一个循环做准备
            if s[left] in "aeiou":
                vowel -= 1
        return ans
''',
    call='Solution().maxVowels("abciiidef", 3)',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（框 = 以 i 为右端点、长为 k 的窗口；绿 = 元音）', cell=100, h=260,
             pointers={_L: 'pink', 'i': 'blue'}, pointer_labels={_L: 'left'}, window=(_L, 'i'),
             color=lambda S, i, v: 'green' if v in V else None),
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"窗口 `{S['s'][max(0, S['i'] - S['k'] + 1):S['i'] + 1]!r}`：元音 `vowel = {S['vowel']}`，答案上限 `k = {S['k']}`"
                           if 'i' in S else '定长滑窗三步：==入 → 更新答案 → 出==')),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c'), ('left', 'left', 'pink'), ('vowel', 'vowel', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = vowel = 0': '`vowel`：窗口内元音个数；`ans`：最大值',
        'for i, c in enumerate(s)': lambda S, B, r: (f'枚举右端点 `i = {S.i}`，字母 `{S.c!r}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        'if c in "aeiou"': _enter,
        'vowel += 1': '==入==：元音进入窗口 → `vowel = {vowel}`',
        'left = i - k + 1': '右端点为 i、长为 k 的窗口，左端点 `left = {i} − {k} + 1 = {left}`',
        'if left < 0': _lt,
        'continue': '继续扩大窗口',
        'ans = max(ans, vowel)': '==更新答案==：`ans = max({B.ans}, {vowel}) = {ans}`',
        'if ans == k': lambda S, B, r: (f'`ans = {S.ans} == k`：窗口全是元音，==不可能更大了==' if S.ans == S.k
                                        else f'`ans = {S.ans} < k = {S.k}`，还可能更大，继续'),
        'break': '提前退出循环',
        'if s[left] in "aeiou"': _out,
        'vowel -= 1': '==出==：元音离开窗口 → `vowel = {vowel}`，为下一个窗口做准备',
        'return ans': '最多 `{ans}` 个元音',
    },
    cards=dict(
        one_liner='窗口右移一格：只看进来的和出去的那个字母',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求字符串 `s` 中长度==恰好为 k== 的子串里，最多含几个元音 `aeiou`',
                 '示例：`s = "abciiidef", k = 3` → `3`（子串 `"iii"`）'],
        quote='我总结成三步：入-更新答案-出。……以上三步适用于所有定长滑窗题目。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从 `abc` 到 `bci`：中间的 `b`、`c` 都在，只需看==离开的 a 和进入的 i==',
              '右端点为 `i` 时左端点是 `i−k+1`；`< 0` 说明第一个窗口还没形成',
              '优化：答案最大就是 `k`，一旦 `ans == k` 直接 `break`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '顺序是 ==入 → 更新 → 出==：出窗口后长度为 k−1，下轮进一个又是 k',
                 '易错：左端点是 `i−k+1` 不是 `i−k`（闭区间长度 R−L+1）',
                 '题解先给不带 break 的基础写法，本视频用带 `ans == k` 提前退出的优化写法'],
    ),
)
