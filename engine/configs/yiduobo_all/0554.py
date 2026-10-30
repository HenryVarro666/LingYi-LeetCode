def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    wall = S['wall']
    n = len(wall)
    tot = sum(wall[0])
    W = x1 - x0 - 80
    unit = W / tot
    rh = min(70, (y1 - y0 - 90) / n)
    cv.text((x0 + 18, y0 + 4), 'wall（每行是一层砖；黄线 = 当前前缀和所在的竖线）', 24, T['muted'], bold=True)
    cur_i = S.get('i', -1)
    cur_j = S.get('j', -1)
    sd = S.get('sum_dict', {})
    best = max(sd.values()) if sd else 0
    for i, row in enumerate(wall):
        y = y0 + 50 + i * rh
        x = x0 + 40
        for j, b in enumerate(row):
            col = T['border']
            if i == cur_i and j < cur_j + 1 and j <= len(row) - 2:
                col = T['blue']
            elif i == cur_i and j == len(row) - 1 and cur_j >= len(row) - 2:
                col = T['dim']
            cv.rect((x + 2, y + 2, x + b * unit - 2, y + rh - 2), fill=col, r=6)
            cv.text((x + b * unit / 2, y + rh / 2), b, 24, T['text'], anchor='mm', bold=True)
            x += b * unit
    if sd:
        for k, v in sd.items():
            X = x0 + 40 + k * unit
            c = T['green'] if v == best else T['yellow']
            cv.line([(X, y0 + 44), (X, y0 + 50 + n * rh + 4)], c, 3)
            cv.text((X, y0 + 50 + n * rh + 8), f'{k}:{v}', 22, c, anchor='mt', bold=True)


CONFIG = dict(
    num=554, title='砖墙', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='前缀和计数（穿过最少砖 = 缝最多）', tags=[],
    code='''
class Solution(object):
    def leastBricks(self, wall):

        sum_dict = {}
        res = 0
        for i in range(len(wall)):
            prefix_sum = 0
            for j in range(len(wall[i]) - 1):
                prefix_sum += wall[i][j]
                sum_dict[prefix_sum] = sum_dict.get(prefix_sum, 0) + 1
                res = max(res, sum_dict[prefix_sum])

        return len(wall) - res
''',
    call='Solution().leastBricks([[1,2,2,1],[3,1,2],[1,3,2],[2,4]])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='sum_dict', fmt=lambda k, v: f'{v} 条缝', h=170, label='sum_dict：竖线位置 → 有多少层在此处有砖缝'),
    ],
    watch=['i', 'j', 'prefix_sum', ('res', 'res', 'green')],
    captions={
        'prefix_sum = 0': '第 `{i}` 层从左边开始，前缀和清零',
        'range(len(wall[i]) - 1)': '只枚举到倒数第二块砖：==最右边的竖线不能算==',
        'prefix_sum += ': '前 `{j+1}` 块砖长度之和 = `{prefix_sum}`：竖线 `x = {prefix_sum}` 恰好落在这一层的砖缝上',
        'sum_dict[prefix_sum] =': '位置 `{prefix_sum}` 的砖缝数 → `{sum_dict[prefix_sum]}`',
        'res = max': '砖缝最多的位置有 `{res}` 层：`res = max({B.res}, {sum_dict[prefix_sum]}) = {res}`',
        'return len(wall)': '共 `{len(wall)}` 层，最多 `{res}` 层有缝 → 穿过 `{len(wall)} − {res} = {ret}` 块砖',
    },
    cards=dict(
        one_liner='竖线经过的砖缝越多，穿过的砖越少',
        complexity='时间 `O(砖总数)`，空间 `O(砖缝位置数)`',
        problem=['一面砖墙，每层砖高相同、长度不同，各层总宽相同',
                 '画一条竖线，穿过砖块内部算“穿过”，贴着砖缝不算；线不能在墙最左/最右边缘',
                 '求竖线最少穿过多少块砖。示例：4 层 `[[1,2,2,1],[3,1,2],[1,3,2],[2,4]]` → `2`'],
        quote='对于一条竖线x=k，要判断其是否穿过了第m层的砖，那么就是检测第m层从左边开始的前n块砖长度之和是否恰好等于k，这个前n块砖的长度之和很明显是一个前缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['竖线 `x = k` 在某层是砖缝 ⇔ 该层有一个前缀和等于 `k`',
              '各层互不影响，逐层算前缀和，用字典统计每个位置出现的次数',
              '出现次数最多的位置 = 砖缝最多，答案 = 总层数 − 最大次数'],
        summary=['时间 `O(n)`（n 为砖块总数），空间 `O(n)`',
                 '易错：不要把最后一块砖算进前缀和，否则最右边的墙边会被当成答案',
                 '若每层只有一块砖，字典为空，`res = 0`，答案是层数',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
