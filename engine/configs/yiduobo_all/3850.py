NUMS, K = [2, 2], 1


def _txt(S):
    if 'need' not in S:
        return '把 `val` 记成幂次三元组 `(two, three, five)`：乘就是加幂次，除就是减幂次'
    need = S['need']
    inner = S['_inner']
    base = f'目标 `k = 2^{need[0]} × 3^{need[1]} × 5^{need[2]}` → 要找 key = ==({need[0]}, {need[1]}, {need[2]})=='
    if 'cnt' in S and 'x' in S and S.get('_line', 0) >= 20:
        c = S['cnt']
        base += f'；当前数含 `({c[0]}, {c[1]}, {c[2]})`'
    return base


def _fmt(k, v):
    return f'({k[0]},{k[1]},{k[2]}): {v}'


CONFIG = dict(
    num=3850, title='统计结果等于K的序列数目', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='质因子幂次三元组 · 滚动哈希表 DP',
    tags=['灵神题单', '动态规划', '难度分 1965'],
    setup='import copy',
    code='''
class Solution(object):
    def countSequences(self, nums, k):
        
        need = [0] * 3
        p = [2, 3, 5]
        for index, v in enumerate(p):
            while k % v == 0:
                need[index] += 1
                k //= v
        
        if k != 1:
            return 0

        f = {(0, 0, 0): 1}
        for x in nums:
            g = copy.deepcopy(f)
            cnt = [0] * 3
            for index, v in enumerate(p):
                while x % v == 0:
                    cnt[index] += 1
                    x //= v
            
            for key in g:
                for sign in [-1, 1]:
                    nxt_key = (key[0] + sign * cnt[0], key[1] + sign * cnt[1], key[2] + sign * cnt[2])
                    f[nxt_key] = f.get(nxt_key, 0) + g[key]
        
        return f.get((need[0], need[1], need[2]), 0)
''',
    call=f'Solution().countSequences({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（处理到哪个数，看下方 cnt）', cell=100, h=160),
        dict(type='map', var='g', label='g（上一轮的 f 的副本，只读）', fmt=_fmt, h=170, font=24),
        dict(type='map', var='f', label='f（key = 幂次三元组，value = 方案数；黄 = 新增 / 改动）', fmt=_fmt, h=250, font=24),
        dict(type='text', h=80, size=26, fn=_txt),
    ],
    watch=['need', 'k', 'x', 'cnt', ('key', 'key', 'blue'), ('sign', 'sign', 'pink')],
    skip=['for index, v in enumerate(p)', 'while k % v', 'need[index] += 1', 'k //= v', 'p = [2, 3, 5]',
          'cnt = [0] * 3', 'for sign in', 'nxt_key = (', 'while x % v', 'cnt[index] += 1', 'x //= v', 'need = [0] * 3'],
    captions={
        'if k != 1': lambda S, B, r: ('`k` 除掉所有 2、3、5 之后 == 1：目标只含这三种质因子 → 可以做 DP' if S.k == 1
                                      else f'`k` 剩下 `{S.k}` ≠ 1：还有别的质因子，nums 里凑不出来 → 返回 0'),
        'f = {(0, 0, 0): 1}': '`f` 初始只有 `(0,0,0): 1`：`val = 1` 即各质因子幂次都是 0，方案数 1；need = `{need}`',
        'for x in nums': lambda S, B, r: ('`nums` 处理完了，`f` 里就是所有幂次组合的方案数' if 'x' in B and S.x == B.x
                                          else f'处理 `nums` 里的 `x = {S.x}`，每个数有 乘 / 除 / 不变 三种选择'),
        'g = copy.deepcopy(f)': '先复制一份 `g`：遍历 `g` 的同时往 `f` 里写；`f` 本身就保留了旧状态，这就是「不变」这一种选择',
        'for key in g': '枚举上一轮的状态 `key = {key}`（方案数 `{g[key]}`）',
        'f[nxt_key] = ': '{"乘以" if sign == 1 else "除以"} `x`：`{key}` {"+" if sign == 1 else "−"} `{cnt}` → `{nxt_key}`；`f[{nxt_key}] = {B.f.get(nxt_key, 0)} + {g[key]}` = =={f[nxt_key]}==',
        'return 0': '直接返回 0',
        'return f.get': '要找的 key 是 `({need[0]}, {need[1]}, {need[2]})` → 方案数 =={ret}==',
    },
    cards=dict(
        one_liner='val 只含质因子 2、3、5：记幂次，乘除变成加减',
        complexity='时间 `O(n^4)`，空间 `O(n^3)`',
        problem=['`nums[i]` 位置三选一：乘、除（有理数除法）、不变',
                 '从 `val = 1` 开始，问最后 `val == k` 的选择序列有多少种',
                 '`nums[i]` 在 1–6，`k` 最大 `10^15`',
                 '本视频：`nums = [2, 2]`，`k = 1` → `3`（乘乘、乘除……幂次互相抵消）'],
        quote='k中所有的2、3、5都分离出来，得到一个长度为3的数组need……若分离后的k不为1，说明k中还有其他的质因子，……最终答案必然为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `k` 拆成 `need = [两个数, 三个数, 五个数]`；剩下不是 1 就无解',
              '`f` 是哈希表：key = `(two, three, five)`，value = 方案数；负幂次直接当 key，不用改下标',
              '每个 `x` 拆成 `cnt`，对每个旧状态：乘 → 加 `cnt`，除 → 减 `cnt`，不变 → 保留',
              '用滚动哈希表省掉 `index` 那一维'],
        summary=['时间 `O(n^4)` 量级：状态数是各幂次取值数的乘积，每个数转移 `O(1)` 个状态',
                 '易错：`k` 剩余部分 `!= 1` 要先返回 0',
                 '易错：写 `f` 前先 `deepcopy` 成 `g`，否则会边遍历边改字典',
                 '「不变」不需要单独写：`f` 本来就带着旧状态',
                 '对比灵神：灵神倒着从 `k` 搜到 1，用 `@cache`；yiduobo 正着推，用哈希表滚动',
                 '原文已是 Python 3 可运行写法，仅在 `setup` 里补了 `import copy`'],
    ),
)
