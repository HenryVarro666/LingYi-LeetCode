NUMS = [-1, 10, 6, 7, -7, 1]


def _col(S, i, v):
    if 'num' not in S or S['_line'] == 14:
        return None
    if S['num'] == v and v == NUMS[i]:
        return 'yellow'
    if v in S['neg_set']:
        return 'cyan'
    return None


def _top(S):
    if 'res' not in S:
        return '第一趟：把所有==负数==放进哈希表 `neg_set`'
    if 'num' in S and S['_line'] in (11, 12):
        return f"第二趟：`num = {S['num']}`，查 `-num = {-S['num']}` 是否是出现过的负数"
    return '第二趟：枚举每个数，看它的相反数在不在 `neg_set`'


def _if2(S, B, ret):
    x = S.num
    if -x in S.neg_set:
        return f'`-num = {-x}` 在 `neg_set` 中：`{x}` 和 `{-x}` 同时存在 → ==可以作为 k=='
    if x < 0:
        return f'`num = {x}` 是负数，`-num = {-x}` 不是负数，不可能在 `neg_set` 里'
    return f'`-num = {-x}` 不在 `neg_set` 中：`{x}` 没有对应的负数'


CONFIG = dict(
    num=2441, title='与对应负数同时存在的最大正整数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='两趟遍历 · 负数哈希表',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1168'],
    code='''
class Solution(object):
    def findMaxK(self, nums):

        neg_set = set()
        for num in nums:
            if num < 0:
                neg_set.add(num)
        
        res = -1
        for num in nums:
            if -num in neg_set:
                res = max(res, num)
        
        return res
''',
    call=f'Solution().findMaxK({NUMS})',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（黄 = 当前 num，青 = 已记入 neg_set 的负数）', cell=110, h=220, color=_col),
        dict(type='set', var='neg_set', label='neg_set：出现过的负数', fmt=lambda x: str(x), h=180),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'neg_set = set()': '第一趟：哈希表 `neg_set` 只记录==负数==',
        'if num < 0': lambda S, B, r: (f'`num = {S.num} < 0`：是负数，记下来' if S.num < 0 else f'`num = {S.num}` 是正数，第一趟跳过'),
        'neg_set.add(num)': '`neg_set` 加入 `{num}`',
        'res = -1': '第二趟开始：`res = -1`，找不到就返回 -1',
        'if -num in neg_set': _if2,
        'res = max': '用 `num` 更新答案：`res = max({B.res}, {num}) = {res}`',
        'return res': '最大的 k 是 =={res}==',
    },
    skip=['for num in nums'],
    cards=dict(
        one_liner='先把负数全部存进哈希表，再枚举正数查它的相反数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 不含 0，找最大的正整数 `k`，使 `k` 和 `-k` 都在数组中',
                 '不存在返回 `-1`',
                 '示例：`[-1,10,6,7,-7,1]` → `7`'],
        quote='先一趟遍历，使用哈希表记录所有出现的负数，然后再一趟遍历，若当前遍历到的数num，且相反数-num出现在了哈希表中，那么就用num来更新最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：只收集负数，`neg_set` 里全是负数',
              '第二趟：`-num` 在 `neg_set` 里 ⇒ `num` 一定是==正数==',
              '所以直接 `max(res, num)`，不用取绝对值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '只存负数，命中时 `num` 必为正数，答案无需 `abs`',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神一趟遍历、边查边存，所以要用 `abs(x)`'],
    ),
)
