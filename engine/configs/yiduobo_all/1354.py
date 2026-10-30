CONFIG = dict(
    num=1354, title='多次求和构造目标数组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='倒推 + 堆 + 取余加速',
    tags=['灵神题单', '难度分 2015'],
    code='''
class Solution(object):
    def isPossible(self, target):

        if len(target) == 1:
            return target[0] == 1

        heap = [-x for x in target]
        s = sum(target)
        n = len(target)
        heapq.heapify(heap)

        while s != n:
            ma = -heapq.heappop(heap)
            rest = s - ma
            if ma <= rest:
                return False

            if ma % rest == 0:
                tmp = rest
            else:
                tmp = ma % rest

            s = rest + tmp
            heapq.heappush(heap, - tmp)

        return True
''',
    call='Solution().isPossible([9,3,5])',
    expect=True,
    views=[
        dict(type='heap', var='heap', fmt=lambda x: str(-x), label='heap（存相反数，这里显示原值，堆顶 = 最大值）', h=200),
        dict(type='text', fn=lambda S: (f"和 `s` = ==`{S['s']}`==，全 1 时和应为 `n` = ==`{S['n']}`==" if 's' in S and 'n' in S else ''), h=90),
        dict(type='text', fn=lambda S: (f"最大值 `{S['ma']}`，其余和 `{S['rest']}`：`{S['ma']} − {S['rest']}×k` 要落到 `1..{S['rest']}`" if S.get('ma') and S.get('rest') and S['_line'] >= 15 else ''), h=90),
    ],
    watch=[('s', 's', 'yellow'), ('n', 'n', 'blue'), ('ma', 'ma', 'pink'), ('rest', 'rest', 'cyan'), ('tmp', 'tmp', 'green')],
    captions={
        'len(target) == 1': lambda S, B, r: ('只有一个数：只有它本来就是 1 才行（不能靠求和构造）' if len(S.target) == 1 else '至少两个数，才能谈「倒推」'),
        'heap = [-x for x in target]': 'Python 只有小根堆 → ==存相反数==当大根堆用，堆顶就是最大值',
        's = sum(target)': '`s` = 当前数组之和 = =={s}==，之后每轮只增量维护',
        'n = len(target)': '全是 1 的数组之和恰好是 `n = {n}`，所以 `s == n` 就是倒推成功',
        'heapq.heapify(heap)': '建堆',
        'while s != n': lambda S, B, r: (f'和 `s = {S.s}` ≠ `n = {S.n}` → 还没倒推回全 1' if S.s != S.n else f'和 `s = {S.s}` = `n`：全是 1 → 结束'),
        'ma = -heapq.heappop(heap)': '弹出最大值 `ma = {ma}`：它是==最后一次求和的结果==',
        'rest = s - ma': '其余数之和 `rest = {s} − {ma} = {rest}`；操作前这位置 = `ma − rest`',
        'if ma <= rest': lambda S, B, r: (f'`ma = {S.ma} ≤ rest = {S.rest}`：减完不是正数 → 构造不出，返回 False' if S.ma <= S.rest
                                          else f'`ma = {S.ma} > rest = {S.rest}`：减完仍为正数，可以继续倒推'),
        'if ma % rest == 0': lambda S, B, r: (f'`{S.ma} % {S.rest} = {S.ma % S.rest}`：整除，减到最后是 `rest` 本身（不能减成 0）' if S.ma % S.rest == 0
                                              else f'`{S.ma} % {S.rest} = {S.ma % S.rest}`：一直减 `rest` 最后剩余数'),
        'tmp = rest': '倒推后该位置 `tmp = {tmp}`',
        'tmp = ma % rest': '直接取余代替==连续多次减法==：`tmp = {ma} % {rest} = {tmp}`',
        's = rest + tmp': '新的和 `s = {rest} + {tmp} = {s}`',
        'heapq.heappush(heap, - tmp)': '把 `{tmp}` 放回堆（存 `-{tmp}`）',
        'return True': '`s == n`：倒推回全 1 → `True`',
        'return False': '无法倒推 → `False`',
    },
    cards=dict(
        one_liner='数组全是正数，最大数必然是最后一次的求和结果',
        complexity='时间 `O(n + log S · log n)`，空间 `O(n)`',
        problem=['初始数组全为 1；每次令 `x` = 全部元素之和，把任一位置改成 `x`',
                 '问能否得到 `target`',
                 '示例：`[9,3,5]` → `true`；`[1,1,1,2]` → `false`'],
        quote='由于数组的初始值都是1，也就是说数组中的所有数必然都是正数，那么在一次求和执行后，这里的和s必然大于数组中的其他数。根据这一点，我们可以从target开始倒推。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 `f` 由 `g` 构造，`f[k]` 最大：`g` 的和 = `f[k]`，所以 `g[k] = f[k] − 其余数之和`',
              '三处优化：==堆==找最大值、==变量 s== 增量维护和、==取余==代替连续相减',
              '`g[k] ≤ 0` 就返回 False；倒推到全 1（`s == n`）就返回 True'],
        summary=['时间 `O(n + log S · log n)`，空间 `O(n)`',
                 '先判 `len(target) == 1`：单个数只有等于 1 才合法',
                 '取余为 0 时要取 `rest` 而不是 0（不能减成 0）',
                 '`ma <= rest` 说明减完不是正数 → False',
                 '对比灵神：灵神用 `(x−1) % s + 1` 一步统一两种情况，yiduobo 分情况写'],
    ),
)
