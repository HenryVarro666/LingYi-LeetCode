def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'f[right]：最后一个分割点在 right 时的最小代价（黄 = 正在更新）', 22, T['muted'], bold=True)
    f = S.get('f')
    nums = S.get('nums')
    if f is None or nums is None:
        return
    n = len(nums)
    cell = min(96, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    ys = y0 + 80
    right, left = S.get('right'), S.get('left')
    line = S.get('_line', 0)
    for i in range(n):
        X = sx + i * cell
        has = i < len(f)
        col = T['yellow'] if (right == i and has and i == len(f) - 1) else T['panel2']
        if left is not None and i == left and line >= 18:
            col = T['green']
        cv.rect((X + 4, ys, X + cell - 4, ys + 64), fill=col, r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + 32), str(f[i]) if has else '', 22, T['bg'] if col != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + 76), i, 18, T['dim'], anchor='mt', mono=True)
        if i < n - 1 or True:
            pass
    for name, idx, c, dy in (('right', right, T['pink'], 0), ('left', left, T['green'], 0)):
        if idx is not None and 0 <= idx < n and (name == 'right' or line >= 18):
            X = sx + idx * cell + cell / 2
            cv.tri_up(X, ys + 108, 10, c)
            cv.text((X, ys + 124 + (26 if (name == 'left' and left == right) else 0)), name, 22, c, anchor='mt', bold=True)


CONFIG = dict(
    num=3500, title='将数组分割为子数组的最小代价', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='提取 k 项 → 去掉序号维度的 O(n^2) DP',
    tags=['灵神题单·动态规划', '难度分 2569'],
    code='''
class Solution(object):
    def minimumCost(self, nums, cost, k):
        
        ps_n = [0]
        for v in nums:
            ps_n.append(ps_n[-1] + v)
        
        ps_c = [0]
        for v in cost:
            ps_c.append(ps_c[-1] + v)

        res = (ps_n[-1] + k) * ps_c[-1]

        if len(nums) > 1:
            f = []
            for right in range(len(nums) - 1):
                f.append(ps_n[right + 1] * ps_c[right + 1] + ps_n[-1] * (ps_c[-1] - ps_c[right + 1]) + k * ps_c[-1] + k * (ps_c[-1] - ps_c[right + 1]))
                for left in range(right):
                    f[-1] = min(f[-1], f[left] - ps_n[-1] * (ps_c[-1] - ps_c[left + 1]) + ps_n[right + 1] * (ps_c[right + 1] - ps_c[left + 1]) + ps_n[-1] * (ps_c[-1] - ps_c[right + 1]) + k * (ps_c[-1] - ps_c[right + 1]))
                res = min(res, f[-1])

        return res
''',
    call='Solution().minimumCost([4,8,5,1], [7,2,8,4], 1)',
    expect=309,
    skip=['ps_n = [0]', 'ps_c = [0]', 'for v in nums', 'for v in cost', 'ps_n.append', 'ps_c.append', 'if len(nums) > 1', 'for left in range(right)', 'f = []'],
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='array', var='nums', label='nums', h=100, cell=64),
        dict(type='array', var='ps_n', label='ps_n（nums 前缀和）', h=110, cell=64),
        dict(type='array', var='ps_c', label='ps_c（cost 前缀和）', h=110, cell=64),
    ],
    watch=[('right', 'right', 'pink'), ('left', 'left', 'green'), ('res', 'res', 'orange'), ('k', 'k')],
    captions={
        'res = (ps_n[-1] + k)': '先算「不分割」：只有 1 段，`res = ({ps_n[-1]} + {k}) × {ps_c[-1]}` = =={res}==',
        'for right in range': lambda S, B, r: (f'`right = {S.right}`：最后一个分割点放在 `right` 之后，算 `f[{S.right}]`' if S.right != B.get('right') else '分割点枚举完毕'),
        'f.append(': '只有一个分割点（第 `right` 个后）：`f[{right}]` = =={f[-1]}==（`k·index` 的项已经化成 `k × cost 后缀和`）',
        'f[-1] = min(f[-1], f[left]': lambda S, B, r: (f'用 `left = {S.left}` 作为上一个分割点：先消去 f[left] 里「到末尾」的前缀项，再换成新增分割点后的两段 → `f[{S.right}]` = =={S.f[-1]}=='
                                                        if S.f[-1] < B.f[-1] else f'`left = {S.left}` 作为上一个分割点：算出的值不比 `{S.f[-1]}` 小，`f[{S.right}]` 不变'),
        'res = min(res, f[-1])': '`res = min({B.res}, f[{right}] = {f[-1]})` = =={res}==',
        'return res': '最小总代价 `res` = =={ret}==',
    },
    cards=dict(
        one_liner='化简 k·index：每多一个分割点，就多付 k × 后面那段 cost 之和',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把 `nums` 分成若干子数组，第 `index` 个子数组 `[left, right]` 代价 `(nums 前缀和 + k·index) × cost 区间和`',
                 '求最小总代价',
                 '示例：`nums=[3,1,4], cost=[4,6,6], k=1` → `110`；本视频：`[4,8,5,1]`，`cost=[7,2,8,4]`，`k=1`'],
        quote='每进行一次划分，都相当于在最终答案中加上k乘以区间和，因此在这里可以尝试去掉状态表示中的index……f[right]表示最后的划分点为right时的最小总代价。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素 `f[right][index]` 要 `O(n^3)`，转移里 `right` 没法消掉，没法用数据结构优化',
              '把每段的 `k·index·区间和` 逐项提出 k，合并成：`k·ps_c[-1] + Σ k·(ps_c[-1] − ps_c[分割点])`',
              '序号 `index` 消失：`f[right]` 只记最后的分割点，从 `f[left]` 转移要先「消去」旧的最后一段前缀项'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：从 `f[left]` 转移要减去旧的「到末尾」那段、加上新增分割后的两段',
                 '`res` 初值是不分割的代价；`f` 只枚举 `right < n-1`（最后一段不需要分割点）',
                 '对比灵神：灵神把 `k·i` 拆成后缀和后得到更简单的 `f[i+1]`，进一步用凸包优化到 `O(n)`；yiduobo 保留「最后分割点」状态，`O(n^2)`'],
    ),
)
