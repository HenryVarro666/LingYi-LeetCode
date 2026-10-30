CONFIG = dict(
    num=340, title='至多包含K个不同字符的最长子串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · 哈希表计数',
    tags=['滑动窗口与双指针'],
    code='''
class Solution(object):
    def lengthOfLongestSubstringKDistinct(self, s, k):

        if k == 0:
            return 0

        cnt = {s[0] : 1}
        left = right = 0
        res = 1
        n = len(s)

        while right + 1 < n:
            right += 1
            cnt[s[right]] = cnt.get(s[right], 0) + 1
            while len(cnt) > k:
                cnt[s[left]] -= 1
                if cnt[s[left]] == 0:
                    cnt.pop(s[left])
                left += 1

            res = max(res, right - left + 1)

        return res
''',
    call="Solution().lengthOfLongestSubstringKDistinct('eceebad', 2)",
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 当前窗口）', cell=100, h=230,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right')),
        dict(type='map', var='cnt', label='cnt（窗口内每种字符的次数）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"窗口 `[{S['left']}, {S['right']}]`：字符种数 ==" + str(len(S['cnt'])) + f"== / k = {S['k']}，长度 {S['right']-S['left']+1}") if 'right' in S and 'cnt' in S and 'left' in S else ''),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('k', 'k', 'yellow'), ('res', 'res', 'green')],
    captions={
        'if k == 0': '`k = {k}`：k 为 0 时任何子串都不合法，答案直接是 0；这里 k > 0，继续',
        'cnt = {s[0]': '窗口先放进第一个字符：`cnt = {cnt}`，答案至少是 ==1==',
        'while right + 1 < n': lambda S, B, r: (f'`right + 1 = {S.right + 1} < n = {S.n}`：还有字符没进窗口，继续' if S.right + 1 < S.n else f'`right + 1 = {S.right + 1}` 不小于 n = {S.n}：字符都扫完了，结束'),
        'right += 1': '枚举右边界：`right` → {right}，新字符 `{s[right]}` 要进窗口',
        'cnt[s[right]] = ': '`{s[right]}` 的次数变成 `{cnt[s[right]]}`，窗口内共有 ==`{len(cnt)}`== 种字符',
        'while len(cnt) > k': lambda S, B, r: (f'种数 `{len(S.cnt)}` > k = `{S.k}`：窗口不合法，必须收缩左边界' if len(S.cnt) > S.k
                                              else f'种数 `{len(S.cnt)}` <= k = `{S.k}`：窗口合法，不用收缩'),
        'cnt[s[left]] -= 1': '左边界字符 `{s[left]}` 离开窗口，次数减 1 → `{cnt[s[left]]}`',
        'if cnt[s[left]] == 0': lambda S, B, r: (f'`{S.s[S.left]}` 的次数降到 0：窗口里已经没有它，要从 cnt 删掉才能让种数减少' if S.cnt[S.s[S.left]] == 0
                                               else f'`{S.s[S.left]}` 还剩 {S.cnt[S.s[S.left]]} 个，窗口里仍有它，不删'),
        'cnt.pop': '删掉 `{B.s[B.left]}`，种数降为 ==`{len(cnt)}`==',
        'left += 1': '`left` 右移到 {left}',
        'res = max': '此时 `[left, right]` 是以 right 结尾、最长的合法窗口，长度 `{right - left + 1}`：`res = max({B.res}, {right - left + 1}) = {res}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='右边界一路向右，种类超了就收左边界',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['给定字符串 `s` 和整数 `k`，求==最多包含 k 种不同字符==的最长子串长度',
                 '示例：`s = "eceba", k = 2` → `3`（子串 `"ece"`）',
                 '本视频：`s = "eceebad", k = 2` → `4`'],
        quote='随着right的向右移动，若当前窗口中出现的字符种数超过了k种，那么就需要将左边界left不断向右移动，直到窗口内出现的字符种树回到k种为止',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt` 记录窗口内每种字符的次数，`len(cnt)` 就是种数',
              '种数超过 k：不断移出 `s[left]`，次数减到 0 就从 `cnt` 里 ==pop==',
              '停下时的 `left` 是以 `right` 结尾的最小合法左端点，用窗口长度更新答案'],
        summary=['时间 `O(n)`：每个字符最多进出窗口各一次；空间 `O(k)`',
                 '`k == 0` 要先单独返回 0，否则初始窗口 `cnt = {s[0]: 1}` 本身就不合法',
                 '次数减到 0 必须 `pop`，否则 `len(cnt)` 不会减少，会一直收缩',
                 '原文题面缺失，题意按 LeetCode 340 补写；代码在 Python 3 下无需修改'],
    ),
)
