CONFIG = dict(
    num=2381, title='字母移位 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分数组 · 后缀操作',
    tags=['灵神题单', '常用数据结构', '难度分 1793'],
    code='''
class Solution(object):
    def shiftingLetters(self, s, shifts):

        n = len(s)
        f = [0] * n
        for start, end, direction in shifts:
            if direction == 0:
                delta = -1
            else:
                delta = 1
            
            f[start] += delta
            if end + 1 < n:
                f[end + 1] -= delta

        res = []
        delta = 0
        for index in range(n):
            delta += f[index]
            now = ord(s[index]) - 97 + delta
            if now < 0:
                now = 26 - (-now) % 26
            now %= 26
            res.append(chr(now + 97))
        
        return ''.join(res)
''',
    call='Solution().shiftingLetters("abc", [[0,1,0],[1,2,1],[0,2,1]])',
    expect='ace',
    views=[
        dict(type='text', fn=lambda S: (f"下标 `{S['index']}`：累计移位 `{S['delta']}`" if 'index' in S and 'delta' in S else (f"当前操作：`[{S['start']}, {S['end']}]`，`delta = {S['delta']}`" if 'start' in S and 'delta' in S else '')), size=28),
        dict(type='string', var='s', label='s', h=170),
        dict(type='array', var='f', label='f[i]：后缀 [i, n) 上的移位操作', h=190,
             color=lambda S, i, v: 'yellow' if v != 0 else None, pointers={'index': 'blue'}),
        dict(type='string', var='res', label='res（已还原的字母）', h=170),
    ],
    watch=[('index', 'index', 'blue'), ('delta', 'delta', 'pink'), 'now'],
    captions={
        'n = len(s)': '`n = {n}`',
        'f = [0]': '`f[i]` 表示后缀区间 `[i, n)` 上被加了多少次移位',
        'for start, end, direction': '取一次操作：`[{start}, {end}]`，`direction = {direction}`',
        'delta = -1': '`direction == 0`：向前，每个字符 `-1`',
        'delta = 1': '`direction == 1`：向后，每个字符 `+1`',
        'f[start] += delta': '区间拆成两个后缀：从 `start` 起整体 `{delta:+d}` → `f[{start}] = {f[start]}`',
        'if end + 1 < n': lambda S, B, r: (f'`end + 1 = {S.end + 1} < {S.n}`：还有后缀要抵消' if S.end + 1 < S.n else f'`end + 1 = {S.end + 1}` 已经到头，没有后缀可抵消'),
        'f[end + 1] -= delta': '从 `end + 1` 起整体反向抵消 → `f[{end+1}] = {f[end+1]}`，区间外不受影响',
        'res = []': '第二遍：从左到右累加 `f`，还原每个字符',
        'delta = 0': '`delta` 重新用来存累计移位量',
        'delta += f[index]': '累加 `f[{index}]` → 下标 `{index}` 的总移位 `delta = {delta}`',
        'now = ord': "`'{s[index]}'` 的序号 `{ord(s[index]) - 97}` + `{delta}` = `{now}`",
        'if now < 0': lambda S, B, r: (f'`{S.now} < 0`：往前越过了 `a`，要绕回来' if S.now < 0 else f'`{S.now} >= 0`：没越过 `a`，不用特殊处理'),
        'now = 26 - (-now) % 26': '负数先取绝对值再模 26，用 `26` 减去 → `now = {now}`',
        'now %= 26': '对 26 取模回绕 → `now = {now}`',
        'res.append': '序号 `{now}` 对应字母 =={chr(now + 97)}==',
        'return': '拼接得到 `{ret}`',
    },
    cards=dict(
        one_liner='区间操作拆成两个后缀操作，最后遍历一趟还原',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['`shifts[i] = [start, end, direction]`：把 `s[start..end]` 每个字符移位',
                 '`direction = 1` 向后一位，`0` 向前一位，`z`/`a` 首尾相接',
                 '示例：`s="abc"`，`[[0,1,0],[1,2,1],[0,2,1]]` → `"ace"`'],
        quote='对于子区间[left, right]上的操作，可以将其拆分为在后缀区间[left, n]上的正向操作，以及在后缀区间[right + 1, n]上的负向操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['最后只问一次结果，适合差分：`f[i]` 表示后缀 `[i, n)` 的操作情况',
              '操作 `[left, right]` = 更新 `f[left]` 与 `f[right + 1]` 两处',
              '遍历一趟累加 `f`，每个位置的最终移位量就出来了'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '`end + 1 == n` 时没有后缀可抵消，要先判断再减',
                 '负数取模：`now < 0` 时写成 `26 - (-now) % 26`，再 `% 26`',
                 '对比灵神：灵神 `diff` 多开一格，直接用 Python 的 `% 26`',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
