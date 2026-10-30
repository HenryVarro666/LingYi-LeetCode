def _text(S):
    if 'h' not in S:
        return '手表有 4 位小时灯、6 位分钟灯：枚举所有时间，数二进制里 1 的个数'
    h = S['h']
    s = f"小时 `{h}` = `{h:04b}`（{h.bit_count()} 盏）"
    if 'm' in S and S.get('_line', 0) >= 7:
        m = S['m']
        s += f"，分钟 `{m}` = `{m:06b}`（{m.bit_count()} 盏）"
    return s


CONFIG = dict(
    num=401, title='二进制手表', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='枚举时间 + bit_count',
    tags=[],
    code='''
class Solution:
    def readBinaryWatch(self, turnedOn: int) -> List[str]:
        ans = []
        for h in range(12):
            for m in range(60):
                if h.bit_count() + m.bit_count() == turnedOn:
                    ans.append(f"{h}:{m:02d}")
        return ans
''',
    call='Solution().readBinaryWatch(1)',
    expect=["0:01", "0:02", "0:04", "0:08", "0:16", "0:32", "1:00", "2:00", "4:00", "8:00"],
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var=lambda S: [int(c) for c in format(S['h'], '04b')] if 'h' in S else [0, 0, 0, 0],
             label='小时灯（4 位，亮 = 1）', cell=90,
             color=lambda S, i, v: 'yellow' if v else None, h=190),
        dict(type='array', var=lambda S: [int(c) for c in format(S['m'], '06b')] if 'm' in S else [0] * 6,
             label='分钟灯（6 位，亮 = 1）', cell=90,
             color=lambda S, i, v: 'cyan' if v else None, h=190),
        dict(type='array', var='ans', label='ans（已找到的时间）', cell=100, h=150),
    ],
    watch=[('h', 'h', 'yellow'), ('m', 'm', 'cyan'), ('turnedOn', 'turnedOn', 'pink')],
    skip=['for m in range'],
    max_steps=50,
    captions={
        'ans = []': '`ans` 收集所有合法时间',
        'for h in range': '枚举小时 `h = {h}`（0–11，共 12 种）',
        'for m in range': '枚举分钟 `m = {m}`（0–59，共 60 种）',
        'if h.bit_count()': lambda S, B, r: (f"`{S['h'].bit_count()} + {S['m'].bit_count()} = {S['h'].bit_count() + S['m'].bit_count()}` "
                                            + (f"== `turnedOn = {S['turnedOn']}` → 恰好亮这么多灯，记下" if S['h'].bit_count() + S['m'].bit_count() == S['turnedOn']
                                               else f"≠ `turnedOn = {S['turnedOn']}` → 跳过")),
        'ans.append': '加入 `{h}:{m:02d}`：分钟不足两位要补前导零（`:02d`），小时不补',
        'return ans': '一共 `{len(ret)}` 个时间：`{ret}`',
    },
    cards=dict(
        one_liner='时间一共才 12×60 种：全部枚举，数亮灯数是否等于 turnedOn',
        complexity='时间 `O(1)`（12×60 次枚举），空间 `O(1)`',
        problem=['二进制手表：4 盏灯表示小时（0–11），6 盏灯表示分钟（0–59）',
                 '给定亮着的灯数 `turnedOn`，返回所有可能的时间（任意顺序）',
                 '小时不补零，分钟必须两位：`"1:00"`、`"10:02"`',
                 '示例：`turnedOn = 1` → `["0:01","0:02",…,"8:00"]`；`9` → `[]`'],
        quote='枚举小时 h=0,1,2,…,11 以及分钟 m=0,1,2,…,59。如果 h 二进制中的 1 的个数加上 m 二进制中的 1 的个数恰好等于 turnedOn，那么把 h:m 添加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一盏灯 = 二进制的一个 `1`：亮灯总数 = `h` 的 1 的个数 + `m` 的 1 的个数',
              '时间只有 `12 × 60 = 720` 种，不需要 DFS，直接两层循环枚举',
              '`bit_count()` 一步数出 1 的个数'],
        after=[dict(heading='动画里没演示的部分', lines=['720 次判断太多，动画只演示了 `h = 0` 的前面几十个分钟，其余快进', '`h = 1, 2, 4, 8` 时只有 `m = 0` 满足（各亮 1 盏灯）', '所以结果是 6 个 `0:xx`（分钟 1,2,4,8,16,32）加上 `1:00,2:00,4:00,8:00`'])],
        summary=['时间 `O(1)`（常数 720 次），空间 `O(1)`',
                 '易错：分钟要 `:02d` 补前导零，小时不能补',
                 '`bit_count()` 需要 Python 3.10+',
                 '同类：191. 位 1 的个数'],
    ),
)
