CONFIG = dict(
    num=159, title='至多包含两个不同字符的最长子串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑窗 · 哈希表计数',
    tags=[],
    code='''
class Solution(object):
    def lengthOfLongestSubstringTwoDistinct(self, s):

        char_cnt = {s[0] : 1}
        res = 1
        left = right = 0
        while right + 1 < len(s):
            right += 1
            char_cnt[s[right]] = char_cnt.get(s[right], 0) + 1
            while len(char_cnt) > 2:
                char_cnt[s[left]] -= 1
                if char_cnt[s[left]] == 0:
                    char_cnt.pop(s[left])
                left += 1
            
            res = max(res, right - left + 1)
        
        return res
''',
    call="Solution().lengthOfLongestSubstringTwoDistinct('abaccc')",
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口）', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), cell=100, h=230),
        dict(type='map', var='char_cnt', label='char_cnt（窗口内每种字符的次数）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'char_cnt = {s[0]': '窗口先含第 0 个字符：`char_cnt = {char_cnt}`',
        'res = 1': '一个字符的窗口长度是 1，`res = 1`',
        'while right + 1 < len(s)': '右边还有字符吗？{"有，继续扩张" if right + 1 < len(s) else "没有了，结束"}',
        'right += 1': '窗口右边界右移到 `right = {right}`，新字符 `{s[right]}`',
        'char_cnt[s[right]] =': '新字符计数 +1：`char_cnt = {char_cnt}`',
        'while len(char_cnt) > 2': '窗口有 `{len(char_cnt)}` 种字符：{"超过 2 种，要缩小窗口" if len(char_cnt) > 2 else "不超过 2 种，窗口合法"}',
        'char_cnt[s[left]] -= 1': '左边界字符 `{s[left]}` 次数 −1：`char_cnt = {char_cnt}`',
        'if char_cnt[s[left]] == 0': '`{s[left]}` 的次数{"减到 0，这种字符已离开窗口" if char_cnt[s[left]] == 0 else "还大于 0，窗口里仍有它"}',
        'char_cnt.pop': '从哈希表里删掉 `{s[left]}`，字符种类少一种',
        'left += 1': '左边界右移到 `left = {left}`',
        'res = max': '窗口长 `{right - left + 1}`：`res = max({B.res}, {right - left + 1}) = {res}`',
        'return res': '最长子串长度 `{res}`',
    },
    cards=dict(
        one_liner='哈希表数窗口里的字符种类，超过 2 种就收左边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定字符串 `s`，求至多包含两种不同字符的最长子串长度',
                 '例如 `eceba` → `3`（子串 `ece`）',
                 '本视频：`abaccc` → `4`（子串 `accc`）'],
        quote='经典的变长滑动窗口问题，使用一个哈希表cnt_dict记录当前窗口中每种字符出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮窗口右边界右移一位，用新字符更新哈希表',
              '哈希表里超过 2 种字符，就不断右移左边界，直到不超过 2 种',
              '定好左右边界后，用窗口长度更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`（哈希表最多 3 项）',
                 '次数减到 0 要 `pop`，否则 `len(char_cnt)` 会算错',
                 '开头直接放入 `s[0]`，所以空串需要另外考虑（本题 s 非空）',
                 '同类题：340（至多 K 个不同字符）'],
    ),
)
