from math import gcd as _g, lcm as _l

_NUMS = [6, 4, 3, 2, 7, 5, 10]


def _table():
    # 预先按同样的循环推一遍，记录每个 (行号, 栈, x) 对应处理到 nums 的哪个下标
    T, st = {}, []
    for k, x in enumerate(_NUMS):
        T.setdefault((4, tuple(st), x), k)
        while True:
            T.setdefault((5, tuple(st), x), k)
            if not (st and _g(x, st[-1]) > 1):
                break
            x = _l(x, st.pop())
            T.setdefault((6, tuple(st), x), k)
        st.append(x)
        T.setdefault((7, tuple(st), x), k)
    T[(8, tuple(st), x)] = len(_NUMS)
    return T


_T = _table()


def _k(S):
    if 'x' not in S:
        return -1
    return _T.get((S.get('_line'), tuple(S['st']), S['x']), -1)


CONFIG = dict(
    num=2197, title='替换数组中的非互质数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 邻项合并',
    tags=['数学算法', '难度分 2057'],
    setup='from math import gcd, lcm',
    code='''
class Solution:
    def replaceNonCoprimes(self, nums: List[int]) -> List[int]:
        st = []
        for x in nums:
            while st and gcd(x, st[-1]) > 1:
                x = lcm(x, st.pop())
            st.append(x)
        return st
''',
    call='Solution().replaceNonCoprimes([6,4,3,2,7,5,10])',
    expect=[12, 7, 10],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前，灰 = 已处理）', h=190,
             color=lambda S, i, v: 'blue' if 'x' in S and i == _k(S) else None,
             dim=lambda S, i, v: 'x' in S and i < _k(S)),
        dict(type='text', fn=lambda S: (f"手里的数 `x = {S['x']}`，栈顶 `{S['st'][-1] if S['st'] else '空'}`" + (f"，`gcd = {_g(S['x'], S['st'][-1])}`" if S.get('st') and S.get('_line') == 5 else '') if 'x' in S else ''), size=28),
        dict(type='stack', var='st', label='栈（已合并结果）', h=240),
    ],
    watch=[('x', 'x', 'blue'), ('st', 'st', 'green')],
    captions={
        'st = []': '栈里保存「已经合并完、互相互质」的数',
        'while st and gcd': lambda S, B, r: (f'`gcd({S.x}, {S.st[-1]}) = {_g(S.x, S.st[-1])}` > 1：非互质 → 要合并' if S.st and _g(S.x, S.st[-1]) > 1
                                              else ('栈为空，没有可合并的邻居' if not S.st else f'`gcd({S.x}, {S.st[-1]}) = 1`：互质，停止合并')),
        'x = lcm': '弹出栈顶 `{B.st[-1]}` 并合并：`lcm({B.x}, {B.st[-1]})` = =={x}==，还要继续和新的栈顶比',
        'st.append': '`x = {x}` 和栈顶互质（或栈已空），入栈 → `{st}`',
        'return st': '栈里相邻两数都互质，就是答案 `{st}`',
    },
    cards=dict(
        one_liner='合并顺序不影响结果：总是先合并最左边的，用栈做',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['相邻两数 `gcd > 1` 就删掉它们，换成 `lcm`，直到没有为止',
                 '返回最终数组，合并顺序不影响结果',
                 '示例：`[6,4,3,2,7,6,2]` → `[12,7,6]`'],
        quote='LCM 本质是质因数分解中质数的指数取最大值，所以 max(a,b,c) = max(max(a,b),c) = max(a,max(b,c))。据此总可以重排成：优先选择最左边的能合并的相邻元素。',
        quote_src='—— 灵茶山艾府题解（节选）',
        idea=['lcm 满足结合律：先合并哪一对都得到同一个结果',
              '所以从左到右，用栈保存已合并的数，新数 `x` 与栈顶不互质就弹出合并',
              '合并后的 `x` 可能又和更左边的数不互质，所以是 `while` 循环'],
        summary=['时间 `O(n log U)`：每个数至多入栈出栈一次，gcd 要 `log`',
                 '易错：合并后必须继续和新的栈顶判断，不能只合并一次',
                 '`gcd`、`lcm` 来自 `math`（Python 3.9+），已在 setup 中导入',
                 '同类题：邻项消除（括号匹配、行星碰撞）'],
    ),
)
