
def _fmt(v):
    if v is None:
        return '-'
    if abs(v) >= 10 ** 6:
        return f'{v:.1e}'
    return str(v)


def _incalc(S):
    return 'lamb' in S and 'q' in S and 'f' in S


def _t1(S):
    if not _incalc(S):
        if 'mid' in S:
            return f"二分 `λ`：`left = {_fmt(S['left'])}`，`right = {_fmt(S['right'])}`，`mid = {_fmt(S['mid'])}`"
        return '`s` 是前缀和，`calc(λ)` 对每次划分罚 λ，求无限制次数的最优 `f` 和对应最多划分次数 `cnt`'
    return f"当前 `λ = {_fmt(S['lamb'])}`（每多切一刀罚 λ）；决策点候选队列 `q[head:tail]` = ==" + str([S['q'][i] for i in range(S['head'], S['tail'])]) + '=='


def _t2(S):
    if not _incalc(S):
        return ''
    f = [_fmt(x) for x in S['f']]
    return f"`f` = [{', '.join(f)}]　`cnt` = {S['cnt']}"


def _hull(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '决策点 (X, Y) = (s[p], f[p]+s[p]^2-s[p])：蓝 = 队列里，灰 = 已淘汰', 22, T['muted'], bold=True)
    if not _incalc(S):
        return
    s, f, p2 = S['s'], S['f'], S['p2']
    n = len(s) - 1
    idx = S.get('index', 0)
    pts = [(s[p], f[p] + p2[p] - s[p]) for p in range(0, min(idx, n) + 1) if p == 0 or p < idx or True]
    done = min(idx, n)
    alive = set(S['q'][S['head']:S['tail']])
    cur = S['q'][S['head']] if S['head'] < len(S['q']) else 0
    xs = [s[p] for p in range(done + 1)]
    ys = [f[p] + p2[p] - s[p] for p in range(done + 1)]
    lo, hi = min(ys), max(ys)
    span = (hi - lo) or 1
    px0, px1, py0, py1 = x0 + 70, x1 - 50, y0 + 90, y1 - 60
    xmax = max(s) or 1
    for p in range(done + 1):
        X = px0 + s[p] / xmax * (px1 - px0)
        Y = py1 - (ys[p] - lo) / span * (py1 - py0)
        c = T['blue'] if p in alive else T['dim']
        if p == cur and p in alive:
            c = T['yellow']
        cv.rect((X - 14, Y - 14, X + 14, Y + 14), fill=c, r=14)
        cv.text((X, Y - 24), f'p={p}', 18, c, anchor='mb', bold=True)
        cv.text((X, py1 + 38), f's={s[p]}', 18, T['dim'], anchor='mt', mono=True)
    cv.line([(px0 - 20, py1 + 24), (px1 + 20, py1 + 24)], T['border'], 2)

CODE = '''
class Solution(object):
    def minPartitionScore(self, nums, k):
        
        n = len(nums)
        s = [0]
        for v in nums:
            s.append(s[-1] + v)

        p2 = []
        for v in s:
            p2.append(v * v)
        
        if k == 1:
            return s[-1] * (s[-1] + 1) // 2

        def calc(lamb):
            f = [0] * (n + 1)
            cnt = [0] * (n + 1)
            # f[index] = min(f[p] + (s[indx] - s[p]) * (s[index] - s[p] + 1) + lam)
            # -> f[p] + s[index]^2 + s[p]^2 - 2 * s[index] * s[p] + s[index] - s[p] + lam
            # -> (s[index]^2 + s[index] + lam) + (f[p] + s[p]^2 - s[p]) + (-2 * s[index] * s[p])

            q = [0] * (n + 1)
            head, tail = 0, 1

            for index in range(1, n + 1):
                while tail - 1 > head:
                    p0 = q[head]
                    p1 = q[head + 1]

                    b0 = f[p0] + p2[p0]
                    b0 -= s[p0]
                    kx = 2 * s[index]
                    kx *= s[p0]
                    b0 -= kx

                    b1 = f[p1] + p2[p1]
                    b1 -= s[p1]
                    kx = 2 * s[index]
                    kx *= s[p1]
                    b1 -= kx

                    if b1 <= b0:
                        #截距相同时，需要使用最老决策点的cnt更新次老决策点的cnt
                        if b1 == b0 and cnt[p0] > cnt[p1]:
                            cnt[p1] = cnt[p0]
                        head += 1
                    else:
                        break

                p = q[head]
                d = s[index] - s[p]
                d *= (d + 1)
                f[index] = f[p] + d
                f[index] += lamb
                cnt[index] = cnt[p] + 1

                while tail - 1 > head:
                    x_index = s[index]
                    y_index = f[index] + p2[index]
                    y_index -= s[index]

                    p_tail1 = q[tail - 1]
                    x_last_1 = s[p_tail1]
                    y_last_1 = f[p_tail1] + p2[p_tail1]
                    y_last_1 -= s[p_tail1]

                    p_tail2 = q[tail - 2]
                    x_last_2 = s[p_tail2]
                    y_last_2 = f[p_tail2] + p2[p_tail2]
                    y_last_2 -= s[p_tail2]

                    x1 = x_index - x_last_2
                    y1 = y_index - y_last_2

                    x2 = x_last_1 - x_last_2
                    y2 = y_last_1 - y_last_2

                    cross = x1 * y2 - x2 * y1
                    if cross > 0:
                        tail -= 1
                    else:
                        break

                q[tail] = index
                tail += 1
            
            return f[-1], cnt[-1]

        left = 0
        right = 10 ** 18
        while left < right:
            mid = (left + right + 1) // 2
            _, cnt = calc(mid)
            if cnt < k:
                right = mid - 1
            else:
                left = mid

        res, _ = calc(left)
        return (res - k * left) // 2
'''


CONFIG = dict(
    num=3929, title='最小分割分数II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='WQS 二分 + 斜率优化（单调队列维护凸包）',
    tags=['灵神题单', '动态规划'],
    code=CODE,
    call='Solution().minPartitionScore([1, 2, 3, 1], 2)',
    expect=16,
    skip=['for v in nums', 's.append', 'p2 = []', 'for v in s', 'p2.append', 'q = [0]', 'f = [0] * (n + 1)',
          'cnt = [0] * (n + 1)', 'p0 = q', 'p1 = q', 'b0 =', 'b0 -=', 'b1 =', 'b1 -=', 'kx =', 'kx *=',
          'd = s[index]', 'd *= ', 'x_index', 'y_index', 'p_tail', 'x_last', 'y_last', 'x1 =', 'y1 =', 'x2 =', 'y2 =',
          'head, tail = 0, 1', 'while tail - 1 > head', 'break', 'tail += 1', 'f[index] = f[p] + d'],
    max_steps=60,
    max_events=200000,
    views=[
        dict(type='text', fn=_t1, h=70),
        dict(type='text', fn=_t2, h=60),
        dict(type='array', var='s', label='前缀和 s（粉 = 当前 index）', h=150, color=lambda S, i, v: 'pink' if i == S.get('index') and _incalc(S) else None),
        dict(type='custom', draw=_hull, h=330),
    ],
    watch=[('index', 'index', 'pink'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'if k == 1': '`k = {k}`：只分一段时直接用公式；这里 `k > 1`，走 WQS 二分',
        'def calc': '`calc(λ)`：每切一刀罚 `λ`，不限次数地求最小分数，并记下取最优时最多切了几段',
        'for index in range': '`index = {index}`：算 `f[{index}]`（前 {index} 个数的最优）',
        'if b1 <= b0': lambda S, B, r: (f"次老 `p{S.p1}` 的截距 `{f'{S.b1:.3g}'}` <= 最老 `p{S.p0}` 的 `{f'{S.b0:.3g}'}` → 最老的以后永远不会更优，淘汰" if S.b1 <= S.b0 else f"次老 `{f'{S.b1:.3g}'}` > 最老 `{f'{S.b0:.3g}'}` → 队首就是最优，停止"),
        'cnt[p1] = cnt[p0]': '截距相同：用最老决策点的 `cnt` 更新次老的，保证取到最优时切的段数最多',
        'head += 1': '淘汰最老决策点，`head` → {head}',
        'p = q[head]': '队首 `p = {p}` 就是 `index = {index}` 的最优决策点',
        'f[index] += lamb': '`f[{index}] = f[{p}] + (s[{index}] - s[{p}]) * (s[{index}] - s[{p}] + 1) + λ` = =={f[index]:.3g}==（λ = {lamb:.3g}）',
        'cnt[index] = cnt[p] + 1': '段数跟着转移：`cnt[{index}] = cnt[{p}] + 1` = =={cnt[index]}==',
        'cross = ': '新点 `index` 和队尾两点做叉积：判断凸包是否还是凸的',
        'if cross > 0': lambda S, B, r: ('`cross > 0`：队尾点在凸包里面（不凸），弹出队尾' if S.cross > 0 else '`cross <= 0`：保持凸，停止弹出'),
        'tail -= 1': '弹出队尾，`tail` → {tail}',
        'q[tail] = index': '新决策点 `index` 入队',
        'return f[-1], cnt[-1]': '`calc` 返回：罚 λ 后的最优 `{f[-1]:.3g}`，最多切 `{cnt[-1]}` 段',
        'left = 0': '二分 `λ` 的下界',
        'right = 10 ** 18': '上界取很大：`λ` 极大时一刀都不想多切，只切 1 段',
        'while left < right': lambda S, B, r: (f"`left = {f'{S.left:.3g}'} < right = {f'{S.right:.3g}'}`，继续二分" if S.left < S.right else f"`left = right = {f'{S.left:.3g}'}`：找到最大的、仍能切满 k 段的 `λ`"),
        'mid = (left': '`mid = {mid:.3g}`：试这个惩罚',
        '_, cnt = calc(mid)': '`calc(mid)` 最多切 `{cnt}` 段，目标 `k = {k}`',
        'if cnt < k': lambda S, B, r: (f"`cnt = {S.cnt} < k = {S.k}`：惩罚太大、切得太少 → 缩小 λ" if S.cnt < S.k else f"`cnt = {S.cnt} >= k = {S.k}`：切得够多 → λ 还可以更大"),
        'right = mid - 1': '`right` → {right:.3g}',
        'left = mid': '`left` → {left:.3g}',
        'res, _ = calc(left)': '用最终的 `λ = {left:.3g}` 再算一遍，拿到 `f[n]`',
        'return (res - k': '去掉罚款：`(res - k * λ) // 2`，除以 2 是因为公式里省掉了 `/2` = =={(res - k * left) // 2}==',
    },
    cards=dict(
        one_liner='切 k 刀太受限？给每一刀罚 λ，二分 λ 让最优恰好切 k 段',
        complexity='时间 `O(n log C)`，空间 `O(n)`',
        problem=['把正整数数组 `nums` 分成恰好 `k` 个子数组',
                 '子数组值 = `sum * (sum + 1) / 2`，求所有子数组值之和的最小值',
                 '`n` 到 5 万，`nk log n` 也不够。本视频：`[1,2,3,1], k=2` → `16`'],
        quote='对于这个问题，有一种处理方法叫做wqs二分，其思路来自于拉格朗日乘数法，通过引入一个惩罚函数叠加在无限制的代价函数上，从而将有次数限制的最优化问题转化为无次数限制的最优化问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['`g[j]` = 切 j 段的最优，单调递减且下凸 → 叠加 `λj` 后最低点会随 λ 左移',
              '二分 `λ`：切得段数 `cnt < k` 说明罚太重，否则可以再大；最后 `(f[n] - kλ)/2` 就是答案',
              '内层转移 `f[i] = min(f[p] + cost + λ)` 展开后是直线截距，用单调队列维护凸包做斜率优化'],
        before=[dict(heading='先看单次 calc', lines=['视频里先完整演示第一次 `calc(λ)`：队列怎么淘汰、怎么入队',
                                                      '随后二分会重复约 60 次，中间会快进，最后看收敛']),],
        summary=['时间 `O(n log C)`，`C = 10^18` 约 60 轮；空间 `O(n)`',
                 '易错：截距相同时要用最老决策点的 `cnt` 更新次老的，否则 `cnt` 偏小，二分会错',
                 '`k == 1` 要单独处理：直接返回 `s*(s+1)//2`',
                 '代码里为了避免小数，公式里省掉了 `/2`，最后统一 `// 2`',
                 '前置题：3826（同题设、数据小的版本）'],
    ),
)
