CONFIG = dict(
    num=1540, title='K次操作转变字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按位移量计数 · 每 26 轮重复',
    code='''
class Solution(object):
    def canConvertString(self, s, t, k):
        
        if len(s) != len(t):
            return False

        cnt_list = [0] * 26
        n = len(s)
        for index in range(n):
            dis = ord(t[index]) - ord(s[index])
            if dis < 0:
                dis += 26
            
            cnt_list[dis] += 1
        
        res = 0
        for index in range(1, 26):
            if cnt_list[index] > 0:
                res = max(res, (cnt_list[index] - 1) * 26 + index)
        
        return res <= k
''',
    call='Solution().canConvertString("aaz", "bca", 27)',
    expect=True,
    views=[
        dict(type='string', var='s', h=200, pointers={'index': 'blue'}, label='s（要变成 t）'),
        dict(type='string', var='t', h=200, pointers={'index': 'pink'}, label='t（目标）'),
        dict(type='array', var='cnt_list', h=200, label='cnt_list[d] = 需要右移 d 位的字符个数',
             color=lambda S, i, v: 'yellow' if v > 0 else None),
    ],
    watch=['index', 'dis', ('res', 'res', 'green'), 'k'],
    captions={
        'if len(s) != len(t)': '长度不同没法逐位变换 → 直接不可能；这里长度相同，继续',
        'cnt_list = [0] * 26': '`cnt_list[d]` 统计需要右移 `d` 位的字符个数（`d` 取 0..25）',
        'res = 0': '`res` 记录所有字符里最晚需要的操作轮次',
        'for index in range(n)': '看第 `{index}` 个字符：`{s[index]}` → `{t[index]}`',
        'dis = ord': '`ord(t) - ord(s) = {dis}`：要右移的位数',
        'if dis < 0': lambda S, B, r: (f'`dis = {S.dis} < 0` → 成立：字母表是环，加 26' if S.dis < 0 else f'`dis = {S.dis} >= 0` → 不用补'),
        'dis += 26': '绕一圈：`dis = {dis}`',
        'cnt_list[dis] += 1': '需要位移 `{dis}` 的字符多了一个：`cnt_list[{dis}] = {cnt_list[dis]}`',
        'for index in range(1, 26)': '检查位移量 `d = {index}`',
        'if cnt_list[index] > 0': lambda S, B, r: (f'`cnt_list[{S.index}] = {S.cnt_list[S.index]} > 0` → 成立，要算它需要的最晚轮次' if S.cnt_list[S.index] > 0 else f'`cnt_list[{S.index}] = 0` → 不成立，没有字符需要位移 {S.index}'),
        'res = max': '同位移的 `n` 个字符要在第 `d`、`d+26`、…、`d+(n-1)×26` 轮操作：最晚 `({cnt_list[index]} - 1) × 26 + {index}`，`res = {res}`',
        'return res <= k': lambda S, B, r: f'最晚需要第 `{S.res}` 轮，`k = {S.k}`：`{S.res} <= {S.k}` → =={r}==',
    },
    skip=['for index in range(1, 26)', 'if cnt_list[index] > 0'],
    max_steps=70,
    cards=dict(
        one_liner='相同位移的字符，只能错开 26 轮去操作',
        complexity='时间 `O(n)`，空间 `O(1)`（26 个计数）',
        problem=['第 `i` 轮（`1..k`）可选一个下标，把该字符右移 `i` 位（z 后回到 a），每个下标至多一次',
                 '问能否在 `k` 轮内把 `s` 变成 `t`',
                 '本视频：`s="aaz"`、`t="bca"`、`k=27` → `true`'],
        quote='若其中存在n个需要切换m次的字符，那么这n个字符需要在第m次、m + 26次、m + 52次、...、m + (n - 1) * 26次操作时进行转换',
        quote_src='—— yiduobo 题解原文',
        idea=['每个位置要右移 `d = (t-s) mod 26` 位，第 `d` 轮或 `d+26`、`d+52`… 轮才能用',
              '同一个 `d` 的字符共 `c` 个：最后一个要等到 `d + (c-1)×26` 轮',
              '取所有 `d` 里最晚的轮次，不超过 `k` 就可行'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：长度不同要先返回 `false`；`d = 0` 不用操作，所以循环从 `1` 开始',
                 '差值为负要加 `26`，因为字母表是环',
                 '原文已是 Python 3 可运行，代码未做改动'],
    ),
)
