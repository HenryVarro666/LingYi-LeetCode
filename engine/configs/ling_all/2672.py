def _col(S, i, v):
    if 'i' not in S or '_inner' not in S or 'c' not in S['_inner']:
        return None
    k = S['i']
    if i == k:
        return 'yellow'
    if i in (k - 1, k + 1) and v and v == S['a'][k]:
        return 'green'
    return None


CONFIG = dict(
    num=2672, title='有相同颜色的相邻元素数目', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 增量维护相邻对数',
    tags=[],
    code='''
class Solution:
    def colorTheArray(self, n: int, queries: List[List[int]]) -> List[int]:
        ans = []
        a, cnt = [0] * (n + 2), 0  # 避免讨论下标出界的情况
        for i, c in queries:
            i += 1  # 下标改成从 1 开始
            if a[i]: cnt -= (a[i] == a[i - 1]) + (a[i] == a[i + 1])
            a[i] = c
            cnt += (a[i] == a[i - 1]) + (a[i] == a[i + 1])
            ans.append(cnt)
        return ans
''',
    call='Solution().colorTheArray(4, [[0,2],[1,2],[3,1],[1,1],[2,1]])',
    expect=[0, 1, 1, 0, 2],
    views=[
        dict(type='text', fn=lambda S: f"染色前后：位置 `{S['i']}` 颜色 `{S['a'][S['i']]}`，相邻对数 =={S['cnt']}==" if 'i' in S and '_inner' in S and 'c' in S['_inner'] else ''),
        dict(type='array', var='a', pointers={'i': 'blue'}, color=_col, h=200, label='a（两端各补一个 0 当哨兵）'),
        dict(type='array', var='ans', h=130, label='ans'),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'pink'), ('cnt', 'cnt', 'green')],
    captions={
        'a, cnt = [0]': '`a` 两端各补一格哨兵 0，查邻居不用判断下标出界；`cnt` = 相邻同色对数',
        'for i, c in queries': lambda S, B, r: ('查询都处理完了，退出循环' if len(S.ans) == len(S.queries)
                                                 else f'取出一个查询：把下标 `{S.i}` 染成颜色 `{S.c}`'),
        'i += 1': '下标整体右移一位，`i` = =={i}==（对应 a 里的位置）',
        'if a[i]': lambda S, B, r: (f'`a[{S.i}] = {S.a[S.i]}` 已经有色：减去旧影响，左 `{S.a[S.i]} == {S.a[S.i-1]}`、右 `{S.a[S.i]} == {S.a[S.i+1]}` → `cnt` = =={S.cnt}=='
                                    if S.a[S.i] else f'`a[{S.i}] = 0` 还没染色，不可能有相同颜色的对，不用减'),
        'cnt -= ': '去掉旧影响：左 `{a[i]} == {a[i-1]}`，右 `{a[i]} == {a[i+1]}` → `cnt` = =={cnt}==',
        'a[i] = c': '改色：`a[{i}]` = =={c}==',
        'cnt += ': '加上新影响：左 `{a[i]} == {a[i-1]}`，右 `{a[i]} == {a[i+1]}` → `cnt` = =={cnt}==',
        'ans.append': '记下这次查询后的答案 =={cnt}==',
        'return ans': '全部查询处理完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='先扣掉旧颜色的影响，改色后再加上新颜色的影响',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`n` 个格子初始为 0（未染色），依次执行染色查询 `[index, color]`',
                 '每次染色后，统计相邻且同色的格子对数',
                 '示例：`n=4`，查询 `[[0,2],[1,2],[3,1],[1,1],[2,1]]` → `[0,1,1,0,2]`'],
        quote='由于每次修改只会影响当前元素与其左右元素的关系，所以模拟即可。代码实现时，可以先去掉当前元素对 cnt 的影响，修改颜色后，再加上当前元素对 cnt 的影响。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一次染色只动一个格子，只会改变它和左右邻居的两对关系',
              '先减后加：旧颜色的相同对减掉，新颜色的相同对加上',
              '数组两头补哨兵 0，`a[i-1]`、`a[i+1]` 永远不越界'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '易错点：未染色（0）的格子不能参与「减」，所以先判断 `if a[i]`',
                 '哨兵 0 不会和真实颜色（≥ 1）相等，所以不影响计数',
                 '作者的思考题：求最长连续同色长度，可以用并查集等方法'],
    ),
)
