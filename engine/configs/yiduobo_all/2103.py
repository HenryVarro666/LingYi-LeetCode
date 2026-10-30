CONFIG = dict(
    num=2103, title='环和杆', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希集合 · 每种颜色记录杆子',
    code='''
class Solution(object):
    def countPoints(self, rings):

        red = set()
        green = set()
        blue = set()

        for index in range(0, len(rings), 2):
            color = rings[index]
            pos = int(rings[index + 1])
            if color == 'R':
                red.add(pos)
            elif color == 'G':
                green.add(pos)
            else:
                blue.add(pos)
        
        res = 0
        for index in range(10):
            if index in red and index in green and index in blue:
                res += 1
        
        return res
''',
    call="Solution().countPoints('B0B6G0R6R0R6G9')",
    expect=1,
    views=[
        dict(type='string', var='rings', label='rings（每两个字符 = 颜色 + 杆编号）', cell=60, h=150,
             pointers={'index': 'blue'}),
        dict(type='set', var='red', label='red（有红环的杆）', h=100, fmt=lambda x: str(x)),
        dict(type='set', var='green', label='green（有绿环的杆）', h=100, fmt=lambda x: str(x)),
        dict(type='set', var='blue', label='blue（有蓝环的杆）', h=100, fmt=lambda x: str(x)),
        dict(type='text', h=70, size=28,
             fn=lambda S: ('杆 `%d`：红 %s 绿 %s 蓝 %s' % (S['index'], '有' if S['index'] in S['red'] else '无',
                                                     '有' if S['index'] in S['green'] else '无',
                                                     '有' if S['index'] in S['blue'] else '无'))
             if S.get('_line') in (19, 20, 21) and 'res' in S else '三个集合分别记录：哪些杆上套了这种颜色的环'),
    ],
    watch=[('index', 'index', 'blue'), ('color', 'color', 'yellow'), ('pos', 'pos', 'pink'), ('res', 'res', 'green')],
    captions={
        'red = set()': '三个集合：`red` / `green` / `blue`，记录每种颜色套在哪些杆上',
        'for index in range(0, len(rings), 2)': lambda S, B, r: (
            f'步长为 2：`index = {S.index}`，一次读一个环（颜色 + 杆编号）' if S.get('index') != B.get('index')
            else '环都读完了，接下来逐根杆子检查'),
        'color = rings[index]': '颜色 `color = {color}`',
        'pos = int(rings[index + 1])': '杆编号 `pos = {pos}`',
        "if color == 'R'": lambda S, B, r: f"`color = {S.color}`" + (' 是红色' if S.color == 'R' else ' 不是红色'),
        "elif color == 'G'": lambda S, B, r: f"`color = {S.color}`" + (' 是绿色' if S.color == 'G' else ' 不是绿色，只剩蓝色'),
        'red.add(pos)': '杆 `{pos}` 上有红环：`red = {red}`',
        'green.add(pos)': '杆 `{pos}` 上有绿环：`green = {green}`',
        'blue.add(pos)': '杆 `{pos}` 上有蓝环：`blue = {blue}`',
        'res = 0': '`res` 统计三色齐备的杆子数',
        'for index in range(10)': '杆子只有 10 根，逐根检查：`index = {index}`',
        'if index in red and': lambda S, B, r: (
            f'杆 `{S.index}` 三色齐备 → ==成立==' if (S.index in S.red and S.index in S.green and S.index in S.blue)
            else f'杆 `{S.index}` 缺颜色（红 {S.index in S.red}，绿 {S.index in S.green}，蓝 {S.index in S.blue}）→ 不算'),
        'res += 1': '又找到一根：`res` → {res}',
        'return res': '三色齐备的杆子共 `{res}` 根',
    },
    cards=dict(
        one_liner='用哈希集合记下每种颜色套在哪些杆上，再看谁三色齐备',
        complexity='时间 `O(n)`，空间 `O(1)`（杆子只有 10 根）',
        problem=['`rings` 每两个字符表示一个环：颜色 `R/G/B` + 杆编号 `0~9`',
                 '统计同时套有红、绿、蓝三种颜色环的杆子数量',
                 '示例：`B0B6G0R6R0R6G9` → `1`（只有 0 号杆三色齐备）'],
        quote='由于杆子只有10根，那么可以使用哈希表记录下每种颜色分别套在哪些杆子上。接下来只需遍历所有的杆子，判断该杆子上是否三种颜色齐备即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个环占两个字符，`range(0, len(rings), 2)` 一次跳两格',
              '颜色决定放进哪个集合，集合里存杆编号',
              '最后遍历 0~9 号杆，同时在三个集合里就计数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`rings` 里杆编号是字符，要 `int()` 转成数字',
                 '三个集合各自去重，同色多个环不影响结果',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
