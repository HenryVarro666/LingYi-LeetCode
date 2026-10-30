_D = lambda arr: {i - 20: c for i, c in enumerate(arr) if c}
_IDX = lambda S: S['nums1'].index(S['v1']) if 'v1' in S else None


def _formula(S):
    if 'v1' not in S:
        return '`f[d]`：以当前下标为右端点，两和之差为 `d` 的方案数'
    return f'选 nums1：差 +{S["v1"]}；选 nums2：差 −{S["v2"]}；已累计 `res` = {S["res"]}'


CONFIG = dict(
    num=2143, title='在两个数组的区间中选取数字', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间右端点 DP · 差值计数',
    tags=[],
    code='''
class Solution(object):
    def countSubranges(self, nums1, nums2):

        f = [0] * 41
        res = 0
        mod = 10 ** 9 + 7
        for v1, v2 in zip(nums1, nums2):
            g = f[:]
            f = [0] * 41
            f[v1 + 20] += 1
            f[-v2 + 20] += 1
            for v, cnt in enumerate(g):
                if cnt == 0:
                    continue

                f[v + v1] += cnt
                if f[v + v1] >= mod:
                    f[v + v1] -= mod

                f[v - v2] += cnt
                if f[v - v2] >= mod:
                    f[v - v2] -= mod

            res += f[20]
            if res >= mod:
                res -= mod

        return res
''',
    call='Solution().countSubranges([1, 2, 5], [2, 6, 3])',
    expect=3,
    skip=['for v, cnt', 'if cnt == 0', 'continue', 'if f[v + v1] >= mod', 'f[v + v1] -= mod',
          'if f[v - v2] >= mod', 'f[v - v2] -= mod', 'if res >= mod', 'res -= mod', 'mod = ', 'f = [0] * 41'],
    views=[
        dict(type='array', var='nums1', label='nums1（选它：差 +）', cell=70, h=165, pointers={_IDX: 'blue'}, pointer_labels={_IDX: 'i'}),
        dict(type='array', var='nums2', label='nums2（选它：差 −）', cell=70, h=135, index=False,
             color=lambda S, i, v: 'pink' if _IDX(S) == i else None),
        dict(type='text', fn=_formula, size=24, h=55),
        dict(type='map', var=lambda S: _D(S['g']) if 'g' in S else {}, label='g：以上一个下标结尾的 {差: 方案数}', h=120,
             fmt=lambda k, v: f'{k:+d}: {v}'),
        dict(type='map', var=lambda S: _D(S['f']), label='f：以当前下标结尾的 {差: 方案数}（黄 = 刚改动）', h=150,
             fmt=lambda k, v: f'{k:+d}: {v}'),
    ],
    watch=[('v1', 'v1', 'blue'), ('v2', 'v2', 'pink'), ('res', 'res', 'green')],
    captions={
        '[0] * 41': '演示把原文的 `20001` 格、偏移 `10000` 缩成 `41` 格、偏移 `20`（示例数很小）；原题差值在 `[-10000, 10000]`',
        'for v1, v2 in zip': '处理下一个下标：`v1 = {v1}`，`v2 = {v2}`',
        'g = f[:]': '先把上一轮的 `f` 存进 `g`（以前一个下标结尾的方案），再重新清零 `f`',
        'f = [0] * 41': '`f` 清零，准备算以当前下标结尾的方案',
        'f[v1 + 20] += 1': '区间只含当前一个数，选 `nums1`：差 = `+{v1}` → `f[+{v1}] = 1`',
        'f[-v2 + 20] += 1': '区间只含当前一个数，选 `nums2`：差 = `-{v2}` → `f[-{v2}]` 加 1',
        'f[v + v1] += cnt': '接在旧方案后：旧差 `{v - 20}`（{cnt} 种），当前选 `nums1[i]` → 新差 `{v - 20 + v1}`，==累加 {cnt}==',
        'f[v - v2] += cnt': '接在旧方案后：旧差 `{v - 20}`（{cnt} 种），当前选 `nums2[i]` → 新差 `{v - 20 - v2}`，==累加 {cnt}==',
        'res += f[20]': '差为 0 就是 nums1 之和 = nums2 之和 → 以当前下标结尾有 `{f[20]}` 种，`res = {B.res} + {f[20]}` = =={res}==',
        'return res': '所有右端点的「差为 0」方案数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='把「两和相等」变成「nums1 之和 − nums2 之和 = 0」',
        complexity='时间 `O(n·V)`（原题 V = 20001），空间 `O(V)`',
        problem=['两个长度为 `n` 的数组，选区间 `[l, r]`，区间内每个下标只能取 `nums1[i]` 或 `nums2[i]` 之一',
                 '要求取自 `nums1` 的和 ==等于== 取自 `nums2` 的和，数出合法的方案数（取模 `10^9+7`）',
                 '示例：`nums1=[1,2,5]`，`nums2=[2,6,3]` → `3`'],
        quote='将题目转化成从区间中选取数字，使得nums1中选取数字之和减去nums2中选取数字之和恰好等于0。……任意选择方案的数字和之差必然在-10000到10000之间，这个数据规模可以使用动态规划来求解。',
        quote_src='—— yiduobo 题解',
        idea=['`f[j]` = 以第 `i` 个数为右边界、两和之差为 `j` 的方案数',
              '新开区间：只选 `nums1[i]`（差 `+v1`）或 `nums2[i]`（差 `−v2`）各 1 种',
              '接在旧方案后：差 `j` 变成 `j + v1` 或 `j − v2`；每个右端点把 `f[0]` 累加进答案',
              '下标加偏移避免负数（原文偏移 10000）'],
        summary=['时间 `O(n × 20001)`；每轮用 `g` 备份旧 `f`，只遍历非 0 项',
                 '易错：新区间的两种单点方案要先放进 `f`；`v1`、`v2` 符号相反',
                 '易错：偏移后 `f[偏移]` 才是差 0（原文 `f[10000]`）；每步都要取模',
                 '为演示把数组长度 `20001`→`41`、偏移 `10000`→`20`，其余原文不变'],
    ),
)
