CONFIG = dict(
    num=821, title='字符的最短距离', difficulty='Easy', category='字符串',
    author='yiduobo', technique='左右各扫一遍',
    code='''
class Solution(object):
    def shortestToChar(self, S, C):

        n = len(S)

        if S[0] == C:
            prev = [0]
        else:
            prev = [-1]
        for index in range(1, n):
            if S[index] == C:
                prev.append(index)
            else:
                prev.append(prev[-1])
        
        if S[n - 1] == C:
            next = [n - 1]
        else:
            next = [-1]
        for index in range(n - 2, -1, -1):
            if S[index] == C:
                next.append(index)
            else:
                next.append(next[-1])
        next.reverse()

        res = []
        for index in range(n):
            if prev[index] == -1:
                res.append(next[index] - index)
            elif next[index] == -1:
                res.append(index - prev[index])
            else:
                res.append(min(next[index] - index, index - prev[index]))
        
        return res
''',
    call='Solution().shortestToChar("loveleetcode", "e")',
    expect=[3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0],
    views=[
        dict(type='string', var='S', pointers={'index': 'blue'}, h=160, label='S（目标字符 e）',
             color=lambda S, i, v: 'green' if v == S.get('C') else None),
        dict(type='array', var='prev', h=150, label='prev（左边最近的 e 的下标，-1 = 没有）'),
        dict(type='array', var=lambda S: S['next'] if isinstance(S.get('next'), list) else [], h=150, label='next（右边最近的 e 的下标，-1 = 没有）'),
        dict(type='array', var='res', h=150, label='res（到最近 e 的距离）'),
    ],
    watch=[('index', 'index', 'blue'), ('n', 'n'), ('C', 'C', 'green')],
    captions={
        'prev = [0]': '`S[0]` 就是 `{C}` → 它左边最近的 `{C}` 就是自己，`prev = [0]`',
        'prev = [-1]': '`S[0]` 不是 `{C}` → 左边还没出现过，记 `-1`',
        'for index in range(1, n)': '从左往右扫：`prev[index]` = 0 到 index 里最后一个 `{C}` 的位置',
        'if S[index] == C': lambda S, B, r: (f'`S[{S.index}] = {S.S[S.index]}` 就是目标 → 位置更新成自己' if S.S[S.index] == S.C else f'`S[{S.index}] = {S.S[S.index]}` 不是目标 → 沿用前一个位置'),
        'prev.append(index)': '`prev[{index}] = {index}`',
        'prev.append(prev[-1])': '`prev[{index}] = {prev[-1]}`（沿用）',
        'if S[n - 1] == C': '`S[n-1]` 是 `{C}` 吗 → 决定 `next` 的起点',
        'next = [n - 1]': '最后一个字符就是目标，`next` 从 `{n-1}` 开始',
        'next = [-1]': '最后一个字符不是目标，右边没有 → 记 `-1`',
        'for index in range(n - 2': '从右往左扫：`next` 先倒着存，最后再反转',
        'next.append(index)': '`S[{index}]` 是目标：右边最近的 `{C}` 就是自己',
        'next.append(next[-1])': '不是目标：沿用右边的 `{next[-1]}`',
        'next.reverse()': '反转后 `next[i]` 就对应下标 i：`{next}`',
        'for index in range(n):': '逐个位置取两边较近者',
        'if prev[index] == -1': '`prev[{index}] = {prev[index]}`：左边没有目标吗 → {"是，只能用右边的" if prev[index] == -1 else "否"}',
        'elif next[index] == -1': '`next[{index}] = {next[index]}`：右边没有目标吗 → {"是，只能用左边的" if next[index] == -1 else "否，两边都有"}',
        'res.append(next[index] - index)': '只有右边：距离 `{next[index]} − {index}` = =={res[-1]}==',
        'res.append(index - prev[index])': '只有左边：距离 `{index} − {prev[index]}` = =={res[-1]}==',
        'res.append(min': '两边都有：`min({next[index]} − {index}, {index} − {prev[index]})` = =={res[-1]}==',
        'return res': '全部位置的最短距离：`{res}`',
    },
    cards=dict(
        one_liner='最近的目标要么在左边，要么在右边：各扫一遍再取小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给字符串 `S` 和其中出现的字符 `C`',
                 '对每个位置，求它到最近的 `C` 的距离（下标差的绝对值）',
                 '示例：`S="loveleetcode"`，`C="e"` → `[3,2,1,0,1,0,0,1,2,2,1,0]`'],
        quote='找出从0到index这一段中C最后一次出现的位置prev[index]，以及从index到n - 1这一段中C最早一次出现的位置next[index]，然后取index - prev[index]以及next[index] - index中较小的那个即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左往右扫一遍，得到每个位置左边最近的目标 `prev`',
              '从右往左扫一遍，得到右边最近的目标 `next`，最后反转对齐',
              '某一侧是 `-1` 就只能用另一侧，否则取较小距离'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`-1` 表示这一侧没有目标，要先判断再算距离',
                 '`next` 倒着 append，最后一定要 `reverse()`',
                 '`next` 覆盖了内置函数名，实际写代码时最好换名'],
    ),
)
