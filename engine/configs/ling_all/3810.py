def _cur(S):
    return S.get('x')


def _col(S, i, v):
    return 'orange' if i < len(S['nums']) and S['nums'][i] != S['target'][i] else None


CONFIG = dict(
    num=3810, title='变成目标数组的最少操作次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='脑筋急转弯 · 不同的 nums[i] 计数',
    tags=['贪心算法', '思维题', '难度分 1492'],
    code='''
class Solution:
    def minOperations(self, nums: List[int], target: List[int]) -> int:
        return len({x for x, t in zip(nums, target) if x != t})
''',
    call='Solution().minOperations([1,2,1,2,7,3], [3,4,5,6,7,3])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=210, label='nums', color=_col),
        dict(type='array', var='target', h=210, label='target', color=lambda S, i, v: 'green' if S['nums'][i] == S['target'][i] else None),
        dict(type='text', h=110, fn=lambda S: '橙色 = `nums[i] ≠ target[i]`：这些位置上的 ==不同 nums 值== 的个数就是答案'),
    ],
    watch=[],
    captions={
        'return len': '只数 `nums[i] != target[i]` 的位置上的 ==不同 nums[i]==：集合 `{sorted({x for x, t in zip(nums, target) if x != t})}` → ==`{ret}`== 次操作',
    },
    cards=dict(
        before=[dict(heading='逐位看例子', lines=['`nums = [1,2,1,2,7,3]`，`target = [3,4,5,6,7,3]`',
                                                  '下标 0–3 不相等，涉及的 nums 值是 `1, 2, 1, 2` → 去重得 `{1, 2}`',
                                                  '下标 4、5 已经相等，不用管 → 答案 `2`'])],
        after=[dict(heading='为什么顺序无所谓', lines=['选 `x = 1`：位置 0、2 改成 `3`、`5`', '选 `x = 2`：位置 1、3 改成 `4`、`6`',
                                                       '已经改好的位置，即使后面再被选中，也只是“改成自己”'])],
        one_liner='操作次数 = 需要改的位置上，不同的 nums 值有几种',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选整数 `x`，把 `nums` 里所有等于 `x` 的极大连续段同时改成对应的 `target` 值',
                 '求把 `nums` 变成 `target` 的最少操作次数',
                 '示例：`[1,2,3] → [2,1,3]` 答案 `2`；本视频：`[1,2,1,2,7,3]` → `[3,4,5,6,7,3]` 答案 `2`'],
        quote='所以答案的理论最小值，等于满足 nums[i] ≠ target[i] 的不同 nums[i] 的个数。这些不同元素都至少要操作一次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每次操作只会改动等于 `x` 的那些数，其他数保持不变，所以每个不同的值至少操作一次',
              '操作后的数已经等于目标，再被选中也只是“改成自己”，==顺序任意==',
              '等价于“删掉”：选 `x`，所有等于 `x` 的、要改的位置就处理完了'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '只收集 `nums[i] != target[i]` 的位置；相等的位置不用管',
                 '下界就是上界：不同值可以按任意顺序操作，所以直接返回集合大小',
                 '「极大连续段」的限制看着复杂，实际上没有影响'],
    ),
)
