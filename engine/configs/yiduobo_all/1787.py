A = [1, 2, 3, 1, 2, 4]
K = 3


def _cnt(S):
    c = S.get('cnt_list')
    return [[d.get(v, 0) for v in range(8)] for d in c] if c else None


def _arr(name):
    return lambda S: (S[name][:8] if name in S else None)


def _txt(S):
    ln = S.get('_line', 0)
    if 'f' not in S:
        return '先按下标模 k 分组，数每组里各个数出现几次，并记下每组的最大次数 `max_cnt`'
    if ln >= 24:
        return f"方案 1 保留 `sum(max_cnt) - min(max_cnt)` = {sum(S['max_cnt']) - min(S['max_cnt'])}；方案 2 保留 `f[0]` = {S['f'][0]}"
    i = S.get('i', 0)
    return f"背包：`f[x]` = 前 {i + 1 if 'g' in S else 1} 组各选一个、异或为 x 时最多保留的个数（只画 x = 0..7）"


CONFIG = dict(
    num=1787, title='使所有区间的异或结果为零', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='分组 + 异或背包（滚动数组）',
    tags=['灵神题单·动态规划', '难度分 2640'],
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
    call=f'Solution().minChanges({A}, {K})',
    expect=1,
    max_events=15000,
    skip=['cnt_list = [{}', 'max_cnt = [0]', 'for j in range(1024)', 'if g[j] > 0', 'g = f[:]', 'f = [0] * 1024'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前读的元素，第 p 组 = 下标模 k 为 p）', cell=70, h=130,
             color=lambda S, idx, v: 'blue' if S.get('_line') in (8, 9, 10) and S.get('index') == idx else None),
        dict(type='table', var=_cnt, label='cnt_list[组][值]：各组里每个值出现次数（只画值 0..7）', cell=70, h=190,
             rows=lambda S: [f'组{g}' for g in range(K)], cols=lambda S: list(range(8))),
        dict(type='array', var=_arr('g'), label='g[x]：上一组处理完的 f（只画 x = 0..7）', cell=70, h=130),
        dict(type='array', var=_arr('f'), label='f[x]：保留数最大值（x = 已选数的异或，黄 = 刚更新）', cell=70, h=130,
             color=lambda S, idx, v: 'yellow' if S.get('_line') == 22 and idx == (S['j'] ^ S['num']) else None),
        dict(type='text', fn=_txt, size=22, h=70),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num', 'pink'), ('p', 'p', 'purple'), ('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('max_cnt', 'max_cnt', 'green')],
    captions={
        'for index, num in enumerate': lambda S, B, r: (f'读 `nums[{S.index}] = {S.num}`，它属于第 `{S.index} % {S.k}` = {S.index % S.k} 组'
                                                       if B.get('index') != S.get('index') or 'index' not in B else '全部分组、计数完毕'),
        'p = index % k': '下标模 `k` 的结果 `p = {p}`：同一组的位置最终必须相等',
        'cnt_list[p][num] =': '第 {p} 组里 `{num}` 出现 `{cnt_list[p][num]}` 次',
        'max_cnt[p] = max': '第 {p} 组的最大出现次数 `max_cnt[{p}] = {max_cnt[p]}`',
        'f = [0] * 1024': '`f[x]` 表示选出的数异或为 x 时最多保留的个数',
        'for num in cnt_list[0]': '第 0 组：它的每个数都可以选，`f[数] = 它的出现次数`',
        'f[num] = cnt_list[0]': '`f[{num}] = {f[num]}`',
        'for i in range(1, k)': lambda S, B, r: (f'`i = {S.i}`：加入第 {S.i} 组，`g` 是上一轮的 `f`' if B.get('i') != S.get('i') or 'i' not in B else '各组都处理完了'),
        'for num, cnt in cnt_list[i].items()': '枚举第 `{i}` 组里选哪个数（出现 `cnt` 次），从上一轮 `g` 转移；这组枚举完就进下一组',
        'f[j ^ num] = max': '`g[{j}] = {g[j]} > 0`：前面各组异或为 `{j}` 能保留 `{g[j]}` 个 → 再选 `{num}` 异或变 `{j ^ num}`，保留 `{g[j]} + {cnt}` → `f[{j ^ num}]` = =={f[j ^ num]}==',
        'return min': lambda S, B, r: (f'方案 2：`n - f[0]` = {len(B.nums) - B.f[0]}（每组留一个、异或为 0）；方案 1：`n - sum(max_cnt) + min(max_cnt)` = '
                                      f'{len(B.nums) - sum(B.max_cnt) + min(B.max_cnt)}（某组全改）→ 取较小 =={r}=='),
    },
    cards=dict(
        one_liner='最终必以 k 为周期；分组后，要么一组全改，要么异或背包',
        complexity='时间 `O(n·2^L)`，空间 `O(k + 2^L)`',
        problem=['整数数组 `nums` 和整数 `k`，要求每个长度为 `k` 的区间异或和为 0',
                 '求最少改动几个元素',
                 '示例：`nums = [1,2,3,1,2,4]`，`k = 3` → `1`'],
        quote='对于任意位置p，有nums[p] ^ nums[p + 1] ^ ... ^ nums[p + k - 1] = 0。……从而可知nums[p] = nums[p + k]',
        quote_src='—— yiduobo 题解原文',
        idea=['先推出结论：`nums[p] == nums[p + k]`，所以按下标模 `k` 分组',
              '方案 1：`k-1` 组各选最多的数，剩下一组去适配 → 保留 `sum(max_cnt) - min(max_cnt)`',
              '方案 2：每组选一个数且异或为 0，是另类背包：`f[j ^ num] = max(…, g[j] + cnt)`',
              '两种方案取改动较少的'],
        summary=['时间 `O(n·2^L)`，空间 `O(k + 2^L)`（`f` 滚动数组）',
                 '易错：方案 2 只从 `g[j] > 0` 的状态转移，没选过的状态不能参与',
                 '易错：方案 1 要扣掉最大次数最小的那一组',
                 '原文本身就是 Python 3 可运行的写法，代码未改；`1024` 是值域上限，演示中只画前 8 格'],
    ),
)
