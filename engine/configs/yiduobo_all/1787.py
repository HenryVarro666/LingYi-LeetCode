def _chips(cv, T, x, y, items, maxw, h=40, size=22, hot=None, fillhot='yellow'):
    """一行 chip，放不下自动换行；返回下一行 y"""
    cx = x
    for key, text in items:
        w = cv.tlen(text, size, mono=True) + 24
        if cx + w > x + maxw:
            cx = x
            y += h + 8
        is_hot = hot is not None and key == hot
        cv.rect((cx, y, cx + w, y + h), fill=T[fillhot] if is_hot else T['panel2'], r=8, outline=T['border'])
        cv.text((cx + w / 2, y + h / 2), text, size, T['bg'] if is_hot else T['text'], anchor='mm', mono=True, bold=is_hot)
        cx += w + 10
    return y + h + 14


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S.get('_inner', {})
    cl = S.get('cnt_list')
    if cl is None:
        return
    k = len(cl)
    ln = S.get('_line', 0)
    cur_i = inner.get('i') if ln >= 16 else None
    cur_p = inner.get('p') if ln in (9, 10) else None
    cur_num = inner.get('num')
    cv.text((x0 + 18, y0 + 4), '按下标 % k 分组：每组 「数值×出现次数」', 22, T['muted'], bold=True)
    y = y0 + 44
    for gi in range(k):
        mark = gi == cur_i or gi == cur_p
        cv.rect((x0 + 14, y - 4, x1 - 14, y + 52), outline=T['blue'] if mark else T['border'], width=3 if mark else 1, r=10)
        cv.text((x0 + 28, y + 24), f'第{gi}组', 22, T['blue'] if mark else T['muted'], anchor='lm', bold=True)
        items = [(v, f'{v}×{c}') for v, c in sorted(cl[gi].items())] or [(None, '（空）')]
        hot = cur_num if mark else None
        _chips(cv, T, x0 + 120, y, items, x1 - x0 - 150, hot=hot)
        y += 66
    y += 6
    f, g = S.get('f'), S.get('g')
    if f is not None and ln >= 12:
        cv.text((x0 + 18, y), 'f：前 i 组异或和为 j 时，最多保留几个数（只列出 > 0 的）', 22, T['muted'], bold=True)
        y += 36
        if g is not None and ln >= 17:
            y = _chips(cv, T, x0 + 14, y, [(j, f'{j}:{v}') for j, v in enumerate(g) if v] or [(None, '无')], x1 - x0 - 40, size=20, h=36) - 4
            cv.text((x0 + 18, y - 8), '↑ g = 上一轮的 f（旧表）', 18, T['dim'])
            y += 24
        hotj = None
        if ln == 22 and 'j' in inner and cur_num is not None:
            hotj = inner['j'] ^ cur_num
        label = 'f（新表）' if g is not None and ln >= 17 else 'f'
        cv.text((x0 + 18, y - 4), label, 18, T['dim'])
        y += 22
        _chips(cv, T, x0 + 14, y, [(j, f'{j}:{v}') for j, v in enumerate(f) if v] or [(None, '全 0')], x1 - x0 - 40, size=20, h=36,
               hot=hotj, fillhot='green')


def _cap_g(S, B, r):
    return f'`g` 先备份旧表：{[(j, v) for j, v in enumerate(S.g) if v]}，`f` 清零后重新算第 {S.i} 组'


def _cap_upd(S, B, r):
    j, num, cnt = S.j, S.num, S.cnt
    t = j ^ num
    return (f'旧表 `g[{j}] = {S.g[j]}`，第 {S.i} 组选 `{num}`（出现 {cnt} 次）：'
            f'`{j} ^ {num} = {t}` → `f[{t}] = max({B.f[t]}, {S.g[j]} + {cnt})` = =={S.f[t]}==')


def _cap_ret(S, B, r):
    n, f0, mc = len(S.nums), S.f[0], S.max_cnt
    a, b = n - f0, n - sum(mc) + min(mc)
    return (f'情况 2：`n − f[0] = {n} − {f0}` = {a}；情况 1：`n − sum(max_cnt) + min(max_cnt)` = {n} − {sum(mc)} + {min(mc)} = {b}；'
            f'取较小者 =={r}==')


CONFIG = dict(
    num=1787, title='使所有区间的异或结果为零', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='模 k 分组 + 异或背包',
    tags=['其他线性 DP', '难度分 2640'],
    code='''
class Solution(object):
    def minChanges(self, nums, k):

        cnt_list = [{} for _ in range(k)]
        max_cnt = [0] * k

        for index, num in enumerate(nums):
            p = index % k
            cnt_list[p][num] = cnt_list[p].get(num, 0) + 1
            max_cnt[p] = max(max_cnt[p], cnt_list[p][num])

        f = [0] * 1024
        for num in cnt_list[0]:
            f[num] = cnt_list[0][num]

        for i in range(1, k):
            g = f[:]
            f = [0] * 1024
            for num, cnt in cnt_list[i].items():
                for j in range(1024):
                    if g[j] > 0:
                        f[j ^ num] = max(f[j ^ num], g[j] + cnt)
        
        return min(len(nums) - f[0], len(nums) - sum(max_cnt) + min(max_cnt))
''',
    call='Solution().minChanges([1,2,3,1,2,4], 3)',
    expect=1,
    skip=['for j in range(1024)', 'if g[j] > 0', 'f = [0] * 1024', 'for index, num in enumerate'],
    views=[
        dict(type='custom', draw=_draw, h=540),
        dict(type='text', size=26, h=70,
             fn=lambda S: ('==证明==：`nums[p] ^ nums[p+k] = 0`，所以 `nums[p] = nums[p+k]`，答案必以 k 为周期'
                           if S.get('_line', 0) < 12 else '情况 1：每组选最多的数，去掉最少那组；情况 2：k 组各选一个，异或为 0')),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p'), ('i', 'i', 'blue'), ('num', 'num', 'orange'), ('cnt', 'cnt'),
           ('max_cnt', 'max_cnt', 'green')],
    captions={
        'cnt_list = [': '`cnt_list[p]`：下标 `% k == p` 的那一组里，每个数出现几次。共 `k = {k}` 组',
        'max_cnt = [': '`max_cnt[p]`：第 `p` 组里出现最多的那个数的次数，用于情况 1',
        'p = index': '`nums[{index}] = {num}`，`{index} % {k} = {p}` → 归入第 `{p}` 组',
        'cnt_list[p][num] =': '第 {p} 组里 `{num}` 出现 `{cnt_list[p][num]}` 次',
        'max_cnt[p] =': '`max_cnt[{p}] = {max_cnt[p]}`：第 {p} 组目前最多的次数',
        'f[num] = cnt_list[0][num]': '第 0 组选 `{num}`，异或和为 `{num}`，保留 `{f[num]}` 个：`f[{num}] = {f[num]}`',
        'for i in range(1, k)': lambda S, B, r: (f'开始第 `{S.i}` 组：在旧表基础上再选一个数' if 'i' in S and (('i' not in B) or S.i != B.i)
                                                else '所有组都处理完，`f[0]` 就是 k 组异或为 0 时最多保留的个数'),
        'for num in cnt_list[0]': lambda S, B, r: (f'第 0 组里有数 `{S.num}`（出现 {S.cnt_list[0][S.num]} 次），先让它作为起点' if 'num' in S and S.get('num') != B.get('num')
                                                  else '第 0 组的初始状态建好了'),
        'for num, cnt in': lambda S, B, r: (f'第 {S.i} 组枚举一个数：`num = {S.num}`，出现 `cnt = {S.cnt}` 次' if S.get('num') != B.get('num') or S.get('cnt') != B.get('cnt')
                                           else f'第 {S.i} 组的数都试过了，`f` 是前 {S.i + 1} 组的新表'),
        'g = f[:]': _cap_g,
        'f[j ^ num] = max': _cap_upd,
        'return min': _cap_ret,
    },
    max_steps=90,
    max_events=60000,
    cards=dict(
        one_liner='结论：答案以 k 为周期，按模 k 分组再做异或背包',
        complexity='时间 `O(n·2^L)`（本题 L = 10），空间 `O(2^L)`',
        problem=['改最少的数，使数组中==每个长为 k 的区间异或都为 0==',
                 '`nums[i] < 2^10`，`k <= n <= 2000`',
                 '示例：`nums = [3,4,5,2,1,7,3,4,7], k = 3` → `3`',
                 '本视频演示：`[1,2,3,1,2,4], k = 3` → `1`（把最后的 4 改成 3）'],
        quote='对于任意位置p，有nums[p] ^ ... ^ nums[p + k - 1] = 0。……从而可知nums[p] = nums[p + k]',
        quote_src='—— yiduobo 题解',
        idea=['相邻两个长 k 的区间只差首尾，所以 `nums[p] == nums[p+k]`，数组按模 k 周期重复',
              '情况 1：有一组全改，其余各留出现最多的数 → 留下 `sum(max_cnt) − min(max_cnt)`',
              '情况 2：每组都留一个数且异或为 0，`f[i][j]` 枚举组内数 `num`：`f[j^num] = max(.., g[j] + cnt)`'],
        summary=['答案 = `n` − 两种情况留下个数的较大者（代码里是取 `min`）',
                 '`f` 只依赖上一轮，所以用 `g = f[:]` 备份做滚动数组',
                 '易错：异或和范围是 0..1023，数组开 1024；`g[j] > 0` 才表示该状态可达',
                 '原文本身已是 Python 3 可运行写法，无需改动'],
    ),
)
