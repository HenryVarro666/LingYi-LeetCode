CONFIG = dict(
    num=3456, title='找出长度为 K 的特殊子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='双指针分离相同段',
    tags=['灵神题单', '难度分 1244'],
    code='''
class Solution(object):
    def hasSpecialSubstring(self, s, k):
        
        p = 0
        while p < len(s):
            q = p + 1
            while q < len(s) and s[p] == s[q]:
                q += 1
            
            if q - p == k:
                return True
            
            p = q
        
        return False
''',
    call="Solution().hasSpecialSubstring('aaabbcc', 2)",
    expect=True,
    views=[
        dict(type='string', var='s', pointers={'p': 'blue', 'q': 'pink'}, h=210,
             color=lambda S, i, v: ('green' if 'p' in S and 'q' in S and S['p'] <= i < S['q'] else None)),
        dict(type='text', h=90, fn=lambda S: f"当前段 s[p:q] 长度 q − p = =={S['q'] - S['p']}==，目标 k = =={S['k']}==" if 'q' in S and 'p' in S else ''),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), 'k'],
    captions={
        'p = 0': '`p` 是当前段的起点',
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p}` 还没到末尾 → 分离下一段' if S.p < len(S.s) else '`p` 到末尾了，所有段都看过'),
        'q = p + 1': '`q` 从 `p + 1` 出发，向后找这一段的终点：`q = {q}`',
        'while q < len(s) and s[p] == s[q]': lambda S, B, r: (f'`s[{S.q}] = {S.s[S.q]}` == `s[p] = {S.s[S.p]}` → 还是同一段，`q` 继续右移'
                                                              if S.q < len(S.s) and S.s[S.p] == S.s[S.q]
                                                              else ('`q` 到末尾了 → 这一段结束' if S.q >= len(S.s) else f'`s[{S.q}] = {S.s[S.q]}` ≠ `s[p] = {S.s[S.p]}` → 这一段结束')),
        'q += 1': '`q` → {q}',
        'if q - p == k': lambda S, B, r: (f'`s[p:q]` 全是 `{S.s[S.p]}`，长度 `{S.q} − {S.p} = {S.q - S.p}` {"==" if S.q - S.p == S.k else "≠"} `k = {S.k}`'
                                          + ('：==恰好是 k，两侧字符也不同，满足条件==' if S.q - S.p == S.k else '：长度不对，换下一段')),
        'return True': '找到了 → 返回 `True`',
        'p = q': '直接跳到下一段的起点：`p` → {p}',
        'return False': '没有长度恰好为 k 的段 → `False`',
    },
    cards=dict(
        one_liner='p、q 两个指针，把相同字符的段一段段剥出来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找长度恰好为 `k`、只含一种字符的子串，且左右相邻字符都与它不同',
                 '示例：`aaabaaa, k=3` → `true`',
                 '本视频：`aaabbcc, k=2` → `true`'],
        quote='若某个子串长度恰好为k，那么答案为true，否则为false。具体的分离方法为初始化起点p为0，然后让q从p + 1开始不断向后移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['`q` 一直走到字符变化或字符串末尾，`s[p:q]` 就是一整段相同字符',
              '这样的段两侧自然是不同字符（或边界），只要比较 `q - p` 和 `k`',
              '检查完后 `p = q`，每个字符只被扫一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '内层 `while` 先判 `q < len(s)` 再访问 `s[q]`，避免越界',
                 '原文为 Python 2 风格，本题代码无需改动，直接可在 Python 3 运行',
                 '对比灵神：灵神用一个 `cnt` 边走边数；yiduobo 用 p、q 显式划出区间'],
    ),
)
