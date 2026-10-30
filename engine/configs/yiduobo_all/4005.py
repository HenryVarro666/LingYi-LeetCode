CONFIG = dict(
    num=4005, title='使数组中所有元素相等的最小操作数III', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='质因数分解构造约数 + 统计约数/倍数',
    tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        ma = int(max(nums) ** 0.5 + 0.5)
        f = [True] * (ma + 1)
        prime = []
        for v in range(2, ma + 1):
            if f[v]:
                prime.append(v)
                for x in range(v + v, ma + 1, v):
                    f[v] = False
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        mul = {}
        div = {}
        for v in freq.keys():
            x = v
            d = [1]
            for p in prime:
                if p * p > x:
                    break
                new_d = []
                power = 1
                while x % p == 0:
                    x //= p
                    power *= p
                    new_d.extend([num * power for num in d])
                d.extend(new_d)

            if x > 1:
                d.extend([num * x for num in d])

            for x in d:
                mul[x] = mul.get(x, 0) + freq[v]
                div[v] = div.get(v, 0) + freq.get(x, 0)
        
        res = len(nums)
        for v in freq.keys():
            if v > 1:
                one = mul[v] - freq[v] + div[v] - freq[v]
                res = min(res, (len(nums) - freq[v] - one) * 2 + one)
        
        return res
''',
    call='Solution().minOperations([2,3,6,12,12,5])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', h=170),
        dict(type='map', var=lambda S: S.get('freq', {}), fmt=lambda k, v: f'{k} : 出现 {v} 次', label='freq', h=190),
        dict(type='map', var=lambda S: S.get('mul', {}), fmt=lambda k, v: f'{k} : 倍数共 {v} 个', label='mul[x]', h=190),
        dict(type='map', var=lambda S: S.get('div', {}), fmt=lambda k, v: f'{k} : 约数共 {v} 个', label='div[v]', h=190),
        dict(type='text', size=30, fn=lambda S: (f"`v` = {S['v']} 的约数 `d` = {S['d']}" if 'd' in S and 'v' in S and 'one' not in S else
                                                  (f"`v` = {S['v']}：一次操作的元素 `one` = =={S['one']}==" if 'one' in S else ''))),
    ],
    watch=[('v', 'v', 'blue'), ('x', 'x', 'yellow'), ('p', 'p', 'pink'), ('one', 'one', 'cyan'), ('res', 'res', 'green')],
    captions={
        'ma = int': '`ma` = =={ma}==：数组最大值的平方根。只要不超过它的质数就够分解了',
        'f = [True]': '筛法标记表 `f`',
        'prime = []': '`prime` 收集质数',
        'prime.append(v)': '`prime` = {prime}',
        'f[v] = False': '筛掉：`f[{v}]` = False',
        'freq[v] = freq.get': '`freq[{v}]` = {freq[v]}：数每个值出现几次',
        'mul = {}': '`mul[x]`：是 x 的倍数的元素个数；`div[v]`：是 v 的约数的元素个数',
        'x = v': '处理值 `v` = {v}：`x` 是还没分解掉的部分，`d` 是已构造出的约数列表',
        'd = [1]': '约数列表从 `[1]` 开始',
        'if p * p > x': lambda S, B, r: (f'`{S.p} * {S.p} > {S.x}`：再往后的质数都用不上了，停止' if S.p * S.p > S.x else f'`{S.p} * {S.p} <= {S.x}`：试除质数 {S.p}'),
        'power *= p': '除掉一个 {p}，`power` = {power}：把 d 里每个约数乘 `power` 得到新约数',
        'new_d.extend': '`new_d` = {new_d}',
        'd.extend(new_d)': '`d` 合并后 = =={d}==',
        'd.extend([num * x': '剩下的 `x` = {x} 是一个大质因子，每个约数再乘它 → `d` = =={d}==',
        'mul[x] = mul.get': '`x` = {x} 是 `v` = {v} 的约数 → `mul[{x}]` += `freq[{v}]` → {mul[x]}',
        'div[v] = div.get': '`freq[{x}]` 个元素是 v 的约数 → `div[{v}]` = =={div[v]}==',
        'res = len(nums)': '上限：全部变成最小公倍数，最多操作 `n` = {res} 次',
        'one = mul': '只需 1 次的元素 `one` = `mul - freq + div - freq` = {mul[v]} − {freq[v]} + {div[v]} − {freq[v]} = =={one}==',
        'res = min': '其余 `{len(nums)} - {freq[v]} - {one}` 个要 2 次：总次数 `({len(nums)} - {freq[v]} - {one}) * 2 + {one}`；`res` = =={res}==',
        'return res': '最少操作 =={res}== 次',
    },
    cards=dict(
        one_liner='选一个已有的值当目标：约数/倍数 1 步，其余 2 步',
        complexity='时间约 `O(n·√V/ln V)`，空间 `O(n·D)`（D 为约数个数）',
        problem=['一次操作：把某个元素乘整数 `k`（`k >= 2`），或除以它的约数 `k`',
                 '求让 `nums` 所有元素相等的最少操作次数',
                 '本视频：`[2,3,6,12,12,5]`，选 `12` 当目标：2、6、3 都是约数，各 1 步，共 `3`？见动画结果'],
        quote='优化的目标就是改为选择nums中原始就存在的某个元素x，此时可以省去所有等于x的元素的操作次数，除此之外，对于不等于x的自身，且为x约数或者倍数的元素，依然需要一次操作，而剩余的元素则需要两次操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['上限：都变成最小公倍数，最多 `n` 次',
              '选已有的值 `v`：等于 v 的 0 步；是 v 约数或倍数的 1 步；其余 2 步',
              '值域 `10^9` 不能筛倍数 → 对每个不同值分解质因数，构造它的约数，累加到 `mul` / `div`'],
        summary=['`one = mul[v] - freq[v] + div[v] - freq[v]`：约数、倍数各自扣掉等于自己的那部分',
                 '目标 `v` 必须 `> 1`（题目性质）',
                 '原文筛质数处写的是 `f[v] = False`（不是 `f[x]`），所以 `prime` 里其实含合数；多出来的试除不影响结果，本视频照原样运行',
                 '原文已是 Python 3 可运行写法，未做修改'],
    ),
)
