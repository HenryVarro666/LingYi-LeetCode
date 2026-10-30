NUMS = [2, -1, 3, 0, -1]
LO = min(NUMS) + 50000 - 1   # 动画只展示有数的桶及其左右各一个空桶
HI = max(NUMS) + 50000 + 1

# 100001 个桶逐行追踪会产生 20 万个事件，无法演示；
# 这里只在 range(0, 100001) 时把首尾「全是 0 的桶」快进跳过（这些桶上 if 不成立，什么都不做，不影响结果）
SETUP = f'''
import builtins as _b
def range(*a):
    if a == (0, 100001):
        return _b.range({LO}, {HI} + 1)
    return _b.range(*a)
'''


def _done_in(S):
    """how many numbers of nums have been counted so far"""
    c = S.get('num_cnt')
    if c is None:
        return 0
    return sum(c[LO:HI + 1])


def _nums(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ln = S.get('_line') or 0
    done = _done_in(S)
    cur = None
    if ln == 4:
        cur = done
    elif ln == 5:
        cur = done - 1
    cv.text((x0 + 18, y0 + 4), 'nums', 22, T['muted'], bold=True)
    cell = 84
    for k, v in enumerate(NUMS):
        X = x0 + 20 + k * cell
        if k == cur:
            fill, tc = T['blue'], T['bg']
        elif k < done:
            fill, tc = T['green'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((X + 4, y0 + 36, X + cell - 4, y0 + 96), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, y0 + 66), v, 30, tc, anchor='mm', bold=True)
        if k == cur:
            cv.text((X + cell / 2, y0 + 104), f'+50000 = {v + 50000}', 18, T['blue'], anchor='mt', bold=True)


def _buckets(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    c = S.get('num_cnt')
    if c is None:
        return
    ln = S.get('_line') or 0
    num = S.get('num')
    cv.text((x0 + 18, y0 + 4), f'num_cnt（共 100001 个桶，只画出 [{LO}, {HI}]，其余全是 0）', 22, T['muted'], bold=True)
    n = HI - LO + 1
    cell = min(128, (x1 - x0 - 120) / n)
    sx = x0 + 60 + (x1 - x0 - 120 - cell * n) / 2
    Y = y0 + 70
    cv.text((sx - 14, Y + 40), '…', 30, T['dim'], anchor='rm')
    cv.text((sx + n * cell + 14, Y + 40), '…', 30, T['dim'], anchor='lm')
    bc = B.get('num_cnt')
    hit = None
    if ln == 5:
        hit = S['num'] + 50000
    elif ln in (8, 9, 10) and num is not None and isinstance(num, int):
        hit = num
    for k in range(n):
        idx = LO + k
        X = sx + k * cell
        v = c[idx]
        changed = bc is not None and bc[idx] != v
        if idx == hit:
            fill, tc = T['orange'], T['bg']
        elif v > 0:
            fill, tc = T['cyan'], T['bg']
        else:
            fill, tc = T['panel2'], T['dim']
        cv.rect((X + 4, Y, X + cell - 4, Y + 80), fill=fill, r=10, outline=T['yellow'] if changed else T['border'],
                width=3 if changed else 1)
        cv.text((X + cell / 2, Y + 40), v, 34, tc, anchor='mm', bold=True)
        cv.text((X + cell / 2, Y + 90), idx, 18, T['muted'], anchor='mt', mono=True)
        cv.text((X + cell / 2, Y + 114), f'↔ {idx - 50000}', 20, T['text'] if v else T['dim'], anchor='mt', bold=True)
    cv.text((x0 + 18, Y + 150), '上排是下标 num + 50000，下排是它代表的原数', 20, T['dim'])


def _res(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    r = S.get('res')
    if r is None:
        return
    cv.text((x0 + 18, y0 + 4), 'res（按桶的顺序输出，天然有序）', 22, T['muted'], bold=True)
    br = B.get('res') or []
    cell = 84
    for k, v in enumerate(r):
        X = x0 + 20 + k * cell
        new = k >= len(br)
        cv.rect((X + 4, y0 + 36, X + cell - 4, y0 + 96), fill=T['green'] if new else T['panel2'], r=10, outline=T['border'])
        cv.text((X + cell / 2, y0 + 66), v, 30, T['bg'] if new else T['text'], anchor='mm', bold=True)


def _cap_range(S, B, ret):
    num = S.num
    if num == B.get('num'):
        return f'`[{HI + 1}, 100000]` 也全是空桶（动画快进）→ 枚举结束'
    if num == LO:
        return f'从 `num = 0` 开始枚举桶：`[0, {LO - 1}]` 全是空桶，==动画快进==到 `num = {num}`'
    return f'看桶 `num_cnt[{num}]`（代表 `{num - 50000}`）'


CONFIG = dict(
    num=912, title='排序数组', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='计数排序（值域 [-50000, 50000]）',
    tags=['字节30天'],
    code='''
class Solution(object):
    def sortArray(self, nums):
        num_cnt = [0] * 100001
        for num in nums:
            num_cnt[num + 50000] += 1

        res = []
        for num in range(0, 100001):
            if num_cnt[num] > 0:
                res.extend([num - 50000] * num_cnt[num])

        return res
''',
    setup=SETUP,
    call=f'Solution().sortArray({NUMS})',
    expect=sorted(NUMS),
    views=[
        dict(type='custom', draw=_nums, h=140),
        dict(type='custom', draw=_buckets, h=285),
        dict(type='custom', draw=_res, h=130),
    ],
    watch=[('num', 'num', 'orange')],
    captions={
        'num_cnt = [0] * 100001': '开 `100001` 个桶：值域 `[-50000, 50000]` 一共 `100001` 个数',
        'for num in nums': lambda S, B, ret: (f'取 `num = {S.num}`' if _done_in(S) < len(NUMS) else '计数完毕'),
        'num_cnt[num + 50000] += 1': lambda S, B, ret: (
            (f'==负数不能直接当下标==：`{S.num} + 50000 = {S.num + 50000}`，' if S.num < 0 else f'`{S.num} + 50000 = {S.num + 50000}`：')
            + f'`num_cnt[{S.num + 50000}]` → {S.num_cnt[S.num + 50000]}'),
        'res = []': '按下标从小到大扫一遍桶，就能按顺序输出',
        'for num in range(0, 100001)': _cap_range,
        'if num_cnt[num] > 0': lambda S, B, ret: (f'`num_cnt[{S.num}] = {S.num_cnt[S.num]}` > 0 → 输出 `{S.num_cnt[S.num]}` 个 `{S.num - 50000}`'
                                                  if S.num_cnt[S.num] > 0 else f'`num_cnt[{S.num}] = 0`：空桶，跳过'),
        'res.extend': '减回 50000：`[{num - 50000}] × {num_cnt[num]}` 追加到 `res`',
        'return res': '返回 `{ret}`',
    },
    max_steps=50,
    cards=dict(
        one_liner='值域只有 10 万：开 100001 个桶计数，再按桶的顺序输出',
        complexity='时间 `O(n + U)`，空间 `O(U)`，`U = 100001`',
        problem=['给定整数数组 `nums`，将其==升序==排列，不使用内置排序',
                 '`1 ≤ n ≤ 5·10^4`，`-5·10^4 ≤ nums[i] ≤ 5·10^4`',
                 '示例：`[5,2,3,1]` → `[1,2,3,5]`',
                 f'本视频：`{NUMS}` → `{sorted(NUMS)}`'],
        quote='注意到这里每个数的范围在-50000到50000之间，那么完全可以开一个大小为100001的数组来进行计数排序。……需要特别注意python没有常规意义下的负数下标，因此需要先将每个数加上50000，最后输出结果时再减去50000。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：`num_cnt[num + 50000] += 1`，统计每个值出现几次',
              '第二遍：下标从小到大扫所有桶，非空就输出 `num_cnt[x]` 个 `x − 50000`',
              '`n = 50000` 时 `O(n + U)` 比 `O(n log n)` 的比较排序更快'],
        summary=['时间 `O(n + U)`，空间 `O(U)`；值域小、数据多时比快排更好',
                 '易错：负数要先平移 `+50000` 再当下标，输出时减回去',
                 '动画说明：100001 个桶逐行追踪太长，首尾全为 0 的空桶被快进跳过（不影响结果）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用随机 pivot 的快速排序，`O(n log n)`，不依赖值域'],
    ),
)
