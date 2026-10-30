CONFIG = dict(
    num=3591, title='检查元素频次是否为质数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='哈希表计数 + 试除判质数',
    tags=['灵神题单·数学算法', '数学算法', '难度分 1235'],
    code='''
class Solution(object):
    def checkPrimeFrequency(self, nums):
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        for f in freq.values():
            if f == 1:
                continue
            
            p = 2
            prime = True
            while p * p <= f:
                if f % p == 0:
                    prime = False
                    break
                p += 1
            
            if prime:
                return True
        
        return False
''',
    call='Solution().checkPrimeFrequency([5,6,5,5,5,6,6])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=90, pointers={}),
        dict(type='map', var='freq', label='freq（元素 → 频次）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', size=30, h=110, fn=lambda S: (
            f"频次 `f = {S['f']}`，试除 `p = {S['p']}`：`{S['p']}×{S['p']} = {S['p']*S['p']}` " + ('`≤ f`，要检查' if S['p'] * S['p'] <= S['f'] else '`> f`，不用再试')
            if 'f' in S and 'p' in S else '')),
    ],
    watch=[('v', 'v', 'blue'), ('f', 'f', 'cyan'), ('p', 'p', 'pink'), ('prime', 'prime', 'green')],
    max_steps=70,
    captions={
        'freq = {}': '`freq` 用哈希表记录每种元素出现的次数',
        'for v in nums': '取出 `nums` 里的 `{v}`',
        'freq[v] = freq.get': '`freq[{v}]` 在原有次数上加一 → =={freq[v]}==',
        'for f in freq.values()': '遍历每种元素的频次，看有没有质数：`f = {f}`',
        'if f == 1': lambda S, B, r: ('`f == 1`：1 ==不是质数==，直接跳过' if S.f == 1 else f'`f = {S.f} ≠ 1`，需要判断它是不是质数'),
        'p = 2': '从最小的因数 `p = 2` 开始试除',
        'prime = True': '先假设 `{f}` 是质数',
        'while p * p <= f': lambda S, B, r: (f'`p×p = {S.p*S.p} ≤ {S.f}`：可能还有因数，继续试' if S.p * S.p <= S.f else f'`p×p = {S.p*S.p} > {S.f}`：不可能再有因数，`{S.f}` 是质数'),
        'if f % p == 0': lambda S, B, r: (f'`{S.f} % {S.p} == 0`：`{S.p}` 整除 `{S.f}`，它是合数' if S.f % S.p == 0 else f'`{S.f} % {S.p} = {S.f % S.p} ≠ 0`，`{S.p}` 不是因数'),
        'prime = False': '找到因数，`prime = False`',
        'break': '已确定是合数，退出试除',
        'p += 1': '换下一个除数 `p = {p}`',
        'if prime': lambda S, B, r: (f'`{S.f}` 是质数 → 答案就是 `true`' if S.prime else f'`{S.f}` 是合数，看下一个频次'),
        'return True': '有一个质数频次，返回 `True`',
        'return False': '所有频次都不是质数，返回 `False`',
    },
    cards=dict(
        one_liner='哈希表数频次，再对每个频次试除判质数',
        complexity='时间 `O(n + k√n)`，空间 `O(n)`',
        problem=['元素的==频次==就是它在数组中出现的次数',
                 '任一元素的频次是质数，就返回 `true`，否则 `false`',
                 '示例：`[1,2,3,4,5,4]` → `true`；`[1,2,3,4,5]` → `false`',
                 '本视频：`[5,6,5,5,5,6,6]` → `true`'],
        quote='一趟遍历，使用哈希表统计每种元素出现的次数，接下来遍历这个哈希表中元素出现的频次，检测其中是否有质数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 只有 100，不必预处理筛，直接对每个频次试除',
              '频次 1 不是质数，先 `continue`',
              '从 2 试到 `p×p <= f`，没有因数就是质数'],
        summary=['时间：计数 `O(n)`，每个频次试除最多 `O(√n)`',
                 '易错点：==频次 1 要跳过==，否则会把 1 当质数',
                 '`while p * p <= f` 避免开方，只试到根号',
                 '对比灵神：灵神先筛表后查 `is_prime`，yiduobo 现场试除，规模小时同样够用'],
    ),
)
