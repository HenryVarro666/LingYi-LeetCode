CONFIG = dict(
    num=2781, title='最长合法子字符串的长度', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='单调左边界 + 枚举后缀',
    tags=['字符串', '难度分 2204'],
    code='''
class Solution(object):
    def longestValidSubstring(self, word, forbidden):

        forbidden_set = set(forbidden)
        left = 0
        res = 0
        right = 0
        while right < len(word):
            for index in range(max(0, right - 9), right + 1):
                if word[index : right + 1] in forbidden_set:
                    left = max(left, index + 1)
            
            res = max(res, right - left + 1)
            right += 1
        
        return res
''',
    call='Solution().longestValidSubstring("cbaaab", ["aaa", "cb"])',
    expect=3,
    max_steps=60,
    views=[
        dict(type='string', var='word', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=150,
             dim=lambda S, i, v: 'left' in S and 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=lambda S: (f"正在查 `word[{S['index']}:{S['right']+1}]` = =={S['word'][S['index']:S['right']+1]}==" if 'index' in S and 'right' in S and S['_line'] in (9, 10) else '')),
        dict(type='set', var='forbidden_set', h=120, fmt=lambda x: str(x)),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'index', ('res', 'res', 'green')],
    captions={
        'forbidden_set = set': '禁用串放进集合：{forbidden_set}，不用建 Trie 自动机',
        'while right': '右端点 `right = {right}`（字母 `{word[right]}`）：这个字母可能让窗口里出现禁用串',
        'for index in range': '禁用串长度 ≤ 10，起点只需从 `right - 9` 到 `right` 枚举',
        'if word[index': '子串 `word[{index}:{right+1}]` = `{word[index:right+1]}`：{"==是禁用串=="  if word[index:right+1] in forbidden_set else "不是禁用串"}',
        'left = max': '以 `{word[index:right+1]}` 为后缀的串不合法，起点至少是 `index+1`：`left = max({B.left}, {index+1}) = =={left}==`',
        'res = max': '当前合法窗口长 `{right-left+1}`，`res = max({B.res}, {right-left+1}) = {res}`',
        'right += 1': '`right` → {right}',
    },
    cards=dict(
        one_liner='left 只会右移；每步只查以 right 结尾的后缀',
        complexity='时间 `O(L + nM^2)`，空间 `O(L)`',
        problem=['不含任何禁用串的字符串是合法的',
                 '求 `word` 的最长合法子串长度',
                 '示例：`word="cbaaab"`，`forbidden=["aaa","cb"]` → `3`'],
        quote='题目保证了不良单词的长度不超过10，在这里就只需枚举所有不良单词可能的起点下标，也就是从right - 9开始枚举到right。',
        quote_src='—— yiduobo 题解',
        idea=['常规做法是 Trie 自动机，这里利用 ==单词长度 ≤ 10== 化简',
              '证明：right−1 对应的 left 左边都含禁用串，加一个字符后仍含，所以 left 不会回退',
              '枚举后缀，命中用 `index+1` 抬高 `left`，最后用窗口长度更新答案'],
        summary=['时间 `O(L + nM^2)`，空间 `O(L)`',
                 '易错：起点从 `max(0, right-9)` 开始，防止负下标切片',
                 '==用 max 更新 left==，因为枚举时后面命中的 index 不一定更大',
                 '禁用串长度上限 10 是关键前提'],
    ),
)
