CONFIG = dict(
    num=1593, title='拆分字符串使唯一子字符串的数目最大', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='回溯 · 枚举前缀 + 最优性剪枝',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def maxUniqueSplit(self, s):

        self.res = 0
        n = len(s)
        used = set()
        self.dfs(s, 0, 0, n, used)
        
        return self.res

    def dfs(self, s, pos, now, n, used):
        if s[pos:] not in used and now + 1 > self.res:
            self.res = now + 1
        if pos == n - 1:
            return

        if n - pos + now <= self.res:
            return
        
        for cut_pos in range(pos, n - 1):
            if s[pos : cut_pos + 1] not in used:
                used.add(s[pos : cut_pos + 1])
                self.dfs(s, cut_pos + 1, now + 1, n, used)
                used.remove(s[pos : cut_pos + 1])
''',
    call='Solution().maxUniqueSplit("abab")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前后缀起点 pos，绿 = 已切出的前缀）', cell=84, h=190,
             pointers={'pos': 'blue'},
             color=lambda S, i, v: 'green' if i < S['_inner'].get('pos', 0) else None),
        dict(type='set', var='used', label='used（已切出的子串）', h=130, fmt=lambda x: x),
        dict(type='calls', h=200, hide=('s', 'used', 'n')),
    ],
    watch=[('pos', lambda S: S['_inner'].get('pos'), 'blue'), ('now', lambda S: S['_inner'].get('now'), 'orange'),
           ('res', 'self.res', 'green')],
    skip=['self.res = 0', 'n = len(s)', 'used = set()'],
    captions={
        'self.dfs(s, 0, 0, n, used)': '从 `pos = 0` 开始，已切出 `0` 段',
        'if s[pos:] not in used': lambda S, B, ret: (
            f"剩余后缀 `{S['s'][S['_inner']['pos']:]}` ==没用过==，整体当作最后一段：共 `{S['_inner']['now']} + 1` 段，和 `res = {S['self'].res}` 比"
            if S['s'][S['_inner']['pos']:] not in S['used'] else
            f"剩余后缀 `{S['s'][S['_inner']['pos']:]}` ==已用过==，不能整体作为最后一段"),
        'if pos == n - 1': lambda S, B, ret: ('只剩最后 1 个字符，没法再切 → 返回' if S['_inner']['pos'] == S.n - 1
                                              else f"`pos = {S['_inner']['pos']}`，还能继续切"),
        'if n - pos + now <= self.res': lambda S, B, ret: (
            f"最优性剪枝：剩余字符全切成单字符也只有 `{S.n - S['_inner']['pos']} + {S['_inner']['now']}` = {S.n - S['_inner']['pos'] + S['_inner']['now']} 段，`<= res = {S['self'].res}` → ==剪枝=="
            if S.n - S['_inner']['pos'] + S['_inner']['now'] <= S['self'].res else
            f"上界 `{S.n - S['_inner']['pos'] + S['_inner']['now']}` > `res = {S['self'].res}`，还有希望，继续"),
        'for cut_pos in range': '枚举前缀 `s[pos:cut_pos+1]`，`cut_pos` 最大到 `n-2`（留下至少 1 个字符）',
        'if s[pos : cut_pos + 1] not in used': lambda S, B, ret: (
            f"前缀 `{S['s'][S['_inner']['pos']:S['_inner']['cut_pos']+1]}` ==没用过== → 可以切"
            if S['s'][S['_inner']['pos']:S['_inner']['cut_pos']+1] not in S['used'] else
            f"前缀 `{S['s'][S['_inner']['pos']:S['_inner']['cut_pos']+1]}` 已用过，跳过"),
        'used.add': '切下 `{s[pos:cut_pos+1]}`，加入 `used`',
        'self.dfs(s, cut_pos + 1': '递归处理剩下的后缀，已切段数 +1',
        'used.remove': '恢复现场：`{s[pos:cut_pos+1]}` 移出 `used`',
        'return self.res': '最多能拆成 `{ret}` 个互不相同的子串',
    },
    max_steps=130,
    cards=dict(
        one_liner='暴力回溯：枚举每个前缀，没用过就切，再递归后缀',
        complexity='时间 `O(2^n)`，空间 `O(n)`（`n <= 16` 才行）',
        problem=['把字符串 `s` 拆成若干==互不相同==的非空子串（拼起来等于 s），求最多能拆成几个',
                 '示例：`"ababccc"` → `5`，拆成 `["a","b","ab","c","cc"]`；本视频：`"abab"` → `3`',
                 '`n` 最大只有 16'],
        quote='若其没有被使用过，那么不划分也是一种选择，此时可以用已划分出来的字符串个数，再加上1来更新答案。除此之外，还可以枚举当前字符串中的所有前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos` 是当前后缀的起点，`now` 是已切出的段数，`used` 记录已切出的子串',
              '后缀整体没用过：当作最后一段，更新 `res = now + 1`',
              '否则枚举前缀，没用过就切、递归、再恢复现场'],
        result='最多拆成 3 个：a, b, ab',
        summary=['时间 `O(2^n)`，空间 `O(n)`',
                 '剪枝：`n - pos + now <= res` 说明就算全切成单字符也超不过现有答案',
                 '循环到 `n - 2`，最后一段由 `s[pos:]` 整体处理，别漏掉这一步',
                 '作者说也可用状压 DP，但状态也是 `2^n` 级别，回溯加剪枝反而更快',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
