C = 122.11


def _draw(cv, S, B, box, T):
    """三根温度计：0°C 和 100°C 对齐，横线 = 输入温度在三种温标下的读数"""
    x0, y0, x1, y1 = box
    c = S.get('celsius', C)
    cv.text((x0 + 18, y0 + 4), '同一个温度，三种温标的读数（0°C、100°C 两条刻度线对齐）', 24, T['muted'], bold=True)
    top, bot = y0 + 120, y1 - 170
    cmax = max(100, c) + 20
    cmin = -10

    def Y(cc):
        return bot - (cc - cmin) / (cmax - cmin) * (bot - top)
    cols = [('摄氏度 °C', lambda x: x, T['blue'], '{:.2f}'), ('开氏度 K', lambda x: x + 273.15, T['purple'], '{:.2f}'),
            ('华氏度 °F', lambda x: x * 1.8 + 32, T['orange'], '{:.3f}')]
    span = (x1 - x0 - 120) / 3
    for k, (name, f, colr, fmt_) in enumerate(cols):
        X = x0 + 90 + span * k + span * 0.25
        cv.text((X, top - 40), name, 24, colr, anchor='mm', bold=True)
        cv.rect((X - 16, top - 10, X + 16, bot + 10), fill=T['panel2'], outline=T['border'], width=2, r=16)
        cv.rect((X - 9, Y(c), X + 9, bot + 4), fill=T['red'], r=9)
        cv.d.ellipse((X - 24, bot - 4, X + 24, bot + 44), fill=T['red'])
        for ref in (0, 100):
            yy = Y(ref)
            cv.line([(X + 18, yy), (X + 34, yy)], T['muted'], 2)
            v = f(ref)
            cv.text((X + 40, yy), (f'{v:g}' if v == int(v) else f'{v:.2f}'), 20, T['muted'], anchor='lm')
        cv.text((X + 40, Y(c) - 6), fmt_.format(f(c)).rstrip('0').rstrip('.'), 26, colr, anchor='lb', bold=True)
    cv.dashed((x0 + 40, Y(c)), (x1 - 30, Y(c)), T['red'], 2)
    yb = bot + 70
    k_ = c + 273.15
    f_ = c * 1.8 + 32
    cv.rich(x0 + 30, yb, f'`celsius + 273.15` = `{c:g} + 273.15` = =={k_:g}==', x1 - x0 - 60, size=26)
    cv.rich(x0 + 30, yb + 46, f'`celsius * 1.8 + 32` = `{c:g} × 1.8 + 32` = =={f_:g}==（超过 100°C 也照样算）', x1 - x0 - 60, size=26)


CONFIG = dict(
    num=2469, title='温度转换', difficulty='Easy', category='数学',
    author='yiduobo', technique='按转换公式直接计算',
    tags=['List.md'],
    code='''
class Solution(object):
    def convertTemperature(self, celsius):
        return [celsius + 273.15, celsius * 1.8 + 32]
''',
    call=f'Solution().convertTemperature({C})',
    expect=[395.26, 251.798],
    views=[dict(type='custom', h=620, draw=_draw)],
    watch=[('celsius', 'celsius', 'blue')],
    captions={
        'return [celsius + 273.15': '按题目给出的转换公式：开氏度 `{celsius} + 273.15`，华氏度 `{celsius} × 1.8 + 32` → =={ret}==',
    },
    cards=dict(
        one_liner='比较基础的题目：根据题目给出的转换公式计算答案即可',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你一个摄氏度 `celsius`（保留两位小数），转换成开氏度和华氏度',
                 '`开氏度 = 摄氏度 + 273.15`，`华氏度 = 摄氏度 × 1.80 + 32.00`',
                 '返回 `[kelvin, fahrenheit]`；示例：`122.11` → `[395.26000, 251.79800]`'],
        quote='比较基础的题目，==根据题目给出的转换公式计算答案即可==。',
        quote_src='—— yiduobo 题解',
        idea=['开氏度：在摄氏度上加 `273.15`',
              '华氏度：摄氏度乘 `1.8` 再加 `32`',
              '按 `[开氏度, 华氏度]` 的顺序放进列表返回'],
        result='`[395.26, 251.798]` ✓ 与示例 2 一致',
        after=[dict(heading='公式里的 1.8 和 32 是怎么来的？', lines=[
            '水结冰 `0°C = 32°F`，水沸腾 `100°C = 212°F`',
            '100 个摄氏度对应 `212 − 32 = 180` 个华氏度 → 每度 `1.8` 倍',
            '再加上起点 `32`：`F = C × 1.8 + 32`；开氏度只是整体平移 `273.15`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '返回顺序：先开氏度、后华氏度',
                 '浮点误差在 `10⁻⁵` 以内都算对，不用手动四舍五入',
                 '和灵神的代码一模一样：这题就是一行公式',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
