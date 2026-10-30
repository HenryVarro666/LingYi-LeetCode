CONFIG = dict(
    num=2900, title='最长相邻不相等子序列 I', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='每段连续相同取最左一个',
    tags=['难度分 1469'],
    code='''
class Solution(object):
    def getWordsInLongestSubsequence(self, n, words, groups):

        res = [words[0]]
        for index in range(1, n):
            if groups[index] != groups[index - 1]:
                res.append(words[index])
        
        return res
''',
    call='Solution().getWordsInLongestSubsequence(7, ["a","b","c","d","e","f","g"], [0,0,0,1,1,0,0])',
    expect=['a', 'd', 'f'],
    views=[
        dict(type='array', var='groups', h=170, label='groups', pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and i <= S['index'] and (i == 0 or S['groups'][i] != S['groups'][i-1]) else None),
        dict(type='array', var='words', h=170, label='words', pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if v in S['res'] else None),
        dict(type='array', var='res', h=170, label='res（已选）'),
    ],
    watch=['index'],
    captions={
        'res = [words[0]]': '第一个单词一定能选，作为起点：`res = {res}`',
        'for index in range': lambda S, B, r: ('遍历完毕，循环结束' if B.get('index') == S['index'] else f'看下标 `{S["index"]}`，和前一个比较 `groups`'),
        'if groups[index] != groups[index - 1]': '`groups[{index}] = {groups[index]}`，前一个 `{groups[index-1]}`：{"不同 → 新的一段开始了" if groups[index] != groups[index-1] else "相同 → 还在同一段里，跳过"}',
        'res.append(words[index])': '这一段的最左边单词入选：`res` = {res}',
        'return res': '每段选一个，共 ==`{len(res)}`== 个：{res}',
    },
    cards=dict(
        one_liner='只看 groups：每段连续相同的取最左一个',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['`words` 与 0/1 数组 `groups` 等长，选子序列使相邻两项的 `groups` 不同',
                 '求最长的这种子序列，任意一个答案即可',
                 '本视频：`groups = [0,0,0,1,1,0,0]` → `[a, d, f]`'],
        quote='相当于每段相同的子数组中只选择了其中最左侧下标对应的单词，保证了子序列中相邻位置对应的group值不同，同时也可以使得子序列最长。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词本身长什么样无关，只看 `groups`',
              '与前一个不同就说明进了新的一段，取它',
              '`res` 以 `words[0]` 起手，所以循环从 1 开始'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文函数名是 `getWordsInLongestSubsequence(n, words, groups)`，多带了参数 `n`，保持原样',
                 '取每段最左（与前一个比较）；灵神取每段最右，都对，答案任意',
                 '只有 0/1 两种值，所以「相邻不同」就是「换段」'],
    ),
)
