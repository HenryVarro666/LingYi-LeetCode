CONFIG = dict(
    num=2424, title='最长上传前缀', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='集合 + 单调递增指针',
    tags=[],
    code='''
class LUPrefix:
    def __init__(self, n: int):
        self.x = 1
        self.s = set()

    def upload(self, video: int) -> None:
        self.s.add(video)

    # 时间复杂度：均摊 O(1)
    def longest(self) -> int:
        while self.x in self.s:
            self.x += 1
        return self.x - 1
''',
    call='''server = LUPrefix(5)
res = []
server.upload(3)
res.append(server.longest())
server.upload(1)
res.append(server.longest())
server.upload(2)
res.append(server.longest())
server.upload(5)
res.append(server.longest())
res''',
    expect=[0, 1, 3, 3],
    views=[
        dict(type='set', var='self.s', label='已上传的视频 s', fmt=lambda x: str(x), h=110),
        dict(type='text', size=32, fn=lambda S: (f"`x = {S['self.x']}`：视频 1 ~ {S['self.x'] - 1} 都已上传" if S['self.x'] > 1 else "`x = 1`：还没确认任何视频") if 'self.x' in S else ''),
    ],
    watch=[('self.x', 'self.x', 'blue'), 'res'],
    captions={
        'self.x = 1': '`x` 表示「下一个要确认的视频编号」，初始是 1',
        'self.s = set()': '`s` 存放所有已上传的视频',
        'self.s.add': '上传视频 `{video}` → 只记进集合，不急着算前缀',
        'while self.x in self.s': lambda S, B, r: (f'`x = {S["self.x"]}` 在 `s` 中 → 前缀还能延长' if S['self.x'] in S['self.s']
                                                    else f'`x = {S["self.x"]}` 不在 `s` 中 → 视频 {S["self.x"]} 还没传，前缀到此为止'),
        'self.x += 1': '视频 `{self.x - 1}` 已经上传 → `x` 后移到 =={self.x}==（前缀只增不减，所以不用回头）',
        'return self.x - 1': '最长上传前缀 = `x - 1` = =={ret}==',
    },
    cards=dict(
        one_liner='前缀只会变长不会变短，用一个变量 x 往后推',
        complexity='`longest` 均摊 `O(1)`，`upload` `O(1)`，空间 `O(n)`',
        problem=['依次上传编号 `1~n` 的视频（顺序任意）', '`longest()`：返回最大的 `i`，使 `1~i` 全部已上传',
                 '本视频：`n=5`，上传 3、1、2、5，每次后问 `longest`'],
        quote='由于最长上传前缀不会减小，因此用一个变量 x 维护即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['上传只往集合里加元素，所以最长前缀单调不减',
              '`x` 指向第一个「可能没上传」的视频，查询时只要 `x` 在集合里就右移',
              '`x` 总共最多移动 `n` 步，均摊下来每次 `O(1)`'],
        summary=['均摊 `O(1)`：`x` 一共最多走 `n` 步，不会重复扫描',
                 '返回的是 `x - 1`，因为 `x` 停在第一个没传的视频上',
                 '易错：不要每次查询都从 1 开始数，会退化成 `O(n)`'],
    ),
)
