def _cmp(S):
    if 'mi' not in S or 'v' not in S or 'index' not in S or S.get('_line') is None:
        return ''
    if 'c' in S and len(S['c']) == 3 and S['v'] in range(1, 16) and S['index'] in range(3) and S.get('_inner', {}).get('v') is not None:
        i, v = S['index'], S['v']
        a, b = abs(S['c'][i] - S['mi'][i] * 17), abs(S['c'][i] - v * 17)
        return f"通道 {i}：`|{S['c'][i]} − {S['mi'][i]}×17|` = =={a}==　对比　`|{S['c'][i]} − {v}×17|` = =={b}=="
    return ''


CONFIG = dict(
    num=800, title='相似RGB颜色', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='逐通道枚举 0~15 取最近',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def similarRGB(self, color):

        c = []
        for index in range(1, 7, 2):
            c.append(0)
            if '0' <= color[index] <= '9':
                c[-1] += int(color[index]) * 16
            else:
                c[-1] += (ord(color[index]) - 87) * 16
            
            if '0' <= color[index + 1] <= '9':
                c[-1] += int(color[index + 1])
            else:
                c[-1] += ord(color[index + 1]) - 87

        mi = [0, 0, 0]
        for v in range(1, 16):
            for index in range(3):
                if abs(c[index] - mi[index] * 17) > abs(c[index] - v * 17):
                    mi[index] = v

        res = '#'
        for v in mi:
            if v >= 10:
                res += chr(v + 87)
                res += chr(v + 87)
            else:
                res += str(v)
                res += str(v)
        
        return res
''',
    call="Solution().similarRGB('#09f166')",
    expect='#11ee66',
    views=[
        dict(type='string', var='color', label='color（每两位十六进制是一个通道）', pointers={'(index if _line < 17 else None)': 'blue'}, pointer_labels={'(index if _line < 17 else None)': 'index'}, h=150, cell=60),
        dict(type='array', var='c', label='c：三个通道的十进制值', pointers={'(index // 2 if _line < 17 else None)': 'blue'}, pointer_labels={'(index // 2 if _line < 17 else None)': '通道'}, h=170, cell=76),
        dict(type='array', var='mi', label='mi：每个通道目前最好的 v（颜色 = v × 17）', pointers={'(index if 17 <= _line <= 21 else None)': 'pink'}, pointer_labels={'(index if 17 <= _line <= 21 else None)': 'index'}, h=240, cell=76),
        dict(type='text', fn=_cmp, size=30, h=90),
        dict(type='string', var='res', label='res', h=120, cell=60),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        "c.append(0)": '新开一个通道，值先记 0',
        "int(color[index]) * 16": '高位是数字：`{color[index]} × 16` → `c[{index//2}]` = {c[-1]}',
        "(ord(color[index]) - 87) * 16": '高位是字母：`ord − 87` 把 a~f 换成 10~15，再乘 16 → `c[{index//2}]` = {c[-1]}',
        "int(color[index + 1])": '低位是数字，直接加上 → `c[{index//2}]` = =={c[-1]}==',
        "ord(color[index + 1]) - 87": '低位是字母，换成 10~15 再加 → `c[{index//2}]` = =={c[-1]}==',
        "mi = [0, 0, 0]": '三个通道先都假设用 `0`（即 00），后面从 1 开始枚举',
        "for v in range(1, 16)": '枚举候选 `v`：对应颜色 `vv`，十进制是 `v × 17`（如 `ee` = 14×17 = 238）',
        "if abs(c[index]": '通道 {index}：现有 `{abs(c[index] - mi[index] * 17)}` 对比 `v={v}` 的 `{abs(c[index] - v * 17)}` → {"==更近，替换==" if abs(c[index] - mi[index] * 17) > abs(c[index] - v * 17) else "没有更近（要严格更小），保持"}',
        "mi[index] = v": '`v = {v}` 更近，通道 {index} 的最佳值更新为 `{v}`（即 `{v*17}`）',
        "res = '#'": '三个 `v` 已定：每个 `v` 写成两位相同的十六进制字符',
        "if v >= 10": '`v = {v}`：{"≥ 10，要用字母 a~f" if v >= 10 else "< 10，直接写数字"}',
        "res += chr(v + 87)": '`chr(v + 87)` 把 {v} 变回字母，写两遍 → `{res}`',
        "res += str(v)": '写数字 `{v}` 两遍 → `{res}`',
        "return res": '三个通道都取到最近的相似色：`{res}`',
    },
    skip=['for index in range(3)', 'for v in range(1, 16)', 'mi[index] = v', 'c.append(0)'],
    max_steps=64,
    cards=dict(
        one_liner='三个平方项各自独立，逐通道选最近的 `vv`',
        complexity='时间 `O(1)`（16×3 次比较），空间 `O(1)`',
        problem=['颜色 `#AABBCC` 与 `#ABCDEF` 的相似度 = `−(AB−AB)² − …` 三项平方的相反数',
                 '`#xyz` 简写等于 `#xxyyzz`，求与给定颜色==最相似==的简写颜色',
                 '示例：`#09f166` → `#11ee66`'],
        quote='要让三个平方项中括号的绝对值最小，于是可以从0到15枚举所有颜色，选择与当前差值绝对值最小的作为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['表达式是三个负的平方项之和，三个通道==互不影响==，各取最小差即可',
              '简写通道 `vv` 的十进制值是 `v × 17`（0、17、34 … 255）',
              '先把 `color` 每两位换成十进制，再对每个通道枚举 `v = 1..15`，取 `|c − 17v|` 最小'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '差值要在十进制（16 进制数值）下算，不能直接比较字符',
                 '`mi` 初始为 0，所以枚举从 1 开始；比较用严格 `>`，同样近时保留较小的 `v`',
                 '字母换算用 `ord(ch) - 87`（`a` 的 ASCII 是 97）；原文本就是 Python 3 可运行的写法，未修改'],
    ),
)
