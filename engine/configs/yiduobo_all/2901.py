CONFIG = dict(
    num=2901, title='最长相邻不相等子序列 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='子序列 DP：f[index] + pre 数组还原',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1899'],
    code='''
class Solution(object):
    def getWordsInLongestSubsequence(self, n, words, groups):

        f = []
        pre = []

        for index in range(n):
            f.append(1)
            pre.append(None)
            for pre_index in range(index):
                if groups[pre_index] != groups[index] and len(words[index]) == len(words[pre_index]) and f[-1] <= f[pre_index]:
                    diff = 0
                    for x, y in zip(words[index], words[pre_index]):
                        if x != y:
                            diff += 1
                            if diff == 2:
                                break

                    if diff < 2:
                        f[-1] = f[pre_index] + 1
                        pre[-1] = pre_index
        
        p = 0
        for index in range(1, n):
            if f[index] > f[p]:
                p = index
        
        res = []
        while p is not None:
            res.append(words[p])
            p = pre[p]
        
        res.reverse()
        return res
''',
    call="Solution().getWordsInLongestSubsequence(3, ['ab','aa','ba'], [1,2,1])",
    expect=['ab', 'aa', 'ba'],
    max_steps=120,
    views=[
        dict(type='text', size=25, h=60, fn=lambda S: (
            f"`{S['words'][S['index']]}`（组 {S['groups'][S['index']]}）能接在 `{S['words'][S['pre_index']]}`（组 {S['groups'][S['pre_index']]}）后面吗？" if 'pre_index' in S and S.get('_line', 0) <= 20 and 'p' not in S else
            ('找 `f` 最大的位置 `p`，再顺着 `pre` 往回走' if 'p' in S else ''))),
        dict(type='array', var='words', label='words', h=230, cell=90, pointers={'index': 'blue', 'pre_index': 'pink'}),
        dict(type='array', var='groups', label='groups', h=130, cell=70, index=False),
        dict(type='array', var='f', label='f（以 words[i] 结尾的最长长度）', h=150, cell=90,
             color=lambda S, k, v: 'green' if k == S.get('p') else None),
        dict(type='array', var='pre', label='pre（上一个下标）', h=150, cell=90,
             color=lambda S, k, v: 'yellow' if k == S.get('p') else None),
    ],
    watch=['index', 'pre_index', 'diff', 'p', ('res', 'res', 'green')],
    captions={
        'f = []': '`f[i]`：以 `words[i]` 结尾的最长合法子序列长度',
        'pre = []': '`pre[i]`：它的前一个下标，用来最后还原方案',
        'for index in range(n)': lambda S, B, r: ('每个位置都算完了' if 'index' in B and B.index == S.index and 'p' not in B and len(S.f) == S.n else f'计算以 `words[{S.index}] = {S.words[S.index]!r}` 结尾的最长长度'),
        'f.append(1)': '先假设前面的都不要，只选自己：`f[{index}] = 1`',
        'pre.append(None)': '此时前一个下标是 `None`',
        'for pre_index in range(index)': lambda S, B, r: (
            '前面没有别的单词，不用找前驱' if S.index == 0 else
            f'尝试接在 `words[{S.pre_index}] = {S.words[S.pre_index]!r}` 后面' if not (S.pre_index == S.index - 1 and B.get('pre_index') == S.pre_index) else
            '前面的单词都试过了'),
        'if groups[pre_index] != groups[index]': lambda S, B, r: (
            f"组 `{S.groups[S.pre_index]}` vs `{S.groups[S.index]}`：" + ("相同 → 不行" if S.groups[S.pre_index] == S.groups[S.index] else
             "不同；" + ("长度不等 → 不行" if len(S.words[S.index]) != len(S.words[S.pre_index]) else
             ("`f[-1] > f[pre_index]`：接上去也不会更长 → 跳过" if S.f[-1] > S.f[S.pre_index] else "长度相同，且接上去能更长 → 数一数有几个字母不同")))),
        'diff = 0': '数不同字母的个数，最多允许 1 个',
        'for x, y in zip': '对比 `{x}` 和 `{y}`',
        'if x != y': lambda S, B, r: (f"`{S.x} != {S.y}`：不同" if S.x != S.y else f"`{S.x} == {S.y}`：相同"),
        'diff += 1': '不同字母数 `diff = {diff}`',
        'if diff == 2': lambda S, B, r: ('`diff == 2`：已经 2 个不同，提前 break' if S.diff == 2 else '`diff = 1`，继续比较'),
        'break': '不同字母不止 1 个，不用再比了',
        'if diff < 2': lambda S, B, r: (f"`diff = {S.diff} < 2`：汉明距离 {S.diff}，==满足题目条件==" if S.diff < 2 else f"`diff = {S.diff}`：不满足汉明距离 1 → 不行"),
        'f[-1] = f[pre_index] + 1': '`f[{index}] = f[{pre_index}] + 1 = {f[-1]}`：接在它后面更长',
        'pre[-1] = pre_index': '`pre[{index}] = {pre_index}`：记下前驱，方便还原',
        'p = 0': '`p` 用来找 `f` 最大的位置，先设 0',
        'for index in range(1, n)': lambda S, B, r: ('找完了，`p` 是最长子序列的结尾' if 'index' in B and B.index == S.index else f'比较 `f[{S.index}] = {S.f[S.index]}` 和 `f[p] = {S.f[S.p]}`'),
        'if f[index] > f[p]': lambda S, B, r: (f"`f[{S.index}] = {S.f[S.index]}` > `f[{S.p}] = {S.f[S.p]}` → 更新 `p`" if S.f[S.index] > S.f[S.p] else f"`f[{S.index}] = {S.f[S.index]}` 不超过 `f[{S.p}]` → 保持"),
        'p = index': '`p = {p}`',
        'res = []': '从最优结尾 `p = {p}` 出发，顺着 `pre` 往回收集单词',
        'while p is not None': lambda S, B, r: (f"`p = {S.p}`，继续往回走" if S.p is not None else '`p` 是 `None`：到头了'),
        'res.append(words[p])': '收集 `{words[p]!r}`',
        'p = pre[p]': '`p = pre[{B.p}] = {p}`',
        'res.reverse()': '是倒着收集的，翻转成正序：`{res}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='经典 LIS 式 DP：f 记长度，pre 记前驱',
        complexity='时间 `O(n²·l)`，空间 `O(n)`',
        problem=['选最长子序列：相邻 `groups` 不同，且单词等长、汉明距离恰为 1，输出单词列表',
                 '示例：`words=["bab","dab","cab"], groups=[1,2,2]` → `["bab","cab"]`',
                 '本视频：`["ab","aa","ba"], [1,2,1]` → `["ab","aa","ba"]`'],
        quote='可以尝试经典的动态规划状态表示，即f[index]表示选定位置index结尾的子序列时，可用的最长子序列是多长。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]` 先设为 1：前面的全不要，必然合法',
              '遍历左边每个 `pre_index`：组不同、等长、最多一个字母不同，就用 `f[pre_index] + 1` 更新，并记 `pre`',
              '先找 `f` 最大的结尾 `p`，顺着 `pre` 往回收集，最后翻转'],
        summary=['时间 `O(n²·l)`，空间 `O(n)`',
                 '加了 `f[-1] <= f[pre_index]` 的剪枝：接上去不会更长就不比较字母',
                 '数不同字母时，`diff` 到 2 就 `break`',
                 '易错：`pre` 是倒着收集的，返回前要 `reverse`',
                 '原文本身是合法的 Python 3 代码，未做修改；对比灵神方法二：灵神用通配符哈希把 `O(n²)` 降到 `O(n·l)`'],
    ),
)
