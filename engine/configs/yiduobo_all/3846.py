CONFIG = dict(
    num=3846, title='使用单指输入字符串的总距离', difficulty='Easy', category='模拟',
    author='yiduobo', technique='模拟 · 字符到坐标的哈希表',
    tags=[],
    code='''
class Solution(object):
    def totalDistance(self, s):
        
        key = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        x = {}
        y = {}

        for i, w in enumerate(key):
            for j, c in enumerate(w):
                x[c] = i
                y[c] = j
        
        res = 0
        nowx, nowy = 1, 0
        for c in s:
            res += abs(x[c] - nowx) + abs(y[c] - nowy)
            nowx, nowy = x[c], y[c]
        
        return res
''',
    call='Solution().totalDistance("hello")',
    expect=17,
    views=[
        dict(type='grid', var=lambda S: [list(r.ljust(10, ' ')) for r in S['key']], label='键盘（黄 = 手指当前位置，蓝 = 目标键）', h=300,
             cursors=[('nowx', 'nowy', 'yellow', '手指')],
             color=lambda S, i, j, v: 'blue' if 'c' in S and S['c'] in S.get('x', {}) and i == S['x'][S['c']] and j == S['y'][S['c']] else None),
        dict(type='string', var='s', label='s（要输入的字符串）', cell=90, h=150),
        dict(type='text', h=90, size=30, fn=lambda S: f"累计距离 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=['c', ('nowx', 'nowx', 'yellow'), ('nowy', 'nowy', 'yellow'), ('res', 'res', 'green')],
    captions={
        'key = [': '键盘三行，第 `i` 行第 `j` 列就是坐标 `(i, j)`',
        'for c in s': '要输入的字符 `c = {c}`',
        'x[c] = i': '记下 `{c}` 的行号 `x[{c!r}] = {x[c]}`，下一行再记列号 `y[c] = j`',
        'nowx, nowy = 1, 0': '手指一开始在 `a`：第 1 行第 0 列 → `(1, 0)`',
        'res += abs': '手指 `({B.nowx}, {B.nowy})` → `{c}` `({x[c]}, {y[c]})`，距离 `|{x[c]}−{B.nowx}| + |{y[c]}−{B.nowy}|` → `res` = =={res}==',
        'nowx, nowy = x[c]': '手指移到 `{c}`：`({nowx}, {nowy})`',
        'return res': '总移动距离 ==`{ret}`==',
    },
    skip=['y[c] = j', 'for j, c in enumerate(w)'],
    max_steps=100,
    cards=dict(
        one_liner='先把每个字母映射成坐标，再模拟手指一步步移动',
        complexity='时间 `O(26 + n)`，空间 `O(26)`',
        problem=['标准键盘三行：`qwertyuiop` / `asdfghjkl` / `zxcvbnm`',
                 '两键距离 = 曼哈顿距离 `|r1−r2| + |c1−c2|`',
                 '手指从 `a` 出发，按顺序输入 `s`，求总移动距离'],
        quote='直接模拟输入过程，记录当前目标字符位置与手指位置间的距离，累加到答案后将手指位置更新为当前目标字符的位置即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先遍历三行字符串，用 `x`、`y` 两个哈希表记下每个字母的行和列',
              '手指坐标 `(nowx, nowy)` 初始是 `a = (1, 0)`',
              '每输入一个字母：累加曼哈顿距离，再把手指移过去'],
        summary=['时间 `O(26 + n)`，空间 `O(26)`',
                 '易错点：初始手指在 `a`，是 `(1, 0)` 不是 `(0, 0)`',
                 '先累加距离，再更新手指位置，顺序不能反',
                 '题面库里缺失，题意按 yiduobo 文章整理'],
    ),
)
