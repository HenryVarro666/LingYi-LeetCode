CONFIG = dict(
    num=2870, title='使数组为空的最少操作次数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='计数 + 分类讨论',
    tags=['贪心与思维', '数学贪心', '难度分 1392'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        if 1 in cnt.values():
            return -1
        return sum((c + 2) // 3 for c in cnt.values())
''',
    call='Solution().minOperations([2,3,3,2,2,4,2,3,4])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', h=200),
        dict(type='map', var='cnt', label='cnt：每个数出现次数 c', fmt=lambda k, v: f'{k}: {v}次', h=280),
        dict(type='text', h=120, size=30, fn=lambda S: ' + '.join(f"(c+2)//3 = ({c}+2)//3 = {(c+2)//3}" for c in S['cnt'].values()) if 'cnt' in S else ''),
    ],
    watch=[('cnt', 'dict(cnt)', 'cyan')],
    captions={
        'cnt = Counter': '统计每个数的出现次数 `c`：`{dict(cnt)}`',
        'if 1 in cnt.values()': lambda S, B, r: ('有数只出现 1 次，两种操作都凑不出 → 无法清空' if 1 in S.cnt.values()
                                              else '没有出现 1 次的数 → 每个数都能删完'),
        'return -1': '`c = 1` 无法操作，返回 `-1`',
        'return sum': lambda S, B, r: f"c 模 3 为 0/1/2 都需要 `ceil(c/3)` 次：{' + '.join(str((c+2)//3) for c in S.cnt.values())} = =={r}==",
    },
    cards=dict(
    after=[dict(heading='三种余数怎么拆', lines=['`c = 6`：`3 + 3`，2 次', '`c = 7`：`3 + 2 + 2`，3 次（c-4 是 3 的倍数，再补 4）', '`c = 8`：`3 + 3 + 2`，3 次（c-2 是 3 的倍数，再补 2）', '统一写成 `(c+2)//3`']),
           dict(heading='和 2244 的关系', lines=['2244 把「任务」换成了「数」，把「轮」换成「操作」', '代码一字不差，也是 `cnt = Counter(...)`', '看懂其中一道就会另一道'])],
        one_liner='每个数出现 c 次，需要 ceil(c/3) 次操作',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次可删除 2 个或 3 个==相等==的元素，求清空数组的最少操作次数，做不到返回 `-1`',
                 '示例：`[2,3,3,2,2,4,2,3,4]` → `4`'],
        quote='如果 c 模 3 为 1，那么 c=(c-4)+4，其中 c-4 是 3 的倍数，剩余的 4 可以用两次操作完成。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先统计每个数的出现次数 `c`，各个数互不影响',
              '`c = 1` 无解；模 3 余 0 / 1 / 2：拆成若干个 3，再补一个 4（两个 2）或一个 2',
              '总的来说都是 `ceil(c/3) = (c+2)//3`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`c = 1` 要先返回 `-1`',
                 '与 2244 题完全相同，只是换了题面',
                 '`(c+2)//3` 等价于向上取整'],
    ),
)
