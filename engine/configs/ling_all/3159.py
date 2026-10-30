CONFIG = dict(
    num=3159, title='查询数组中元素的出现位置', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='预处理下标 + 查表',
    code='''
class Solution:
    def occurrencesOfElement(self, nums: List[int], queries: List[int], x: int) -> List[int]:
        pos = [i for i, num in enumerate(nums) if num == x]
        return [-1 if q > len(pos) else pos[q - 1] for q in queries]
''',
    call='Solution().occurrencesOfElement([1,3,1,7,1], [1,3,2,4], 1)',
    expect=[0, 4, 2, -1],
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 等于 x）', pointers={'i': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if v == S['x'] else None),
        dict(type='array', var='pos', label='pos（x 出现的下标，按顺序）', h=150),
        dict(type='array', var='queries', label='queries', h=150),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"查询 `q = {S['q']}`：pos 长 {len(S['pos'])}，" + ('==不够长 → -1==' if S['q'] > len(S['pos']) else f"取 `pos[{S['q']-1}]` = =={S['pos'][S['q']-1]}=="))
             if 'q' in S and 'pos' in S and isinstance(S['q'], int) else '第 q 个 x 的下标 = pos[q-1]'),
    ],
    watch=['x', ('pos', 'pos', 'green')],
    captions={
        'pos = [': '扫一遍 nums，把等于 `x = {x}` 的下标按顺序收进 `pos` → =={pos}==',
        'return [': '每个询问 `q`：`q > len(pos)` 就不存在第 q 个 x → -1，否则答案是 `pos[q-1]`（第 q 个对应下标 q-1）',
    },
    cards=dict(
        one_liner='先把所有 x 的下标收好，第 q 个 x 就是 pos[q-1]',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['给 `nums`、`queries`、`x`；每个 `q` 问：第 `q` 个 `x` 的下标是多少',
                 '出现次数不足 `q` 则答案为 `-1`',
                 '示例：`[1,3,1,7]`，`queries=[1,3,2,4]`，`x=1` → `[0,-1,2,-1]`',
                 '本视频：`[1,3,1,7,1]` → `[0,4,2,-1]`'],
        quote='用 pos 数组记录所有等于 x 的 nums[i] 的下标 i。对于每个询问 q，如果 q 大于 pos 的长度，则答案为 -1，否则答案为 pos[q-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['询问很多，不要每次都重新扫 `nums`', '一次预处理：==按顺序收集 x 的所有下标==', '之后每个询问 `O(1)` 查表'],
        after=[dict(heading='逐个询问（本例）', lines=['`pos = [0, 2, 4]`，长度 3',
               '`q=1` → `pos[0]` = 0；`q=3` → `pos[2]` = 4', '`q=2` → `pos[1]` = 2；`q=4` > 3 → -1',
               '每个询问都是 `O(1)`，答案 `[0, 4, 2, -1]`']),
               dict(heading='为什么要预处理', lines=['暴力：每个询问都扫一遍 `nums`，`O(nq)`', '预处理：只扫一遍 `nums`，之后查表', '`n, q` 都到 `10^5`，只有后者能过'])],
        summary=['时间 `O(n+q)`，空间 `O(n)`（返回值不计）',
                 '易错点：第 `q` 个对应 `pos[q-1]`，下标从 0 开始',
                 '判断是 `q > len(pos)` 而不是 `>=`',
                 '两处都用列表推导式，一行写完'],
    ),
)
