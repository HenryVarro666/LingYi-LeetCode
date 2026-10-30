S0 = 'abab'
N = len(S0)


def _sa(S):
    v = S.get('self.sa')
    if v is None:
        return None
    return list(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sa = _sa(S)
    rank = S.get('self.rank')
    ln = S.get('_line')
    cv.text((x0 + 18, y0 + 4), '后缀数组 sa（按字典序排好的后缀）与 rank', 22, T['muted'], bold=True)
    if sa is None:
        return
    sorted_ok = ln is not None and ln >= 12 and 'self.rank' in S
    rowh = min(52, (y1 - y0 - 80) / max(N, 1))
    X0 = x0 + 40
    cv.text((X0, y0 + 40), 'sa 下标', 20, T['dim'])
    cv.text((X0 + 110, y0 + 40), '后缀起点', 20, T['dim'])
    cv.text((X0 + 240, y0 + 40), '后缀', 20, T['dim'])
    cv.text((X0 + 560, y0 + 40), 'rank', 20, T['dim'])
    cur_i, last = S.get('index'), S.get('last_pos')
    in_final = ln is not None and ln >= 26 and ln <= 37
    for r, p in enumerate(sa):
        y = y0 + 70 + r * rowh
        hi = None
        if in_final and cur_i is not None and p == cur_i:
            hi = T['blue']
        if in_final and last is not None and p == last:
            hi = T['pink']
        if hi:
            cv.rect((X0 - 14, y - 4, x1 - 40, y + rowh - 8), fill=hi, alpha=60, r=8)
        cv.text((X0 + 20, y + rowh / 2 - 6), r, 26, T['dim'], anchor='lm', mono=True)
        cv.text((X0 + 140, y + rowh / 2 - 6), p, 28, T['text'], anchor='lm', mono=True, bold=True)
        suf = S0[p:]
        cv.text((X0 + 240, y + rowh / 2 - 6), suf, 30, T['green'] if in_final and hi else T['text'], anchor='lm', mono=True, bold=True)
        if rank is not None:
            cv.text((X0 + 580, y + rowh / 2 - 6), rank[p], 28, T['cyan'], anchor='lm', mono=True, bold=True)
    if in_final and cur_i is not None and last is not None:
        cv.text((x0 + 18, y1 - 30), f"蓝 = index {cur_i}，粉 = 排名前一位的后缀 last_pos {last}，公共前缀长度 l = {S.get('l')}", 22, T['text'])
    elif not sorted_ok:
        cv.text((x0 + 18, y1 - 30), '（还没排好：sa 现在只是按首字母或按前 k 个字符排的中间结果）', 20, T['dim'])


def _pi(S):
    return S.get('index') if 26 <= S.get('_line', 0) <= 37 else None


def _pl(S):
    return S.get('last_pos') if 26 <= S.get('_line', 0) <= 37 else None


def _top(S):
    k = S.get('k')
    if k is not None and S.get('_line', 0) < 23:
        return f"倍增：每轮把后缀按前 `{2 * k}` 个字符排序（这一轮 `k = {k}`）"
    return ''


def _cmp(S):
    if S.get('_line', 0) >= 26 and S.get('index') is not None and S.get('last_pos') is not None:
        return S['index'], S['last_pos']
    return None



CONFIG = dict(
    num=1044, title='最长重复子串', difficulty='Hard', category='字符串',
    author='yiduobo', technique='后缀数组（倍增 + 桶排序）+ 相邻后缀的 LCP',
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
    call='Solution().longestDupSubstring("abab")',
    expect='ab',
    skip=[45, 51, 60, 14, 46, 47, 48, 49, 52, 53, 54, 61, 62, 63, 64, 65, 66, 67, 5, 10, 11, 7, 8, 23, 24, 25, 28, 36, 37],
    max_steps=100,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var=lambda S: S0, label='s', cell=84, h=210,
             pointers={_pi: 'blue', _pl: 'pink'}, pointer_labels={_pi: 'index', _pl: 'last_pos'}),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('k', 'k'), ('l', 'l', 'blue'), ('res', 'res', 'green'), ('p', 'p')],
    captions={
        4: '`self.n = {self.n}`，`s = "abab"`',
        9: '先按首字母给所有后缀桶排序：`sa` 里相同首字母的后缀挨在一起',
        12: '（getRank）按 sa 顺序给每个后缀一个 ==rank==：相同首字母 rank 相同（`a` → 0，`b` → 1）',
        15: lambda S, B, r: (f'`k = {S.k} < n = {S.n}`：已经按前 {S.k} 个字符排好，继续把长度翻倍'
                             if S.k < S.n else f'`k = {S.k} ≥ n`：前 {S.k} 个字符已覆盖整个后缀，排序结束 → `sa` 就是所有后缀的字典序'),
        16: '第二关键字 `b[i]` = 后缀 `i+k` 的 rank（越界记 ==-1==，因为较短的串更小）',
        17: '先按第二关键字 `b` 桶排序（再排第一关键字才能保证稳定）',
        18: '第一关键字 `a` = 上一轮的 rank',
        19: '再按第一关键字 `a` 桶排序（桶排序是稳定的，所以第二关键字的顺序保留下来）',
        20: '（getRank）重新给 rank：`(a, b)` 二元组不同，rank 才增加',
        21: '`k` 翻倍 → {k}',
        45: '开桶 `cnt`：统计每个 key 出现几次 → 前缀和后就是它在排序结果里的起止位置',
        51: '按 `s` 里的 key 把后缀稳定地放进 `order`（`for` 倒序保证稳定）',
        57: '桶排序（统计每个 key 的个数 → 前缀和 → 倒序稳定放入）完成：`sa = {self.sa}`',
        60: '`getRank`：从小到大扫 `sa`，key 变了 rank 就 +1，key 相同 rank 不变',
        26: lambda S, B, r: ('后缀都枚举完了' if B.get('index') == S.index else f'枚举后缀起点 `index = {S.index}`'),
        27: lambda S, B, r: ('`rank[index] == 0`：它是字典序最小的后缀，前面没有相邻后缀 → 跳过' if S.self.rank[S.index] == 0
                             else f'`rank[{S.index}] = {S.self.rank[S.index]}`：前面有相邻后缀，可以比较'),
        29: '`last_pos` = 排名紧挨在前面的那个后缀的起点 = `sa[rank[index] - 1]` = {last_pos}',
        30: lambda S, B, r: (f"比较 `s[{S.index + S.l}] = {S0[S.index + S.l]}` 和 `s[{S.last_pos + S.l}] = {S0[S.last_pos + S.l]}`"
                             f" → {'相等，公共前缀可以再长一位' if S0[S.index + S.l] == S0[S.last_pos + S.l] else '不等，公共前缀到此为止'}"
                             if S.index + S.l < S.self.n and S.last_pos + S.l < S.self.n
                             else '有一个后缀到头了，公共前缀到此为止'),
        31: '`l` → {l}：两个后缀又多匹配了一个字符',
        32: lambda S, B, r: (f'`l = {S.l} > res = {S.res}` → ==发现更长的重复子串==' if S.l > S.res else f'`l = {S.l} ≤ res = {S.res}`，不更新'),
        33: '`res = {res}`',
        34: '记下起点 `p = {p}`：`s[p:p+res]` 就是当前最长重复子串',
        39: lambda S, B, r: ('`res == 0`：没有重复子串，返回空串' if S.res == 0 else '`res > 0`，有重复子串'),
        42: '最长重复子串 = `s[{p}:{p}+{res}]` = `{ret}`',
    },
    cards=dict(
        one_liner='重复子串 = 两个后缀的公共前缀：排序后只比相邻后缀',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['找 `s` 里==出现两次及以上==的最长子串（可重叠），没有则返回 `""`',
                 '示例：`"banana"` → `"ana"`；`"abcd"` → `""`',
                 '本视频：`"abab"` → `"ab"`'],
        quote='所有子串都是某个后缀的前缀，最终答案ana是anana以及ana这两个后缀的最长公共前缀。最长公共前缀必然是出现在按字典序排序之后的两个相邻后缀之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['子串 = 后缀的前缀 → 重复子串 = ==两个后缀的公共前缀==，最长的一定出现在字典序相邻的后缀之间',
              '排序：前缀长度按 1、2、4、8…倍增，每轮用 (上一轮 rank, 后半段 rank) 二元组做两趟桶排序',
              '求 LCP：若后缀 `k` 与相邻后缀的 LCP 是 `l`，则后缀 `k+1` 的 LCP ≥ `l-1`，所以 `l` 只增不回头，总共 `O(n)`'],
        result='排好序的后缀 `ab, abab, b, bab`，相邻的 `abab` 和 `ab` 公共前缀 `ab` → 返回 `"ab"` ✓',
        summary=['时间 `O(n log n)`（倍增 log n 轮，每轮桶排序 O(n)），空间 `O(n)`',
                 '易错：先排第二关键字再排第一关键字；越界的第二关键字记 -1（比所有 rank 都小）',
                 '求 LCP 时每个 index 后 `l -= 1`，复用上一次的结果',
                 '原文是 Python 2 风格，`range(self.n)` 在 Python 3 下同样可以当 `sa` 初值，无需改动',
                 '视频里排序内部的桶循环被折叠，只展示每轮排序前后 sa/rank 的变化'],
    ),
)
