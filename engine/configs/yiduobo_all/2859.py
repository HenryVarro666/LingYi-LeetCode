def _pos(S):
    return S['nums'].index(S['v']) if 'v' in S else None


def _col(S, i, v):
    p = _pos(S)
    if p is None:
        return None
    if i == p:
        return 'blue'
    if i < p and bin(i).count('1') == S['k']:
        return 'green'
    return None


CONFIG = dict(
    num=2859, title='计算 K 置位下标对应元素的和', difficulty='Easy', category='位运算',
    author='yiduobo', technique='lowbit 逐个去掉最低位的 1 计数',
    code='''
class Solution(object):
    def sumIndicesWithKSetBits(self, nums, k):

        res = 0
        for index, v in enumerate(nums):
            cnt = 0
            while index:
                cnt += 1
                index -= index & -index

            if cnt == k:
                res += v
        
        return res
''',
    call='Solution().sumIndicesWithKSetBits([5,10,1,6,2], 1)',
    expect=13,
    views=[
        dict(type='array', var='nums', color=_col, dim=lambda S, i, v: _pos(S) is not None and i < _pos(S) and bin(i).count('1') != S['k'], h=300),
        dict(type='text', fn=lambda S: (f"当前 `index = {S['index']}` = `{bin(S['index'])[2:]}`，`cnt = {S['cnt']}`，k = {S['k']}" if 'cnt' in S else f"目标：下标二进制里恰有 `k = {S['k']}` 个 1"), h=70),
    ],
    watch=['index', 'v', 'cnt', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累加满足条件的元素',
        'for index, v in enumerate': lambda S, B, r: (
            '下标都遍历完，退出循环' if B.get('index') == S.index and B.get('v') == S.v
            else f'取下标 `index = {S.index}`（二进制 `{bin(S.index)[2:]}`），元素 `v = {S.v}`'),
        'cnt = 0': '`cnt` 用来数 `index` 里 1 的个数，先清零',
        'while index': lambda S, B, r: (
            f'`index = {S.index}` 还有 1 → 继续数' if S.index else '`index` 变成 0：1 已经数完'),
        'cnt += 1': '找到一个 1：`cnt` → {cnt}',
        'index -= index & -index': 'lowbit：`index & -index` 取出最低位的 1，减掉它 → `index = {index}`',
        'if cnt == k': '`cnt == k`？{cnt} vs {k} → {"相等，累加" if cnt == k else "不等，跳过"}',
        'res += v': '`res` += `{v}` → =={res}==',
        'return res': '全部下标处理完，答案 `{res}`',
    },
    cards=dict(
        one_liner='用 lowbit 不断去掉最低位的 1，数几次就是置位数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['给 `nums` 和 `k`，求下标二进制里恰有 `k` 个 1 的元素之和',
                 '例如下标 `1, 2, 4` 的二进制都只有一个 1',
                 '示例：`[5,10,1,5,2], k=1` → `13`',
                 '本视频：`[5,10,1,6,2], k=1` → 同样是 `13`'],
        quote='直接按照题目的描述一趟遍历，对于当前遍历到的下标index对应的数字v，计算index二进制表示中1的数目cnt，若cnt等于k，那么就将v累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，对每个下标自己数 1 的个数 `cnt`',
              '数法：`index & -index` 取最低位的 1，`index -= lowbit` 去掉它',
              '`cnt == k` 就把 `v` 加进 `res`'],
        summary=['时间 `O(n log n)`（每个下标最多数 log n 次），空间 `O(1)`',
                 '易错点：循环里改的是 `index` 本身，不要拿它再去取 `nums`',
                 '原文为 Python 2 风格，代码逐字保留，只删去了空行里的说明',
                 '对比灵神：灵神直接用 `bit_count()`，这里手写 lowbit 计数，思路相同'],
    ),
)
