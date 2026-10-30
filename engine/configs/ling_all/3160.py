CONFIG = dict(
    num=3160, title='所有球里面不同颜色的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='两个哈希表：球色 + 颜色计数',
    code='''
class Solution:
    def queryResults(self, _: int, queries: List[List[int]]) -> List[int]:
        ans = []
        color = {}
        cnt = defaultdict(int)
        for x, y in queries:
            if x in color:
                c = color[x]
                cnt[c] -= 1
                if cnt[c] == 0:
                    del cnt[c]
            color[x] = y
            cnt[y] += 1
            ans.append(len(cnt))
        return ans
''',
    call='Solution().queryResults(4, [[1,4],[2,5],[1,3],[3,4],[2,4]])',
    expect=[1, 2, 2, 3, 2],
    views=[
        dict(type='map', var='color', label='color：球号 → 颜色', fmt=lambda k, v: f'球{k}: 色{v}', h=170, font=30),
        dict(type='map', var='cnt', label='cnt：颜色 → 球数（键的个数 = 答案）', fmt=lambda k, v: f'色{k}: {v}个', h=170, font=30),
        dict(type='array', var='ans', label='ans', h=130),
    ],
    watch=['x', 'y', 'c', ('ans', 'ans', 'green')],
    captions={
        'if x in color': '球 `{x}` {"已经有颜色了 → 要先把旧颜色的计数减掉" if x in color else "还没染过色 → 不用减旧颜色"}',
        'c = color[x]': '球 `{x}` 的旧颜色是 `{c}`',
        'cnt[c] -= 1': '旧颜色 `{c}` 少了一个球：`cnt[{c}]` = {cnt[c]}',
        'if cnt[c] == 0': '`cnt[{c}] == 0` → {"没球用这个颜色了，从 cnt 删掉，颜色数才会减少" if cnt[c] == 0 else "还有球是这个颜色，保留"}',
        'del cnt[c]': '删除颜色 `{c}`：颜色种数 -1',
        'color[x] = y': '球 `{x}` 染成颜色 `{y}`',
        'cnt[y] += 1': '新颜色 `{y}` 多了一个球：`cnt[{y}]` = {cnt[y]}',
        'ans.append': '`cnt` 里有几个键就有几种颜色 → 追加 ==`{len(cnt)}`==',
    },
    cards=dict(
        one_liner='cnt 里还剩几种颜色，答案就是几',
        complexity='时间 `O(q)`，空间 `O(q)`',
        problem=['有 `limit+1` 个球，一开始都没颜色',
                 '每次 `[x, y]` 把球 `x` 染成颜色 `y`，求每次操作后的颜色种数',
                 '示例：`[[1,4],[2,5],[1,3],[3,4]]` → `[1,2,2,3]`',
                 '本视频多加一步 `[2,4]` → `[1,2,2,3,2]`'],
        quote='用哈希表 color 维护第 x 个球的颜色，哈希表 cnt 维护每种颜色的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`limit` 可达 `10^9`，不能开数组，用字典只记染过色的球',
              '重染：先把旧颜色的计数减一，减到 0 就删掉这个键',
              '再给新颜色计数加一，`len(cnt)` 就是颜色种数'],
        summary=['时间 `O(q)`，空间 `O(q)`',
                 '易错点：旧颜色计数减到 0 必须 `del`，否则 `len` 会多算',
                 '`limit` 参数用不上，所以代码里写成 `_`',
                 '同色重染（旧色 == 新色）也成立：先减后加，结果不变'],
    ),
)
