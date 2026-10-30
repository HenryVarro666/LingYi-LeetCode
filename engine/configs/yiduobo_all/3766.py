def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pali = S.get('pali') or []
    cv.text((x0 + 18, y0 + 4), f'pali：1 ~ 5000 里的二进制回文数，共 {len(pali)} 个（最后一个 5049 是哨兵）', 24, T['muted'], bold=True)
    n = len(pali)
    if n < 3:
        return
    live = S.get('_line', 0) >= 31 and 'left' in S and 'right' in S
    v = S.get('v')
    L, R = (S['left'], S['right']) if live else (0, n - 1)
    cell = (x1 - x0 - 60) / n
    sx = x0 + 30
    base = y0 + 220
    top = y0 + 90
    for i, p in enumerate(pali):
        X = sx + i * cell
        inside = L <= i <= R
        col = T['blue'] if inside else T['dim']
        if live and 'mid' in S and S['_line'] >= 35 and i == S['mid']:
            col = T['yellow']
        h = (base - top) * (0.45 + 0.55 * (i / n))
        cv.rect((X + 1, base - h, X + max(2, cell - 1), base), fill=col, alpha=230 if inside else 120)
    cv.line([(sx, base), (sx + n * cell, base)], T['border'], 2)
    if isinstance(v, int) and live:
        pos = sum(1 for p in pali if p <= v)
        X = sx + pos * cell
        cv.dashed((X, top - 20), (X, base + 8), T['green'], 3)
        cv.text((X, top - 24), f'v = {v}', 24, T['green'], anchor='mb', bold=True)
    if live:
        marks = [('left', L, T['blue']), ('right', R, T['pink'])]
        if 'mid' in S and S['_line'] >= 35:
            marks.append(('mid', S['mid'], T['yellow']))
        lx = x0 + 30
        for k, (name, idx, c) in enumerate(marks):
            if not (0 <= idx < n):
                continue
            X = sx + idx * cell + cell / 2
            cv.tri_up(X, base + 12 + k * 16, 9, c)
            cv.text((lx, base + 100), f'{name} = {idx}（pali = {pali[idx]}）', 26, c, bold=True)
            lx += 300
        cv.text((x0 + 30, base + 145), '蓝色柱 = 还在二分区间 [left, right] 内；灰色 = 已丢弃；黄色 = mid', 22, T['muted'])
    else:
        cv.text((x0 + 18, base + 30), '预处理：把区间内所有二进制回文数按从小到大收集起来，之后每个查询只做二分', 22, T['muted'])


def _top(S):
    if S.get('_line', 0) < 27 or 'v' not in S:
        return ''
    pali = S.get('pali') or []
    return f"当前 `v` = {S['v']}（二进制 `{S['v']:b}`），在 pali 里找最大的 `pali[p] <= v`"


CONFIG = dict(
    num=3766, title='将数字变成二进制回文数的最少操作', difficulty='Medium', category='位运算',
    author='yiduobo', technique='预处理回文数 + 手写二分',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        pali = []
        for v in range(1, 5001):
            digits = []
            x = v
            while x:
                digits.append(x % 2)
                x //= 2
            
            left, right = 0, len(digits) - 1
            flag = True
            while left < right:
                if digits[left] != digits[right]:
                    flag = False
                    break
                left += 1
                right -= 1
            
            if flag:
                pali.append(v)
        
        pali.append(5049)

        res = []
        for v in nums:
            if v < pali[0]:
                res.append(pali[0] - v)
            else:
                left = 0
                right = len(pali) - 1
                while left < right:
                    mid = (left + right + 1) // 2
                    if pali[mid] <= v:
                        left = mid
                    else:
                        right = mid - 1
                
                res.append(min(v - pali[left], pali[left + 1] - v))
        
        return res
''',
    call='Solution().minOperations([12])',
    expect=[3],
    skip=list(range(5, 23)),
    max_steps=80,
    max_events=400000,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='custom', draw=_draw, h=420),
        dict(type='array', var='res', label='res（每个数的最少操作次数）', cell=100, h=130),
    ],
    watch=[('v', 'v', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('len(pali)', 'len(pali)')],
    captions={
        4: '`pali` 用来收集 1~5000 内所有的二进制回文数',
        24: lambda S, B, r: f'1~5000 都检查完了：共 {len(S.pali) - 0} 个回文数。再补一个哨兵 5049（5000 往上最近的二进制回文数）',
        'res = []': '`res` 保存每个数的答案',
        'for v in nums': lambda S, B, r: (f'处理 `v = {S.v}`' if S.v != B.get('v') or 'v' not in B else 'nums 都处理完了'),
        'if v < pali[0]': lambda S, B, r: ('`v` 比最小的回文数 1 还小，只能一路加上去' if S.v < S.pali[0]
                                           else f'`v = {S.v} ≥ pali[0] = {S.pali[0]}`，走二分'),
        'left = 0': '二分区间 `[0, len(pali) - 1]`：找最大的 `p` 满足 `pali[p] <= v`',
        'right = len': '`right = {right}`，覆盖整个 pali',
        'while left < right': lambda S, B, r: (f'区间 `[{S.left}, {S.right}]` 还有多个候选，继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`：找到了，`pali[{S.left}] = {S.pali[S.left]}`'),
        'mid = ': '取偏右的中点 `mid = ({B.left} + {B.right} + 1) // 2 = {mid}`（偏右，避免 `left = mid` 死循环）',
        'if pali[mid] <= v': lambda S, B, r: (f'`pali[{S.mid}] = {S.pali[S.mid]} <= {S.v}` → 答案在 mid 或右侧' if S.pali[S.mid] <= S.v
                                              else f'`pali[{S.mid}] = {S.pali[S.mid]} > {S.v}` → mid 太大了，答案在左侧'),
        'left = mid': '`left` 移到 `mid`：`left = {left}`（`pali[{left}] = {pali[left]}` 仍然 <= v）',
        'right = mid - 1': '`right = mid - 1 = {right}`，丢掉 mid 及右边',
        'res.append(min': lambda S, B, r: (f'向下取 `pali[{S.left}] = {S.pali[S.left]}`：差 {S.v - S.pali[S.left]}；向上取 `pali[{S.left + 1}] = {S.pali[S.left + 1]}`：差 {S.pali[S.left + 1] - S.v}'
                                           f' → 取较小的 =={min(S.v - S.pali[S.left], S.pali[S.left + 1] - S.v)}=='),
        'return res': '全部算完：`res = {res}`',
    },
    cards=dict(
        one_liner='值域只有 5000：先把所有二进制回文数列出来，再二分找最近的',
        complexity='时间 `O(U log U + n log U)`，空间 `O(U)`，`U = 5000`',
        problem=['每次可把数 `+1` 或 `-1`；二进制（无前导零）正反读一样叫二进制回文数',
                 '求每个 `nums[i]` 变成二进制回文数的最少操作次数',
                 '本视频：`[12]` → `[3]`（12 → 15）'],
        quote='可以先从1枚举到5000，检测其中的所有元素是否为二进制回文数，并将这些数记录下来，得到数组pali。',
        quote_src='—— yiduobo 题解原文',
        idea=['1~5000 里逐个转成二进制数位，双指针从两端往中间比对，记下回文数',
              '5000 往上最近的回文数是 5049（`1001110111001`），补在末尾当哨兵',
              '二分找最大的 `pali[p] <= v`：答案是 `v - pali[p]` 与 `pali[p+1] - v` 的较小者'],
        result='`pali[p] = 9`、`pali[p+1] = 15`，距离 3 与 3 → `res = [3]` ✓',
        summary=['时间 `O(U log U + n log U)`，空间 `O(U)`',
                 '==哨兵 5049 必须有==：否则 v 接近 5000 时 `pali[left + 1]` 越界',
                 '`v < pali[0]` 时单独处理（pali[0] = 1），否则 `pali[left]` 不存在',
                 '二分取 `mid = (left + right + 1) // 2`（原文已用整除），配合 `left = mid` 不会死循环',
                 '视频略去了前面 5000 次回文检测的逐行过程，只展示它的结果 pali'],
    ),
)
