CONFIG = dict(
    num=3718, title='缺失的最小倍数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='集合 + while 步长 k',
    tags=[],
    code='''
class Solution(object):
    def missingMultiple(self, nums, k):
        
        num_set = set(nums)
        res = k
        while res in num_set:
            res += k
        return res
''',
    call='Solution().missingMultiple([8,2,3,4,6], 2)',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums', cell=80, h=170),
        dict(type='set', var='num_set', label='num_set', fmt=lambda x: str(x), h=170, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"`res = {S['res']}`：{'已在集合中，继续 +k' if S['res'] in S['num_set'] else '不在集合中，结束'}" if 'res' in S and 'num_set' in S else '')),
    ],
    watch=['k', ('res', 'res', 'green')],
    captions={
        'num_set = set': '先把 `nums` 转成集合：`num_set = {num_set}`',
        'res = k': '最小的倍数是 `k` 本身，从 `res = {res}` 开始试',
        'while res in num_set': '`{res}` 在集合里吗？ → ' + '{"在，说明这个倍数没缺失，继续" if res in num_set else "不在，缺失，退出循环"}',
        'res += k': '步长为 `k` 向上：`res` → {res}',
        'return res': '循环结束时 `res` 首个不在集合里 → 返回 `{res}`',
    },
    cards=dict(
        one_liner='从 k 开始，以步长 k 往上走，撞上第一个不在集合里的就停',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `nums` 与整数 `k`',
                 '找出==不在 nums 中、且是 k 的倍数==的最小值',
                 '示例：`[8,2,3,4,6]`，`k=2` → `10`'],
        quote='先将nums转化为集合，然后从k开始，以步长k向上迭代，迭代过程中首个不在集合中的元素即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums` 转集合，查询 `O(1)`',
              '`res = k` 起步，`while res in num_set` 就 `res += k`',
              '跳出循环时的 `res` 就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '起点是 `k`，不是 0',
                 '循环最多 `len(nums)` 次就会跳出，不会死循环',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改'],
    ),
)
