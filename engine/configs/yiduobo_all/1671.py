CONFIG = dict(
    num=1671, title='得到山形数组的最少删除次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='枚举山顶 + 两侧 LIS（贪心二分）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1913'],
    code='''
class Solution(object):
    def minimumMountainRemovals(self, nums):

        f = [1]
        f_pos = [nums[0]]

        for num in nums[1:]:
            if num > f_pos[-1]:
                f_pos.append(num)
                f.append(len(f_pos))
            else:
                l = 0
                r = len(f_pos) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if f_pos[mid] < num:
                        l = mid + 1
                    else:
                        r = mid
                    
                f.append(l + 1)
                f_pos[l] = num
        
        n = len(nums)
        g = [1]
        g_pos = [nums[-1]]
        for num in nums[-2::-1]:
            if num > g_pos[-1]:
                g_pos.append(num)
                g.append(len(g_pos))
            else:
                l = 0
                r = len(g_pos) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if g_pos[mid] < num:
                        l = mid + 1
                    else:
                        r = mid
                
                g.append(l + 1)
                g_pos[l] = num
        
        g.reverse()

        res = n
        for index in range(n):
            if f[index] > 1 and g[index] > 1:
                res = min(res, n - (f[index] + g[index] - 1))
        
        return res
''',
    call='Solution().minimumMountainRemovals([1,3,2,4,1])',
    expect=1,
    skip=['n = len', 'mid = (l + r)', 'l = mid + 1', 'r = mid'],
    max_steps=110,
    views=[
        dict(type='text', size=25, h=60, fn=lambda S: (
            '第三步：枚举山顶 `index`，山长 = `f[index] + g[index] - 1`，删除数 = `n - 山长`' if 'res' in S else
            ('第二步：从右往左，`g[i]` = 以 `nums[i]` 开头的最长递减长度' if 'g' in S else
             ('第一步：从左往右，`f[i]` = 以 `nums[i]` 结尾的最长递增长度' if 'f' in S else '')))),
        dict(type='array', var='nums', label='nums', h=140, cell=80,
             color=lambda S, k, v: 'yellow' if S.get('index') == k else None, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f（以 nums[i] 结尾的最长上升长度）', h=130, cell=80,
             color=lambda S, k, v: 'green' if S.get('index') == k else None),
        dict(type='array', var='g', label='g（先按从右往左存，最后 reverse）', h=130, cell=80,
             color=lambda S, k, v: 'cyan' if S.get('index') == k else None),
        dict(type='array', var=lambda S: S['g_pos'] if 'g_pos' in S else S.get('f_pos'), label='贪心数组（第一遍是 f_pos，第二遍是 g_pos）：每个长度的最小结尾', h=150, cell=88,
             pointers={"l if 'res' not in S else None": 'blue', "r if 'res' not in S else None": 'pink'}),
    ],
    watch=['num', 'l', 'r', 'index', ('res', 'res', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：以第一个数结尾的上升子序列长 1',
        'f_pos = [': '`f_pos` 保存「每种长度的最小结尾」，初始 `[{nums[0]}]`',
        'for num in nums[1:]': lambda S, B, r: ('从左往右扫完，`f` 已算好' if 'num' in B and B.num == S.num else f'看 `num = {S.num}`'),
        'if num > f_pos[-1]': lambda S, B, r: (f"`{S.num} > {S.f_pos[-1]}`：比所有结尾都大 → 能接在最长的后面" if S.num > S.f_pos[-1] else f"`{S.num} <= {S.f_pos[-1]}`：接不上最长的 → 在 `f_pos` 里二分找位置替换"),
        'f_pos.append(num)': '`f_pos` 追加 `{num}`',
        'f.append(len(f_pos))': '`f` 记下长度 `{len(f_pos)}`：以 `{num}` 结尾的最长上升子序列',
        'l = 0': '二分找第一个 `>= {num}` 的位置',
        'while l < r': lambda S, B, r_: (f"`l = {S.l}`，`r = {S.r}`，区间还没缩成一个点 → 继续" if S.l < S.r else f"`l = r = {S.l}`：位置找到了"),
        'if f_pos[mid] < num': lambda S, B, r_: (f"`mid = {S.mid}`，`f_pos[{S.mid}] = {S.f_pos[S.mid]}` < `{S.num}` → 答案在右边，`l = mid + 1`" if S.f_pos[S.mid] < S.num else f"`mid = {S.mid}`，`f_pos[{S.mid}] = {S.f_pos[S.mid]}` >= `{S.num}` → 答案在 mid 或左边，`r = mid`"),
        'if g_pos[mid] < num': lambda S, B, r_: (f"`mid = {S.mid}`，`g_pos[{S.mid}] = {S.g_pos[S.mid]}` < `{S.num}` → 答案在右边，`l = mid + 1`" if S.g_pos[S.mid] < S.num else f"`mid = {S.mid}`，`g_pos[{S.mid}] = {S.g_pos[S.mid]}` >= `{S.num}` → 答案在 mid 或左边，`r = mid`"),
        'f.append(l + 1)': '`f` 记下 `{l+1}`：`{num}` 放在第 `{l+1}` 位',
        'f_pos[l] = num': '`f_pos[{l}] = {num}`：同长度结尾更小更好',
        'g = [1]': '同样地，从右往左做一遍：`g[·] = 1`',
        'g_pos = [': '`g_pos` 从最后一个数开始 `[{nums[-1]}]`',
        'for num in nums[-2::-1]': lambda S, B, r: ('从右往左扫完，`g` 已算好' if 'num' in B and 'g_pos' in B and B.num == S.num and B.get('_ln') is None and S.num == S.nums[0] else f'从右往左看 `num = {S.num}`'),
        'if num > g_pos[-1]': lambda S, B, r: (f"`{S.num} > {S.g_pos[-1]}`：比所有结尾都大 → 接在后面" if S.num > S.g_pos[-1] else f"`{S.num} <= {S.g_pos[-1]}`：二分找位置替换"),
        'g_pos.append(num)': '`g_pos` 追加 `{num}`',
        'g.append(len(g_pos))': '`g` 记下 `{len(g_pos)}`：以 `{num}` 开头的最长下降子序列',
        'g.append(l + 1)': '`g` 记下 `{l+1}`',
        'g_pos[l] = num': '`g_pos[{l}] = {num}`',
        'g.reverse()': '`g` 是从右往左存的，翻转后 `g[i]` 对应 `nums[i]`：`{g}`',
        'res = n': '先假设全删掉，`res = n = {res}`',
        'for index in range': lambda S, B, r: ('枚举完毕，`res` 就是答案' if 'index' in B and B.index == S.index else f'枚举 `nums[{S.index}] = {S.nums[S.index]}` 当山顶'),
        'if f[index] > 1': lambda S, B, r: (f"`f = {S.f[S.index]}`，`g = {S.g[S.index]}`：两边都 > 1 → 左右都有数，==是合法山顶==" if S.f[S.index] > 1 and S.g[S.index] > 1 else f"`f = {S.f[S.index]}`，`g = {S.g[S.index]}`：有一侧没有数 → ==不能当山顶=="),
        'res = min': '山长 `{f[index]} + {g[index]} - 1 = {f[index]+g[index]-1}`，`res = min(.., {n} - 山长) = {res}`',
        'return res': '最少删除 `{res}` 个',
    },
    cards=dict(
        one_liner='枚举山顶，左边要最长上升，右边要最长下降',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['删最少的数，使数组变成山形：先严格递增再严格递减，峰顶两侧都要有数',
                 '示例：`[2,1,1,5,6,2,3,1]` → `3`',
                 '本视频：`[1,3,2,4,1]` → `1`'],
        quote='对于山形数组这种类型的问题，通常的做法就是枚举这个山的山顶，然后分别考察两侧应该如何处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定山顶后：左侧是「以山顶结尾的最长上升子序列」，右侧反过来看也是一个 LIS',
              '先用贪心二分，求出每个位置结尾的 LIS 长度 `f`，再从右往左求 `g`',
              '一趟枚举山顶，两侧长度都 > 1 才有效，用 `n - (f + g - 1)` 更新答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：左右 LIS 长度都必须 `> 1`，否则不是山峰',
                 '山顶被左右各算一次，所以山长是 `f + g - 1`',
                 '原文本身是合法的 Python 3 代码，未做修改；与灵神不同，这里二分写在循环里，且分别扫 `f`、`g` 两遍'],
    ),
)
