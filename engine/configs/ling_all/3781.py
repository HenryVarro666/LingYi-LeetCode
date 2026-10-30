NUMS = [2, 1, 5, 4, 3]
SS = '01010'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'x' not in S or 'h' not in S:
        return
    n = len(NUMS)
    cur = NUMS.index(S['x'])
    inh = set(S['h'])
    cell = min(100, (x1 - x0 - 80) / n)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    ys = y0 + 56
    ch = cell * 0.9
    cv.text((x0 + 18, y0 + 4), '从右往左扫（绿 = 当前被箭头选中，灰 = 已被舍弃，青框 = 正在处理）', 21, T['muted'], bold=True)
    for i in range(n):
        X = sx + i * cell
        done = i >= cur
        chosen = done and NUMS[i] in inh
        if chosen:
            fill, fg = T['green'], T['bg']
        elif done:
            fill, fg = (52, 60, 72), T['dim']
        else:
            fill, fg = T['panel2'], T['text']
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['cyan'] if i == cur else T['border'],
                width=5 if i == cur else 1)
        cv.text((X + cell / 2, ys + ch / 2), NUMS[i], 36, fg, anchor='mm', bold=True)
        one = SS[i] == '1'
        cv.rect((X + 14, ys + ch + 12, X + cell - 14, ys + ch + 12 + cell * 0.5), fill=T['blue'] if one else T['panel2'], r=8)
        cv.text((X + cell / 2, ys + ch + 12 + cell * 0.25), SS[i], 28, T['bg'] if one else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + cell * 0.5 + 24), i, 18, T['dim'], anchor='mt', mono=True)
    cv.text((sx - 8, ys + ch + 12 + cell * 0.25), 's', 22, T['muted'], anchor='rm', bold=True, mono=True)


CONFIG = dict(
    num=3781, title='二进制交换后的最大分数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='从右到左 · 最小堆维护前 k 大',
    tags=['堆（优先队列）', '难度分 1823'],
    code='''
class Solution:
    def maximumScore(self, nums: List[int], s: str) -> int:
        h = []
        for x, ch in zip(reversed(nums), reversed(s)):
            heappush(h, x)
            if ch == '0':
                heappop(h)  # 更快的写法见【Python3 写法二】
        return sum(h)
''',
    call="Solution().maximumScore([2,1,5,4,3], '01010')",
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=270),
        dict(type='heap', var='h', label='h（最小堆）= 目前被箭头选中的数', h=120),
        dict(type='text', fn=lambda S: f"堆里 `{len(S['h'])}` 个数 = 已遇到的 `1` 的个数 ，和 = =={sum(S['h'])}==" if 'h' in S and 'x' in S else '', h=60),
    ],
    watch=[('x', 'x', 'blue'), ('ch', 'ch', 'pink'), ('堆大小', lambda S: len(S['h']), 'green')],
    captions={
        'h = []': '堆 `h` 保存目前被箭头选中的数；==堆顶是其中最小的==',
        'for x, ch in zip': lambda S, B, r: ('全部扫完，循环结束' if B.get('x') == S['x'] else
                                              f"倒着看第 `{NUMS.index(S['x'])}` 个：`x = {S['x']}`，`s` 里是 `{S['ch']}`"),
        'heappush(h, x)': '先把 `{x}` 放进堆：假设有箭头能选它，==堆里选的是前 k 大==',
        "if ch == '0'": lambda S, B, r: ("`ch` 是 `1`：多了一根箭头，要多选一个数 → 堆里留着 `{}`，不弹".format(S['x']) if S['ch'] == '1'
                                         else "`ch` 是 `0`：没有新箭头，数太多了 → 要舍弃最小的那个"),
        'heappop(h)': '弹出堆顶（最小值）：箭头只能向左走，保留较大的 → 堆里始终是前 k 大',
        'return sum(h)': '堆里剩下的就是每根箭头选中的数：和 = =={ret}==',
    },
    cards=dict(
        one_liner='倒着扫：遇到 1 多一根箭头，遇到 0 就扔掉堆里最小的',
        complexity='时间 `O(n log k)`，空间 `O(k)`，k 为 `1` 的个数',
        problem=['`s[i]=1` 的下标，分数加上 `nums[i]`；每次可把 `s` 中相邻的 `01` 换成 `10`',
                 '换任意多次，求最大可能分数',
                 '示例：`nums=[2,1,5,4,3]`，`s="01010"` → ==7=='],
        quote='由于箭头只能左移，无法右移，所以最右边的箭头右侧的数无法选择。……倒着遍历的过程中，维护前 k 大元素，其中 k 是遍历过的 s[i]=1 的个数。',
        quote_src='—— 灵茶山艾府题解（方法二：从右到左）',
        idea=['把每个 `1` 看成一根只能左移的箭头，它能选自己及左边的数',
              '倒着扫：能选到当前数的箭头数 = 右边 `1` 的个数 k（含当前）',
              '先入堆，若 `s[i]` 是 `0` 就弹出最小：堆始终是前 k 大，最后求和'],
        summary=['时间 `O(n log k)`，空间 `O(k)`',
                 '`1` 只多一根箭头，不弹；`0` 才弹最小的',
                 '灵神方法一是从左到右 + 最大堆：每遇到 `1` 就弹出最大的数',
                 '`heappushpop` 比「先 push 再 pop」更快（写法二）'],
    ),
)
