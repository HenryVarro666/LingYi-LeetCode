def _win(S):
    if 'i' not in S or 'j' not in S:
        return ''
    return f"当前子数组 `{S['nums'][S['i']:S['j'] + 1]}`，其中能被 `p` 整除的有 ==`{S.get('cnt', 0)}`== 个（上限 `k = {S['k']}`）"


CONFIG = dict(
    num=2261, title='含最多 K 个可整除元素的子数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举子数组 + 元组哈希去重',
    tags=['灵神题单·常用数据结构', '灵神题单·字符串'],
    code='''
class Solution:
    def countDistinct(self, nums: List[int], k: int, p: int) -> int:
        s, n = set(), len(nums)
        for i in range(n):
            cnt = 0
            for j in range(i, n):
                if nums[j] % p == 0:
                    cnt += 1
                    if cnt > k:
                        break
                s.add(tuple(nums[i: j + 1]))
        return len(s)
''',
    call='Solution().countDistinct([2, 3, 3, 2], 1, 2)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=150, pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'),
             color=lambda S, i, v: 'orange' if v % S['p'] == 0 else None),
        dict(type='set', var='s', label='s（已收集的不同子数组）', fmt=lambda x: str(list(x)), h=300),
        dict(type='text', h=60, size=26, fn=_win),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cnt', 'cnt', 'orange'), ('len(s)', lambda S: len(S['s']), 'green')],
    captions={
        's, n = set(), len(nums)': '`s` 存放所有合格的子数组（转成元组才能放进集合），自动去重',
        'for i in range(n)': lambda S, B, r: (f'枚举左端点 `i = {S.i}`' if S.i != B.get('i', -1) else '所有左端点都枚举完了'),
        'cnt = 0': '换新的左端点，可整除元素的个数 `cnt` 清零',
        'for j in range(i, n)': lambda S, B, r: (f'右端点 `j = {S.j}`：子数组 `{S.nums[S.i:S.j+1]}`' if not (S.j == B.get('j') and S.i == B.get('i') and (B.get('cnt', 0) > 0 or S.j > S.i))
                                                 else f'`j` 到头了，左端点 `i = {S.i}` 枚举完'),
        'if nums[j] % p == 0': '`nums[{j}] % {p} = {nums[j] % p}` → ' + '{"==能被整除==" if nums[j] % p == 0 else "不能被整除，不计数"}',
        'cnt += 1': '多了一个可整除元素：`cnt` = {cnt}',
        'if cnt > k': lambda S, B, r: f'`cnt = {S.cnt}` 和 `k = {S.k}` 比：' + ('超过上限 → ==break==，右端点再往右只会更多' if S.cnt > S.k else '没超过，子数组合格'),
        'break': '这个左端点不能再往右延伸了，换下一个 `i`',
        's.add(tuple': lambda S, B, r: (f'`{list(S.nums[S.i:S.j+1])}` 合格：加入集合 → `len(s) = {len(S.s)}`' if len(S.s) > len(B.s)
                                         else f'`{list(S.nums[S.i:S.j+1])}` 合格，但集合里==已经有了==，不重复计数 → `len(s) = {len(S.s)}`'),
        'return len(s)': '集合里不同子数组一共 `{len(s)}` 个',
    },
    skip=[],
    max_steps=90,
    cards=dict(
        one_liner='数据范围小：枚举所有子数组，合格的转元组放进集合去重',
        complexity='时间 `O(n³)`（切片和哈希），空间 `O(n³)`',
        problem=['`nums`、`k`、`p`：数出「最多含 `k` 个能被 `p` 整除的元素」的==不同==子数组个数',
                 '内容相同的子数组只算一次，例如两个 `[2]` 只计一次',
                 '本视频：`nums=[2,3,3,2]`，`k=1`，`p=2` → `7`'],
        quote='if cnt > k: break　　s.add(tuple(nums[i: j + 1]))　　return len(s)',
        quote_src='—— 灵茶山艾府题解代码（原文只有代码，无文字）',
        idea=['固定左端点 `i`，右端点 `j` 向右扩，`cnt` 单调不减，超过 `k` 就停',
              '`nums[i:j+1]` 是列表不能哈希，转成 `tuple` 再放进 `set`',
              '题目进阶要 `O(n²)`：用字典树或字符串哈希，这里是最直接的暴力写法'],
        summary=['时间 `O(n³)`，空间 `O(n³)`；`n ≤ 200` 能过',
                 '`cnt` 要在每个新 `i` 处清零',
                 '先判断 `cnt > k` 再 `add`：超限的子数组不能加进集合',
                 '切片 `nums[i: j+1]` 右端点要 +1'],
    ),
)
