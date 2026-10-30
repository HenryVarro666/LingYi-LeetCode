K = 7


def _di(S):
    v = S.get('v')
    if v is None or v not in S['diff']:
        return None
    return S['diff'].index(v)


def _txt(S):
    if 'res' not in S:
        return '`diff[i] = (nums[i] ^ k) - nums[i]`：异或后是赚还是亏'
    if 'v' not in S:
        return f"`res = {S['res']}`（原数组之和）"
    mp, mn = S.get('mi_pos'), S.get('ma_non_pos')
    return (f"`res = {S['res']}`   正数个数 `pos_cnt = {S['pos_cnt']}`   最小正数 `mi_pos = {mp}`   最大非正数 `ma_non_pos = {mn}`")


CONFIG = dict(
    num=3068, title='最大节点价值之和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='贪心 · 取正收益，奇数个时调整',
    tags=['灵神题单', '动态规划', '难度分 2268'],
    code='''
class Solution(object):
    def maximumValueSum(self, nums, k, edges):

        diff = [(x ^ k) - x for x in nums]
        res = sum(nums)
        mi_pos = None
        pos_cnt = 0
        ma_non_pos = None

        for v in diff:
            if v > 0:
                if mi_pos is None or mi_pos > v:
                    mi_pos = v
                res += v
                pos_cnt += 1
            else:
                if ma_non_pos is None or ma_non_pos < v:
                    ma_non_pos = v
        
        if pos_cnt % 2 == 1:
            if ma_non_pos is not None and mi_pos + ma_non_pos > 0:
                res += ma_non_pos
            else:
                res -= mi_pos
        
        return res
''',
    call='Solution().maximumValueSum([2, 3, 5, 8], 7, [[0, 1], [1, 2], [2, 3]])',
    expect=28,
    skip=['mi_pos = None', 'pos_cnt = 0', 'ma_non_pos = None'],
    views=[
        dict(type='array', var='nums', label='nums（边是多余的，不用管）', h=180, cell=100),
        dict(type='array', var='diff', label='diff = (x^k) − x（绿 = 异或后变大，粉 = 不赚；蓝框 = 当前 v）', h=210, cell=100,
             color=lambda S, i, v: ('blue' if i == _di(S) else ('green' if v > 0 else 'pink'))),
        dict(type='text', fn=_txt, size=26, h=110),
    ],
    watch=[('res', 'res', 'green'), 'v', 'pos_cnt', 'mi_pos', 'ma_non_pos'],
    captions={
        'diff = [': '`diff = {diff}`：每个数异或 `k` 之后的变化量，正数才值得异或',
        'res = sum(nums)': '先把原数组之和 `{res}` 当作基础答案',
        'for v in diff': lambda S, B, r: ('diff 都扫完了' if B.get('v') == S.v else f'`v = {S.v}`'),
        'if v > 0': lambda S, B, r: (f'`v = {S.v} > 0`：异或有收益 → ==选它==' if S.v > 0 else f'`v = {S.v} ≤ 0`：异或不赚，先记下最大的非正数'),
        'if mi_pos is None': '`mi_pos` 记录最小的正收益：万一正数个数是奇数，要扔掉的就是它',
        'mi_pos = v': '`mi_pos = {mi_pos}`',
        'res += v': '`res += {v}` → {res}',
        'pos_cnt += 1': '正数个数 `pos_cnt = {pos_cnt}`',
        'if ma_non_pos is None': '`ma_non_pos` 记录最大的非正收益：奇数个时可以拉它来凑成一对',
        'ma_non_pos = v': '`ma_non_pos = {ma_non_pos}`',
        'if pos_cnt % 2 == 1': lambda S, B, r: (f'正数有 `{S.pos_cnt}` 个，==奇数==：必须成对操作，要么再拉一个凑对，要么扔掉最小的正数'
                                                if S.pos_cnt % 2 == 1 else f'正数有 `{S.pos_cnt}` 个，偶数个，直接成对操作'),
        'if ma_non_pos is not None and': lambda S, B, r: (f'`mi_pos + ma_non_pos = {S.mi_pos} + {S.ma_non_pos} = {S.mi_pos + S.ma_non_pos}`'
                                                          + (' > 0 → 拉进来仍然赚' if S.mi_pos + S.ma_non_pos > 0 else ' ≤ 0 → 凑对要亏，不如不操作')),
        'res += ma_non_pos': '多异或一个非正数：`res += {ma_non_pos}` → {res}',
        'res -= mi_pos': '放弃最小的正数：`res -= {mi_pos}` → {res}',
        'return res': '最大价值之和 =={ret}==',
    },
    cards=dict(
        one_liner='能异或得正收益的都选，个数是奇数就舍一个最亏的',
        complexity='时间 `O(n)`，空间 `O(n)`（`diff` 数组）',
        problem=['树上每次选一条边，把两端点的值都异或 `k`',
                 '求操作若干次后所有节点之和的最大值',
                 '示例：`nums=[2,3,5,8]`, `k=7` → `28`'],
        quote='换言之，本题中树的形态无关紧要，可以视为给出一个数组，每一轮从中选出两个数执行异或k的操作，要求执行操作之后数组和最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['路径两端异或一次、中间节点异或两次抵消 → 树形态无关',
              '同一个数异或两次没意义，只看每个数异或后的差 `diff`，正的全选',
              '操作必须成对：正数个数为奇数时，比较「拉进最大非正数」与「扔掉最小正数」'],
        summary=['时间 `O(n)`，空间 `O(n)`；灵神用状态机 DP 同样 `O(n)` 时间，常数空间',
                 '奇数个正数时，只需比较 `mi_pos + ma_non_pos` 是否 > 0',
                 '`ma_non_pos` 可能不存在（全是正数），要先判 `is not None`',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
