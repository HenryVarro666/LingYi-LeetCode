CONFIG = dict(
    num='LCP 39', title='无人机方阵', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 能配对的颜色先抵掉',
    tags=[],
    code='''
class Solution(object):
    def minimumSwitchingTimes(self, source, target):

        cnt = {}
        n = len(source)
        m = len(source[0])
        for i in range(n):
            for j in range(m):
                cnt[source[i][j]] = cnt.get(source[i][j], 0) + 1
        
        res = 0
        for i in range(n):
            for j in range(m):
                if cnt.get(target[i][j], 0) > 0:
                    cnt[target[i][j]] -= 1
                else:
                    res += 1
        
        return res
''',
    call='Solution().minimumSwitchingTimes([[1,2,2],[3,4,4]], [[2,4,9],[1,4,3]])',
    expect=1,
    skip=['n = len', 'm = len'],
    views=[
        dict(type='grid', var='source', label='source（蓝框 = 当前格）', cell=90, h=230,
             cursors=[('i if _line <= 10 else None', 'j', 'blue')]),
        dict(type='grid', var='target', label='target（蓝框 = 当前格）', cell=90, h=230,
             cursors=[('i if _line >= 12 else None', 'j', 'blue')]),
        dict(type='map', var='cnt', label='cnt（source 里还没被配走的数量）', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '位置可以任意调，等价于问两个矩阵有==多少个数字不一样==；先用 `cnt` 数 source 里每种颜色',
        'for i in range(n)': lambda S, B, r: (f'第 `{S.i}` 行' if 'i' not in B or S.i != B.i else '所有行都扫完了'),
        'for j in range(m)': lambda S, B, r: (f'第 `{S.j}` 列' if 'j' not in B or S.j != B.j or S.i != B.i else '这一行扫完了'),
        'cnt[source[i][j]] =': '`source[{i}][{j}] = {source[i][j]}` 计数 → `cnt[{source[i][j]}] = {cnt[source[i][j]]}`',
        'res = 0': 'source 统计完：`{cnt}`。接着看 target，`res` 记要换色的数量',
        'if cnt.get(target[i][j], 0) > 0': lambda S, B, r: (
            f'`target[{S.i}][{S.j}] = {S.target[S.i][S.j]}`：source 里还剩 {S.cnt.get(S.target[S.i][S.j], 0)} 个'
            + ('，能配对' if S.cnt.get(S.target[S.i][S.j], 0) > 0 else '，没有了 → 这个位置得换色')),
        'cnt[target[i][j]] -= 1': '配走一个：`cnt[{target[i][j]}] = {cnt[target[i][j]]}`',
        'res += 1': '配不上，必须有一架无人机换成 `{target[i][j]}`：`res = {res}`',
        'return res': '一共 `{res}` 架要换色',
    },
    cards=dict(
        one_liner='把 target 里的颜色去 source 里配对，配不上的个数就是答案',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['两个 `n×m` 颜色矩阵 `source`、`target`，无人机位置可随意调整',
                 '求最少需要切换几架无人机的灯光颜色',
                 '本视频：`[[1,2,2],[3,4,4]]` → `[[2,4,9],[1,4,3]]`，答案 `1`'],
        quote='由于题目中的无人机可以任意调整位置，那么实际上问的就是两个矩阵中有多少个不一样的数字。',
        quote_src='—— yiduobo 题解原文',
        idea=['先遍历 source，哈希表统计每种颜色的个数',
              '再遍历 target：哈希表里该颜色次数大于 0，就减一（配对成功）',
              '否则 `res` 加一：这个位置只能靠换色得到'],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '易错：用 `cnt.get(x, 0)`，target 里的颜色 source 可能完全没有',
                 '与灵神对比：yiduobo 直接数配不上的个数，不需要最后除以 2',
                 '代码未做修改（原文已可在 Python 3 运行）'],
    ),
)
