CATS = [1, 2, 1, 3, 2, 1]
NAMES = {1: 'A', 2: 'B', 3: 'C'}
COLS = {1: 'blue', 2: 'orange', 3: 'purple'}
SETUP = '''
class CategoryHandler:
    def __init__(self, cats):
        self.cats = cats
    def haveSameCategory(self, a, b):
        return self.cats[a] == self.cats[b]
CATS = [1, 2, 1, 3, 2, 1]
'''


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(CATS)
    a, b = S.get('a'), S.get('b')
    sample = S.get('sample', [])
    cv.text((x0 + 18, y0 + 4), '元素 0..n-1（字母 = 真实类别，程序看不到，只能两两询问）', 22, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    ys = y0 + 90
    for i, c in enumerate(CATS):
        X = sx + i * cell
        fill = T[COLS[c]]
        inside = i in sample
        dim = a is not None and i > a
        cv.rect((X + 6, ys, X + cell - 6, ys + cell - 12), fill=fill, alpha=70 if dim else 255, r=12,
                outline=T['green'] if inside else T['border'], width=6 if inside else 1)
        cv.text((X + cell / 2, ys + (cell - 12) / 2), NAMES[c], 40, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + cell - 4), i, 20, T['dim'], anchor='mt', mono=True)
        if i == a:
            cv.tri_up(X + cell / 2, ys + cell + 34, 11, T['pink'])
            cv.text((X + cell / 2, ys + cell + 50), 'a', 24, T['pink'], anchor='mt', bold=True)
        if b is not None and i == b and a is not None and S.get('_line') in (8, 9, 10):
            cv.rect((X + 2, ys - 6, X + cell - 2, ys + cell - 6), outline=T['yellow'], width=4, r=14)
            cv.text((X + cell / 2, ys - 12), 'b', 24, T['yellow'], anchor='mb', bold=True)
    yb = ys + cell + 130
    cv.text((x0 + 18, yb - 40), 'sample（每个类别只留一个代表，绿框 = 已在 sample 里）', 22, T['muted'], bold=True)
    for k, e in enumerate(sample):
        X = x0 + 40 + k * 120
        c = CATS[e]
        cv.rect((X, yb, X + 100, yb + 100), fill=T[COLS[c]], r=12, outline=T['green'], width=4)
        cv.text((X + 50, yb + 42), NAMES[c], 36, T['bg'], anchor='mm', bold=True)
        cv.text((X + 50, yb + 80), f'元素 {e}', 20, T['bg'], anchor='mm', bold=True)
    if not sample:
        cv.text((x0 + 40, yb + 40), '（空）', 26, T['dim'])


CONFIG = dict(
    num=2782, title='唯一类别的数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='维护每个类别的代表元',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def numberOfCategories(self, n, categoryHandler):

        sample = []
        for a in range(n):
            flag = True
            for b in sample:
                if categoryHandler.haveSameCategory(a, b):
                    flag = False
                    break
            
            if flag:
                sample.append(a)
        
        return len(sample)
''',
    setup=SETUP,
    call='Solution().numberOfCategories(6, CategoryHandler(CATS))',
    expect=3,
    skip=['for b in sample'],
    max_steps=100,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('a', 'a', 'pink'), ('b', 'b', 'yellow'), ('flag', 'flag', 'orange'), ('sample', 'sample', 'green')],
    captions={
        'sample = []': '`sample` 为每个已发现的类别保存一个代表元素',
        'for a in range(n)': lambda S, B, r: (f'依次看元素 `a = {S.a}`：它属于已有类别，还是一个新类别？' if S.get('a') != B.get('a') else f'`n = {S.n}` 个元素都看完了'),
        'flag = True': '先假设 `a` 是新类别：`flag = True`',
        'if categoryHandler.haveSameCategory': lambda S, B, r: (f'问：`a = {S.a}` 和代表 `b = {S.b}` 同类吗？`haveSameCategory({S.a}, {S.b})` → ==是==，`a` 不是新类别' if S.categoryHandler.haveSameCategory(S.a, S.b) else f'问：`a = {S.a}` 和代表 `b = {S.b}` 同类吗？`haveSameCategory({S.a}, {S.b})` → ==否==，换下一个代表（比完都不同类 = 新类别）'),
        'flag = False': '`a = {a}` 已有同类代表：`flag = False`',
        'break': '已找到同类，不用再比了，跳出内层循环',
        'if flag': lambda S, B, r: (f'`flag = True`：`a = {S.a}` 和所有代表都不同类 → ==新类别==' if S.flag else f'`flag = False`：`a = {S.a}` 的类别已经有代表了，跳过'),
        'sample.append(a)': '`a = {a}` 成为新类别的代表：`sample = {sample}`',
        'return len(sample)': '`sample` 有 `{len(sample)}` 个代表 → 共 `{ret}` 个类别',
    },
    cards=dict(
        one_liner='每个类别只留一个代表，新元素与所有代表比一遍',
        complexity='时间 `O(n·m)`（m 为类别数，最坏 `O(n²)`），空间 `O(m)`',
        problem=['有 `n` 个元素（编号 `0..n-1`），看不到类别，只能调用 `haveSameCategory(a, b)` 判断同类',
                 '求一共有多少个不同的类别',
                 '本视频：`n = 6`，真实类别 `A B A C B A`（程序并不知道）→ `3`'],
        quote='使用一个数组sample来保存每种类别的一个实例，接下来从0开始进行遍历。对于当前遍历到的元素a，检测sample中是否存在某个元素b与a是同一类别。',
        quote_src='—— yiduobo 题解原文',
        idea=['`sample` 里每个元素各代表一个类别',
              '新元素 `a` 与 sample 里的代表逐个比：有同类就跳过',
              '和所有代表都不同类 → 新类别，`a` 入 sample',
              '最后 `len(sample)` 就是类别数'],
        summary=['时间 `O(n·m)`，m 为类别数；空间 `O(m)`',
                 '`flag` 先设 True，只在找到同类时设 False；找到后立即 `break` 省去无用比较',
                 '同类关系传递，所以只需和每个类别的一个代表比较',
                 '原文已是 Python 3 可运行，未做改动；CategoryHandler 在 setup 中定义'],
    ),
)
