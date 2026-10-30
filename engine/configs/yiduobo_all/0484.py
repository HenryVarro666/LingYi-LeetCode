CONFIG = dict(
    num=484, title='寻找排列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='连续 D 逆序填充',
    tags=['贪心', '数组'],
    code='''
class Solution(object):
    def findPermutation(self, s):

        res = []
        now = 1
        p = 0
        n = len(s)
        while p < n:
            cnt = 0
            while p < n and s[p] == 'D':
                cnt += 1
                p += 1
            
            res.extend(range(now + cnt, now - 1, -1))
            now += cnt + 1
            p += 1

            while p < n and s[p] == 'I':
                res.append(now)
                now += 1
                p += 1
        
        if s[-1] == 'I':
            res.append(now)
        return res
''',
    call="Solution().findPermutation('DDIID')",
    expect=[3, 2, 1, 4, 6, 5],
    views=[
        dict(type='text', fn=lambda S: (f"下一个要填的最小数 `now = {S['now']}`；已填 {len(S['res'])} 个，共需 {len(S['s']) + 1} 个" if 'now' in S else '')),
        dict(type='string', var='s', pointers={'p': 'blue'}, h=200, label='s（I 升 / D 降）',
             color=lambda S, i, v: ('orange' if v == 'D' else 'green') if 'p' in S and i < S['p'] else None),
        dict(type='array', var='res', h=200, label='res（答案）'),
    ],
    watch=[('p', 'p', 'blue'), ('now', 'now', 'yellow'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 用来收集答案',
        'now = 1': '字典序最小：优先用最小的未用数，`now = 1`',
        'p = 0': '`p` 是扫描 `s` 的下标',
        'while p < n:': lambda S, B, r: (f'`p = {S.p} < {S.n}`：还有字符没处理，继续' if S.p < S.n else f'`p = {S.p} >= {S.n}`：`s` 扫完，退出主循环'),
        'cnt = 0': '数连续的 `D`：`cnt = 0`',
        "s[p] == 'D'": lambda S, B, r: (f"`s[{S.p}] = '{S.s[S.p]}'`" + (' 是 D → 继续数' if S.s[S.p] == 'D' else ' 不是 D → 停')) if S.p < S.n else '`p` 越界，停',
        'cnt += 1': '又一个 D：`cnt = {cnt}`',
        'p += 1': lambda S, B, r: (f'跳过 D 段后紧跟的那个 I（它的值已被 D 段带出）：`p = {S.p}`' if S['_line'] == 16 else f'`p = {S.p}`'),
        'res.extend': '连续 `{cnt}` 个 D 要预留空间：从 `now + cnt = {B.now + B.cnt}` ==逆序==填到 `now = {B.now}` → `res = {res}`',
        'now += cnt + 1': '这一段用掉了 `cnt + 1 = {cnt + 1}` 个数，下一个最小未用数 `now = {now}`',
        "s[p] == 'I'": lambda S, B, r: (f"`s[{S.p}] = '{S.s[S.p]}'`" + (' 是 I → 按顺序填 now' if S.s[S.p] == 'I' else ' 不是 I → 回到 D 的处理')) if S.p < S.n else '`p` 越界，停',
        'res.append(now)': '`I` 就按顺序填：放入 `now = {B.now}`，`res = {res}`',
        'now += 1': '`now` → {now}',
        "if s[-1] == 'I'": lambda S, B, r: ('`s` 以 I 结尾：最后一个 I 前面没有 D 接着，==要补上== `now`' if S.s[-1] == 'I' else '`s` 以 D 结尾：最后的数已由 D 段填完，不用补'),
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='要字典序最小：用小数填，但连续的 D 要先预留空间逆序填',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['`s` 由 `I`（升）和 `D`（降）组成，`s[i]` 表示 `perm[i]` 与 `perm[i+1]` 的大小关系',
                 '求 `1..n+1` 的排列，满足 `s` 且字典序最小',
                 '示例：`"DI"` → `[2,1,3]`；本视频：`"DDIID"` → `[3,2,1,4,6,5]`'],
        quote='若接下来连续出现了cnt个D，那么就需要从now + cnt开始逆序填充到now。而对于I，则只需要按照正常顺序填充就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['要字典序小，就想用最小的 `now` 开头；但开头有 D 就得先预留，如 `"DI"` 只能 2 开头',
              '轮流找连续的 D 和 I：D 段 `now+cnt → now` 逆序填，I 段依次填 `now, now+1, ...`',
              '跳过 D 段后的第一个 I：它的值由后面的 D 段带出；`s` 以 I 结尾时末尾要补一个 `now`'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计答案）',
                 '易错：`s` 以 `I` 结尾，最后要 `res.append(now)`',
                 '易错：D 段之后 `p += 1` 是跳过紧跟的那个 I，不是多余的',
                 '原文为 Python 2 风格，该代码在 Python 3 下无需修改'],
    ),
)
