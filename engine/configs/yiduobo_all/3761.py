def _txt(S):
    if 'r' in S and S.get('_line') in (11, 12, 13):
        return f"逐位反转：`r = {S['r']}`，剩余 `v = {S['v']}`"
    if 'index' not in S:
        return '`last`：前缀中每个数==反转后==最后一次出现的位置'
    i, x = S['index'], S['nums'][S['index']]
    if x in S['last'] and S['last'][x] < i:
        return f"`last[{x}] = {S['last'][x]}`：候选距离 `{i} − {S['last'][x]}` = =={i - S['last'][x]}=="
    return f"`nums[{i}] = {x}` 不在 `last` 中，没有可配对的左端"


CONFIG = dict(
    num=3761, title='镜像对之间最小绝对距离', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 · 哈希表记最后位置',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1669'],
    code='''
class Solution(object):
    def minMirrorPairDistance(self, nums):

        last = {}
        res = -1
        for index, v in enumerate(nums):
            if v in last and (res == -1 or res > index - last[v]):
                res = index - last[v]

            r = 0
            while v:
                r = r * 10 + v % 10
                v //= 10
            last[r] = index

        return res
''',
    call='Solution().minMirrorPairDistance([45,120,54,21,12])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（index = 当前位置）', pointers={'index': 'blue'}, h=210,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='map', var='last', label='last：reverse(nums[p]) → 最后位置 p',
             fmt=lambda k, v: f'{k} → {v}', h=170, font=34),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=[('index', 'index', 'blue'), 'v', ('r', 'r', 'orange'), ('res', 'res', 'green')],
    skip=['r = 0', 'v //= 10'],
    max_steps=60,
    captions={
        'last = {}': '`last`：前缀中每种元素==反转后==最后一次出现的位置',
        'res = -1': '`res = -1`：既是初值，也表示「还没有镜像对」',
        'for index, v in': lambda S, B, r: (f'遍历到 `index = {S.index}`，`v = {S.v}`' if 'index' not in B or S.index != B.index else '遍历结束'),
        'if v in last and': lambda S, B, r: (
            (f'`last[{S.v}] = {S.last[S.v]}`，距离 `{S.index - S.last[S.v]}` 比 `res = {S.res}` 更优 → 更新' if (S.res == -1 or S.res > S.index - S.last[S.v])
             else f'`last[{S.v}] = {S.last[S.v]}`，但距离 `{S.index - S.last[S.v]}` 不比 `res = {S.res}` 小 → 不更新')
            if S.v in S.last else f'`{S.v}` 不在 `last` 中：前面没有数反转后等于它'),
        'res = index - last[v]': '`res = {index} − {last[v]}` = =={res}==',
        'while v:': lambda S, B, r: (f'`v = {S.v}` 还有数位，继续反转' if S.v else f'`v` 变成 0，反转完成：`r = {S.r}`'),
        'r = r * 10': '取出末位 `{v % 10}` 接到 r 后面：`r = {r}`，再 `v //= 10` 去掉末位',
        'v //= 10': '去掉末位：`v = {v}`',
        'last[r] = index': lambda S, B, r: (f'`{S.r}` 已在表中，更新为更靠后的位置 `{S.index}`（距离只会更短）' if S.r in B.last
                                            else f'记录 `last[{S.r}] = {S.index}`，等右边的 `{S.r}` 来配对'),
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先用 last[v] 更新答案，再记下 reverse(v) 的位置',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['镜像对 `(i, j)`：`i < j` 且 `reverse(nums[i])` 与 `nums[j]` 相等',
                 '反转忽略前导零，如 `reverse(120) = 21`；求最小距离，没有返回 `-1`',
                 '本视频：`[45,120,54,21,12]` → `1`'],
        quote='使用哈希表last记录前缀中每种元素反转后最后一次出现的位置。对于当前遍历到的index，先使用index - last[nums[index]]更新答案，然后将last[reverse(nums[index])]更新为index即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个 index，要找前面 ==最大的 p== 满足 `reverse(nums[p]) = nums[index]`',
              '所以表里只存「最后一次出现」的位置',
              '反转用 `% 10` 与 `//= 10` 逐位完成，前导零自然消失'],
        summary=['时间 `O(n log U)`，空间 `O(n)`',
                 '`res = -1` 兼作「未找到」标记，更新条件要写 `res == -1 or res > …`',
                 '顺序：==先查询，再写入== `last`，避免 `i = j`',
                 '原文已用 `//=` 做整除，代码无需修改即可在 Python 3 运行'],
    ),
)
