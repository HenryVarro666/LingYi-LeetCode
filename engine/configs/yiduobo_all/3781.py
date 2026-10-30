NUMS = [2, 1, 5, 4, 3]
SS = '01010'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'v' not in S or 'heap' not in S:
        return
    n = len(NUMS)
    cur = NUMS.index(S['v'])
    inh = set(-t for t in S['heap'])
    cell = min(100, (x1 - x0 - 80) / n)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    ys = y0 + 56
    ch = cell * 0.9
    cv.text((x0 + 18, y0 + 4), '从左往右扫（橙 = 还在堆里的候选数，青框 = 正在处理，无色 = 已被取走或未扫到）', 21, T['muted'], bold=True)
    for i in range(n):
        X = sx + i * cell
        seen = i <= cur
        fill, fg = T['panel2'], T['text']
        if seen and NUMS[i] in inh:
            fill, fg = T['orange'], T['bg']          # 还在堆里等着被取
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['cyan'] if i == cur else T['border'],
                width=5 if i == cur else 1)
        cv.text((X + cell / 2, ys + ch / 2), NUMS[i], 36, fg, anchor='mm', bold=True)
        one = SS[i] == '1'
        cv.rect((X + 14, ys + ch + 12, X + cell - 14, ys + ch + 12 + cell * 0.5), fill=T['blue'] if one else T['panel2'], r=8)
        cv.text((X + cell / 2, ys + ch + 12 + cell * 0.25), SS[i], 28, T['bg'] if one else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + cell * 0.5 + 24), i, 18, T['dim'], anchor='mt', mono=True)
    cv.text((sx - 8, ys + ch + 12 + cell * 0.25), 'g', 22, T['muted'], anchor='rm', bold=True, mono=True)


CONFIG = dict(
    num=3781, title='二进制交换后的最大分数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='每个 1 取左侧最大 · 大顶堆',
    tags=['堆（优先队列）', '难度分 1823'],
    code='''
class Solution(object):
    def maximumScore(self, nums, s):
        
        heap = []
        res = 0
        for v, g in zip(nums, s):
            heapq.heappush(heap, -v)
            if g == '1':
                res -= heapq.heappop(heap)
        return res
''',
    call="Solution().maximumScore([2,1,5,4,3], '01010')",
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=270),
        dict(type='heap', var='heap', fmt=lambda x: str(-x), label='heap（存相反数；格内 = 真实数值，堆顶 = 最大）', h=120),
        dict(type='text', fn=lambda S: f"已取走的分数 `res` = =={S['res']}==；堆里候选 `{len(S['heap'])}` 个" if 'res' in S and 'heap' in S and 'v' in S else '', h=60),
    ],
    watch=[('v', 'v', 'blue'), ('g', 'g', 'pink'), ('res', 'res', 'green')],
    captions={
        'heap = []': '堆里放「可以被 1 取走的候选数」，用 ==大顶堆==（存相反数）',
        'res = 0': '`res` 累计分数',
        'for v, g in zip': lambda S, B, r: ('扫完了，循环结束' if B.get('v') == S['v'] else
                                            f"第 `{NUMS.index(S['v'])}` 位：`v = {S['v']}`，`g = {S['g']}`"),
        'heapq.heappush': '不管 `g` 是什么，先把 `{v}` 入堆（存 `{-v}`）：它可以被自己或右边的 1 取走',
        "if g == '1'": lambda S, B, r: ("`g` 是 `1`：这个 1 可以和左边任意一个 0 交换 → ==取堆里最大的==" if S['g'] == '1'
                                         else "`g` 是 `0`：它自己没有分数，数留在堆里等后面的 1"),
        'heappop': '弹出堆顶（最大值 `{-B.heap[0]}`），`res` += ==`{-B.heap[0]}`==，得 `{res}`' ,
        'return res': '最大可能分数 = =={ret}==',
    },
    cards=dict(
        one_liner='每个 1 都能换到左边任意一个 0：取左边最大的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`s[i]=1` 的下标，分数加上 `nums[i]`；可把 `s` 里相邻的 `01` 交换成 `10`',
                 '操作次数不限，求最大可能分数',
                 '示例：`nums=[2,1,5,4,3]`，`s="01010"` → ==7=='],
        quote='对于每个\'1\'，其可以与左侧任意一个\'0\'进行交换。为了使得最终得分最大，那么对于每个\'1\'，其最佳的交换位置就是左侧所有的\'0\'中，对应元素最大的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`01` 可以换成 `10` → 每个 1 能不断左移，==相当于能取左边任意位置的数==',
              '一趟遍历，用大顶堆装「左侧还没被取走」的数',
              '遇到 1：先把自己入堆，再弹出堆顶（最大）加到答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`heapq` 只有最小堆，所以入堆存 `-v`，弹出时 `res -= ...`',
                 '遇到 1 也要先入堆再弹：它自己也是候选',
                 '灵神方法二倒着扫 + 最小堆，只保留前 k 大，空间 `O(k)`'],
    ),
)
