CONFIG = dict(
    num=3662, title='按频率筛选字符', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表计数 + 二次遍历',
    tags=[],
    code='''
class Solution(object):
    def filterCharacters(self, s, k):
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        res = []
        for c in s:
            if cnt[c] < k:
                res.append(c)
        return ''.join(res)
''',
    call="Solution().filterCharacters('abcbadeab', 3)",
    expect='cde',
    views=[
        dict(type='string', var='s', label='s（黄 = 当前遍历的字符）', cell=84, h=150,
             color=lambda S, i, v: 'yellow' if S.get('c') == v else None),
        dict(type='map', var='cnt', label='cnt（字符出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=190, font=30),
        dict(type='array', var='res', label='res（出现次数 < k 的字符）', h=150),
    ],
    watch=['k', 'c', ('res', "''.join(res)", 'green')],
    captions={
        'cnt = {}': '先建一个哈希表 `cnt`，记录每个字符在整个 `s` 里出现几次',
        'cnt[c] = cnt.get': '`{c}` 出现次数加一：`cnt[{c!r}] = {cnt[c]}`',
        'res = []': '第一趟统计完了，第二趟再决定哪些字符留下，`res` 按原顺序收集',
        'if cnt[c] < k': lambda S, B, r: (f"`cnt[{S.c!r}] = {S.cnt[S.c]}` < k = {S.k} → ==出现太少，保留=="
                                           if S.cnt[S.c] < S.k else f"`cnt[{S.c!r}] = {S.cnt[S.c]}` ≥ k = {S.k} → 出现太多，跳过"),
        'res.append(c)': '`{c}` 加入答案，顺序和 `s` 中一致：`res` = {res}',
        'return': "拼起来返回：`{ret!r}`",
    },
    cards=dict(
        one_liner='先数一遍，再按原顺序留下出现次数小于 k 的字符',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 26 种字符）',
        problem=['给定小写字母字符串 `s` 和整数 `k`',
                 '构造新字符串：只保留在 `s` 中出现次数 ==少于 k 次== 的字符，顺序不变',
                 '没有合法字符就返回空串。本视频：`s = "abcbadeab"`，`k = 3` → `"cde"`'],
        quote='一趟遍历，使用哈希表记录每种字符出现的次数。接下来再一趟遍历，通过哈希表检测当前字符出现的次数是否小于k，若小于，则将当前字符加入到答案数组中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['出现次数是对整个字符串而言的，边走边判断不行',
              '第一趟：哈希表记下每个字符的总次数',
              '第二趟：按原顺序查表，次数 `< k` 就收进 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：是 ==小于 k== 才保留，等于 k 的要去掉',
                 '重复出现的字符每个位置都要单独判断并保留，不要去重',
                 '没有字符满足时 `\'\'.join([])` 自然返回空串'],
    ),
)
