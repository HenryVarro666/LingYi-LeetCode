C = 36.50


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
    cv.rich(x0 + 30, yb, f'开氏度 = 摄氏度 + 273.15 = `{c:g} + 273.15` = =={k_:g}==', x1 - x0 - 60, size=26)
    cv.rich(x0 + 30, yb + 46, f'华氏度 = 摄氏度 × 1.80 + 32.00 = `{c:g} × 1.8 + 32` = =={f_:g}==', x1 - x0 - 60, size=26)


CONFIG = dict(
    num=2469, title='温度转换', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='根据公式计算',
    tags=['List.md'],
    code='''
class Solution:
    def convertTemperature(self, celsius: float) -> List[float]:
        return [celsius + 273.15, celsius * 1.8 + 32]
''',
    call=f'Solution().convertTemperature({C})',
    expect=[309.65, 97.7],
    views=[dict(type='custom', h=620, draw=_draw)],
    watch=[('celsius', 'celsius', 'blue')],
    captions={
        'return [celsius + 273.15': '直接套公式：`[{celsius} + 273.15, {celsius} × 1.8 + 32]` = =={ret}==（先开氏度，后华氏度）',
    },
    cards=dict(
        one_liner='直接套题目给的两个公式，按 [开氏度, 华氏度] 返回',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你一个摄氏度 `celsius`（保留两位小数），转换成开氏度和华氏度',
                 '`开氏度 = 摄氏度 + 273.15`，`华氏度 = 摄氏度 × 1.80 + 32.00`',
                 '返回 `ans = [kelvin, fahrenheit]`；示例：`36.50` → `[309.65000, 97.70000]`'],
        before=[dict(heading='三种温标对一对', lines=[
            '水结冰：`0°C` = `273.15 K` = `32°F`',
            '水沸腾：`100°C` = `373.15 K` = `212°F`',
            '开氏度只是==平移==；华氏度先==缩放 1.8 倍==再平移 32'])],
        quote='根据公式计算：`return [celsius + 273.15, celsius * 1.8 + 32]`',
        quote_src='—— 灵茶山艾府题解（标题与代码）',
        idea=['题目已经给出公式，照着算即可，一行代码',
              '返回顺序是 ==先开氏度、后华氏度==',
              '本视频：`celsius = 36.50`（人体体温附近）'],
        result='`[309.65, 97.7]` ✓ 与示例一致',
        after=[dict(heading='小数怎么判对？', lines=[
            '浮点数运算可能有极小误差',
            '题目规定：与实际答案误差不超过 `10⁻⁵` 就算正确',
            '所以直接返回 `float` 即可，不需要手动保留 5 位小数'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：返回顺序写反；把 `1.8` 写成 `9 / 5` 也可以',
                 '这类题的关键是==读懂题目给的公式==，不需要额外算法',
                 '灵神题解共有 Python/Java/C++/C/Go/JS/Rust 七种语言，写法都是一行公式'],
    ),
)
