BOARD = ["abcde", "fghij", "klmno", "pqrst", "uvwxy", "z"]

CONFIG = dict(
    num=1138, title='字母板上的路径', difficulty='Medium', category='模拟',
    author='yiduobo', technique='编码成行列 · 先横后竖（z 反过来）',
    tags=[],
    code='''
class Solution(object):
    def alphabetBoardPath(self, target):

        nowx = 0
        nowy = 0
        res = ''
        for char in target:
            num = ord(char) - 97
            x = num // 5
            y = num % 5

            if nowy > y:
                h = 'L' * (nowy - y)
            else:
                h = 'R' * (y - nowy)
            

            if nowx > x:
                v = 'U' * (nowx - x)
            else:
                v = 'D' * (x - nowx)

            if nowx == 5:
                res += v
                res += h
            else:
                res += h
                res += v

            nowx = x
            nowy = y
            res += '!'
        
        return res
''',
    call='Solution().alphabetBoardPath("code")',
    expect="RR!RRDD!LUU!R!",
    skip=['x = num //', 'nowx = x', 'nowy = y', 'nowx = 0', 'nowy = 0'],
    views=[
        dict(type='grid', var=lambda S: BOARD, label='字母板（蓝框 = 当前位置，绿 = 本次要去的字母）', cell=84, h=330,
             color=lambda S, i, j, v: 'green' if ('x' in S and (i, j) == (S['x'], S['y'])) else None,
             cursors=[('nowx', 'nowy', 'blue')]),
        dict(type='text', fn=lambda S: f"已生成指令：`{S['res'] or '（空）'}`" if 'res' in S else '', size=34, h=90),
        dict(type='string', var='target', label='target', cell=70, h=120),
    ],
    watch=[('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue'), 'char', 'x', 'y', 'h', 'v'],
    captions={
        'for char in target': lambda S, B, r: ('`target` 的字母都处理完，循环结束' if S.res.count('!') == len(S.target) else f'取下一个字母 `char = {S.char}`'),
        "res = ''": '`res` 保存指令序列；起点 `({nowx},{nowy})`',
        'num = ord': '字母 `{char}` 编码为 `{num}`（a=0 … z=25）',
        'y = num % 5': '一行 5 个字母：行 `x = {num} // 5 = {x}`，列 `y = {num} % 5 = {y}`',
        'if nowy > y': lambda S, B, r: f'当前列 `{B.nowy}` 与目标列 `{S.y}` 比较：' + ('目标在左边 → 向左' if B.nowy > S.y else '目标不在左边 → 向右（相等则 0 步）'),
        "h = 'L'": '向左 `{nowy} - {y}` 步：`h = {h!r}`',
        "h = 'R'": '向右 `{y} - {nowy}` 步：`h = {h!r}`',
        'if nowx > x': lambda S, B, r: f'当前行 `{B.nowx}` 与目标行 `{S.x}` 比较：' + ('目标在上面 → 向上' if B.nowx > S.x else '目标不在上面 → 向下（相等则 0 步）'),
        "v = 'U'": '向上 `{nowx} - {x}` 步：`v = {v!r}`',
        "v = 'D'": '向下 `{x} - {nowx}` 步：`v = {v!r}`',
        'if nowx == 5': lambda S, B, r: ('==从 z 出发（第 5 行）：先竖后横==，否则第一步就走出板外' if B.nowx == 5
                                        else '不在 z 上：先横后竖。去 z 时横着走到第 0 列，再竖着下去，不会越界'),
        'res += v': lambda S, B, r: f"{'先竖（从 z 出发）' if B.nowx == 5 else '再竖'}：`res` = `{S.res}`",
        'res += h': lambda S, B, r: f"{'再横' if B.nowx == 5 else '先横'}：`res` = `{S.res}`",
        "res += '!'": '`!` 拾取字母 `{char}`：`res` = `{res}`',
        'return res': '全部字母处理完：`{ret}`',
    },
    cards=dict(
        one_liner='字母编码成行列，行列分别算指令；z 的位置特殊，顺序要换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母板 `abcde / fghij / ... / uvwxy / z`，从 `(0,0)` 出发',
                 '`U D L R` 移动、`!` 拾取当前字母，求拼出 `target` 的最短指令',
                 '示例：`code` → 官方答案 `RR!DDRR!UUL!R!`，本解先横后竖得 `RR!RRDD!LUU!R!`（同样最短）'],
        quote='需要注意的是，这里的字母板并不规整，如果从某个字母到z的话，应当先移动列，再移动行。同样地，从z往别的字母移动时则应当先移动行，再移动列。',
        quote_src='—— yiduobo 题解原文',
        idea=['字母 a~z 编号 0~25，`行 = num // 5`，`列 = num % 5`',
              '比较当前位置和目标位置：大了往上/左，小了往下/右，距离就是差值',
              '非 z 的移动横竖顺序无所谓；去 z 先横后竖，从 z 出发先竖后横'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`nowx == 5` 才是「在 z 上」，此时先竖后横；其余一律先横后竖',
                 '用 `if nowx == 5` 一个判断同时解决去 z 和离开 z 两种情况',
                 '原文为 Python 2 写法，`num / 5` 的整数除法已改为 `num // 5`',
                 '对比灵神：灵神用 `divmod` 与布尔下标一行完成，这里分步写清楚'],
    ),
)
