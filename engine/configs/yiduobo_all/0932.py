CONFIG = dict(
    num=932, title='漂亮数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶分治构造',
    tags=['灵神题单·贪心与思维', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def beautifulArray(self, N):

        l = 1
        now = [1]
        while l < N:
            now = [x + x - 1 for x in now] + [x + x for x in now]
            l += l
        
        res = []
        for num in now:
            if num <= N:
                res.append(num)
        
        return res
''',
    call='Solution().beautifulArray(7)',
    expect=[1, 5, 3, 7, 2, 6, 4],
    skip=['for num in now'],
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"`now` 长度 {len(S['now'])}，包含 1..{len(S['now'])} 每个数一次；目标 N = {S['N']}" if 'l' in S and 'now' in S
                           else '奇数放左边、偶数放右边，就不会有 A[i]+A[j] = 2·A[k]')),
        dict(type='array', var='now', label='now（奇数在前、偶数在后，都是漂亮数组）', cell=84, h=200,
             color=lambda S, i, v: ('blue' if v % 2 else 'pink') if 'now' in S else None),
        dict(type='array', var=lambda S: S.get('res'), label='res（只保留 ≤ N 的数）', cell=84, h=200,
             color=lambda S, i, v: 'green'),
    ],
    watch=['N', 'l', ('res', 'res', 'green')],
    captions={
        'l = 1': '`l` 是 `now` 当前的长度（也是最大值），从 1 开始',
        'now = [1]': '`[1]` 显然是漂亮数组',
        'while l < N': lambda S, B, r: (f'`l = {B.l} < N = {B.N}`：还不够长，继续翻倍' if B.l < B.N
                                        else f'`l = {B.l} ≥ N = {B.N}`：够了，`now` 是 1..{B.l} 的漂亮排列'),
        'now = [x + x - 1': '每个数 ×2−1 得奇数部分，×2 得偶数部分，奇数在前拼起来：`{now}`。==奇 + 偶 ≠ 2·任何数==，所以拼接安全',
        'l += l': '长度翻倍：`l = {l}`',
        'res = []': '`now` 包含 1..`l` 的所有数，要删掉大于 `N` 的',
        'if num <= N': lambda S, B, r: (f'`{S.num} ≤ {S.N}`：保留' if S.num <= S.N else f'`{S.num} > {S.N}`：丢弃'),
        'res.append': '`res` 加入 `{num}` → {res}',
        'return res': '删掉大数后顺序不变，子序列仍是漂亮数组：`{res}`',
    },
    cards=dict(
        one_liner='漂亮数组乘 2 或乘 2 减 1 仍漂亮，奇偶拼起来也漂亮',
        complexity='时间 `O(N)`，空间 `O(N)`',
        problem=['返回 `1..N` 的一个排列 `A`，称为漂亮数组：',
                 '对任意 `i < j`，不存在 `i < k < j` 使 `A[k]*2 = A[i]+A[j]`',
                 '示例：`N=4` → `[2,1,4,3]`；本视频 `N=7`'],
        quote='若存在一个数组A为漂亮数组，那么将A中每个数乘以2，得到的也必然是漂亮数组。同样的，将A中每个数乘以2再减1，得到的也必然是漂亮数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['`A[i]+A[j]` 若一奇一偶，必为奇数，不可能等于 `2·A[k]` → 奇偶分开',
              '漂亮数组整体 ×2 或 ×2−1 保持漂亮（两边约掉 2 得矛盾）',
              '从 `[1]` 开始每轮翻倍：奇数部分 + 偶数部分，直到长度 ≥ N，再删去大于 N 的'],
        summary=['时间 `O(N)`，空间 `O(N)`',
                 '易错：奇数部分是 `x+x-1`，要放在偶数部分前面',
                 '删去大于 `N` 的数不改变相对顺序，子序列仍然漂亮',
                 '原文为 Python 2 风格，代码在 Python 3 下无需改动'],
    ),
)
