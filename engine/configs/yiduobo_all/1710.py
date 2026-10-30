CONFIG = dict(
    num=1710, title='卡车上的最大单元数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='按单元数降序 · 贪心装车',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maximumUnits(self, boxTypes, truckSize):

        res = 0
        for number, unit in sorted(boxTypes, key=lambda d:d[1], reverse=True):
            if truckSize >= number:
                res += number * unit
                truckSize -= number
            else:
                res += truckSize * unit
                break
        
        return res
''',
    call='Solution().maximumUnits([[1,3],[2,2],[3,1],[4,5]], 6)',
    expect=25,
    views=[
        dict(type='array', var=lambda S: sorted(S['boxTypes'], key=lambda d: d[1], reverse=True), label='按单元数降序后的 boxTypes = [箱数, 每箱单元数]', cell=130, h=250,
             fmt=lambda v: f'{v[0]}箱×{v[1]}' if hasattr(v, '__len__') else str(v),
             color=lambda S, i, v: ('green' if 'number' in S and v == [S['number'], S['unit']] else None)),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"卡车剩余 `truckSize = {S['truckSize']}`；已装 `res = {S['res']}` 个单元" if 'res' in S else '')),
    ],
    watch=[('number', 'number', 'blue'), ('unit', 'unit', 'pink'), ('truckSize', 'truckSize', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计装上车的单元总数',
        'for number, unit in sorted': lambda S, B, r: (f'下一种：`{S.number}` 箱，每箱 `{S.unit}` 单元（按单元数从大到小）' if 'number' in S else ''),
        'if truckSize >= number': lambda S, B, r: (f'剩余 `{S.truckSize}` ≥ `{S.number}` 箱：这种箱子能==全部装下==' if S.truckSize >= S.number
                                                  else f'剩余 `{S.truckSize}` < `{S.number}` 箱：只能装一部分'),
        'res += number * unit': '全装：`{number} × {unit}` = {number * unit} → `res = {res}`',
        'truckSize -= number': '车上位置用掉 `{number}` → 剩 `{truckSize}`',
        'res += truckSize * unit': '位置不够，只装 `{truckSize}` 箱：`{truckSize} × {unit}` = {truckSize * unit} → `res = {res}`',
        'break': '卡车装满了，不用再看后面单元数更少的箱子',
        'return res': '最多装 =={ret}== 个单元',
    },
    cards=dict(
        one_liner='每个箱子占的位置一样：单元数多的先装',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`boxTypes[i] = [箱数, 每箱单元数]`，卡车最多装 `truckSize` 个箱子',
                 '每个箱子占一个位置，求能装的单元总数最大值',
                 '本视频：`[[1,3],[2,2],[3,1],[4,5]]`，`truckSize = 6` → `25`'],
        quote='由于选择每种箱子的代价都一样，那么显然应该优先选择units多的箱子。于是可以将箱子按照units从大到小进行排序，一趟扫描。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个箱子都占 1 个位置，所以谁单元数多就先装谁',
              '按 `unit` 降序遍历：装得下就整种装完；装不下就用剩余位置装一部分',
              '剩余位置一用完立刻 `break`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：排序的关键字是单元数 `d[1]`，不是箱数 `d[0]`',
                 '装不下整种时，只装 `truckSize` 个，然后直接退出',
                 '原文已是可直接运行的写法，无需改动'],
    ),
)
