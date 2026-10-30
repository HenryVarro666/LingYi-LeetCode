S0 = 'aabbaacb'


def _color(S, i, v):
    if 'right' in S and 'left' in S and S['left'] <= i <= S['right'] and v == S['s'][S['right']] \
            and S['freq'].get(v, 0) > 2:
        return 'red'
    return None


CONFIG = dict(
    num=3090, title='每个字符最多出现两次的最长子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def maximumLengthSubstring(self, s):

        freq = Counter()
        left = 0
        res = 0
        for right in range(len(s)):
            freq[s[right]] += 1
            while freq[s[right]] > 2:
                freq[s[left]] -= 1
                left += 1

            res = max(res, right - left + 1)

        return res
''',
    call=f'Solution().maximumLengthSubstring({S0!r})',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口 [left, right]，红 = 出现了 3 次）', h=250, cell=100,
             pointers={'left': 'pink', 'right': 'blue'}, window=('left', 'right'), color=_color),
        dict(type='map', var='freq', label='freq（窗口内字符频次）', h=170, font=36,
             fmt=lambda k, v: f"'{k}': {v}"),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"当前窗口 `{S['s'][S['left']:S['right'] + 1]!r}`，`res = {S['res']}`" if 'right' in S else '')),
    ],
    watch=[('left', 'left', 'pink'), ('right', 'right', 'blue'), ('res', 'res', 'green')],
    captions={
        'freq = Counter()': '`freq` 记录窗口里每种字符出现几次',
        'left = 0': '窗口左边界 `left = 0`',
        'res = 0': '`res` 记录最长合法窗口',
        'for right in': lambda S, B, r: ('右边界走到头，结束' if B.get('right') == S.right
                                         else f'右边界扩到 `right = {S.right}`，读入 `{S.s[S.right]!r}`'),
        'freq[s[right]] += 1': '`freq[{s[right]!r}]` → {freq[s[right]]}',
        'while freq[s[right]] > 2': lambda S, B, r: (
            f'`{S.s[S.right]!r}` 出现了 {S.freq[S.s[S.right]]} 次，==超过两次== → 左边界右移' if S.freq[S.s[S.right]] > 2
            else f'`{S.s[S.right]!r}` 出现 {S.freq[S.s[S.right]]} 次，不超过两次，窗口合法'),
        'freq[s[left]] -= 1': '移出 `{s[left]!r}`：`freq[{s[left]!r}]` → {freq[s[left]]}',
        'left += 1': '左边界右移，窗口缩小：`left` → {left}',
        'res = max': '合法窗口长 `{right - left + 1}`，`res = {res}`',
        'return res': '答案 =={res}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='保持窗口内每种字符不超过两次，窗口越长越好',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['求最长的子串，使得其中==每个字符最多出现两次==，返回长度',
                 '示例：`s = "bcbbbcba"` → `4`；`s = "aaaa"` → `2`',
                 '本视频：`s = "aabbaacb"` → `5`（`"baacb"`）'],
        quote='题目的数据规模很小，直接暴力是完全可行的。我在这里使用的是变长的滑动窗口从左向右滑动，保持窗口内每种字符出现次数不超过两次即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 100`，暴力枚举所有子串也能过',
              '更好的做法：右边界每次扩一格，`freq` 记录频次',
              '新字符超过两次就移动左边界，直到它回到两次'],
        summary=['时间 `O(n)`：左右边界各最多走 n 步',
                 '只有新进来的字符可能超标，所以 `while` 只看 `freq[s[right]]`',
                 '原文的 Python 2 风格代码可直接在 Python 3 运行，未做改动',
                 '与灵神写法几乎一致：灵神用 `defaultdict`，yiduobo 用 `Counter`'],
    ),
)
