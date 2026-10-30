CONFIG = dict(
    num=2781, title='最长合法子字符串的长度', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='滑动窗口 + 枚举短后缀',
    tags=['字符串', '难度分 2204'],
    code='''
class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        fb = set(forbidden)
        ans = left = 0
        for right in range(len(word)):
            for i in range(right, max(right - 10, left - 1), -1):
                if word[i: right + 1] in fb:
                    left = i + 1  # 当子串右端点 >= right 时，合法子串一定不能包含 word[i]
                    break
            ans = max(ans, right - left + 1)
        return ans
''',
    call='Solution().longestValidSubstring("cbaaab", ["aaa", "cb"])',
    expect=3,
    views=[
        dict(type='string', var='word', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=150,
             dim=lambda S, i, v: 'left' in S and 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=lambda S: (f"正在查 `word[{S['i']}:{S['right']+1}]` = =={S['word'][S['i']:S['right']+1]}==" if 'i' in S and 'right' in S and S['_line'] in (7, 8) else '')),
        dict(type='set', var='fb', h=120, fmt=lambda x: str(x)),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'i', ('ans', 'ans', 'green')],
    captions={
        'fb = set': '禁用串放进哈希表：{fb}，查询 `O(1)` 级；每个禁用串最长 10',
        'for right in': '右端点 `right = {right}`（字母 `{word[right]}`）：新字母可能凑成禁用串',
        'for i in range': '从 `right` 往左枚举起点 `i`，只查长度 ≤ 10 且不越过 `left` 的后缀',
        'if word[i': '子串 `word[{i}:{right+1}]` = `{word[i:right+1]}`：{"==是禁用串==" if word[i:right+1] in fb else "不在禁用表里"}',
        'left = i + 1': '`{word[i:right+1]}` 被禁，窗口不能含 `word[{i}]`：`left` → =={left}==，break（再往左的更靠左，不用管）',
        'ans = max': '合法窗口长 `right - left + 1 = {right-left+1}`，`ans = max({B.ans}, {right-left+1}) = {ans}`',
    },
    cards=dict(
        one_liner='右端点右移，只查以它结尾的短后缀有没有被禁',
        complexity='时间 `O(L + nM^2)`，空间 `O(L)`',
        problem=['不含任何禁用串的字符串叫合法串',
                 '求 `word` 最长合法子串的长度',
                 '示例：`word="cbaaab"`，`forbidden=["aaa","cb"]` → `3`'],
        quote='当 right 右移到一个新的字母时，枚举以该字母为右端点的 forbidden[i] 的最短长度。如果发现子串 word[i] 到 word[right] 在 forbidden 中，那么更新 left=i+1 并结束枚举。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左端点只会右移（单调），典型滑动窗口',
              '禁用串长度 ≤ 10，所以==只需从 right 往左看最多 10 个字符==',
              '从短到长枚举，命中就 `left = i + 1` 并 break'],
        summary=['时间 `O(L + n M^2)`，`M = 10`，字符串哈希查询 `O(M)`',
                 '易错：枚举下界是 `max(right-10, left-1)`，不要越过 `left`',
                 '命中后 ==最近的起点 i 最大，直接 break==，不用继续往左',
                 '另一种做法：Trie / AC 自动机'],
    ),
)
