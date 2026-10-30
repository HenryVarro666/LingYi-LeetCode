CONFIG = dict(
    num=3540, title='访问所有房屋的最短时间', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 环形两种走法',
    code='''
class Solution(object):
    def minTotalTime(self, forward, backward, queries):
        
        n = len(forward)

        ps_f = [0]
        for v in forward[:n - 1]:
            ps_f.append(ps_f[-1] + v)
        
        ss_b = [0]
        for v in backward[n - 1: 0: -1]:
            ss_b.append(ss_b[-1] + v)
        ss_b.reverse()

        res = 0
        now = 0
        for nxt in queries:
            if now < nxt:
                res += min(ps_f[nxt] - ps_f[now], ss_b[0] - ss_b[now] + backward[0] + ss_b[nxt])
            else:
                res += min(ss_b[nxt] - ss_b[now], ps_f[-1] - ps_f[now] + forward[-1] + ps_f[nxt])
            
            now = nxt
        
        return res
''',
    call='Solution().minTotalTime([1,4,4], [4,1,2], [1,2,0,2])',
    expect=12,
    views=[
        dict(type='array', var='forward', h=150, label='forward[i]：i → i+1（最后一个回到 0）'),
        dict(type='array', var='backward', h=150, label='backward[i]：i → i-1（0 回到 n-1）'),
        dict(type='array', var=lambda S: S['ps_f'] if 'ps_f' in S else [], h=150, label='ps_f：forward 的前缀和（ps_f[i] = 0 → i 的正向代价）',
             color=lambda S, i, v: 'blue' if 'now' in S and i in (S['now'],) else ('pink' if 'nxt' in S and i == S['nxt'] and 'now' in S else None)),
        dict(type='array', var=lambda S: S['ss_b'] if 'ss_b' in S else [], h=150, label='ss_b：backward 的后缀和（ss_b[i] = n-1 → i 的反向代价）',
             color=lambda S, i, v: 'blue' if 'now' in S and i in (S['now'],) else ('pink' if 'nxt' in S and i == S['nxt'] and 'now' in S else None)),
        dict(type='text', h=70, fn=lambda S: f"queries = `{S['queries']}`" + (f"　　当前：房屋 ==={S['now']}== → ==={S['nxt']}==".replace('===','==') if 'nxt' in S and 'now' in S else '')),
    ],
    watch=[('now', 'now', 'blue'), ('nxt', 'nxt', 'pink'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}` 栋房子围成环',
        'ps_f = [0]': '`ps_f[i]`：从房屋 0 一路正向走到房屋 i 的代价，先放 `0`',
        'ps_f.append': '`ps_f` 追加 `{ps_f[-2]} + {v} = {ps_f[-1]}`',
        'ss_b = [0]': '`ss_b[i]`：从房屋 n-1 一路反向走到房屋 i 的代价，先放 `0`（对应 n-1）',
        'ss_b.append': '`ss_b` 追加 `{ss_b[-2]} + {v} = {ss_b[-1]}`（此时是倒着存的）',
        'ss_b.reverse': '翻转后下标与房屋对齐：`ss_b = {ss_b}`',
        'res = 0': '`res` 累计总时间',
        'now = 0': '从房屋 0 出发，`now` 是当前位置',
        'for nxt in queries': lambda S, B, r: ('所有询问都处理完了' if S.now == S.nxt else f'下一个要去的房屋：`nxt = {S.nxt}`，一次询问 = 求 `now → nxt` 的最短距离'),
        'if now < nxt': lambda S, B, r: f"`now = {S.now}` {'<' if S.now < S.nxt else '≥'} `nxt = {S.nxt}`：" + ('目标在前方，可以直接正向走，或反向绕一圈' if S.now < S.nxt else '目标在后方，可以直接反向走，或正向绕一圈'),
        'res += min(ps_f': lambda S, B, r: (f"正向直达 `ps_f[{S.nxt}] - ps_f[{S.now}] = {S.ps_f[S.nxt] - S.ps_f[S.now]}`；"
                                            f"反向绕圈 `{S.ss_b[0] - S.ss_b[S.now]} + {S.backward[0]} + {S.ss_b[S.nxt]} = {S.ss_b[0] - S.ss_b[S.now] + S.backward[0] + S.ss_b[S.nxt]}`（走到 0、再 0 → n-1、再到 nxt）"
                                            f" → 取小，`res` = =={S.res}=="),
        'res += min(ss_b': lambda S, B, r: (f"反向直达 `ss_b[{S.nxt}] - ss_b[{S.now}] = {S.ss_b[S.nxt] - S.ss_b[S.now]}`；"
                                            f"正向绕圈 `{S.ps_f[-1] - S.ps_f[S.now]} + {S.forward[-1]} + {S.ps_f[S.nxt]} = {S.ps_f[-1] - S.ps_f[S.now] + S.forward[-1] + S.ps_f[S.nxt]}`（走到 n-1、再 n-1 → 0、再到 nxt）"
                                            f" → 取小，`res` = =={S.res}=="),
        'now = nxt': '到达房屋 `{nxt}`，下一段从这里出发',
        'return res': '访问完所有房屋，总时间 `{res}`',
    },
    cards=dict(
        one_liner='每一段询问只有两种走法：直达，或者绕环一圈',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['`n` 栋房子围成环，`forward[i]` 是 i → i+1 的单行线，`backward[i]` 是 i → i-1',
                 '从房屋 0 出发，按 `queries` 的顺序依次访问',
                 '示例：`forward=[1,4,4]`，`backward=[4,1,2]`，`queries=[1,2,0,2]` → `12`'],
        quote='由于必须按顺序进行访问，那么queries实际上可以拆分为若干组询问，每个询问都是计算两个房屋间的最短距离，累加起来即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now < nxt`：正向 `ps_f[nxt] - ps_f[now]`，或反向走到 0、套圈到 n-1、再走到 nxt',
              '`now > nxt`：反向 `ss_b[nxt] - ss_b[now]`，或正向走到 n-1、套圈到 0、再走到 nxt',
              '区间和用前缀 / 后缀和 `O(1)` 取，每段取两种走法的较小值'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '易错点：套圈要加上 `backward[0]` 或 `forward[-1]` 这条跨越 0 与 n-1 的边',
                 '`now == nxt` 时走 else 分支，两种走法里直达代价为 0',
                 '`ss_b` 先倒着累加再 `reverse()`，下标才与房屋对齐',
                 '代码原文即为 Python 3 可运行写法，未做修改'],
    ),
)
