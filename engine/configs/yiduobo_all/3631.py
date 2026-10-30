CONFIG = dict(
    num=3631, title='按严重性和可利用性排序', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='自定义排序键', tags=[],
    code='''
class Solution(object):
    def sortThreats(self, threats):
        
        return sorted(threats, key=lambda d:(-(d[1] * 2 + d[2]), d[0]))
''',
    call='Solution().sortThreats([[1,3,5],[2,6,1],[3,2,9],[4,4,3],[5,1,8]])',
    expect=[[2,6,1],[3,2,9],[1,3,5],[4,4,3],[5,1,8]],
    views=[
        dict(type='table', var='threats', rows=['威胁0','威胁1','威胁2','威胁3','威胁4'], cols=['id','sev','exp'], h=300),
        dict(type='text', h=120, size=30, fn=lambda S: '分数 `score = 2×sev + exp`：' + '，'.join(
            f'==id{d[0]}=={2*d[1]+d[2]}' for d in S['threats'])),
    ],
    watch=[('threats', 'threats')],
    captions={
        'return sorted': '排序键 `(-(2×sev + exp), id)`：==分数大的排前面==，分数相同 id 小的在前。排序后返回 `{ret}`',
    },
    cards=dict(
        after=[dict(heading='键怎么比较', lines=['Python 比较元组：先比第一项，相同再比第二项','`(-13, 2)` 与 `(-13, 3)`：第一项相同，比 id → 2 在前','`(-13, 3)` 与 `(-11, 1)`：-13 更小 → 分数 13 排在分数 11 前面'])],
        one_liner='把分数取负当排序键，就能一行搞定降序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个威胁 `[id, sev, exp]`，分数 `score = 2 * sev + exp`',
                 '按分数降序返回 `threats`，分数相同按 id 升序',
                 '本视频：`[[1,3,5],[2,6,1],[3,2,9],[4,4,3],[5,1,8]]`'],
        quote='直接按照题目要求计算每个威胁的分数，然后以分数为第一关键字倒序，下标为第二关键字正序，排序原数组的下标就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['id 1..5 的分数依次是 `11, 13, 13, 11, 10`，有两组并列',
              'sorted 默认升序 → 第一关键字取负数 `-score`，就变成降序',
              '第二关键字 `d[0]` 升序，处理分数相同的并列情况'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '降序 = 对关键字取负，比 `reverse=True` 更方便混合升降序',
                 '易错点：并列时要按 id 升序，不能依赖排序稳定性碰运气',
                 '原文代码只有一行，无需改动 Python 3'],
    ),
)
