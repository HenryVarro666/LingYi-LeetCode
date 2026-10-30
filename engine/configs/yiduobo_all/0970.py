CONFIG = dict(
    num=970, title='强整数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举幂次 · 哈希去重', tags=[],
    code='''
class Solution(object):
    def powerfulIntegers(self, x, y, bound):

        pow_x = [1]
        if x > 1:
            while pow_x[-1] * x <= bound:
                pow_x.append(pow_x[-1] * x)
        
        pow_y = [1]
        if y > 1:
            while pow_y[-1] * y <= bound:
                pow_y.append(pow_y[-1] * y)
        
        res_set = set()
        for px in pow_x:
            for py in pow_y:
                if px + py <= bound:
                    res_set.add(px + py)
        
        return list(res_set)
''',
    call='Solution().powerfulIntegers(2, 3, 10)',
    expect=[2, 3, 4, 5, 7, 9, 10],
    result_fn=sorted,
    views=[
        dict(type='array', var='pow_x', label='pow_x：x 的各次幂（≤ bound）', h=160, cell=90,
             color=lambda S, i, v: 'blue' if S.get('px') == v and S['_line'] >= 16 else None),
        dict(type='array', var='pow_y', label='pow_y：y 的各次幂（≤ bound）', h=160, cell=90,
             color=lambda S, i, v: 'pink' if S.get('py') == v and S['_line'] >= 16 else None),
        dict(type='set', var='res_set', label='res_set：已找到的强整数', h=130, font=28),
        dict(type='text', fn=lambda S: (f"`{S['px']} + {S['py']}` = =={S['px'] + S['py']}== " + ('≤' if S['px'] + S['py'] <= S['bound'] else '>') + f" bound `{S['bound']}`") if 'px' in S and 'py' in S else '', size=34),
    ],
    watch=['x', 'y', 'bound', 'px', 'py'],
    captions={
        'pow_x = [1]': '`pow_x` 从 `x^0 = 1` 开始，存 x 的各次幂',
        'if x > 1': lambda S, B, r: '`x = %d > 1`：幂会不断增长，需要逐个算' % S.x if S.x > 1 else '`x = 1`：幂永远是 1，只保留 `[1]`，否则会死循环',
        'while pow_x[-1] * x <= bound': lambda S, B, r: f'下一个幂 `{S.pow_x[-1]} × {S.x} = {S.pow_x[-1] * S.x}`，' + ('不超过 bound → 继续加' if S.pow_x[-1] * S.x <= S.bound else '超过 bound → 停，指数增长所以幂很少'),
        'pow_x.append': '没超过 bound，加入：`pow_x = {pow_x}`',
        'pow_y = [1]': '`pow_y` 同理，从 `y^0 = 1` 开始',
        'if y > 1': lambda S, B, r: '`y = %d > 1`：逐个算幂' % S.y if S.y > 1 else '`y = 1`：只保留 `[1]`',
        'while pow_y[-1] * y <= bound': lambda S, B, r: f'下一个幂 `{S.pow_y[-1] * S.y}`，' + ('不超过 bound → 继续加' if S.pow_y[-1] * S.y <= S.bound else '超过 bound → 停，==个数很少=='),
        'pow_y.append': '没超过 bound，加入：`pow_y = {pow_y}`',
        'res_set = set()': '用集合存结果，同一个和只算一次',
        'for px in pow_x': '外层取 x 的幂 `px = {px}`',
        'for py in pow_y': '内层取 y 的幂 `py = {py}`',
        'if px + py <= bound': lambda S, B, r: f'`{S.px} + {S.py} = {S.px + S.py}`，' + (f'不超过 `bound = {S.bound}` → 收下' if S.px + S.py <= S.bound else f'超过 `bound = {S.bound}` → 丢掉'),
        'res_set.add': '`{px + py}` 是强整数，放进集合（重复的自动去掉）',
        'return list': '集合里就是全部强整数：`{sorted(res_set)}`',
    },
    cards=dict(
        one_liner='幂次个数很少：先列出所有幂，再两两相加去重',
        complexity='时间 `O(log²bound)`，空间 `O(log²bound)`',
        problem=['强整数：存在整数 `i >= 0`、`j >= 0` 使得 `x^i + y^j` 等于它',
                 '给定 `x`、`y`、`bound`，返回所有 `<= bound` 的强整数（可任意顺序，不重复）',
                 '本视频：`x=2, y=3, bound=10` → `[2,3,4,5,7,9,10]`'],
        quote='我们可以计算出x和y的所有小于等于bound的幂次。当某个数等于1时，其幂次只有1，否则由于其指数增长，其幂次很快就能达到bound，因此总的数量是很少的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x > 1` 时幂是指数增长，不超过 bound 的幂只有 `log` 个',
              '`x = 1` 时幂永远是 1，必须单独处理，否则 while 死循环',
              '两两枚举幂次，和不超过 bound 就放进哈希集合去重'],
        summary=['幂的个数 `O(log bound)`，两两枚举 `O(log²bound)`',
                 '易错：`x = 1` 或 `y = 1` 时只保留 `[1]`，不然死循环',
                 '易错：不同的 `(i, j)` 可能得到同一个和（如 `2+3` 和 `4+1` 都是 5），所以要用集合去重',
                 '返回的 `list(res_set)` 顺序不固定，视频里排序后比较',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
