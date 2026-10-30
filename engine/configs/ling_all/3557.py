def _seen_txt(S):
    if 'seen' not in S:
        return ''
    letters = [chr(97 + b) for b in range(26) if S['seen'] >> b & 1]
    s = '、'.join(letters) if letters else '空'
    return f"`seen` 里的字母（下标 ≤ i−3）：=={s}=="


CONFIG = dict(
    num=3557, title='不相交子字符串的最大数量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='划分型贪心 · 位运算记录字母',
    tags=['贪心算法', '划分型贪心', '难度分 1720'],
    code='''
class Solution:
    def maxSubstrings(self, word: str) -> int:
        ans = seen = 0
        i = 3
        while i < len(word):
            seen |= 1 << (ord(word[i - 3]) - ord('a'))
            if seen >> (ord(word[i]) - ord('a')) & 1:  # 再次遇到 word[i]
                ans += 1
                seen = 0
                i += 3
            i += 1
        return ans
''',
    call="Solution().maxSubstrings('abcdeafdef')",
    expect=2,
    views=[
        dict(type='string', var='word', pointers={'i': 'blue', 'i - 3': 'pink'}, h=260,
             color=lambda S, k, v: ('green' if 'i' in S and k == S['i'] and S.get('seen', 0) >> (ord(v) - 97) & 1 else None)),
        dict(type='text', fn=_seen_txt, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('seen', 'seen', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = seen = 0': '`ans` 记答案，`seen` 是 26 位二进制数：第 c 位为 1 表示字母 c 出现过',
        'i = 3': '子串长度至少 4，右端点最早是下标 `3`，所以 `i` 从 3 开始',
        'seen |= ': '把 `word[{i-3}] = {word[i-3]!r}` 加入 `seen`：只有下标 ≤ `i-3` 的字母才能和 `word[i]` 组成长度 ≥ 4 的子串',
        'if seen >>': lambda S, B, r: (f"`word[{S.i}] = {S.word[S.i]!r}` 在 `seen` 里 → ==找到右端点最小的子串=="
                                        if S.seen >> (ord(S.word[S.i]) - 97) & 1
                                        else f"`word[{S.i}] = {S.word[S.i]!r}` 不在 `seen` 里，继续右移"),
        'ans += 1': '右端点越小，后面能选的越多 → 立刻选它，`ans` = =={ans}==',
        'seen = 0': '这个子串用掉了前面的字母，`seen` 清空，从后面重新开始',
        'i += 3': '新子串必须从 `i+1` 起，至少再走 3 步才有右端点 → `i` 先加 3（再加 1）',
        'i += 1': '`i` 右移到 {i}',
    },
    cards=dict(
        one_liner='最左的子串，右端点越小越好：一遇到就切',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找首尾字母相同、长度 ≥ 4 的==不相交==子串，求最多几个',
                 '示例：`abcdeafdef` → `abcdea` 和 `fdef`，答案 `2`',
                 '子串不必铺满整个字符串'],
        quote='想一想，第一个（最左边的）子串选哪个最好？贪心地想，这个子串的右端点越小越好，这样后面能选的子串就越多。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选完右端点为 `i` 的子串，剩下 `[i+1, n-1]` 是同样的子问题',
              '长度 ≥ 4 等价于：下标 ≤ `i-3` 的字母里出现过 `word[i]`',
              '布尔数组压缩成一个二进制数 `seen`，位运算判断'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`i` 从 3 开始；切出子串后 `i += 3` 再 `+= 1`，跳过新子串至少需要的 3 个位置',
                 '优化前写法：用 `pos` 字典记首次位置，`i - pos[ch] > 2` 就答案加一并清空字典',
                 '同类题见灵神贪心题单 §1.5 划分型贪心'],
    ),
)
