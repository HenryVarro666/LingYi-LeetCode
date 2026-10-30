CONFIG = dict(
    num=1354, title='多次求和构造目标数组', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='逆向思维 + 最大堆 + 取模',
    tags=['贪心与思维', '难度分 2015'],
    code='''
class Solution:
    def isPossible(self, target: List[int]) -> bool:
        s = sum(target)
        h = target
        heapify_max(h)

        # 如果最大值等于 1，说明所有数都等于 1
        while h[0] > 1:
            x = h[0]
            s -= x  # 减去 x 后，s 为其余元素之和

            # s 不能是 0，这意味着 target 只有一个数且这个数大于 1
            # x 减去 s 后必须是正数
            if s == 0 or x <= s:
                return False

            # 把 x 多次减去 s，直到 x <= s 为止
            # 也就是计算 x%s，但如果 x%s == 0 则调整为 s
            x = (x - 1) % s + 1
            s += x
            heapreplace_max(h, x)

        return True
''',
    # Python 3.14 才自带 heapify_max / heapreplace_max；这里用 heapq 内部函数补上（不被追踪）
    setup='''
heapify_max = heapq._heapify_max

def heapreplace_max(heap, item):
    heap[0] = item
    heapq._siftup_max(heap, 0)
''',
    call='Solution().isPossible([3,5,25])',
    expect=True,
    views=[
        dict(type='heap', var='h', fmt=lambda x: str(x), label='h（最大堆，堆顶 = 当前最大值）', h=200),
        dict(type='text', fn=lambda S: ('' if 's' not in S else f"`s` = 其余元素之和 = =={S['s']}==，最大值 `x` = =={S['x']}==" if 'x' in S and S['_line'] in (10, 14, 19) else f"`s` = 当前元素和 = =={S['s']}=="), h=90),
        dict(type='text', fn=lambda S: (f"一直减 `{S['s']}`：`{S['x']}` → ... → `{(S['x'] - 1) % S['s'] + 1}`，等价于 `({S['x']} − 1) % {S['s']} + 1`" if S.get('s') and S.get('x') and S['x'] > S['s'] else ''), h=90),
    ],
    watch=[('s', 's', 'yellow'), ('x', 'x', 'pink'), ('最大值', 'h[0]', 'blue')],
    captions={
        's = sum(target)': '`s` = 全部元素之和 = =={s}==。==逆向==：最后一步写入的就是当前最大值',
        'h = target': '`h` 直接用 `target` 原地堆化，省空间',
        'heapify_max(h)': '建最大堆：堆顶 = ==最大值== `{h[0]}`',
        'while h[0] > 1': lambda S, B, r: (f'堆顶 `{S.h[0]}` > 1 → 还没倒推回全 1，继续' if S.h[0] > 1 else '堆顶 = 1，说明所有数都是 1 → 倒推成功'),
        'x = h[0]': '最大值 `x = {x}`：它是最后一次操作写入的 → 操作前所有元素和就是 `{x}`',
        's -= x': '`s -= x` → `s = {s}` 是==其余元素之和==',
        'if s == 0 or x <= s': lambda S, B, r: (f'`s = {S.s}`，`x = {S.x}`：x 要先减去 s 才是操作前的值，必须为正，这里 `x <= s` → 不可能，返回 False' if (S.s == 0 or S.x <= S.s)
                                              else f'`x = {S.x} > s = {S.s}` → 操作前这位置的值 `{S.x} − {S.s}` 是正数，合法'),
        'x = (x - 1) % s + 1': '一次性减去很多个 `{s}`：`x = ({B.x} − 1) % {s} + 1` = =={x}==（不能减成 0）',
        's += x': '`s += x` → 新的元素和 `{s}`',
        'heapreplace_max(h, x)': '把堆顶换成 `{x}`，重新堆化 → 新最大值 `{h[0]}`',
        'return True': '倒推回全 1，可以构造 → `True`',
        'return False': '无法倒推 → `False`',
    },
    cards=dict(
        one_liner='倒着想：每次的最大值就是上一步的元素和',
        complexity='时间 `O(n + log S · log n)`，空间 `O(1)`（原地堆化）',
        problem=['一开始 `A` 全是 1；每次操作令 `x` = 全部元素之和，把某个位置改成 `x`',
                 '问能否从 `A` 得到 `target`',
                 '示例：`[9,3,5]` → `true`；`[1,1,1,2]` → `false`',
                 '本视频：`[3,5,25]` → `true`'],
        quote='由于每次操作得到的元素和会越来越大，所以 target 的最大值就是最后一步操作的元素和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['倒推：最大值 `x` = 操作前的元素和，所以操作前这位置 = `x − 其余和 s`',
              '最大堆取最大值，变量 `s` 维护元素和，不用每次重新求和',
              '`x` 比 `s` 大很多时会连续减 `s`：==等价于取模==，写成 `(x−1) % s + 1` 保证结果在 `1..s`'],
        summary=['时间 `O(n + log S · log n)`，两轮循环元素和至少减半',
                 '易错点：==`s == 0`== 表示只有一个数且大于 1，直接 False',
                 '易错点：取模结果为 0 要改成 `s`，所以用 `(x-1) % s + 1`',
                 '`x <= s` 时减完不是正数，也是 False',
                 'Python 3.14 才有 `heapify_max`；视频里用 `heapq` 内部函数补了等价实现'],
    ),
)
