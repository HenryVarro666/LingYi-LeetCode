CONFIG = dict(
    num=2197, title='替换数组中的非互质数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='栈 · 辗转相除求 gcd',
    tags=['数学算法', '难度分 2057'],
    code='''
class Solution(object):
    def replaceNonCoprimes(self, nums):

        res = [nums[0]]
        for num in nums[1:]:
            while res:
                last = res.pop()
                x, y = last, num
                while y:
                    x, y = y, x % y

                if x == 1:
                    res.append(last)
                    break
                else:
                    num *= last // x
        
            res.append(num)

        return res
''',
    call='Solution().replaceNonCoprimes([4,2,3,9,5,10])',
    expect=[4, 9, 10],
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] and S.get('_line') in (5, 6) else None),
        dict(type='text', fn=lambda S: (f"新数 `num = {S['num']}`" + (f"，刚弹出的 `last = {S['last']}`" if 'last' in S and S.get('_line', 0) >= 7 else '') + (f"，`gcd = {S['x']}`" if S.get('_line') in (11, 12, 13) else '') if 'num' in S else ''), size=28),
        dict(type='stack', var='res', label='res（栈，已合并结果）', h=240),
    ],
    skip=['while y:'],
    max_steps=100,
    watch=[('num', 'num', 'blue'), ('last', 'last', 'pink'), ('x', 'x', 'yellow'), ('y', 'y', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = [nums[0]]': '`res` 当栈用：先放进第一个数 `{nums[0]}`',
        'for num in nums[1:]': lambda S, B, r: ('数组扫完了' if B.get('num') == S.num and B.get('res') == S.res else f'for 循环取下一个新数：`num = {S.num}`'),
        'while res:': lambda S, B, r: ('栈里还有数，取出栈顶来比较' if S.res else '栈空了，没有邻居可合并，直接放入'),
        'last = res.pop()': '弹出栈顶 `last = {last}`（先弹出来，要合并就不用放回了）',
        'x, y = last, num': '用辗转相除算 `gcd({last}, {num})`：`x, y = {x}, {y}`',
        'while y:': lambda S, B, r: (f'`y = {S.y}` ≠ 0，继续辗转' if S.y else f'`y = 0`，`x = {S.x}` 就是最大公约数'),
        'x, y = y, x % y': lambda S, B, r: (f'辗转相除：`x, y = {S.x}, {S.y}`' + (f'，`y = 0` 结束，最大公约数 =={S.x}==' if S.y == 0 else '')),
        'if x == 1': lambda S, B, r: (f'`gcd = 1`：互质，不用合并' if S.x == 1 else f'`gcd = {S.x}` > 1：非互质，需要合并'),
        'res.append(last)': '互质：把 `last = {last}` 放回栈，结束合并',
        'break': '停止，下一步把 `num` 压入栈',
        'num *= last // x': '`lcm = num × last ÷ gcd`：`num` 变为 =={num}==，再和新的栈顶比',
        'res.append(num)': '`{num}` 入栈 → `{res}`',
        'return res': '栈里相邻两数都互质，就是答案 `{res}`',
    },
    cards=dict(
        one_liner='每个数只进出栈一次：新数不断吃掉不互质的栈顶',
        complexity='时间 `O(n log C)`，空间 `O(n)`',
        problem=['相邻两数 `gcd > 1` 就删掉它们，换成 `lcm`，直到没有为止',
                 '返回最终数组',
                 '示例：`[6,4,3,2,7,6,2]` → `[12,7,6]`'],
        quote='可以利用这一点，每次将当前已知的两个不互质的数合并起来就好了。一趟遍历，若num与之前储存的相邻的数不互质，那么就将这个相邻的数删去，同时将num更新为二者的最小公倍数。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目说合并顺序不影响结果（作者没去证明，直接利用）',
              '从左到右，已合并的数放进栈，最近的在栈顶：后进先出',
              '新数和栈顶比：不互质就弹出合并，互质就放回并入栈'],
        summary=['时间 `O(n log C)`：每个数至多进出栈一次，gcd 用辗转相除',
                 '易错：互质时要把弹出的 `last` 放回去，再 `break`',
                 '最小公倍数 `lcm = num × last // gcd`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神用 `math.gcd/lcm`，这里手写辗转相除'],
    ),
)
