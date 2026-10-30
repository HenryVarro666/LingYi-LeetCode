def _pal(S):
    """已知回文中心 mid / 右边界 right 之外，画出当前 index 的回文半径 f[index]"""
    return S['s']


def _txt(S):
    if 'index' not in S or 'f' not in S:
        return ''
    if 'g' in S:
        n = len(S['g']) - 1
        return f"`g[i]` = 前 i 个字母最多能拆出的回文串数：`g = {S['g']}`"
    t = S['s']
    return f"Manacher：`f[index]` = 以 `{t[S['index']]}` 为中心的回文半径，`f = {S['f']}`"


CONFIG = dict(
    num=2472, title='不重叠回文子字符串的最大数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='Manacher 预处理 + 划分型 DP',
    tags=['字符串', '难度分 2013'],
    code='''
class Solution(object):
    def maxPalindromes(self, s, k):

        n = len(s)

        if k == 1:
            return n

        s = '!' + '#'.join(list(s)) + '@'
        f = [0]
        mid = 0
        right = 0
        for index in range(1, len(s) - 1, 1):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            while s[index - f[index]] == s[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index
    
        g = [0]
        for index in range(1, n + 1):
            f_pos = index * 2 - 1
            if f_pos >= k - 1 and f[f_pos - (k - 1)] >= k:
                g.append(g[(f_pos - k - k + 2) // 2] + 1)
            elif f_pos >= k and f[f_pos - k] >= k + 1:
                g.append(g[(f_pos - k - k) // 2] + 1)
            else:
                g.append(g[-1])
        
        return g[-1]
''',
    call='Solution().maxPalindromes("aabb", 2)',
    expect=2,
    max_steps=90,
    skip=['f = [0]', 'mid = 0', 'right = 0', 'mid = index', 'n = len(s)'],
    views=[
        dict(type='string', var='s', pointers={'index': 'blue', 'mid': 'orange'}, label='s 插入 # 后：index = 当前中心，mid = 已知最右回文的中心', h=200),
        dict(type='array', var=lambda S: S['f'], label='f：每个位置的回文半径（Manacher）', pointers={'index': 'blue'}, h=200),
        dict(type='array', var=lambda S: S['g'] if 'g' in S else [], label='g[i]：前 i 个字母最多拆出几个回文串', h=190),
    ],
    watch=[('index', 'index', 'blue'), ('mid', 'mid', 'orange'), ('right', 'right', 'pink'), ('k', 'k', 'cyan')],
    captions={
        'if k == 1': '`k = 1` 时每个字母都是回文串，答案直接是 `n`',
        "s = '!'": '用 `#` 隔开每个字母，让奇偶回文都变成奇回文；两端加哨兵 `!`、`@` 防越界',
        'f = [0]': '`f[index]`：以 `s[index]` 为中心的最长回文的半径',
        'mid = 0': '`mid`：当前覆盖最靠右的回文的中心',
        'right = 0': '`right`：这个回文的右边界',
        'if index < right': lambda S, B, r: (f'`index = {S.index} < right = {S.right}`：落在已知回文里，可以借镜像位置的结果' if S.index < S.right else f'`index = {S.index} ≥ right = {S.right}`：在已知范围外，从头开始扩'),
        'f.append(min': '借镜像：半径至少是 `min(f[2*mid-index], right-index)` = =={f[index]}==',
        'f.append(1)': '没有可借的信息，半径从 `1` 开始',
        'while s[index - f[index]]': lambda S, B, r: (f"两边 `{S.s[S.index - S.f[S.index]]}` == `{S.s[S.index + S.f[S.index]]}` → 半径还能 +1" if S.s[S.index - S.f[S.index]] == S.s[S.index + S.f[S.index]] else f"两边 `{S.s[S.index - S.f[S.index]]}` ≠ `{S.s[S.index + S.f[S.index]]}` → 停止扩展，半径 `{S.f[S.index]}`"),
        'f[index] += 1': '半径扩大：`f[{index}] = {f[index]}`',
        'if right < index + f[index]': '这个回文的右边界 `{index + f[index]}` 是否超过 `right = {right}`',
        'mid = index': '`mid = {mid}`：新的最靠右回文的中心',
        'right = index + f[index]': '更新最靠右回文：`right = {right}`，`mid = {index}`',
        'g = [0]': '`g[i]` = 前 `i` 个字母最多能拆出的回文串数，`g[0] = 0`',
        'f_pos = ': '第 `{index}` 个字母在加了 `#` 的串里的位置：`f_pos = {f_pos}`',
        'if f_pos >= k - 1': lambda S, B, r: ('长 `k` 的回文刚好以第 `index` 个字母结尾 → 选它，从 `g` 往前 `k` 位转移' if (S.f_pos >= S.k - 1 and S.f[S.f_pos - (S.k - 1)] >= S.k) else '没有以它结尾、长 `k` 的回文'),
        'elif f_pos >= k': lambda S, B, r: ('长 `k+1` 的回文以它结尾 → 选它，从 `g` 往前 `k+1` 位转移' if (S.f_pos >= S.k and S.f[S.f_pos - S.k] >= S.k + 1) else '长 `k+1` 的也没有 → 不使用这个字母'),
        'g.append(g[(f_pos - k - k + 2)': '选长 `k` 的回文：`g[{index}] = g[{index-k}] + 1` = =={g[-1]}==',
        'g.append(g[(f_pos - k - k)': '选长 `k+1` 的回文：`g[{index}] = g[{index-k-1}] + 1` = =={g[-1]}==',
        'g.append(g[-1])': '不用最后一个字母：`g[{index}] = g[{index-1}]` = =={g[-1]}==',
        'return g[-1]': '答案：`g[n]` = =={ret}==',
    },
    cards=dict(
        one_liner='Manacher 一次算出回文半径，DP 只需检查长 k 和 k+1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选出若干不重叠的回文子串，每个长度至少为 `k`，求最多能选几个',
                 '示例：`s = "abaccdbbd"`，`k = 3` → `2`',
                 '本视频：`s = "aabb"`，`k = 2`（`aa` 和 `bb`）'],
        quote='划分出来的回文子串应该尽量的短，即对于一个长度为k + 2的回文子串而言，将其两侧的字符去掉之后依然能得到一个长度为k的回文子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['`g[i]` 表示前 i 个字符最多拆几个：不用 `s[i-1]`，或枚举回文串的左边界 `j`',
              '预处理：用马拉车算法 `O(n)` 求出每个中心的最长回文，判回文变成 `O(1)`',
              '回文越短越好 → 只考虑以 `s[i-1]` 结尾、长 `k` 或 `k+1` 的回文'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`k = 1` 要特判，直接返回 `n`',
                 '插入 `#` 后下标要换算：`f_pos = 2*index - 1`',
                 '原文为 Python 2 写法，转移里的整数除法 `/` 已改为 `//`'],
    ),
)
