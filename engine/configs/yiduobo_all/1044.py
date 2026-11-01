def _sufs(S):
    s = S.get('s')
    sa = S.get('self.sa')
    if not s or sa is None:
        return ''
    sa = list(sa)
    return '按 sa 排出的后缀：' + ' | '.join(s[p:] for p in sa)


def _ptr(S):
    return S.get('index') if S['_line'] >= 12 else None


CONFIG = dict(
    num=1044, title='最长重复子串', difficulty='Hard', category='字符串',
    author='yiduobo', technique='倍增 + 桶排序建后缀数组，再求相邻 LCP',
    tags=['灵神题单', '字符串', '难度分 2429'],
    code='''
class Solution(object):
    def longestDupSubstring(self, s):

        self.n = len(s)
        a = [ord(char) - 96 for char in s]

        self.sa = range(self.n)
        self.max_rank = 26
        self.sort(a)
        b = [0] * self.n
        self.rank = [0] * self.n
        self.getRank(a, b)

        k = 1
        while k < self.n:
            b = [self.rank[index + k] if index + k < self.n else -1 for index in range(self.n)]
            self.sort(b)
            a = self.rank[:]
            self.sort(a)
            self.getRank(a, b)
            k += k

        l = 0
        res = 0
        p = None
        for index in range(self.n):
            if self.rank[index] == 0:
                continue
            last_pos = self.sa[self.rank[index] - 1]
            while index + l < self.n and last_pos + l < self.n and s[index + l] == s[last_pos + l]:
                l += 1
            if l > res:
                res = l
                p = index
            
            if l > 0:
                l -= 1

        if res == 0:
            return ""
        
        return s[p:p + res]

    def sort(self, s):
        cnt = [0] * (self.max_rank + 2)
        for index in range(self.n):
            cnt[s[index] + 1] += 1
        for index in range(1, self.max_rank + 2):
            cnt[index] += cnt[index - 1]

        order = [0] * self.n
        for index in range(self.n - 1, -1, -1):
            cnt[s[self.sa[index]] + 1] -= 1
            order[cnt[s[self.sa[index]] + 1]] = self.sa[index]
            
        
        self.sa = order[:]

    def getRank(self, a, b):
        self.max_rank = 0
        for index in range(self.n):
            if index > 0:
                now = self.sa[index]
                last = self.sa[index - 1]
                if a[now] != a[last] or b[now] != b[last]:
                    self.max_rank += 1
            self.rank[self.sa[index]] = self.max_rank
''',
    call='Solution().longestDupSubstring("banana")',
    expect='ana',
    views=[
        dict(type='text', fn=_sufs, size=24),
        dict(type='string', var='s', label='s（粉 = 后缀 index 的比较位置，蓝 = 前一名后缀的比较位置）', cell=84,
             pointers={'index + l': 'pink', 'last_pos + l': 'blue'}, pointer_labels={'index + l': 'index+l', 'last_pos + l': 'last+l'}),
        dict(type='array', var='self.sa', label='sa[名次] = 后缀起点', cell=84, h=150),
        dict(type='array', var='self.rank', label='rank[起点] = 名次', cell=84, h=150),
    ],
    watch=[('k', 'k', 'cyan'), ('max_rank', 'self.max_rank', 'orange'), ('l', 'l', 'pink'), ('res', 'res', 'green'), 'p'],
    skip=['self.n = len(s)', 'a = [ord', 'b = [0] * self.n', 'self.rank = [0]', 'cnt = [0]', 'order = [0]',
          'for index in range(self.n):', 'for index in range(1, self.max_rank', 'cnt[index] +=', 'cnt[s[index] + 1] += 1',
          'cnt[s[self.sa[index]]', 'order[cnt', 'now = self.sa', 'last = self.sa', 'if a[now]', 'self.max_rank += 1',
          'for index in range(self.n - 1', 'self.max_rank = 0', 'if index > 0', 'self.rank[self.sa[index]]'],
    captions={
        'self.sa = range': '`sa` 先随便放：起点 0..n-1',
        'self.max_rank = 26': '字符只有 26 种，桶数就是 26',
        'self.sort(a)': '第一轮：先只看首字母，对所有后缀做桶排序（`a` = 字母序号 1..26）',
        'self.getRank(a, b)': '按排好的顺序编名次：和前一名的 `(a, b)` 完全相同就并列，不同才加一档',
        'self.sa = order[:]': lambda S, B, ret: '桶排序完成 → `sa = ' + str(list(S.self.sa)) + '`',
        'k = 1': '第一轮后：`rank = {self.rank}`（同字母并列）。`k` 是已排好的前缀长度',
        'while k < self.n': lambda S, B, ret: (f'`k = {S.k} < n`：再倍增一轮，比较长度 `{2 * S.k}` 的前缀' if S.k < len(S.s) else '`k >= n`：前缀已覆盖整个串，后缀数组排完了'),
        'b = [self.rank': '次关键字 `b`：后半段（`index + k` 开头）上一轮的名次，没有就是 -1 → `{b}`',
        'self.sort(b)': '先按次关键字 `b` 桶排序（基数排序：先排次要的）',
        'a = self.rank[:]': '主关键字 `a` = 前半段上一轮的名次 → `{a}`',
        'self.sort(a)': '再按主关键字 `a` 桶排序（稳定，次序不乱）',
        'k += k': '这一轮名次：`rank = {self.rank}`；`k` 翻倍 → `{k}`',
        'l = 0': '开始求相邻后缀的公共前缀，`l` 是当前 LCP',
        'res = 0': '`res` 记录最长重复子串长度',
        'for index in range(self.n):': '处理起点 `index = {index}` 的后缀',
        'if self.rank[index] == 0': lambda S, B, ret: ('名次 0 是最小的后缀，没有前一名' if S.self.rank[S.index] == 0 else '`rank[{}] ≠ 0`，有前一名'.format(S.index)),
        'continue': '跳过',
        'last_pos = ': '前一名后缀从 `last_pos = {last_pos}` 开始',
        'while index + l < self.n': lambda S, B, ret: (f'`s[{S.index + S.l}] = {S.s[S.index + S.l]}` == `s[{S.last_pos + S.l}]` → `l` 再加一' if S.index + S.l < len(S.s) and S.last_pos + S.l < len(S.s) and S.s[S.index + S.l] == S.s[S.last_pos + S.l]
                                                       else f'不再匹配，这两个后缀的 LCP = `{S.l}`'),
        'l += 1': '`l` → {l}',
        'if l > res': lambda S, B, ret: (f'`{S.l} > {S.res}` → 找到更长的重复子串' if S.l > S.res else f'`{S.l} ≤ {S.res}`，不更新'),
        'res = l': '`res = {res}`：最长重复子串长度更新',
        'p = index': '`p = {p}`：答案从 `s[{p}]` 开始',
        'p = None': '`p` 记录答案的起点',
        'if l > 0': '`index+1` 的后缀至少有 `l - 1` 的 LCP，所以 `l` 只减一，不用清零',
        'l -= 1': '`l` → {l}',
        'if res == 0': '`res = {res}`：有重复子串',
        'return s[p': lambda S, B, ret: f'答案 `s[{S.p}:{S.p + S.res}]` = `"{ret}"`',
    },
    max_steps=110,
    cards=dict(
        one_liner='倍增排好所有后缀，相邻后缀的最长公共前缀就是重复子串',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['找出 `s` 中出现 ==至少两次== 的最长子串，可以重叠',
                 '没有则返回 `""`',
                 '示例：`"banana"` → `"ana"`'],
        quote='最长公共前缀必然是出现在按字典序排序之后的两个相邻后缀之间',
        quote_src='—— yiduobo 题解原文',
        idea=['按前缀长度 1、2、4、8… 倍增排序，每轮用上一轮的名次当关键字，两趟桶排序搞定',
              '排好后，相邻后缀的 LCP 里最大的就是答案',
              '`s[k:]` 的 LCP 为 `l`，则 `s[k+1:]` 的 LCP 至少 `l-1`，所以求 LCP 总共 `O(n)`'],
        result='倍增排完后缀，最大相邻 LCP 为 3 → 返回 `"ana"` ✓',
        summary=['原文为 Python 2 写法，本题代码在 Python 3 下无需修改',
                 '排序用 `sa`（名次→起点）和 `rank`（起点→名次）互为反函数',
                 '次关键字缺失记 `-1`，保证较短的后缀更小',
                 '对比灵神：灵神直接用库函数得到 sa，yiduobo 手写倍增 + 桶排序'],
    ),
)
