def _fml(S):
    f = S.get('f')
    if f is None or 'index' not in S or len(f) < 3:
        return '规则：偶数 `f[i] = f[i/2]`，奇数 `f[i] = f[i//2] + f[i//2 + 1]`'
    i = S['index']
    if i >= len(f):
        return f'开始计算 `f[{i}]`'
    h = i // 2
    if i & 1:
        return f'`index = {i}` 奇数：`f[{i}] = f[{h}] + f[{h + 1}] = {f[h]} + {f[h + 1]}` = =={f[i]}=='
    return f'`index = {i}` 偶数：`f[{i}] = f[{h}]` = =={f[i]}=='


CONFIG = dict(
    num=1646, title='获取生成数组中的最大值', difficulty='Easy', category='模拟',
    author='yiduobo', technique='按规则逐项模拟',
    code='''
class Solution(object):
    def getMaximumGenerated(self, n):

        if n == 0:
            return 0
        
        res = 1
        f = [0, 1]
        for index in range(2, n + 1):
            f.append(f[index // 2])
            if index & 1:
                f[-1] += f[index // 2 + 1]
            res = max(res, f[-1])

        return res
''',
    call='Solution().getMaximumGenerated(7)',
    expect=3,
    views=[
        dict(type='text', fn=_fml),
        dict(type='array', var='f', pointers={'index': 'blue'}, label='f（生成数组 nums）', h=260,
             color=lambda S, i, v: 'green' if 'res' in S and v == S['res'] and i > 0 else None),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'if n == 0': '`n = 0` 时数组只有 `nums[0] = 0`，最大值就是 0',
        'res = 1': '`f[1] = 1` 已知，答案先记为 `1`',
        'f = [0, 1]': '初始 `f = [0, 1]`',
        'for index in range': '枚举 `index = {index}`，算 `f[{index}]`',
        'f.append(f[index // 2])': '先放 `f[{index}//2] = f[{index // 2}]` = `{f[-1]}`',
        'if index & 1': lambda S, B, r: (f'`index = {S.index}` 是奇数 → 还要再加 `f[{S.index // 2 + 1}]`' if S.index & 1 else f'`index = {S.index}` 是偶数 → 不用再加'),
        'f[-1] +=': '奇数项：再累加 `f[{index // 2 + 1}] = {f[index // 2 + 1]}` → `f[{index}] = {f[-1]}`',
        'res = max': '每得到一项就顺手更新答案：`max({B.res}, {f[-1]}) = {res}`',
        'return res': '最大值 `{res}`',
    },
    cards=dict(
        one_liner='规则写得清清楚楚：老老实实一项项模拟',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums[0]=0`，`nums[1]=1`；`2i` 项等于 `nums[i]`，`2i+1` 项等于 `nums[i]+nums[i+1]`',
                 '求生成数组 `nums` 里的最大值',
                 '示例：`n=7` → `nums=[0,1,1,2,1,3,2,3]`，答案 `3`'],
        quote='感觉应该有数学方法可以直接计算，但是没有想出来，只好老老实实逐个模拟计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f` 从 `[0, 1]` 开始，`index` 从 2 枚举到 n',
              '先 append `f[index//2]`；奇数再加上 `f[index//2 + 1]`',
              '每得到一项就更新答案 `res`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`n = 0` 要单独返回 0，`n = 1` 时循环不执行，答案是 1',
                 '奇数项依赖 `index//2 + 1`，它一定已算出（小于 index）',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
