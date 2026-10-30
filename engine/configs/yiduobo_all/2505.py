CONFIG = dict(
    num=2505, title='所有子序列和的按位或', difficulty='Medium', category='位运算',
    author='yiduobo', technique='一趟遍历 · 累加和 + 逐个 OR',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def subsequenceSumOr(self, nums):

        res = 0
        s = 0
        for num in nums:
            res |= num
            s += num
            res |= s
        
        return res
''',
    call='Solution().subsequenceSumOr([2,1,3])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None),
        dict(type='text', h=70, size=34, fn=lambda S: f"`res` = `{S['res']:04b}` = =={S['res']}==" if 'res' in S else ''),
        dict(type='text', h=70, size=34, fn=lambda S: f"`s`   = `{S['s']:04b}` = {S['s']}" if 's' in S else ''),
    ],
    watch=['num', ('s', 's', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 是答案：所有子序列和的 OR',
        's = 0': '`s` 是目前所有数的累加和',
        'for num in nums': lambda S, B, r: (f'取下一个数 `num = {S.num}`' if S.num != B.get('num') else '遍历完了'),
        'res |= num': '这个数本身就是一个子序列的和：`res = {B.res:b} | {num:b}` = `{res:b}`',
        's += num': '把它加进累加和：`s` = {s}（二进制 `{s:b}`）。某一位若靠进位变成 1，累加顺序不影响',
        'res |= s': '累加和也是某个子序列的和：`res = {B.res:b} | {s:b}` = `{res:b}` = =={res}==',
        'return res': '一趟下来，`res` = `{res:b}` = =={res}==',
    },
    cards=dict(
        one_liner='每个数和累加和各 OR 一次，进位不会被漏掉',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 的每个子序列都有一个元素和',
                 '返回所有这些子序列和的按位或',
                 '数组很长，不能枚举子序列；本视频：`[2,1,3]` → `7`'],
        quote='如果当前的某个子序列的和第p位同样不为1，那么数组中还不属于该子序列的任意数加入到子序列中，其产生的进位也不可能越过p这一位而直接进位到p左侧这一位。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 p 位若在答案里为 1：要么某个数这一位是 1，要么靠累加和的进位',
              '要靠累加和：说明所有数这一位都是 0，进位不会跳过这一位',
              '所以顺序不重要：逐个累加，每次把 `num` 和 `s` 都 OR 进 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文是 Python 2 风格，在 Python 3 下可直接运行，未做改动',
                 '易错：只 OR 累加和会漏掉「单个数」；只 OR 单个数会漏掉进位产生的位',
                 '简报中没有题面，题意按 yiduobo 文章和原题理解'],
    ),
)
