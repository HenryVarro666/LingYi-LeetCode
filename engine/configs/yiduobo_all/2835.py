def _txt(S):
    nl = S.get('num_list')
    if nl is None:
        return ''
    t = S.get('target')
    return f"要凑的幂：`{nl}`　当前 target = =={t}==　可用小数之和 s = =={S.get('s', 0)}=="


CONFIG = dict(
    num=2835, title='使子序列的和等于目标的最少操作次数', difficulty='Hard', category='位运算',
    author='yiduobo', technique='拆 target 的幂 · 排序后逐个适配', tags=['位运算', '贪心与思维', '难度分 2207'],
    code='''
class Solution(object):
    def minOperations(self, nums, target):

        if sum(nums) < target:
            return -1

        v = target
        num_list = []
        while v:
            num_list.append(v & -v)
            v -= num_list[-1]
        
        nums.sort()
        p = 0
        res = 0
        s = 0
        for target in num_list:
            while p < len(nums) and nums[p] <= target:
                s += nums[p]
                p += 1

            if s >= target:
                s -= target
            else:
                x = nums[p]
                while x != target:
                    res += 1
                    x >>= 1
                s += nums[p] - target
                p += 1
        
        return res
''',
    call='Solution().minOperations([1,32,1,2], 12)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'p': 'blue'}, label='nums（排序后，p 指向下一个没用的数）', h=230,
             dim=lambda S, i, v: 'p' in S and i < S['p']),
        dict(type='array', var='num_list', label='num_list（target 拆出的 2 的幂）', h=150),
    ],
    watch=[('p', 'p', 'blue'), ('s', 's', 'cyan'), ('res', 'res', 'green'), 'target'],
    captions={
        'sum(nums) < target': '总和都不够就不可能：`{sum(nums)} < {target}` → 不成立，继续',
        'num_list.append': '`v & -v` 取出最低位的 1：加入 `{num_list[-1]}`',
        'v -= num_list[-1]': '去掉这一位，`v` = {v}',
        'nums.sort()': '把 `nums` 从小到大排好：`{nums}`',
        'for target in num_list': '逐个适配 target 里的幂：当前要凑 =={target}==',
        'while p < len(nums) and nums[p] <= target': lambda S, B, r: (
            f'`nums[{S.p}] = {S.nums[S.p]} <= {S.target}`：不超过它的数都能拿来凑' if S.p < len(S.nums) and S.nums[S.p] <= S.target
            else f'没有更多 ≤ {S.target} 的数了，凑数用的 `s` = {S.s}'),
        's += nums[p]\n': '累加到 `s`：`s` = =={s}==',
        'p += 1\n': '`p` → {p}',
        'if s >= target': '`s = {s}` 与 `target = {target}`：' + '{"够，小数和能直接凑出" if s >= target else "不够，必须拆下一个数"}',
        's -= target': '用掉 `{target}`：`s` 剩 =={s}==',
        'x = nums[p]': '要拆 `nums[{p}] = {nums[p]}`',
        'res += 1': '拆一次：`x` 对半，`res` → =={res}==',
        'x >>= 1': '`x` 对半 → {x}',
        's += nums[p] - target': '拆出 `{target}` 后，剩下的连续前导 1 都留给后面：`s` += {nums[p]} − {target} → =={s}==',
        'p += 1': '`p` → {p}',
        'return res': '最少操作 `{res}` 次',
    },
    cards=dict(
        one_liner='把 target 拆成 2 的幂，小数凑不够就拆下一个大数',
        complexity='时间 `O(n log n)`，空间 `O(log target)`',
        problem=['`nums` 全是 2 的幂；一次操作把 `>1` 的数拆成两个一半',
                 '求最少操作次数使某子序列和为 `target`，不可能返回 -1',
                 '示例：`[1,32,1,2]`，`target=12` → `2`'],
        quote='若当前所有小于等于v的数之和s大于v，那么一定存在一种方法从中选出部分数，使得这些数之和恰好等于v。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `target` 按二进制拆成 2 的幂，从小到大逐个适配',
              '拆一个 `2^k` 来凑 `v`：剩下的部分正好覆盖 v 到 2^k 之间所有的幂',
              '二进制加法都是 2 的幂，不会越级进位：`s ≥ v` 就一定凑得出'],
        summary=['时间排序 `O(n log n)`，空间 `O(log target)`',
                 '先 `sum(nums) < target` 判无解，保证 `nums[p]` 不越界',
                 '拆大数后剩余部分全并入 `s`',
                 '对比灵神：灵神用 Counter 按位扫描，yiduobo 排序后用双指针'],
    ),
)
