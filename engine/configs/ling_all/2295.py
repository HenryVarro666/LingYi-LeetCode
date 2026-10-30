CONFIG = dict(
    num=2295, title='替换数组中的元素', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='倒序遍历 + 哈希表',
    tags=[],
    code='''
class Solution:
    def arrayChange(self, nums: List[int], operations: List[List[int]]) -> List[int]:
        mp = {}
        for x, y in reversed(operations):
            mp[x] = mp.get(y, y)
        return [mp.get(num, num) for num in nums]
''',
    call='Solution().arrayChange([1,2,4,6], [[1,3],[3,5],[6,1]])',
    expect=[5, 2, 4, 1],
    views=[
        dict(type='array', var='nums', label='nums（原数组，不修改）', cell=100, h=170,
             pointers={'_k': 'blue'}),
        dict(type='array', var='operations', label='operations（倒着遍历）', cell=130, h=170,
             fmt=lambda v: str(v)),
        dict(type='map', var='mp', label='mp（x 最终会变成什么）', fmt=lambda k, v: f'{k} → {v}', h=150, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"`mp[{S['x']}] = mp.get({S['y']}, {S['y']})` = =={S['mp'][S['x']]}==" if 'x' in S and 'y' in S and 'mp' in S and S['x'] in S['mp'] else '')),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('num', 'num', 'orange')],
    captions={
        'mp = {}': '`mp` 记录：==被替换的数 x，最终会变成谁==',
        'for x, y in reversed': lambda S, B, ret: (f'倒着看操作：`{S.x} → {S.y}`' if S.x not in S.mp else '操作倒着看完了'),
        'mp[x] =': lambda S, B, ret: (f'`y = {S.y}` 在 `mp` 里已有记录 → `{S.y}` 之后还会变成 `{S.mp[S.y]}`，所以 `{S.x}` 直接变成 =={S.mp[S.x]}=='
                                      if S.y in B.mp else f'`y = {S.y}` 之后不再被替换，`{S.x}` 最终就是 =={S.mp[S.x]}=='),
        'return [': lambda S, B, ret: f'每个数查 `mp`：在表里就换成最终值，不在就保持不变 → `{ret}`',
    },
    cards=dict(
        one_liner='倒着处理操作，一步看穿“最终变成谁”',
        complexity='时间 `O(n+m)`，空间 `O(m)`',
        problem=['依次把 `operations[i][0]` 替换成 `operations[i][1]`',
                 '保证被换的数存在、新数不存在；返回最终数组',
                 '示例：`[1,2,4,6]`，操作 `[[1,3],[4,7],[6,1]]` → `[3,2,7,1]`；本视频换成 `[[1,3],[3,5],[6,1]]` → `[5,2,4,1]`'],
        quote='倒着遍历 operations，同时用一个哈希表 mp 将 x 映射到 mp[y] 上，如果 mp[y] 不存在则直接映射到 y 上。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['先 1→3 再 3→5：倒着来，先知道 3 最终是 5',
              '于是 1 也直接记成 5，一步到位',
              '最后遍历 `nums`，在 `mp` 里就替换，不在就不动'],
        summary=['时间 `O(n+m)`，空间 `O(m)`',
                 '方法一（正序）：哈希表记下标，依赖元素互不相同；本视频选通用的方法二',
                 '易错：倒序时用 `mp.get(y, y)`，没有记录就取 y 本身',
                 '方法二不要求 `nums` 元素互不相同，更通用'],
    ),
)
