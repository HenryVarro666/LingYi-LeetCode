def _txt(S):
    if 'res' not in S or 'mapping' not in S or 's' not in S or 'f' not in S:
        return '总数 − 在范围内的：`s − goal − k <= p <= s − goal + k`'
    return (f"前缀和 `s = {S['s']}`：要数 `{S['s'] - S['goal'] - S['k']} <= p <= {S['s'] - S['goal'] + S['k']}` 的前缀和，"
            f"已累计 `res = {S['res']}`")


def _hl(S, i, v):
    x = S.get('_inner', {}).get('x') if isinstance(S.get('_inner'), dict) else None
    return 'yellow' if x is not None and i == x else None


CONFIG = dict(
    num=4051, title='统计遥远子数组的数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 收集端点离散化 + 树状数组',
    tags=['常用数据结构', '前缀和', '难度分 2140'],
    code='''
class Solution(object):
    def distantSubarrays(self, nums, goal, k):
        
        nums_set = set([0])
        s = 0
        for v in nums:
            s += v
            nums_set.add(s)
            nums_set.add(s - goal + k)
            nums_set.add(s - goal - k)

        nums_list = sorted(list(nums_set))
        mapping = {}
        for index, v in enumerate(nums_list):
            mapping[v] = index + 1

        m = len(mapping)
        f = [0] * (m + 1)
        
        def add(x):
            while x <= m:
                f[x] += 1
                x += x & -x
        
        def get(x):
            v = 0
            while x > 0:
                v += f[x]
                x -= x & -x
            return v
        
        s = 0
        res = 0
        add(mapping[0])
        for v in nums:
            s += v
            if s - goal + k > s - goal - k:
                res += get(mapping[s - goal + k] - 1) - get(mapping[s - goal - k])
            add(mapping[s])
        
        return len(nums) * (len(nums) + 1) // 2 - res
''',
    call='Solution().distantSubarrays([-3,1,2], 0, 3)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=150),
        dict(type='array', var='nums_list', label='nums_list：所有前缀和与两个端点，排序后映射到 1..m', cell=64, h=150),
        dict(type='array', var='f', label='f：树状数组（f[0] 不用）', cell=64, h=150, color=_hl),
        dict(type='map', var='mapping', label='mapping：值 → 序号', fmt=lambda k, v: f'{k}→{v}', h=120, font=28),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    watch=[('s', 's', 'blue'), ('res', 'res', 'green')],
    skip=['nums_set.add(s - goal', 'while x <= m', 'while x > 0', 'v = 0', 'for v in nums', 'for index, v', 'm = len(mapping)'],
    captions={
        'nums_set = set': '`nums_set` 收集所有要比较大小的值，先放入空前缀 `0`',
        'nums_set.add(s)': '前缀和 `s = {s}`；同时把查询用的两端 `s − goal ± k` = `{s - goal - k}`、`{s - goal + k}` 也收进集合（只关心大小关系）',
        'nums_list = sorted': '全部排序去重：`nums_list = {nums_list}`',
        'mapping[v] = index': '映射到 `1..m`：`{v} → {index + 1}`',
        'f = [0]': '建大小 `m + 1` 的树状数组 `f`，`m` = {m}',
        5: '`s` 是当前前缀和，从空前缀 0 开始',
        32: '重新从头扫一遍：这次真的查询',
        33: '`res` 累计「在范围内」的子数组数',
        'add(mapping[0])': '先放入空前缀：值 `0` 的序号 `{mapping[0]}`',
        'if s - goal + k > s - goal - k': '当前前缀和 `s = {s}`；`k > 0` 时 `s−goal−k < s−goal+k`，范围非空才需要查',
        'res += get': '值域 `({s - goal - k}, {s - goal + k})`，即序号 `({mapping[s - goal - k]}, {mapping[s - goal + k]})` 之间：`get(右 − 1) − get(左)`，累加到 `res`',
        'add(mapping[s])': '此时 `res` = =={res}==；把当前前缀和登记进树状数组：序号 `{mapping[s]}` 加 1',
        'f[x] += 1': '`f[{x}] += 1`',
        'x += x & -x': '加上最低位，跳到父节点：`x` = {x}',
        'v += f[x]': '累加 `f[{x}]` = {f[x]}，结果 `{v}`',
        'x -= x & -x': '去掉最低位，跳到前面一段：`x` = {x}',
        'return v': '`get` 返回 `{v}`',
        'return len(nums)': '总数 `{len(nums) * (len(nums) + 1) // 2}` 减去不遥远的 `{res}` = =={len(nums) * (len(nums) + 1) // 2 - res}==',
    },
    cards=dict(
        one_liner='区间和不在范围内 → 总数减去在范围内的，再离散化后查树状数组',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums`，整数 `goal`、`k`：子数组和与 `goal` 的绝对差 `>= k` 叫遥远',
                 '数出遥远子数组的个数（元素可为负）',
                 '本视频：`nums=[-3,1,2]`，`goal=0`，`k=3` → `2`'],
        quote='判断不在特定范围内需要查两头，那么就不如改为判断在特定范围内子数组的数目，然后用总的子数组的数目减去这个值。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间和 = 前缀和之差，每个前缀 `s` 看左边有多少个 `p` 使 `s − p` 落在 `(goal−k, goal+k)`',
              '变形成 `s − goal − k < p < s − goal + k`：只需要大小关系',
              '把所有前缀和与两个端点一起收集、排序，映射成 `1..m`，再建树状数组'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先收集 `s`、`s−goal+k`、`s−goal−k` 离散化，再扫一遍用树状数组查询',
                 '查询是开区间：`get(右 − 1) − get(左)`，易错点是 −1',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神用 `bisect` 离散化，这里把端点一并放进映射表，查询时直接取序号'],
    ),
)
