CONFIG = dict(
    num=3114, title='替换字符可以得到的最晚时间', difficulty='Easy', category='字符串',
    author='yiduobo', technique='分情况讨论', tags=[],
    code='''
class Solution(object):
    def findLatestTime(self, s):

        res = list(s)
        if res[0] == '?':
            if res[1] == '?':
                res[0] = '1'
                res[1] = '1'
            elif res[1] <= '1':
                res[0] = '1'
            else:
                res[0] = '0'
        
        elif res[1] == '?':
            if res[0] == '0':
                res[1] = '9'
            else:
                res[1] = '1'
        

        if res[3] == '?':
            res[3] = '5'
        if res[4] == '?':
            res[4] = '9'
        
        return ''.join(res)
''',
    call='Solution().findLatestTime("?4:5?")',
    expect='04:59',
    views=[
        dict(type='array', var='res', h=220, cell=100,
             color=lambda S, i, v: 'yellow' if v == '?' else None),
        dict(type='text', size=32, fn=lambda S: '小时最大 11，分钟最大 59'),
    ],
    watch=[('时间', "''.join(res)", 'green')],
    captions={
        'res = list': '转成列表，`?` 的位置待填',
        "if res[0] == '?'": lambda S, B, r: ("小时高位是 `?`，分三种情况" if S.res[0] == '?' else f"小时高位已是 `{S.res[0]}`"),
        "if res[1] == '?':": lambda S, B, r: ("高低位都是 `?` → 填 11" if S.res[0] == '1' and False else
                                              ("低位也是 `?`" if S.res[1] == '?' else f"低位是 `{S.res[1]}`")),
        "elif res[1] <= '1'": '低位 `{res[1]}` <= 1：高位填 1（10、11 都合法）',
        "res[0] = '0'": '低位是 2~9：高位只能填 `0`',
        "res[1] = '9'": '高位是 0：低位最大填 `9`',
        "res[1] = '1'": '高位是 1：低位最大只能到 `1`（11）',
        "if res[3] == '?'": lambda S, B, r: ("分钟高位是 `?`" if S.res[3] == '?' else f"分钟高位已是 `{S.res[3]}`"),
        "res[3] = '5'": '分钟高位填 `5`',
        "if res[4] == '?'": lambda S, B, r: ("分钟低位是 `?`" if S.res[4] == '?' else f"分钟低位已是 `{S.res[4]}`"),
        "res[4] = '9'": '分钟低位填 `9`',
        "return ''.join": '拼回字符串：=={r}==',
    },
    cards=dict(
        one_liner='小时位分情况填，分钟位直接 5 和 9',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['12 小时制 `HH:MM`，`?` 要被数字替换', '要求结果有效且时间最晚',
                 '本视频：`"?4:5?"` → `"04:59"`'],
        quote='若仅有高位为问号，那么只有当低位上为0或者1时，高位上才能填充1，否则只能填充0。',
        quote_src='—— yiduobo 题解原文',
        idea=['小时最多 11，分钟最多 59', '小时高位是 `?`：低位也是 `?` 填 11；低位 <= 1 填 1；否则填 0',
              '仅低位是 `?`：高位为 0 填 9，否则填 1'],
        summary=['时间 `O(1)`，空间 `O(1)`', '代码原样照搬，Python 3 可直接运行',
                 '易错：高位是 `?` 时低位若是 `?` 要同时填 `1`，不能漏',
                 '对比灵神：灵神把小时位压成两个三目表达式，这里列全分支'],
    ),
)
