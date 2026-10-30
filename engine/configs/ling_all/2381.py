CONFIG = dict(
    num=2381, title='字母移位 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 · 导数与积分',
    tags=['常用数据结构', '二、差分', '难度分 1793'],
    setup='from string import ascii_lowercase',
    code='''
c2i = {c: i for i, c in enumerate(ascii_lowercase)}

class Solution:
    def shiftingLetters(self, s: str, shifts: List[List[int]]) -> str:
        diff = [0] * (len(s) + 1)
        for start, end, dir in shifts:
            diff[start] += dir * 2 - 1
            diff[end + 1] -= dir * 2 - 1
        return ''.join(ascii_lowercase[(c2i[c] + shift) % 26] for c, shift in zip(s, accumulate(diff)))
''',
    call='Solution().shiftingLetters("abc", [[0,1,0],[1,2,1],[0,2,1]])',
    expect='ace',
    views=[
        dict(type='text', fn=lambda S: (f"当前操作：区间 `[{S['start']}, {S['end']}]`，方向 `dir = {S['dir']}` → 每个字符 ==`{S['dir']*2-1:+d}`==" if 'start' in S and 'dir' in S and 'end' in S else ''), size=28),
        dict(type='string', var='s', label='s', h=170),
        dict(type='array', var='diff', label='diff（在 start 加 x，在 end+1 减 x）', h=190, pointers={'start': 'blue', 'end + 1': 'pink'},
             color=lambda S, i, v: 'yellow' if v != 0 else None),
        dict(type='text', fn=lambda S: ('累加 diff 得到每个字符的移位量：' + '，'.join(f"`{x}`" for x in list(accumulate(S['diff']))[:len(S['s'])])) if 'diff' in S else '', size=26),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink'), 'dir'],
    captions={
        'c2i = ': '先建字母到数字的映射：`a→0 … z→25`',
        'diff = [0]': '`diff` 记录变化量，长度 `n + 1`，多出的一格给 `end + 1` 越界时用',
        'for start, end, dir': '取一次移位：`[{start}, {end}]`，`dir = {dir}`',
        'diff[start] +=': '`dir * 2 - 1` 把 0/1 变成 -1/+1；在 `start` 处变化量加上它 → `diff[{start}] = {diff[start]}`（类比导数）',
        'diff[end + 1] -=': '到 `end + 1` 变化量减回去，区间外不受影响 → `diff[{end+1}] = {diff[end+1]}`',
        'return': lambda S, B, ret: f"`accumulate(diff)` 累加变化量得到每个字符的移位量（类比积分），再 `% 26` 回绕，拼出 =={ret}==",
    },
    cards=dict(
        one_liner='区间移位记成「导数」，累加一遍还原每个字符',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['`shifts[i] = [start, end, dir]`：把 `s[start..end]` 每个字符移位',
                 '`dir = 1` 向后一位，`dir = 0` 向前一位，`z`/`a` 环绕',
                 '示例：`s="abc"`，`[[0,1,0],[1,2,1],[0,2,1]]` → `"ace"`'],
        quote='用差分数组 diff 表示一段区间上的更新，即在 start 变化量增加了 x，在 end+1 变化量减少了 x（类比导数的概念）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x = 2·dir − 1`：把 0 / 1 变成 −1 / +1',
              '`diff[start] += x`，`diff[end+1] -= x`：只在区间两端记账',
              '从左到右累加 `diff`（类比积分），第 `i` 个字符的移位量就是前缀和'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '`diff` 开 `n + 1` 格，`end + 1` 才不会越界',
                 'Python 的 `%` 对负数结果非负，向前移位不需要特判',
                 '相似题：1094 拼车、1109 航班预订统计',
                 '对比 yiduobo：他手动处理负数取模，灵神直接用 `% 26`'],
    ),
)
