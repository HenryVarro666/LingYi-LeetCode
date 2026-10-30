def _txt(S):
    if 'res' not in S or 'index' not in S:
        return ''
    i, v = S['index'], S['v']
    return f"`index = {i}` 是{'奇' if i % 2 else '偶'}数 → {'减去' if i % 2 else '加上'} `{v}`，当前 `res = {S['res']}`"


CONFIG = dict(
    num=3701, title='计算交替和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='按下标奇偶分支累加', tags=[],
    code='''
class Solution(object):
    def alternatingSum(self, nums):
        
        res = 0
        for index, v in enumerate(nums):
            if index % 2 == 0:
                res += v
            else:
                res -= v
        
        return res
''',
    call='Solution().alternatingSum([6,2,9,4,1,3])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 偶数下标加，粉 = 奇数下标减）', pointers={'index': 'blue'}, cell=100, h=220,
             color=lambda S, i, v: 'pink' if i % 2 else 'green'),
        dict(type='text', h=80, size=30, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 保存交替和，初始为 0',
        'for index, v': '看第 `{index}` 个元素 `{v}`',
        'if index % 2 == 0': '`index % 2 = {index % 2}` → {"偶数下标，要加" if index % 2 == 0 else "奇数下标，要减"}',
        'res += v': '`res = {B.res} + {v}` = =={res}==',
        'res -= v': '`res = {B.res} - {v}` = =={res}==',
        'return': '遍历结束，交替和 `{ret}`',
    },
    cards=dict(
        one_liner='看下标奇偶：偶数加，奇数减',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['交替和 = 偶数下标元素之和 − 奇数下标元素之和',
                 '即 `nums[0] - nums[1] + nums[2] - ...`',
                 '本视频：`[6,2,9,4,1,3]` → `7`'],
        quote='对nums进行一趟遍历，根据当前下标的奇偶性来更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`enumerate` 同时拿到下标和值',
              '`index % 2 == 0` 加到 `res`，否则从 `res` 减去'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：下标从 0 开始，首个元素是加',
                 '对比灵神：灵神写成一行 `ans += -x if i % 2 else x`，这里用 if / else 分支，逻辑一样'],
    ),
)
