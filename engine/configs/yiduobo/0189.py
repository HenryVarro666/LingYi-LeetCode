import math

NUMS, K = [1, 2, 3, 4, 5, 6], 2
N = len(NUMS)


def _order():
    """按 yiduobo 的走法预先列出每次替换的 (from, to)，只用于画图"""
    out, cnt = [], 0
    for s in range(N):
        p = s
        while True:
            q = (p + K) % N
            out.append((p, q))
            p = q
            cnt += 1
            if q == s:
                break
        if cnt == N:
            return out
    return out


ORDER = _order()


def _placed(S):
    return {q for _, q in ORDER[:S.get('cnt', 0) or 0]}


def _ring(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'位置 i 的数要去 (i + k) % n：箭头连成 {math.gcd(N, K)} 个环（绿 = 已归位）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2 - 80, (y0 + y1) / 2 + 22
    R = min(x1 - x0, y1 - y0 - 60) / 2 - 62
    pos = {p: (cx + R * math.sin(2 * math.pi * p / N), cy - R * math.cos(2 * math.pi * p / N)) for p in range(N)}
    cnt = S.get('cnt', 0) or 0
    nums = S.get('nums') or NUMS
    nxt = ORDER[cnt] if cnt < len(ORDER) and 'next_pos' in S and S['next_pos'] == ORDER[cnt][1] else None
    rad = 38
    for e, (p, q) in enumerate(ORDER):
        (ax, ay), (bx, by) = pos[p], pos[q]
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        c = T['green'] if e < cnt else (T['pink'] if (p, q) == nxt else T['border'])
        cv.arrow((ax + ux * rad, ay + uy * rad), (bx - ux * (rad + 4), by - uy * (rad + 4)), c, 5 if c != T['border'] else 3, 16)
    placed = _placed(S)
    start = S.get('index')
    for p, (px, py) in pos.items():
        fill = T['green'] if p in placed else T['panel2']
        outline = T['yellow'] if p == start and 'last_pos' in S else T['border']
        cv.d.ellipse((px - rad, py - rad, px + rad, py + rad), fill=fill, outline=outline, width=5 if outline == T['yellow'] else 2)
        cv.text((px, py), str(nums[p]), 30, T['bg'] if p in placed else T['text'], anchor='mm', bold=True)
        ox, oy = (px - cx) / R, (py - cy) / R
        cv.text((px + ox * (rad + 22), py + oy * (rad + 22)), f'{p}', 20, T['muted'], anchor='mm', mono=True)
    if 'last_num' in S:
        hx = x1 - 170
        cv.rect((hx - 120, cy - 60, hx + 120, cy + 60), fill=T['panel2'], r=14)
        cv.text((hx, cy - 26), '手上拿着', 22, T['muted'], anchor='mm')
        cv.text((hx, cy + 16), f'last_num = {S["last_num"]}', 30, T['orange'], anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num=189, title='轮转数组', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='环形替换',
    code='''
class Solution(object):
    def rotate(self, nums, k):
        if not nums:
            return []

        k %= len(nums)

        cnt = 0
        for index in range(len(nums)):
            last_pos, last_num = index, nums[index]
            while True:
                next_pos = (last_pos + k) % len(nums)
                last_num, nums[next_pos] = nums[next_pos], last_num
                last_pos = next_pos
                cnt += 1
                if next_pos == index:
                    break
            if cnt == len(nums):
                return
''',
    call=f'nums = {NUMS}\nSolution().rotate(nums, {K})\nnums',
    expect=[5, 6, 1, 2, 3, 4],
    views=[
        dict(type='array', var='nums', pointers={'index': 'yellow', 'last_pos': 'blue', 'next_pos': 'pink'},
             color=lambda S, i, v: 'green' if i in _placed(S) else None, cell=90, h=262),
        dict(type='custom', draw=_ring, h=370),
    ],
    skip=['while True'],
    watch=[('k', 'k'), ('index', 'index', 'yellow'), ('last_pos', 'last_pos', 'blue'), ('next_pos', 'next_pos', 'pink'),
           ('last_num', 'last_num', 'orange'), ('cnt', 'cnt', 'green')],
    captions={
        'if not nums': '`nums` 非空，继续',
        'k %= len(nums)': '`k %= n` → `k = {k}`',
        'cnt = 0': '`cnt` 统计已经换过的数：到 `n` 个就说明交换完成',
        'for index in range': lambda S, B, ret: (f'从位置 `{S.index}` 开始一轮环形替换' if 'index' not in B or S.index != B.index
                                                 else '所有起点都试过了'),
        'last_pos, last_num = index': '拿起 `nums[{index}] = {last_num}`，它要往后挪 `k = {k}` 格',
        'next_pos = (last_pos + k)': '位置 `{last_pos}` 的数该去 `next_pos = ({last_pos} + {k}) % {len(nums)} = {next_pos}`',
        'last_num, nums[next_pos]': lambda S, B, ret: (
            f'手上的 `{B.last_num}` 放进起点 `nums[{S.next_pos}]`；换出的 `{S.last_num}` 早已归位，不用管了'
            if S.next_pos == S.index else
            f'手上的 `{B.last_num}` 放进 `nums[{S.next_pos}]`，换出原来的 `{S.last_num}` 拿在手上'),
        'last_pos = next_pos': '走到位置 `{last_pos}`，接着处理手上的 `{last_num}`',
        'cnt += 1': '已换过 `cnt = {cnt}` 个数',
        'if next_pos == index': lambda S, B, ret: (f'`next_pos = {S.next_pos}` 回到起点 `{S.index}`：==这一圈闭合了=='
                                                   if S.next_pos == S.index else
                                                   f'`next_pos = {S.next_pos}` ≠ 起点 `{S.index}`，沿着环继续走'),
        'break': '跳出 `while`，这一圈结束',
        'if cnt == len(nums)': lambda S, B, ret: ('`cnt = n`：==所有数都换过了==，交换完成' if S.cnt == len(S.nums) else
                                                  f'只换了 `{S.cnt}` 个 < `{len(S.nums)}`：还有别的环，从 `{S.index + 1}` 开始（它一定没被换过）'),
        'return': '提前结束',
    },
    cards=dict(
        one_liner='每个数直接跳到 (i + k) % n：沿着环一路替换，一圈不够就从下一个位置再开一圈',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组元素==向右轮转 k 个位置==（原地修改）',
                 '示例：`nums = [1,2,3,4,5,6,7], k = 3` → `[5,6,7,1,2,3,4]`',
                 '演示用 `nums = [1,2,3,4,5,6], k = 2` → `[5,6,1,2,3,4]`（会出现两个环）'],
        quote='对于当前的数a[pos]，其下一个位置为next_pos = (pos + k)% n。将a[pos]移动到a[next_pos]后再计算next_pos的下一个位置，往复计算直到走回到pos为止。',
        quote_src='—— yiduobo 题解「方法二：环形替换」',
        idea=['拿起一个数放到目标位，被挤出来的数接着往后放 → 一路走成一个==环==',
              '走回起点：一圈闭合；换过的数达到 `n` 个就完成',
              '否则从 `pos + 1` 再开一圈：它==一定没被换过==（能走到 pos + 1 就能走遍整个数组）'],
        result='全部归位：`nums = [5,6,1,2,3,4]`（原地修改，没有返回值）',
        summary=['每个数只移动一次：时间 `O(n)`，空间 `O(1)`',
                 '`cnt` 计数决定何时停：不能只靠「走回起点」，否则会把一个环转好几遍',
                 '补充：环的个数是 `gcd(n, k)`，本例 `gcd(6, 2) = 2`',
                 '原文还提到「三次 reverse」做法（与灵神相同），代码给的是环形替换',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
