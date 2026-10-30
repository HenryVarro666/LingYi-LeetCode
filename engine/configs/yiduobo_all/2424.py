CONFIG = dict(
    num=2424, title='最长上传前缀', difficulty='Medium', category='设计',
    author='yiduobo', technique='布尔数组 + 上次位置继续查',
    tags=[],
    code='''
class LUPrefix(object):

    def __init__(self, n):
        self.p = 0
        self.n = n
        self.uploaded = [False] * n

    def upload(self, video):
        self.uploaded[video - 1] = True

    def longest(self):
        while self.p < self.n and self.uploaded[self.p]:
            self.p += 1

        return self.p
''',
    call='''server = LUPrefix(5)
res = []
server.upload(3)
res.append(server.longest())
server.upload(1)
res.append(server.longest())
server.upload(2)
res.append(server.longest())
server.upload(5)
res.append(server.longest())
res''',
    expect=[0, 1, 3, 3],
    views=[
        dict(type='array', var='self.uploaded', label='uploaded（下标 i 对应视频 i+1）',
             pointers={'self.p': 'blue'},
             color=lambda S, i, v: 'green' if v else None, h=190),
        dict(type='text', size=30, fn=lambda S: (f"`p = {S['self.p']}`：下标 0 ~ {S['self.p'] - 1} 都是 True" if S['self.p'] > 0 else "`p = 0`：前缀长度为 0") if 'self.p' in S else ''),
    ],
    watch=[('self.p', 'self.p', 'blue'), 'res'],
    captions={
        'self.p = 0': '`p` 是已确认的前缀长度，也是下一个要检查的下标',
        'self.uploaded = ': '`uploaded[i]` 记录视频 `i+1` 是否上传',
        'self.uploaded[video - 1] = True': '视频 `{video}` 上传 → `uploaded[{video - 1}] = True`（视频编号从 1 开始，下标减 1）',
        'while self.p < self.n': lambda S, B, r: (f'`p = {S["self.p"]}`，`uploaded[{S["self.p"]}]` 为 True → 前缀继续延长'
                                                   if S['self.p'] < S['self.n'] and S['self.uploaded'][S['self.p']]
                                                   else (f'`p = {S["self.p"]}` 已到 n → 停' if S['self.p'] >= S['self.n']
                                                         else f'`uploaded[{S["self.p"]}]` 为 False → 视频 {S["self.p"] + 1} 没传，停')),
        'self.p += 1': '这一格已上传 → `p` 前进到 =={self.p}==',
        'return self.p': '最长上传前缀 = `p` = =={ret}==（接着上次的位置查，不用重来）',
    },
    cards=dict(
        one_liner='上传越多前缀越长，每次接着上次的位置往后查',
        complexity='`upload` `O(1)`，`longest` 均摊 `O(1)`，空间 `O(n)`',
        problem=['依次上传编号 `1~n` 的视频', '`longest()` 返回最长的 `i`，使视频 `1~i` 都已上传',
                 '本视频：`n=5`，上传 3、1、2、5'],
        quote='对着上传的进行，题目要查询的当前最长上传前缀必然是越来越长的。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目看似是区间问题，其实只要记录哪些视频已上传',
              '每次询问在==上次结果==的基础上继续向后查',
              '`p` 只增不减，总共最多走 `n` 步，均摊 `O(1)`'],
        summary=['均摊 `O(1)`，空间 `O(n)`',
                 '易错：视频编号从 1 开始，数组下标要 `video - 1`',
                 '`while` 条件先判 `p < n` 再访问数组，防止越界',
                 '对比灵神：灵神用集合并从 1 开始数；这里用布尔数组，`p` 直接当长度'],
    ),
)
