HENS, GRAINS = [3, 6, 7], [2, 4, 7, 9]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴（橙 = 母鸡，黄点 = 还没分配的谷子，绿点 = 已分配）', 22, T['muted'], bold=True)
    lo, hi = 0, 10
    sx, ex = x0 + 60, x1 - 60
    cell = (ex - sx) / (hi - lo)
    ay = y0 + 250
    X = lambda v: sx + (v - lo) * cell
    cv.line([(sx - 20, ay), (ex + 20, ay)], T['border'], 3)
    for v in range(lo, hi + 1):
        cv.line([(X(v), ay - 6), (X(v), ay + 6)], T['border'], 2)
        cv.text((X(v), ay + 14), v, 18, T['dim'], anchor='mt', mono=True)
    grains = S['grains']
    hens = S['hens']
    p = S.get('p', 0) if 'mid' in S else 0
    cur = S.get('h') if 'mid' in S else None
    # 当前母鸡覆盖的范围
    if cur is not None and 'forward' in S:
        a, b = cur - S['forward'], cur + S['backward']
        cv.rect((X(a), ay - 120, X(b), ay - 8), fill=T['orange'], alpha=40, r=8)
        cv.text(((X(a) + X(b)) / 2, ay - 150), f"最远：前 {S['forward']} / 后 {S['backward']}", 22, T['orange'], anchor='mm', bold=True)
    for i, g in enumerate(grains):
        done = i < p
        c = T['green'] if done else T['yellow']
        cv.rect((X(g) - 17, ay - 74, X(g) + 17, ay - 40), fill=c, r=17)
        cv.text((X(g), ay - 57), i, 20, T['bg'], anchor='mm', bold=True)
    for h in hens:
        on = h == cur
        cv.tri_up(X(h), ay + 70, 18, T['orange'] if on else T['muted'])
        cv.text((X(h), ay + 96), '鸡', 24, T['orange'] if on else T['muted'], anchor='mt', bold=True)
    if 'mid' in S:
        cv.text((x1 - 18, y0 + 4), f"mid = {S['mid']}", 26, T['yellow'], anchor='ra', bold=True)
        cv.text((x0 + 18, y1 - 50), f"已分配前 p = {p} 颗谷子，共 {len(grains)} 颗", 26, T['green'], anchor='la', bold=True)


def _cost(S):
    f, b = S['forward'], S['backward']
    return f"先前后：`{f}×2 + {b}` = {2*f+b}；先后前：`{b}×2 + {f}` = {2*b+f}"


CONFIG = dict(
    num=2604, title='吃掉所有谷子的最短时间', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 + 贪心分配',
    tags=['二分算法'],
    code='''
class Solution(object):
    def minimumTime(self, hens, grains):

        hens.sort()
        grains.sort()

        left = 0
        right = abs(hens[0] - grains[0]) + grains[-1] - grains[0]

        while left < right:
            mid = (left + right) >> 1
            p = 0
            for h in hens:
                backward = forward = 0
                while p < len(grains):
                    if grains[p] < h:
                        forward = max(forward, h - grains[p])
                    elif grains[p] > h:
                        backward = max(backward, grains[p] - h)
                    
                    if forward + forward + backward <= mid or backward + backward + forward <= mid:
                        p += 1
                    else:
                        break
                
                if p == len(grains):
                    break
            
            if p == len(grains):
                right = mid
            else:
                left = mid + 1

        return left
''',
    call=f'Solution().minimumTime({HENS}, {GRAINS})',
    expect=2,
    skip=['hens.sort', 'grains.sort', 'backward = forward = 0', 'elif grains[p] > h'],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=70, size=30,
             fn=lambda S: (f"二分区间 `[{S['left']}, {S['right']}]`" if 'left' in S else '') +
             ((' ｜ ' + _cost(S)) if 'forward' in S and 'mid' in S and S.get('_line') in (14, 15, 17, 18) else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('p', 'p', 'green'),
           ('forward', 'forward', 'cyan'), ('backward', 'backward', 'orange')],
    captions={
        'left = 0': '下界 0：最少用 0 秒',
        'right = abs': '上界：最靠左的鸡先走到最左谷子，再一路吃到最右 `right = {right}`，一定够',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`：继续二分' if B.left < B.right
                                               else f'`left = right = {B.left}`：最短时间找到了'),
        'mid = (left + right)': '时间越长越容易吃完 → 能二分。试 `mid = {mid}`：能否在 {mid} 秒内吃光？',
        'p = 0': '`p` = 下一颗没分配的谷子，从最左边开始',
        'for h in hens': '轮到位置 `{h}` 的母鸡：从谷子 `{p}` 起尽量多分给它',
        'while p < len(grains)': lambda S, B, r: (f'还有谷子 `{B.p}` 没分配，试着交给这只鸡' if B.p < len(B.grains) else '谷子全部分配完了'),
        'if grains[p] < h': lambda S, B, r: (f'谷子 `{B.grains[B.p]}` 在鸡 `{B.h}` 前方（左边）' if B.grains[B.p] < B.h
                                             else (f'谷子 `{B.grains[B.p]}` 在鸡 `{B.h}` 后方（右边）' if B.grains[B.p] > B.h
                                                   else f'谷子 `{B.grains[B.p]}` 就在鸡脚下，不用多走')),
        'forward = max': '它前方最远的谷子距离：`forward = {forward}`',
        'backward = max': '它后方最远的谷子距离：`backward = {backward}`',
        'if forward + forward': lambda S, B, r: (
            f'两种走法取小：先前后 `{S.forward}×2+{S.backward}` = {2*S.forward+S.backward}，先后前 `{S.backward}×2+{S.forward}` = {2*S.backward+S.forward}；'
            + (f'有一个 ≤ {S.mid} → ==这颗谷子归它=='
               if min(2*S.forward+S.backward, 2*S.backward+S.forward) <= S.mid else f'都 > {S.mid} → 它吃不下，换下一只鸡')),
        'p += 1': '谷子归当前这只鸡，`p` → {p}，继续看下一颗',
        24: '这只鸡不够了（再加这颗就超时），跳出，换下一只鸡',
        26: lambda S, B, r: ('谷子已经全分完 → 不用再找鸡了' if B.p == len(B.grains) else f'还剩谷子从 `{B.p}` 起没分配 → 下一只鸡接着来'),
        27: '全部分完，提前结束这次判定',
        29: lambda S, B, r: ('全部谷子分完 → `mid` 够用' if B.p == len(B.grains) else '鸡用完了还有谷子 → `mid` 不够'),
        'right = mid': '`mid = {mid}` 秒够用 → 答案 ≤ mid，`right = {right}`',
        'left = mid + 1': '`mid = {mid}` 秒不够（谷子只分到 `p = {p}`）→ `left = {left}`',
        'return left': '最短时间 `{left}` 秒',
    },
    cards=dict(
        one_liner='鸡的路线不重叠：二分时间，从左到右贪心分谷子',
        complexity='时间 `O((n+m) log W)`，空间 `O(1)`',
        problem=['数轴上有若干母鸡和谷子，鸡可以同时、各自向左右走去吃谷子（到达即吃掉）',
                 '求吃光所有谷子的==最短时间==',
                 '本视频：鸡 `[3,6,7]`，谷子 `[2,4,7,9]` → `2`'],
        quote='时间越长，吃掉所有谷子的可能性就越大，因此在这里可以使用二分法，二分吃掉所有谷子的最短时间mid。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序：每只鸡负责一段==连续==的谷子，路线不重叠',
              '一只鸡负责的谷子里，前方最远 `forward`、后方最远 `backward`',
              '耗时 = `min(2×forward + backward, 2×backward + forward)`，不超过 mid 就继续多分一颗'],
        summary=['时间 `O((n+m) log W)`：每次判定每只鸡、每颗谷子各看一遍',
                 '纯向前或纯向后是特例：另一个方向为 0，公式照样成立',
                 '易错：`forward`、`backward` 要在每只新鸡处清零；谷子 `p` 只增不减',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
