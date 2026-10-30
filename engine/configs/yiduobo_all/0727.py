CONFIG = dict(
    num=727, title='最小窗口子序列', difficulty='Hard', category='字符串',
    author='yiduobo', technique='枚举起点 + 下一位置表',
    tags=['灵神题单', '字符串', '子序列自动机'],
    code='''
class Solution(object):
    def minWindow(self, s1, s2):

        n = len(s1)
        m = len(s2)

        next = [{}]
        for index in range(n - 1, 0, -1):
            next.append(next[-1].copy())
            next[-1][s1[index]] = index
        
        next.reverse()
        
        mi = None
        mi_start = None

        for index in range(n):
            if s1[index] != s2[0]:
                continue

            p = 1
            now = index
            while p < m:
                if s2[p] in next[now]:
                    now = next[now][s2[p]]
                    p += 1
                else:
                    break
            
            if p == m and (mi is None or mi > now - index + 1):
                mi = now - index + 1
                mi_start = index
        
        if mi is None:
            return ""
        
        return s1[mi_start : mi_start + mi]
''',
    call="Solution().minWindow('bcdbde', 'bde')",
    expect='bde',
    views=[
        dict(type='string', var='s1', label='s1（蓝 = 起点 index，粉 = 当前匹配到的位置 now）', pointers={'index': 'blue', 'now': 'pink'}, h=170),
        dict(type='string', var='s2', label='s2', pointers={'p': 'orange'}, h=170),
        dict(type='text', h=70, size=30,
             fn=lambda S: (f"目前最短窗口：==`{S['s1'][S['mi_start']:S['mi_start']+S['mi']]}`== 长度 {S['mi']}" if S.get('mi') else '还没找到窗口')),
        dict(type='map', var=lambda S: S['next'][S['now']] if 'now' in S and 'next' in S and S['now'] < len(S['next']) and isinstance(S['next'], list) and S['_line'] >= 0 and 'index' in S and S.get('p') else {},
             label='next[now]：now 右侧每个字母最早出现的下标', fmt=lambda k, v: f"'{k}': {v}", h=140, font=30),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'pink'), ('p', 'p', 'orange'), ('mi', 'mi', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'm = len': '`m = {m}`',
        'next = [{}]': '`next[i]` 记录 s1 在 i ==右侧==每种字母最早出现的位置',
        'next.append': '先继承右边一位的表',
        'next[-1][s1[index]] = index': '`{s1[index]}` 出现在 `{index}`，更靠左，覆盖旧位置',
        'next.reverse': '翻转：`next[i]` 对应下标 i',
        'mi = None': '`mi` 记最短窗口长度，`mi_start` 记它的起点',
        'if s1[index] != s2[0]': lambda S, B, r: (f"`s1[{S.index}] = '{S.s1[S.index]}'` ≠ `s2[0] = '{S.s2[0]}'` → 不能做起点，跳过"
                                                  if S.s1[S.index] != S.s2[0] else
                                                  f"`s1[{S.index}] = '{S.s1[S.index]}'` == `s2[0]` → ==这里可以当窗口起点=="),
        'p = 1': 's2[0] 已匹配，接着找 `s2[1]`',
        'now = index': '`now` 从起点开始往右跳',
        'while p < m': '`p = {p}`，{"还要继续匹配" if p < m else "s2 全部匹配完"}',
        'if s2[p] in next[now]': lambda S, B, r: (f"`'{S.s2[S.p]}'` 在 `now={S.now}` 右侧最早出现在 `{S.next[S.now][S.s2[S.p]]}` → 跳过去"
                                                  if S.s2[S.p] in S.next[S.now] else
                                                  f"`'{S.s2[S.p]}'` 在 `{S.now}` 右侧再没出现 → ==这个起点失败=="),
        'now = next[now][s2[p]]': '贪心：跳到最近的 `{s2[p]}`，`now = {now}`',
        'p += 1': '`s2` 又匹配了一个，`p = {p}`',
        'break': '匹配不下去，放弃这个起点',
        'if p == m and': lambda S, B, r: (f"`p == m`，窗口 `[{S.index}, {S.now}]` 长 `{S.now - S.index + 1}`，比当前最短 `{S.mi}` 更短？"
                                          if S.p == S.m and S.mi is not None else
                                          ('`p == m`，第一个窗口 → ==记下==' if S.p == S.m else '`p < m`，没有匹配完整，不更新')),
        'mi = now - index + 1': '更新最短窗口：长度 `{mi}`',
        'mi_start = index': '起点记为 `{mi_start}`',
        'if mi is None': '`mi` 是 None 就说明没有窗口',
        'return ""': '没有窗口，返回空串',
        'return s1[': '最短窗口 `s1[{mi_start}:{mi_start + mi}]` = =={s1[mi_start:mi_start + mi]}==',
    },
    cards=dict(
        one_liner='枚举起点，用“下一位置表”几步贪心跳完 s2',
        complexity='时间 `O(n·m + 26n)`，空间 `O(26n)`',
        problem=['在 `s1` 中找最短的连续子串，使 `s2` 是它的子序列',
                 '有多个最短时取最靠左的；没有则返回空串',
                 '本视频：`s1=bcdbde`，`s2=bde` → `bde`'],
        quote='如果将每个位置右侧各种字符的下一次出现位置提前预处理出来，那么在执行贪心算法时就不需要在s1中枚举，而是改成通过下一个位置进行m次跳跃就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定起点 `start`，贪心地在 s1 里一路匹配 s2，就是最短的窗口',
              '朴素匹配要 `O(n+m)`；预处理 next 表后只需 `m` 次跳跃',
              '起点必须等于 `s2[0]`，枚举所有这样的起点取最短'],
        summary=['`next[i]` 记录的是 i ==右侧（不含 i）==的最早位置，所以起点 `s1[index] == s2[0]` 要单独判断',
                 '比较用严格 `>`，长度相同保留靠左的起点',
                 '时间 `O(mn)`，每个起点最多跳 m 次',
                 '原文为 Python 2 风格，代码无需修改（变量名 next 遮蔽了内置函数，原样保留）'],
    ),
)
