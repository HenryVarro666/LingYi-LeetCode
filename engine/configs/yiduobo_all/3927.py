CONFIG = dict(
    num=3927, title='可整除替换后的数组最小元素和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛法 · 从小到大枚举倍数',
    tags=['灵神题单', '数论', '难度分 1652'],
    code='''
class Solution(object):
    def minArraySum(self, nums):
        
        cnt = {}
        ma = 0
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            ma = max(ma, v)
            
        res = 0
        for v in range(1, ma + 1):
            if cnt.get(v, 0) > 0:
                for x in range(v, ma + 1, v):
                    if x in cnt:
                        res += cnt[x] * v
                        cnt.pop(x)

        return res
''',
    call='Solution().minArraySum([6,4,2,9,3,6])',
    expect=14,
    views=[
        dict(type='map', var='cnt', label='cnt（还没被换掉的数）', h=210),
        dict(type='text', h=90, fn=lambda S: (f"当前 `v = {S['v']}`，沿着 {S['v']}、{2*S['v']}、{3*S['v']}… 把倍数都换成 {S['v']}" if S.get('_line') and 'v' in S and 'res' in S and isinstance(S.get('cnt'), dict) and S['cnt'].get(S['v'], 0) > 0 else '')),
    ],
    watch=['v', 'x', 'ma', ('res', 'res', 'green')],
    captions={
        'cnt[v] = cnt.get': '`cnt[{v}]` = =={cnt[v]}==',
        'ma = max': '`ma` 记最大值：筛的范围只到 `{ma}`',
        'res = 0': '`res` 累计最终元素和',
        'for v in range': '从小到大枚举 `v = {v}`',
        'if cnt.get': lambda S, B, r: (f'`cnt` 里还有 {S.v}（出现 {S.cnt.get(S.v, 0)} 次）→ 它没被更小的数换掉，是新的"根"' if S.cnt.get(S.v, 0) > 0 else f'{S.v} 已被更小的约数换掉或不存在 → 跳过'),
        'for x in range': '沿着 v 的倍数走：`x = {x}`',
        'if x in cnt': lambda S, B, r: (f'`{S.x}` 在 cnt 里：它能被 {S.v} 整除，可以换成 {S.v}' if S.x in S.cnt else f'`{S.x}` 不在 cnt 里，略过'),
        'res += cnt[x]': '`{x}` 共 `{B.cnt[x]}` 个，全换成 `{v}` → `res` = =={res}==',
        'cnt.pop(x)': '删掉 `{x}`：留在 cnt 里的必然是无法再变小的数',
        'return res': '最小元素和 `{res}`',
    },
    cards=dict(
        one_liner='像筛法一样：小的数先把它的倍数"吃掉"',
        complexity='时间 `O(M log M)`（M 为最大值），空间 `O(n)`',
        problem=['`nums[a] % nums[b] == 0` 时可把 `nums[a]` 换成 `nums[b]`，次数不限',
                 '求最后数组元素和的最小值',
                 '示例：`[4,2,8,3]` → `9`'],
        quote='最佳的处理方式就是将每个元素都变成可以整除它的最小元素。……因此可以使用类似筛法的方法来进行处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表 `cnt` 记每种数出现的次数',
              '从 1 往上枚举 `v`：若 `cnt` 里还有 v，沿 `2v、3v…` 把存在的数全换成 v',
              '换完就 `pop`，所以 cnt 里留下的都不能再变小'],
        summary=['时间 `O(M log M)`：调和级数，M 是数组最大值',
                 '必须==从小到大==枚举 v，否则大因子会先把数吃掉',
                 '被吃掉的数要 `pop`，否则会被更大的 v 重复计算',
                 '对比灵神：灵神按数找最小因子，yiduobo 按因子筛倍数'],
    ),
)
