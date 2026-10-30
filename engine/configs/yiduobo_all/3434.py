N0, K0 = [2, 3, 1, 3, 3, 2], 1


def _seg(S, i, v):
    idx = S.get('index')
    if idx is None:
        return None
    if v == K0:
        return 'green'
    st = S.get('start', {})
    if i == idx and v != K0:
        return 'yellow'
    if v != K0 and v in st and i >= st[v] and i <= idx:
        return 'blue' if v == S.get('v') else None
    return None


def _text(S):
    if 'index' not in S or 'v' not in S:
        return '对目标值 `v`：`v` 记 +1，`k` 记 −1，其余 0，求最大子段和 → 就是「v 个数 − k 个数」'
    v = S['v']
    if v == K0:
        return f'`v = k = {K0}`：只累计前缀 k 的个数 `cnt_k[-1] = {S["cnt_k"][-1]}`'
    if v not in S['start']:
        return f'`v = {v}` 还没有可用子段'
    st = S['start'][v]
    kk = S['cnt_k'][-1] - S['cnt_k'][st]
    return f'`v = {v}`：子段从下标 `{st}` 起，`v` 有 `{S["cnt"].get(v, 0)}` 个，`k` 有 `{kk}` 个 → 净增益 =={S["cnt"].get(v, 0) - kk}=='


CONFIG = dict(
    num=3434, title='子数组操作后的最大频率', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='转成最大子段和 · 每个值各记一个起点',
    tags=['灵神题单', '动态规划', '难度分 2094'],
    code='''
class Solution(object):
    def maxFrequency(self, nums, k):
        
        cnt = {}
        cnt_k = [0]
        start = {}
        res = 0

        for index, v in enumerate(nums):
            cnt_k.append(cnt_k[-1])
            if v == k:
                cnt_k[-1] += 1
            else:
                cnt[v] = cnt.get(v, 0) + 1
                if cnt[v] == 1 or cnt_k[-1] - cnt_k[start[v]] >= cnt[v]:
                    cnt[v] = 1
                    start[v] = index
                
                res = max(res, cnt[v] - (cnt_k[-1] - cnt_k[start[v]]))

        return res + cnt_k[-1]
''',
    call=f'Solution().maxFrequency({N0!r}, {K0})',
    expect=3,
    skip=['cnt = {}', 'start = {}', 'res = 0', 'cnt_k = [0]'],
    views=[
        dict(type='array', var='nums', label='nums（绿 = k，黄 = 当前元素）', h=200, cell=84,
             pointers={'index': 'blue'}, color=_seg),
        dict(type='array', var='cnt_k', label='cnt_k[i]：前 i 个数里 k 的个数（前缀和）', h=140, cell=70),
        dict(type='map', var='cnt', label='cnt[v]：v 在当前可用子段里的个数', h=100),
        dict(type='map', var='start', label='start[v]：v 的可用子段起点', h=100),
        dict(type='text', fn=_text, size=24, h=80),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        'for index, v in enumerate': lambda S, B, r: ('`nums` 遍历完了，循环结束' if S.get('index') == B.get('index')
                                                      else f'看第 `{S.index}` 个数 `v = {S.v}`'),
        'cnt_k.append': '前缀和多一格：先抄上一格 `cnt_k[-1] = {cnt_k[-1]}`',
        'if v == k': lambda S, B, r: (f'`v = {S.v}` 就是 `k`：不能当目标，只记前缀' if S.v == S.k else f'`v = {S.v}` 不是 `k`：当目标值 `v` 来处理'),
        'cnt_k[-1] += 1': '遇到 `k`：前缀 `k` 的个数 +1 → `cnt_k[-1] = {cnt_k[-1]}`',
        'cnt[v] = cnt.get': '`v = {v}` 在可用子段里多一个：`cnt[{v}] = {cnt[v]}`',
        'if cnt[v] == 1 or': lambda S, B, r: (f'`cnt[{S.v}] = 1`：第一次出现，从这里开始一个新子段' if S.cnt[S.v] == 1
                                              else f'子段内 `k` 有 `{S.cnt_k[-1] - S.cnt_k[S.start[S.v]]}` 个，`v` 有 `{S.cnt[S.v]}` 个：' + ('k 不比 v 少 → 子段不划算，丢掉重来' if S.cnt_k[-1] - S.cnt_k[S.start[S.v]] >= S.cnt[S.v] else 'v 更多 → 继续延长子段')),
        'cnt[v] = 1': '重置：`cnt[{v}] = 1`（只含当前这个 v）',
        'start[v] = index': '新起点 `start[{v}] = {index}`',
        'res = max(': lambda S, B, r: f'净增益 `cnt[{S.v}] − (k 的个数)` = `{S.cnt[S.v]} − {S.cnt_k[-1] - S.cnt_k[S.start[S.v]]}` = {S.cnt[S.v] - (S.cnt_k[-1] - S.cnt_k[S.start[S.v]])}，`res = max({B.res}, ·)` = =={S.res}==',
        'return res': '最大净增益 `{res}` + 原有 `k` 的个数 `{cnt_k[-1]}` = =={res + cnt_k[-1]}==',
    },
    cards=dict(
        one_liner='只改非 k 的值 v：转成「v 记 +1、k 记 −1」的最大子段和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选一个子数组，把里面每个数都加上同一个整数，求操作后 `k` 最多出现几次',
                 '示例：`nums = [2,3,1,3,3,2], k = 1` → `3`',
                 '把 `[3,1,3,3]` 整体减 2，得到 3 个 1'],
        quote='对于指定的非k元素v，如果仅考虑将v修改成k，那么问题就可以转化为将nums中所有的v变为1，所有的k变为-1，其他的元素变为0，求数组中的最大子段和。',
        quote_src='—— yiduobo 题解原文',
        idea=['修改子数组里的 `k` 一定不划算，所以答案 = 原有 `k` 的个数 + 最大净增益',
              '净增益 = 子段里 `v` 的个数 − 子段里 `k` 的个数',
              '一趟遍历同时处理所有 `v`：`cnt[v]` 记个数，`start[v]` 记子段起点，`cnt_k` 前缀和算子段里的 k'],
        summary=['时间 `O(n)`：每个元素只处理一次',
                 '子段里 `k` 不比 `v` 少，就等价于「子段和 ≤ 0」，丢弃重来',
                 '易错：重置时 `cnt[v] = 1`、`start[v] = index` 要一起改',
                 '对比灵神：灵神用左/中/右三个状态机；yiduobo 用最大子段和 + 每值一个起点'],
    ),
)
