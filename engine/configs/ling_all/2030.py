def _top(S):
    if 'q' not in S:
        return '用单调队列求长为 k 的字典序最小子序列，同时保证 letter 够 repetition 个'
    need = S['repetition'] - S['inQ']
    return f"还需 `{S['repetition']}` 个 `{S['letter']}`；队列里有 `{S['inQ']}` 个，后面还剩 `{S['unread']}` 个"


def _scolor(S, i, v):
    if 'i' in S and i == S['i']:
        return 'blue'
    if S.get('letter') == v:
        return 'orange'
    return None


CONFIG = dict(
    num=2030, title='含特定字母的最小子序列', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调队列 · 弹队尾前先看 letter 够不够（Go 原文转写）',
    tags=['灵神题单', '单调栈', '难度分 2562'],
    code='''
class Solution:
    def smallestSubsequence(self, s: str, k: int, letter: str, repetition: int) -> str:
        ans = []
        unread = s.count(letter)  # 未遍历到的 letter 个数
        inQ = 0  # 在单调队列中的 letter 个数
        q = []
        n = len(s)
        i = 0
        while len(ans) < k:
            # 将 s[i] 插入单调队列
            while i < n and len(q) > 0 and s[i] < q[-1]:
                if q[-1] == letter:  # 特判队尾是 letter 的情况
                    if inQ + unread <= repetition:  # 弹出队尾会导致无法凑足 repetition 个 letter，及时退出
                        break
                    inQ -= 1
                q.pop()
            if i < n:
                if s[i] == letter:
                    unread -= 1
                    inQ += 1
                q.append(s[i])

            if i >= n - k:
                # 从队首拿到字典序最小的字符
                if q[0] == letter:
                    inQ -= 1
                    repetition -= 1
                    ans.append(q[0])
                elif len(ans) + repetition < k:  # 还有足够空间可以放 letter
                    ans.append(q[0])
                q = q[1:]
            i += 1
        return ''.join(ans)
''',
    call='Solution().smallestSubsequence("leetcode", 4, "e", 2)',
    expect='ecde', max_steps=110,
    skip=['ans = []', 'q = []', 'n = len(s)', 'i = 0', 'i += 1', 'inQ = 0', 'inQ += 1', 'inQ -= 1', 'if i < n:', 'unread -= 1', 'while len(ans) < k'],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', pointers={'i': 'blue'}, label='s（蓝 = 当前读到的位置，橙 = letter）', h=210, cell=70, color=_scolor,
             ),
        dict(type='queue', var='q', label='单调队列 q（队首最小）', h=170),
        dict(type='array', var='ans', label='ans（已确定的答案）', h=170, cell=70, index=False),
    ],
    watch=[('i', 'i', 'blue'), ('unread', 'unread', 'cyan'), ('inQ', 'inQ', 'orange'), ('repetition', 'repetition', 'pink')],
    captions={
        'unread = s.count': '`unread = {unread}`：整个 `s` 里一共 {unread} 个 `{letter}`，还都没读到',
        'inQ = 0': '`inQ`：队列里已有的 `{letter}` 个数',
        'while len(ans) < k': '`len(ans) = {len(ans)} < k = {k}` → {"答案还没凑满，继续读" if len(ans) < k else "凑满了，结束"}',
        'while i < n and len(q) > 0': lambda S, B, r: ((f"`s[{S.i}] = '{S.s[S.i]}'` < 队尾 `'{S.q[-1]}'` → 队尾比它大，可以考虑弹掉" if S.q and S.s[S.i] < S.q[-1] else (f"`s[{S.i}] = '{S.s[S.i]}'` 不小于队尾 `'{S.q[-1]}'`，不弹，直接入队" if S.q else '队列为空，直接入队')) if S.i < len(S.s) else '`s` 已经读完，只从队首取'),
        'if q[-1] == letter': '队尾是 letter：弹掉它要小心，先看后面够不够',
        'if inQ + unread <= repetition': '`inQ + unread = {inQ} + {unread}` {"<=" if inQ + unread <= repetition else ">"} `repetition = {repetition}` → {"弹掉就凑不够 letter 了，==及时退出==" if inQ + unread <= repetition else "后面还够，可以弹"}',
        'q.pop()': '弹出队尾 `{B.q[-1]}`，字典序更小的字符顶上来：`q = {q}`',
        'if i < n:': '`i = {i}`，`n = {n}` → {"还有字符可读" if i < n else "已读完"}',
        'if s[i] == letter': '`{s[i]}` {"就是" if s[i] == letter else "不是"} `{letter}` → {"这个 letter 从「没读」变成「在队里」：`unread` 减 1，`inQ` 加 1" if s[i] == letter else "普通字符，只入队"}',
        'q.append(s[i])': '`{s[i]}` 入队尾：`q = {q}`',
        'if i >= n - k': '`i = {i}` {">=" if i >= n - k else "<"} `n - k = {n - k}` → {"现在起队首可以安全取出（后面还够 k 个）" if i >= n - k else "还早，剩下的字符多，队首还可能被更小的换掉"}',
        'if q[0] == letter': '队首 `{q[0]}` {"是" if q[0] == letter else "不是"} letter',
        'repetition -= 1': '取走一个 letter：`repetition = {repetition}`',
        'elif len(ans) + repetition < k': '`len(ans) + repetition = {len(ans)} + {repetition}` {"<" if len(ans) + repetition < k else ">="} `k = {k}` → {"还有空位给非 letter，取它" if len(ans) + repetition < k else "位置要留给 letter，丢掉这个字符"}',
        'ans.append(q[0])': '`ans = {ans}`',
        'q = q[1:]': '队首出队：`q = {q}`',
        'i += 1': '`i` → {i}',
        "return ''.join(ans)": '答案 `{"".join(ans)}`',
    },
    cards=dict(
        one_liner='单调队列求最小字典序，弹队尾前先数够 letter',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `s` 里选长为 `k` 的子序列，字典序最小，且 `letter` 至少出现 `repetition` 次',
                 '示例：`s = "leetcode"`，`k = 4`，`letter = "e"`，`repetition = 2` → `"ecde"`'],
        quote='对于本题需要注意的是，在弹出队尾元素时，需要判断后续能否构成 repetition 个 letter，从而及时退出循环。以及在弹出队首元素时，需要判断是否还有空间来放置后续的 letter。',
        quote_src='—— 灵茶山艾府题解',
        idea=['去掉 repetition，就是经典的「长为 k 的字典序最小子序列」：单调队列',
              '弹队尾是 letter 时：`inQ + unread <= repetition` 就不能再弹',
              '从队首取字符时：不是 letter 且 `len(ans) + repetition >= k` 就要把位置留给 letter，丢掉它'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`q = q[1:]` 对应队首出队）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：`inQ`、`unread`、`repetition` 三个计数要在入队/出队时同步更新',
                 '易错：`i >= n - k` 之后才能取队首，保证剩下的字符还凑得出 k 个',
                 '同类题：402. 移掉 K 位数字、316. 去除重复字母（单调栈求最小字典序）'],
    ),
)
