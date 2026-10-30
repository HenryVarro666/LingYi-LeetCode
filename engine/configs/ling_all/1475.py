CONFIG = dict(
    num=1475, title='商品折扣后的最终价格', difficulty='Easy', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 从左到右 todolist',
    tags=['单调栈', '基础', '难度分 1263'],
    code='''
class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        st = []  # todolist
        for i, p in enumerate(prices):
            while st and prices[st[-1]] >= p:
                prices[st.pop()] -= p  # p 是栈顶的折扣值
            st.append(i)
        return prices
''',
    call='Solution().finalPrices([8,4,6,2,3])',
    expect=[4, 2, 4, 2, 3],
    views=[
        dict(type='array', var='prices', label='prices（原地改成折扣后的价格；绿 = 已出结果）', cell=96, h=250,
             pointers={'i': 'blue'},
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else ('green' if 'st' in S and 'i' in S and i < S['i'] and i not in S['st'] else None)),
        dict(type='stack', var='st', label='st（todolist：还没找到折扣的商品下标）', fmt=lambda i: f"{i}", h=250),
        dict(type='text', fn=lambda S: (f"当前价格 p = =={S['p']}== 是折扣候选；栈里待办 {list(S['st'])}" if 'p' in S and 'st' in S else ''), size=26),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p', 'pink'), 'st'],
    captions={
        'st = []': '`st` 是 todolist：存==还不知道折扣==的商品下标',
        'for i, p in enumerate': '看第 `{i}` 个价格 `p = {p}`：它可能是栈里某些商品的折扣',
        'while st and prices[st[-1]] >= p': lambda S, B, r: (
            f'`prices[{S.st[-1]}] = {S.prices[S.st[-1]]} >= {S.p}` → 成立：==p 就是它右边第一个 ≤ 它的数==，结算它'
            if S.st and S.prices[S.st[-1]] >= S.p else
            ('栈空了，没有待办要结算' if not S.st else f'`prices[{S.st[-1]}] = {S.prices[S.st[-1]]} < {S.p}` → 不成立：p 不能当它的折扣，停止弹栈')),
        'prices[st.pop()] -= p': '弹出下标 `{B.st[-1]}`：价格 `{B.prices[B.st[-1]]}` 减去折扣 `{p}` → =={prices[B.st[-1]]}==',
        'st.append(i)': '`i = {i}` 入栈：它的折扣要等后面更小或相等的价格来决定',
        'return prices': '栈里剩下的没有折扣，`prices` 已是最终价格：`{prices}`',
    },
    cards=dict(
        one_liner='栈是 todolist：遇到更小的价格就结算栈顶',
        complexity='时间 `O(n)`，空间 `O(min(n, U))`',
        problem=['`prices[i]` 买第 `i` 件可减去右边第一个 `<= prices[i]` 的价格',
                 '没有这样的价格就不打折，返回最终价格数组',
                 '示例：`[8,4,6,2,3]` → `[4,2,4,2,3]`'],
        quote='栈相当于是一个 todolist，在循环的过程中，现在还不知道答案是多少，在后面的循环中会算出答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右扫，栈里放==还没算出折扣==的下标',
              '当前 `p <= 栈顶价格`：p 就是栈顶的折扣，弹出并结算',
              '结算完把 `i` 入栈，等后面的数来决定它的折扣'],
        summary=['时间 `O(n)`：每个元素最多入栈出栈各一次，双重循环不是 `O(n^2)`',
                 '比较用 `>=`：折扣条件是 `<=`，相等也算',
                 '灵神另一种写法：从右到左，栈里记录折扣值，用哨兵 0 表示无折扣',
                 '这里在原数组上改，写法二栈中没有重复元素'],
    ),
)
