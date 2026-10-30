CONFIG = dict(
    num=898, title='子数组按位或操作', difficulty='Medium', category='位运算',
    author='yiduobo', technique='哈希表保存以当前数结尾的所有 OR',
    tags=['难度分 2133'],
    code='''
class Solution(object):
    def subarrayBitwiseORs(self, arr):

        res = set()
        now = set([0])
        for num in arr:
            now = {x | num for x in now}
            now.add(num)
            for x in now:
                if x not in res:
                    res.add(x)
        return len(res)
''',
    call='Solution().subarrayBitwiseORs([1,2,1,4])',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"处理 `{S['num']}`：`now` 是 ==所有以它结尾的子数组 OR=="
                                        if 'num' in S else '')),
        dict(type='array', var='arr', h=170),
        dict(type='set', var='now', fmt=lambda x: str(x), h=170, label='now（以当前数结尾的 OR 值）'),
        dict(type='set', var='res', fmt=lambda x: str(x), h=170, label='res（已见过的全部 OR 值）'),
    ],
    watch=[('num', 'num', 'blue'), ('len(now)', 'len(now)', 'cyan'), ('len(res)', 'len(res)', 'green')],
    captions={
        'res = set()': '`res` 收集所有出现过的 OR 结果',
        'now = set([0])': '`now` 先放 0：0 与任何数 OR 都等于这个数本身，相当于「空子数组」',
        'for num in arr': '处理下一个数：`num = {num}`',
        'now = {x | num': '`now` 里每个值都和 `{num}` 做 OR：得到 OR(0,i)…OR(i-1,i)（也含 0|num），集合自动去重 → `{sorted(now)}`',
        'now.add(num)': '再加入 `{num}` 自己：它是 OR(i, i) → `{sorted(now)}`',
        'for x in now': '把 `now` 里的值逐个检查，看 `res` 里有没有',
        'if x not in res': lambda S, B, r: f'`{S.x}` ' + ('已经在 `res` 里 → 跳过' if S.x in S.res else '还不在 `res` 里 → 新的结果'),
        'res.add(x)': '`{x}` 加入 `res` → 共 {len(res)} 个',
        'return len(res)': '不同的 OR 值一共 ==`{len(res)}`== 个',
    },
    cards=dict(
        one_liner='以 i 结尾的 OR 值至多 32 种，用集合滚动维护',
        complexity='时间 `O(n log U)`，空间 `O(log U)`（外加 `res`）',
        problem=['求 `arr` 所有非空子数组的按位或，有多少个==不同的值==',
                 '示例：`[1,1,2]` → `3`',
                 '本视频：`[1,2,1,4]` → `6`（1,2,3,4,5,7）'],
        quote='OR(i, j) 就是在 OR(i, j - 1) 的基础上将某些二进制位上的 0 变成了 1……即使每次都恰好只变了 1 个 1，那么也最多只有 32 种不同的结果，因此完全可以使用一个哈希表储存计算的中间结果。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定左端点 i：OR 值只会==把 0 变成 1==，最多变 32 次，所以只有 ≤ 32 种结果',
              '换成固定右端点：`now` 存「以当前数结尾」的全部 OR，新来一个数就整体 OR 一遍再加它自己',
              '`now` 是集合，重复值自动合并，所以始终很小；再并入 `res`'],
        summary=['每步 `now` 至多 ~32 个数，总时间 `O(n log U)`',
                 '`now` 初始放 `0`，让第一个数也走同一套流程',
                 '易错：别忘了 `now.add(num)`，单个元素也是子数组',
                 '对比灵神：灵神原地改写 `arr` 并提前 break；yiduobo 用集合整体重算'],
    ),
)
