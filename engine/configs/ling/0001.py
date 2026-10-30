def _look(S, B, ret):
    j, x, t, idx = S.j, S.x, S.target, S.idx
    need = t - x
    if not idx:
        return f'在左边找 `target − x = {t} − {x} = {need}`：`idx` 还是空的 → 找不到（==先查后存==，`{x}` 不会和自己配对）'
    if need in idx:
        return f'在左边找 `{t} − {x} = {need}`：==在 idx 里==，下标是 `{idx[need]}` → 找到了！'
    return f'在左边找 `{t} − {x} = {need}`：左边的 `{list(idx)}` 里没有 → 不成立'


def _store(S, B, ret):
    s = f'查完再存：`idx[{S.x}] = {S.j}`，留给右边的数来找'
    if S.j == 0:
        s += '（存进去之前已经查过，所以不会用到自己）'
    return s


CONFIG = dict(
    num=1, title='两数之和', difficulty='Easy', category='哈希',
    author='灵茶山艾府', technique='枚举右，维护左 · 哈希表',
    code='''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        idx = {}  # 创建一个空哈希表（字典）
        for j, x in enumerate(nums):  # x=nums[j]
            if target - x in idx:  # 在左边找 nums[i]，满足 nums[i]+x=target
                return [idx[target - x], j]  # 返回两个数的下标
            idx[x] = j  # 保存 nums[j] 和 j
''',
    call='Solution().twoSum([5,2,9,4,6], 10)',
    expect=[3, 4],
    views=[
        dict(type='text', fn=lambda S: (f"target = `{S['target']}`，当前 `x = nums[{S['j']}] = {S['x']}` → 要找 `{S['target']} − {S['x']}` = =={S['target'] - S['x']}==")
             if 'x' in S else f"target = `{S['target']}`"),
        dict(type='array', var='nums', pointers={'j': 'pink'}, h=250,
             color=lambda S, i, v: ('green' if 'idx' in S and S['target'] - S['x'] in S['idx'] and i in (S['idx'][S['target'] - S['x']], S['j'])
                                    else ('blue' if 'j' in S and i < S['j'] else None)) if 'j' in S else None,
             dim=lambda S, i, v: 'j' in S and i > S['j'],
             label='nums（蓝 = 左边已存进 idx，暗 = 还没枚举到）'),
        dict(type='map', var='idx', fmt=lambda k, v: f'{k} → {v}', font=30, h=200,
             label='idx：数值 → 下标（j 左边见过的数）'),
    ],
    watch=[('j', 'j', 'pink'), 'x', ('target - x', 'target - x', 'yellow')],
    captions={
        'idx = {}': '创建空哈希表 `idx`：==key 是数值，value 是下标==，专门记 j 左边见过的数',
        'for j, x in': lambda S, B, r: (f'枚举==右边==的数 `nums[{S.j}] = {S.x}`：把它当常量，问题变成"左边有没有 `{S.target - S.x}`"'
                                        if S.j == 0 else f'枚举右边：`j = {S.j}`，`x = {S.x}`，左边要有 `{S.target - S.x}`'),
        'if target - x in idx': _look,
        'return [': '`idx[{target - x}] = {idx[target - x]}` → 两个数的下标 `[{idx[target - x]}, {j}]`，`{nums[idx[target - x]]} + {x} = {target}`',
        'idx[x] = j': _store,
    },
    cards=dict(
        one_liner='枚举右边的数，用哈希表在左边找它的另一半',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `nums` 中找出和为 `target` 的==两个==整数，返回它们的下标',
                 '同一个元素不能用两次；保证只有一个答案',
                 '示例：`nums = [2,7,11,15], target = 9` → `[0,1]`',
                 '本视频：`nums = [5,2,9,4,6], target = 10` → `[3,4]`'],
        quote='很多涉及到「两个变量」的题目，都可以枚举其中一个变量，把它当成==常量==看待，从而转化成「一个变量」的问题。……通常来说「==枚举右，寻找左==」是更加好写的。',
        quote_src='—— 灵茶山艾府题解「总结」',
        idea=['枚举右边的 `nums[j]`，要找的左边数就固定为 `target − nums[j]`',
              '暴力每次 `O(1)` 时间只拿到 `O(1)` 信息；哈希表一次查询就知道左边 ==j 个数== 里有没有它',
              '==先查询，再存入== `nums[j]`：反过来写会把同一个元素用两次'],
        summary=['时间 `O(n)`，空间 `O(n)`：==空间换时间==',
                 '易错：先存后查 → `nums=[2,3,1], target=4` 会错误返回 `[0,0]`',
                 '暴力写法：两重循环枚举 `i < j`，时间 `O(n²)`',
                 '同套路"枚举右，维护左"：1512、219、1010、2748'],
    ),
)
