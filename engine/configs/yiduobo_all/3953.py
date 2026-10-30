CONFIG = dict(
    num=3953, title='互质元素的最大得分', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='质数筛 + 容斥求不互质个数 f[v]',
    tags=['灵神题单', '数学算法', '难度分 2390'],
    code='''
class Solution(object):
    def maxScore(self, nums, maxVal):
        
        ma = maxVal
        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            ma = max(ma, v)
        
        f = [0] * (ma + 1)
        g = [v for v in range(ma + 1)]

        for v in range(2, ma + 1):
            if g[v] == v:
                tot = 0
                for x in range(v, ma + 1, v):
                    tot += cnt.get(x, 0)
                    g[x] //= -v
                
                for x in range(v, ma + 1, v):
                    f[x] += tot
            
            elif abs(g[v]) == 1:
                tot = 0
                for x in range(v, ma + 1, v):
                    tot += cnt.get(x, 0)
                
                for x in range(v, ma + 1, v):
                    f[x] -= g[v] * tot
        
        if 1 in cnt:
            res = 1
        else:
            res = 0

        for v in range(2, maxVal + 1):
            if v in cnt:
                res = max(res, v - (f[v] - 1))
            elif f[v] == 0:
                res = max(res, v - 1)
            else:
                res = max(res, v - f[v])

        for v in range(maxVal + 1, ma + 1):
            if v in cnt:
                res = max(res, v - (f[v] - 1))
        
        return res
''',
    call='Solution().maxScore([2,3,3,6,5], 6)',
    expect=5,
    views=[
        dict(type='map', var='cnt', label='cnt：nums 里每个数出现几次', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='array', var='f', label='f[v]：nums 中与 v 不互质的个数', h=150, cell=70, pointers={'x': 'blue'}),
        dict(type='array', var='g', label='g[v]：v 依次除以 −p（−1 / 1 = 容斥符号）', h=150, cell=70, pointers={'v': 'pink'}),
        dict(type='text', h=90, size=28,
             fn=lambda S: f"当前 v = =={S['v']}==，f 已经算完时，f[v] = 不互质个数" if 'res' in S and 'v' in S else ''),
    ],
    watch=[('v', 'v', 'pink'), ('tot', 'tot', 'orange'), ('x', 'x', 'blue'), ('res', 'res', 'green')],
    captions={
        'ma = maxVal': '`ma` 取 `maxVal` 与 `nums` 最大值中较大者：所有可能的 selectedValue 都 `<= ma`',
        'cnt[v] = cnt.get': '`cnt[{v}]` → {cnt[v]}',
        'f = [0] * (ma + 1)': '`f[v]`：nums 中与 `v` 不互质的元素个数（先全 0）',
        'g = [v for v': '`g[v]` 初值 = `v`，用来标记“v 是质数 / 由几个不同质数相乘”',
        'for v in range(2, ma + 1)': lambda S, B, r: (f'`v = {S.v}`' if 'v' not in B or S.v != B.v else '`f` 计算完毕'),
        'if g[v] == v': lambda S, B, r: (f'`g[{S.v}] == {S.v}`：没被任何更小的质数改过 → `{S.v}` 是==质数==' if S.g[S.v] == S.v
                                         else f'`g[{S.v}] = {S.g[S.v]} ≠ {S.v}`：不是质数'),
        'tot += cnt.get(x, 0)': '`tot` = nums 中 `{v}` 的倍数个数：加上 `cnt[{x}]` → `{tot}`',
        'g[x] //= -v': '`g[{x}]` 除以 `-{v}`：每含一个不同的质因子就变一次号',
        'f[x] += tot': '这 `{tot}` 个 `{v}` 的倍数都与 `{x}` 有公因子 `{v}` → `f[{x}] += {tot}` = `{f[x]}`（`{x}` 自己若在 nums 里也被算进去了，最后再减 1）',
        'elif abs(g[v]) == 1': lambda S, B, r: (f'`g[{S.v}] = {S.g[S.v]}`：除干净了，说明 `{S.v}` 是若干不同质数之积 → 容斥要修正' if abs(S.g[S.v]) == 1
                                                else f'`g[{S.v}] = {S.g[S.v]}`：有平方因子或没除干净 → 不用算'),
        'f[x] -= g[v] * tot': '容斥修正：`f[{x}] -= g[{v}] × tot` = `-({g[v]} × {tot})` → `f[{x}] = {f[x]}`',
        'if 1 in cnt': lambda S, B, r: ('nums 里有 1：选它不用改，得分 1' if 1 in S.cnt else 'nums 里没有 1：改一个数为 1，得分 0'),
        'res = 1': '`res = 1`',
        'res = 0': '`res = 0`',
        'if v in cnt': lambda S, B, r: (f'`{S.v}` 在 nums 里：保留它，其他 `f[{S.v}] - 1` 个不互质的改成 1' if S.v in S.cnt
                                        else f'`{S.v}` 不在 nums 里'),
        'elif f[v] == 0': lambda S, B, r: (f'`f[{S.v}] = 0`：没有不互质的数，把任一元素改成 {S.v}，代价 1' if S.f[S.v] == 0
                                           else f'`f[{S.v}] = {S.f[S.v]}`：有不互质的数，其中一个改成 {S.v}，其余改成 1'),
        'res = max(res, v - (f[v] - 1))': '得分 `{v} - ({f[v]} - 1)` = `{v - (f[v] - 1)}` → `res = {res}`',
        'res = max(res, v - 1)': '得分 `{v} - 1` = `{v - 1}` → `res = {res}`',
        'res = max(res, v - f[v])': '得分 `{v} - {f[v]}` = `{v - f[v]}` → `res = {res}`',
        'return res': '最大得分：`{res}`',
    },
    skip=['for x in range(v, ma + 1, v)', 'tot = 0', 'for v in nums:', 'res = 0', 'res = 1'],
    max_steps=100,
    cards=dict(
        one_liner='用质数当“桥梁”数出不互质的个数，再枚举选中的值',
        complexity='时间 `O(U log U)`，空间 `O(U)`（U = max(nums, maxVal)）',
        problem=['可把任意元素改成 `<= maxVal` 的正整数，每次代价 1',
                 '最后选一个下标，使它与其他元素都互质',
                 '得分 = 选中的值 − 修改次数，求最大得分',
                 '本视频：`nums=[2,3,3,6,5], maxVal=6` → `5`'],
        quote='对于任意两个不互质的元素x和y，至少存在一个质因子p，满足x和y同时为p的倍数。基于这一点，在这里就可以尝试枚举所有质数p，以p作为桥梁连接起所有p的倍数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[v]` = nums 中与 `v` 不互质的个数；按质数 p 把 p 的倍数连起来，先加 `tot`',
              '多个质因子会重复计数（如 12）→ 用 `g` 标记不同质数之积，按奇偶容斥加减',
              '再枚举 selectedValue：在 nums 里就 `v-(f[v]-1)`；不在且 f=0 就 `v-1`；否则 `v-f[v]`；大于 maxVal 的只能取 nums 里已有的'],
        summary=['时间 `O(U log U)`，空间 `O(U)`',
                 '`g[x] //= -v` 一直能整除，所以改成 `//` 结果不变',
                 '原文为 Python 2 写法，其中 `g[x] /= -v` 的整数除法已改为 `//=`',
                 '易错：`v` 自己在 nums 里时，`f[v]` 把它也算进去了，所以要 `f[v] - 1`',
                 '对比灵神：灵神用莫比乌斯函数和 `cnt_multi` 直接对 selectedValue 的因子求和，yiduobo 用筛法一次性算出所有 `f`'],
    ),
)
