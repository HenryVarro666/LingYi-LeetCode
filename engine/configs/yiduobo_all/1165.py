CONFIG = dict(
    num=1165, title='单行键盘', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表记位置 · 累加距离',
    tags=[],
    code='''
class Solution(object):
    def calculateTime(self, keyboard, word):

        pos = {}
        for index, char in enumerate(keyboard):
            pos[char] = index
        
        now = 0
        res = 0
        for char in word:
            p = pos[char]
            res += abs(now - p)
            now = p
        
        return res
''',
    call='Solution().calculateTime("abcdefghij", "cabd")',
    expect=7,
    views=[
        dict(type='string', var='keyboard', label='keyboard（单行键盘，手指起点在下标 0）', cell=80, h=240,
             pointers={'now': 'blue', 'p': 'pink'}),
        dict(type='string', var='word', label='word（按顺序敲出）', cell=80, h=150,
             color=lambda S, i, v: 'pink' if S.get('char') == v and i == S.get('_wi') else None),
        dict(type='map', var='pos', label='pos（字母 → 键盘下标）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=28),
    ],
    watch=[('now', 'now', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green'), 'char'],
    captions={
        'pos[char] = index': '`pos[{char!r}] = {index}`：记下字母 `{char}` 在键盘上的位置',
        'now = 0': '手指一开始在下标 `0`，`now` 记录手指当前位置',
        'p = pos[char]': '要敲 `{char}`，查哈希表得到它的位置 `p = {p}`，不用再扫一遍键盘',
        'res += abs': '手指从 `{now}` 移到 `{p}`：距离 `|{now} − {p}|` = {abs(now - p)} → `res` = =={res}==',
        'now = p': '手指停在 `{p}`，`now` = {now}，下一个字母从这里出发',
        'return res': '所有字母敲完，总用时 ==`{res}`==',
    },
    cards=dict(
        one_liner='先记下每个字母的位置，再累加相邻字母的距离',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['键盘只有一行，给出 26 个字母的排列 `keyboard`，手指从下标 0 出发',
                 '从下标 `i` 移到 `j` 用时 `|i − j|`，要按顺序敲出 `word`',
                 '返回敲完单词的总用时',
                 '本视频：键盘 `"abcdefghij"`，单词 `"cabd"` → `7`'],
        quote='首先对键盘一趟遍历，使用哈希表记录每个字符的位置，接下来遍历单词，通过哈希表计算相邻字符间的距离并累计起来作为最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历键盘，建哈希表 `pos`：字母 → 下标',
              '`now` 表示手指当前位置，初始为 0',
              '每个字母：距离 `abs(now − p)` 累加到 `res`，再更新 `now`'],
        summary=['时间 `O(n + m)`，键盘最多 26 个字母，空间 `O(1)`',
                 '易错点：手指起点是下标 0，不是第一个要敲的字母',
                 '距离要取绝对值，向左移动也是正的用时',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
