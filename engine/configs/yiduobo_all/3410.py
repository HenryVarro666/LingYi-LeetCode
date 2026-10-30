NUMS = [-2, 3, -1, -2, 4]


def _calc(S):
    I = S.get('_inner') or S
    return 'now' in I and 'pre' in I


def _row(cv, T, x0, y, sx, cell, ch, label, color, vals, n, hi=None, fixed_n=None):
    cv.text((x0 + 18, y - 4), label, 22, T[color], bold=True)
    for k in range(n):
        X = sx + k * cell
        cur = hi == k
        known = vals is not None and k < len(vals)
        cv.rect((X + 4, y + 28, X + cell - 4, y + 28 + ch), fill=T['panel2'], r=8,
                outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
        cv.text((X + cell / 2, y + 28 + ch / 2), vals[k] if known else '·', 30,
                T['text'] if known else T['dim'], anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(NUMS)
    W = x1 - x0 - 40
    cell = min(92, W / n)
    sx = x0 + 20 + (W - cell * n) / 2
    ch = 56
    ln = S.get('_line', 0)
    I = S.get('_inner') or S
    if _calc(S):
        nums = I['nums']
        rev = nums != NUMS
        idx = I.get('index')
        cv.text((x0 + 18, y0 + 4), f"calc(nums)：{'对反转后的 nums，从右往左' if rev else '从左到右'}，每个下标算 f 和 g", 22, T['muted'], bold=True)
        y = y0 + 40
        _row(cv, T, x0, y, sx, cell, ch, 'nums' + ('（反转后）' if rev else ''), 'muted', nums, n, idx)
        _row(cv, T, x0, y + 100, sx, cell, ch, 's：前缀和', 'cyan', I.get('s'), n, idx)
        _row(cv, T, x0, y + 200, sx, cell, ch, 'f[i]：以 i 结尾、不删的最大子段和', 'blue', I.get('f'), n, idx)
        _row(cv, T, x0, y + 300, sx, cell, ch, 'g[i]：以 i 结尾、删掉所有 nums[i] 的最大子段和（非负数记 0）', 'pink', I.get('g'), n, idx)
        cv.text((x0 + 18, y + 410), f"pre = {I.get('pre')}（值 → 上次出现的下标）　now = {I.get('now')}", 22, T['yellow'], bold=True)
        return
    idx = S.get('index') if ln >= 41 else None
    cv.text((x0 + 18, y0 + 4), '正向、反向各算一遍，删掉 nums[i] 时：左边 g + 右边 g', 22, T['muted'], bold=True)
    y = y0 + 40
    rows = [('nums', 'muted', NUMS)]
    if S.get('f_left') is not None:
        rows.append(('f_left / g_left：以 i 结尾', 'blue', None))
    _row(cv, T, x0, y, sx, cell, ch, 'nums', 'muted', NUMS, n, idx)
    _row(cv, T, x0, y + 100, sx, cell, ch, 'f_left[i]', 'blue', S.get('f_left'), n, idx)
    _row(cv, T, x0, y + 200, sx, cell, ch, 'g_left[i]（以 i 结尾，删掉 nums[i]）', 'pink', S.get('g_left'), n, idx)
    _row(cv, T, x0, y + 300, sx, cell, ch, 'g_right[i]（以 i 开头，删掉 nums[i]）' + ('' if ln >= 38 else '（反向扫出来，下标还是反的）'), 'purple',
         S.get('g_right') if ln >= 38 else (S.get('g_right') if S.get('g_right') else None), n, idx)
    _row(cv, T, x0, y + 400, sx, cell, ch, 'f_right[i]（以 i 开头）' + ('' if ln >= 37 else '（还没 reverse）'), 'cyan', S.get('f_right'), n, idx)


def _fm(S):
    ln = S.get('_line', 0)
    if not _calc(S) and ln >= 41 and 'index' in S and S.get('g_left') and S.get('g_right'):
        i = S['index']
        v = NUMS[i]
        if v < 0:
            return f"删掉所有 `{v}`：`g_left[{i}] + g_right[{i}]` = `{S['g_left'][i]} + {S['g_right'][i]}` = =={S['g_left'][i] + S['g_right'][i]}==；`res` = {S['res']}"
        return '`nums[i] >= 0` 不用删'
    return ''


def _c_now(S, B, r):
    v, i = S.v, S.index
    prev = S.f[i - 1]
    how = f'上一段和 `{prev}` < 0，丢掉、从 0 重新开始' if prev < 0 else f'上一段和 `{prev}` ≥ 0，接着加'
    return f'`f[{i}]`：{how}；再加 `{v}` → `now = {S.now}`'


def _c_g1(S, B, r):
    return f'`{S.v}` < 0 且==第一次出现==：删掉它，只能取它左边以 `{S.index - 1}` 结尾的不删最优 `f[{S.index - 1}] = {S.f[-2]}` → `g[{S.index}] = {S.g[-1]}`'


def _c_g2(S, B, r):
    p, i = S.pre_index, S.index
    a = S.g[p] + S.s[-2] - S.s[p]
    b = S.f[-2]
    return (f'`{S.v}` 上次在 `{p}`。情形一（起点在 `{p}` 之前）：`g[{p}] + (s[{i - 1}] − s[{p}])` = `{S.g[p]} + {S.s[-2] - S.s[p]}` = `{a}`；'
            f'情形二（起点在 `{p}` 之后）：`f[{i - 1}] = {b}` → 取大 ==`g[{i}] = {S.g[-1]}`==')


def _c_g0(S, B, r):
    return f'`{S.v}` ≥ 0，删它没意义 → `g[{S.index}]` 记 0'


def _c_res(S, B, r):
    i = S.index
    return (f'删掉 `{S.v}`（所有 `{S.v}`）：左边 `g_left[{i}] = {S.g_left[i]}` + 右边 `g_right[{i}] = {S.g_right[i]}` = {S.g_left[i] + S.g_right[i]}，'
            f'`res` → =={S.res}==')


CONFIG = dict(
    num=3410, title='删除所有值为某个元素后的最大子数组和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='f / g 双数组 · 正反两趟 DP',
    tags=['灵神题单·动态规划', '难度分 2844'],
    code='''
class Solution(object):
    def maxSubarraySum(self, nums):
        
        if max(nums) <= 0 and len(set(nums)) == 1:
            return nums[0]

        def calc(nums):
            f = [nums[0]]
            g = [0]
            s = [nums[0]]
            pre = {nums[0] : 0}

            now = nums[0]
            for index, v in enumerate(nums[1:], 1):
                s.append(s[-1] + v)

                if now < 0:
                    now = 0
                now += v
                f.append(now)

                if v < 0:
                    if v not in pre:
                        g.append(f[-2])
                    else:
                        pre_index = pre[v]
                        g.append(max(g[pre_index] + s[-2] - s[pre_index], f[-2]))
                else:
                    g.append(0)
            
                pre[v] = index

            return f, g
        
        f_left, g_left = calc(nums)
        f_right, g_right = calc(nums[::-1])
        f_right.reverse()
        g_right.reverse()

        res = max(f_left)
        for index, v in enumerate(nums):
            if v < 0:
                res = max(res, g_left[index] + g_right[index])
        
        return res
''',
    call=f'Solution().maxSubarraySum({NUMS})',
    expect=6,
    skip=['if max(nums) <= 0', 'return nums[0]', 'def calc', 'f = [nums[0]]', 'g = [0]', 's = [nums[0]]', 'pre = {nums[0]',
          's.append', 'if now < 0', 'now = 0', 'f.append(now)', 'if v < 0', 'if v not in pre', 'pre_index = pre[v]',
          'pre[v] = index', 'for index, v in enumerate(nums[1:], 1)', 'return f, g', 'f_right.reverse()', 'g_right.reverse()',
          'for index, v in enumerate(nums)'],
    views=[
        dict(type='custom', draw=_draw, h=600),
        dict(type='text', fn=_fm, size=24, h=80),
    ],
    watch=[('index', 'index', 'yellow'), ('v', 'v', 'cyan'), ('res', 'res', 'green')],
    captions={
        'now = nums[0]': '`now` 滚动记录「以当前位置结尾的最大子段和」（贪心：前面和为负就丢掉）',
        'now += v': _c_now,
        'g.append(f[-2])': _c_g1,
        'g.append(max(': _c_g2,
        'g.append(0)': _c_g0,
        'f_left, g_left = calc': '正向算一遍：`f_left[i]` 不删；`g_left[i]` = 以 `i` 结尾、==删掉所有 `nums[i]`== 的最大子段和',
        'f_right, g_right = calc': '反向再算一遍（把 `nums` 反转）：得到「以 `i` 开头」的 `f_right`、`g_right`（下标还是反的，后面 reverse）',
        'res = max(f_left)': '不删元素的答案：`max(f_left)` = `{res}`；删了以后的情形接着比',
        'res = max(res, g_left': _c_res,
        'return res': '最大子数组和 = ==`{res}`==',
    },
    cards=dict(
        one_liner='f：不删的最大子段和；g：删掉当前值的最大子段和；正反各算一遍再拼',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选一个值 `x`，把数组里==所有等于 x 的元素删掉==（至多一次，剩下不能为空）',
                 '求所有可能结果里的最大子数组和',
                 '本视频：`[-2,3,-1,-2,4]` → `6`（删 `-2`，得到 `[3,-1,4]`）'],
        quote='令f[index]表示以nums[index]结尾，且不执行删除操作的最大子段和，而g[index]则表示以nums[index]结尾，同时删去了所有nums[index]的最大子段和。',
        quote_src='—— yiduobo 题解原文',
        idea=['不删：经典贪心，`f[i] = max(f[i-1], 0) + nums[i]`',
              '删 `nums[i]`（只有负数有意义）：看上一个相同值的下标 `pre`，两种情形取大：起点在 `pre` 之前 `g[pre] + 区间和`，或起点在 `pre` 之后就是 `f[i-1]`',
              '`g` 只管「以 i 结尾」，右边还能接更多 → ==反转再算一遍，`g_left[i] + g_right[i]`== 拼出完整答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '区间和用前缀和 `s` 之差，值的上一次位置用哈希表 `pre`',
                 '`g_left[i] + g_right[i]` 里 `nums[i]` 只被删、不重复计算',
                 '全是同一个负数时不能删光，开头单独返回 `nums[0]`',
                 '对比灵神：灵神方法三只扫一遍，维护「左端 + 被删数」的最小值；yiduobo 是正反两趟 DP'],
    ),
)
