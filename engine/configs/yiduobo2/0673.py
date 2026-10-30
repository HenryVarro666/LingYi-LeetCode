NUMS = [1, 3, 5, 4, 7]
N = len(NUMS)

# 字幕回调按步骤顺序执行：用全局变量记住“上一步之前”的状态，好在跳过的行之后解释发生了什么
ST = dict(prev=(0, 1), arr=None)


def _lb(i):
    return i & -i


def _cap_arr(S, B, ret):
    ST['arr'] = [list(x) for x in S.index_array]
    return f'离散化完成：`{NUMS}` → 排名 `{S.nums}`；建树状数组 `index_array[1..{N}]`，每格存 `[最长长度, 个数]`'


def _cap_for(S, B, ret):
    if 'num' in B and B.num == S.num:
        return '所有数都处理完了'
    ST['prev'] = (0, 1)
    if S.num == 1:
        return '处理 `num = 1`：排名最小，前面==没有更小的数==，查询区间为空'
    return f'处理 `num = {S.num}`：先查排名在 `[1, {S.num - 1}]` 里、以它们结尾的==最长长度和个数=='


def _cap_query(S, B, ret):
    i = B.index
    node = B.index_array[i]
    pl, pc = ST['prev']
    if node[0] > pl:
        how = f'更长 → 替换为 `({B.now_len}, {B.now_cnt})`'
    elif node[0] == pl and node[0] > 0:
        how = f'一样长 → 个数相加 `{pc} + {node[1]} = {B.now_cnt}`'
    else:
        how = '不更长 → 不变'
    ST['prev'] = (B.now_len, B.now_cnt)
    return f'查询节点 `{i}`（管 `({i - _lb(i)}, {i}]`）存 `{node}`：{how}；`index` 跳到 `{S.index}`'


def _cap_plus(S, B, ret):
    if B.now_len == 0:
        return f'前面没有更小的数 → 自己单独成一个序列：长度 `1`，个数 `1`'
    return f'接上 `{S.num}`：得到长度 `{S.now_len}` 的递增子序列共 `{S.now_cnt}` 条'


def _cap_update(S, B, ret):
    i = B.index
    old = ST['arr'][i]
    new = B.index_array[i]
    ST['arr'] = [list(x) for x in B.index_array]
    if new[0] > old[0]:
        how = f'`{B.now_len} > {old[0]}` → 覆盖为 `{new}`'
    elif new != old:
        how = f'`{B.now_len}` 一样长 → 个数相加，变成 `{new}`'
    else:
        how = f'`{B.now_len} < {old[0]}` → 不变'
    return f'更新节点 `{i}`（管 `({i - _lb(i)}, {i}]`）：{how}；`index` 跳到 `{S.index}`'


def _cap_final(S, B, ret):
    i = B.index
    node = B.index_array[i]
    if node[0] == B.max_len and node[1] == B.res and i == N:
        how = '先记下'
    elif node[0] < B.max_len:
        how = f'`{node[0]} < {B.max_len}` 不更长，不变'
    else:
        how = '更新'
    return f'查整个 `[1, {N}]`：节点 `{i}`（管 `({i - _lb(i)}, {i}]`）存 `{node}`，{how} → `max_len = {B.max_len}`，`res = {B.res}`'


def bit_view(cv, S, B, box, T):
    """树状数组：每格写 长度/个数，上方横条 = 该格管辖的区间 (i - lowbit(i), i]；黄 = 这一步访问的节点"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'index_array[i]（格内 = 最长长度 / 个数；横条 = 管辖区间；黄 = 刚访问）', 24, T['muted'], bold=True)
    arr = S.get('index_array')
    if arr is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    hot = B.get('index') if S.get('_line') in (28, 38, 48) else None
    cw = min(130, (x1 - x0 - 80) / N)
    sx = x0 + (x1 - x0 - cw * N) / 2
    base = y1 - 70
    ch = 70

    def X(i):
        return sx + (i - 1) * cw

    for i in range(1, N + 1):
        lv = _lb(i).bit_length() - 1
        yb = base - ch - 26 - lv * 26
        c = T['yellow'] if i == hot else T['border']
        cv.rect((X(i - _lb(i) + 1) + 6, yb, X(i) + cw - 6, yb + 12), fill=c, r=6)
    bA = B.get('index_array')
    for i in range(1, N + 1):
        v = arr[i]
        changed = bA is not None and bA[i] != v
        fill = T['yellow'] if i == hot else T['panel2']
        cv.rect((X(i) + 4, base - ch, X(i) + cw - 4, base), fill=fill, r=10,
                outline=T['green'] if changed else T['border'], width=3 if changed else 1)
        cv.text((X(i) + cw / 2, base - ch / 2), f'{v[0]}/{v[1]}', 30, T['bg'] if i == hot else T['text'],
                anchor='mm', bold=True, mono=True)
        cv.text((X(i) + cw / 2, base + 8), str(i), 20, T['muted'], anchor='mt', mono=True)


def _pos(S):
    if S.get('_line', 0) < 19 or 'now_len' not in S and S.get('_line') != 19:
        return None
    if 'num' in S and isinstance(S.get('nums'), list) and S['num'] in S['nums']:
        return S['nums'].index(S['num'])
    return None


def _info(S):
    line = S.get('_line', 0)
    if line <= 6:
        return '第一步 ==离散化==：把每个数换成它在排序后的排名，值域变成 `1..n`'
    if line < 40:
        nl, nc = S.get('now_len'), S.get('now_cnt')
        if nl is None:
            return '扫描 nums：对每个数，查前缀 `[1, num-1]` 的 (最长长度, 个数)，再把 `长度+1` 写回树状数组'
        return f"`num = {S['num']}`：当前 `now_len = {nl}`，`now_cnt = {nc}`"
    return f"整体查询 `[1, {N}]`：`max_len = {S.get('max_len')}`，`res = {S.get('res')}`"


CONFIG = dict(
    num=673, title='最长递增子序列的个数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='DP + 离散化 + 树状数组（前缀最大值及其个数）',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findNumberOfLIS(self, nums):
        num_dict = {}
        now = 1
        last = None
        for index, num in enumerate(sorted(nums)):
            if index > 0 and num == last:
                continue
            else:
                num_dict[num] = now
                now += 1
                last = num

        for index in range(len(nums)):
            nums[index] = num_dict[nums[index]]

        index_array = [[0, 0] for _ in range(len(nums) + 1)]

        for num in nums:
            index = num - 1
            now_len, now_cnt = 0, 1
            while index > 0:
                if index_array[index][0] > now_len:
                    now_len = index_array[index][0]
                    now_cnt = index_array[index][1]
                elif index_array[index][0] == now_len:
                    now_cnt += index_array[index][1]
                index -= index & -index

            now_len += 1
            index = num
            while index <= len(nums):
                if now_len > index_array[index][0]:
                    index_array[index][0] = now_len
                    index_array[index][1] = now_cnt
                elif now_len == index_array[index][0]:
                    index_array[index][1] += now_cnt
                index += index & -index

        res, max_len = 0, 0
        index = len(nums)
        while index > 0:
            if index_array[index][0] > max_len:
                max_len = index_array[index][0]
                res = index_array[index][1]
            elif index_array[index][0] == max_len:
                res += index_array[index][1]
            index -= index & -index
        return res
''',
    call=f'Solution().findNumberOfLIS({NUMS})',
    expect=2,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='nums', label='nums（离散化后是排名；蓝 = 正在处理）', cell=96, h=160,
             color=lambda S, i, v: 'blue' if i == _pos(S) else None),
        dict(type='map', var='num_dict', label='num_dict（原数 → 排名）', h=100, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='custom', draw=bit_view, h=300),
    ],
    watch=[('num', 'num', 'blue'), ('index', 'index', 'yellow'), ('now_len', 'now_len', 'pink'),
           ('now_cnt', 'now_cnt', 'green')],
    captions={
        'num_dict = {}': '离散化：排序后依次编号，`num_dict` 记录每个数的排名（相同的数排名相同）',
        'index_array = [[0, 0]': _cap_arr,
        'for num in nums': _cap_for,
        'index -= index & -index': lambda S, B, r: (_cap_final(S, B, r) if S._line == 48 else _cap_query(S, B, r)),
        'now_len += 1': _cap_plus,
        'index += index & -index': _cap_update,
        'res, max_len = 0, 0': '扫描完成：再查一次整个区间 `[1, n]`，得到全局最长长度和个数',
        'return res': '最长递增子序列长度 `{max_len}`，共 =={ret}== 个',
    },
    skip=['for index, num in enumerate(sorted(nums))', 'now = 1', 'last = None', 'if index > 0 and num == last', 'continue', 'num_dict[num] = now', 'now += 1',
          'last = num', 'for index in range(len(nums))', 'nums[index] = num_dict', 'index = num - 1',
          'now_len, now_cnt = 0, 1', 'while index > 0', 'if index_array[index][0] > now_len',
          'now_len = index_array', 'now_cnt = index_array', 'elif index_array[index][0] == now_len',
          'now_cnt += index_array', 'index = num', 'while index <= len(nums)', 'if now_len > index_array',
          'index_array[index][0] = now_len', 'index_array[index][1] = now_cnt', 'elif now_len == index_array',
          'index_array[index][1] += now_cnt', 'index = len(nums)', 'if index_array[index][0] > max_len',
          'max_len = index_array', 'res = index_array', 'elif index_array[index][0] == max_len',
          'res += index_array'],
    max_steps=60,
    cards=dict(
        one_liner='f/g 平方 DP 的“查前面更小的数里的最长长度和个数”，用树状数组加速',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给定整数数组 `nums`，返回==最长严格递增子序列==的个数',
                 '示例 1：`[1,3,5,4,7]` → `2`（`[1,3,4,7]` 和 `[1,3,5,7]`）',
                 '示例 2：`[2,2,2,2,2]` → `5`（长度都是 1，共 5 个）'],
        before=[dict(heading='先看平方 DP（原文）', lines=[
            '`f[i]`：以 `nums[i]` 结尾的最长递增子序列==长度==',
            '`g[i]`：以 `nums[i]` 结尾的最长递增子序列==个数==',
            '枚举 `j < i` 且 `nums[j] < nums[i]`：`f[j]` 更大就覆盖 `f[i] = f[j]+1, g[i] = g[j]`',
            '`f[j]` 相等就累加 `g[i] += g[j]`；时间 `O(n²)`',
        ])],
        quote='对于每个i，我们要找的是0到i - 1中值，nums的值位于0到nums[i] - 1之间的最大的f[i]……可以将问题转化为求0到nums[i] - 1这个区间中的最大值的问题，==可以使用线段树或者树状数组来进行优化==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['先==离散化==：只关心大小关系，把数换成排名 `1..n`',
              '从左往右扫：查排名 `[1, num-1]` 里的 (最长长度, 个数)，长度 +1 后写回位置 `num`',
              '树状数组每格存 (最长长度, 个数)：查询时更长就替换、一样长就累加'],
        result='返回 `2`：最长长度 4，`[1,3,4,7]` 和 `[1,3,5,7]` ✓',
        summary=['时间 `O(n log n)`：每个数一次前缀查询 + 一次更新，都是 `O(log n)`',
                 '易错：查询区间是 `[1, num-1]`（严格递增），离散化时相同的数排名要相同',
                 '`now_cnt` 初始为 1：前面没有更小的数时，自己单独构成一个序列',
                 '原文为 Python 2 风格：删去了文档字符串，代码未改；视频跳过了部分细碎的行'],
    ),
)
