IDS = ["one", "two", "three", "four"]


def _fmt(k, v):
    best = '-' if v[1] is None else IDS[v[1]]
    return f'{k}: 总播放 {v[0]} · 最佳 id {best}'


def _cur(S):
    if 'index' not in S:
        return '一趟遍历：哈希表 `user_dict[作者] = [播放总和, 最佳视频下标]`'
    i = S['index']
    return f"第 {i} 个视频：作者 `{S['creators'][i]}`，id `{S['ids'][i]}`，播放 =={S['views'][i]}=="


def _res_txt(S):
    if 'res' not in S or S.get('res') is None:
        return ''
    return f"当前领先的作者 `res` = =={S['res']}=="


CONFIG = dict(
    num=2456, title='最流行的视频创作者', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 总和 + 最佳视频下标',
    tags=[],
    code='''
class Solution(object):
    def mostPopularCreator(self, creators, ids, views):

        user_dict = {}
        n = len(creators)
        for index in range(n):
            name = creators[index]
            if name not in user_dict:
                user_dict[name] = [0, None]
            
            user_dict[name][0] += views[index]
            if user_dict[name][1] is None or views[user_dict[name][1]] < views[index] or (views[user_dict[name][1]] == views[index] and ids[user_dict[name][1]] > ids[index]):
                user_dict[name][1] = index
        
        res = None
        for name in user_dict:
            if res is None or user_dict[res[0]][0] < user_dict[name][0]:
                res = [name]
            elif user_dict[res[0]][0] == user_dict[name][0]:
                res.append(name)
        
        return [[x, ids[user_dict[x][1]]] for x in res]
''',
    call='Solution().mostPopularCreator(["alice","bob","alice","chris"], ["one","two","three","four"], [5,10,5,4])',
    expect=[["alice", "one"], ["bob", "two"]],
    views=[
        dict(type='text', fn=_cur, size=26, h=80),
        dict(type='array', var='views', label='views（蓝 = 当前视频）', cell=108, h=225, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='map', var='user_dict', label='user_dict：作者 → [播放总和, 最佳视频下标]', fmt=_fmt, font=30, h=230),
        dict(type='text', fn=_res_txt, size=28, h=70),
    ],
    watch=[('index', 'index', 'blue'), ('name', 'name', 'pink'), ('res', 'res', 'green')],
    captions={
        'user_dict = {}': '`user_dict` 以作者名为 key，记录每人的总播放量和最佳视频',
        'n = len': '一共 `n = {n}` 个视频',
        'for index in range': lambda S, B, r: ('视频全部统计完，开始挑最流行的作者' if S.index == B.get('index') and S.index == S.n - 1 else f'看第 `{S.index}` 个视频'),
        'name = creators[index]': '作者是 `{name}`',
        'if name not in user_dict': lambda S, B, r: (f'`{S.name}` 还没有记录 → 先建一条' if S.name not in S.user_dict else f'`{S.name}` 已有记录'),
        'user_dict[name] = [0, None]': '新建：总播放 `0`，最佳视频还没有（`None`）',
        'user_dict[name][0] +=': '`{name}` 总播放加上 `{views[index]}` → `{user_dict[name][0]}`',
        'if user_dict[name][1] is None': lambda S, B, r: (
            f'`{S.name}` 还没有最佳视频 → 当前视频就是最佳' if S.user_dict[S.name][1] is None
            else (f'`{S.views[S.user_dict[S.name][1]]} < {S.views[S.index]}`：新视频播放更多 → 更新最佳'
                  if S.views[S.user_dict[S.name][1]] < S.views[S.index]
                  else (f'播放量相同，`{S.ids[S.user_dict[S.name][1]]!r} > {S.ids[S.index]!r}`：新 id 字典序更小 → 更新最佳'
                        if S.views[S.user_dict[S.name][1]] == S.views[S.index] and S.ids[S.user_dict[S.name][1]] > S.ids[S.index]
                        else (f'播放量相同，但 `{S.ids[S.index]!r}` 字典序不更小 → 保持原最佳'
                              if S.views[S.user_dict[S.name][1]] == S.views[S.index]
                              else f'`{S.views[S.user_dict[S.name][1]]} > {S.views[S.index]}`：旧的更受欢迎 → 保持原最佳')))),
        'user_dict[name][1] = index': '`{name}` 的最佳视频记为下标 `{index}`（id `{ids[index]}`）',
        'res = None': '`res` 保存目前总播放最高的作者们（可能并列）',
        'for name in user_dict': lambda S, B, r: ('作者都看完了' if S.name == B.get('name') and S.name == list(S.user_dict)[-1]
                                                  else f'看作者 `{S.name}`：总播放 `{S.user_dict[S.name][0]}`'),
        'if res is None or': lambda S, B, r: (
            f'还没有领先者 → `{S.name}` 先当' if S.res is None
            else (f'`{S.user_dict[S.res[0]][0]} < {S.user_dict[S.name][0]}`：`{S.name}` 更高 → 取代，重新开始' if S.user_dict[S.res[0]][0] < S.user_dict[S.name][0]
                  else '没有更高，再看是否并列')),
        'res = [name]': '领先者变为 `{res}`',
        'elif user_dict[res[0]][0] ==': lambda S, B, r: (f'`{S.user_dict[S.res[0]][0]} == {S.user_dict[S.name][0]}` → ==并列最高==，也要保留' if S.user_dict[S.res[0]][0] == S.user_dict[S.name][0]
                                                         else f'`{S.user_dict[S.name][0]}` 比领先者 `{S.user_dict[S.res[0]][0]}` 低 → 不要'),
        'res.append(name)': '并列：`res = {res}`',
        'return [[x': '每个领先作者配上最佳视频的 id：`{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='作者名做 key，累加播放量，再记最佳视频的下标',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['流行度 = 创作者所有视频播放量之和，求流行度==最高==的创作者（可并列）',
                 '并要给出他们各自播放量最大的视频 id，并列时取字典序最小',
                 '示例：alice、bob 总播放都是 10 → `[["alice","one"],["bob","two"]]`'],
        quote='一趟遍历，以作者名称作为哈希表的key，利用哈希表统计每个作者所有视频流行程度之和，同时记录每个作者最受欢迎的视频的id。',
        quote_src='—— yiduobo 题解原文',
        idea=['`user_dict[作者] = [总播放, 最佳视频下标]`，存==下标==而不是播放量，之后可同时查 views 与 ids',
              '更新最佳：当前视频播放更多，或 ==播放相同且 id 更小==',
              '第二轮扫哈希表：更高就重置 `res`，并列就追加'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '存下标可以同时拿到播放量和 id，一次比较写得有点长',
                 '易错：并列最高的作者都要返回；用 `elif` 追加',
                 '原文本身已是 Python 3 可运行写法，只保留代码、去掉文档字符串',
                 '对比灵神：灵神一边遍历一边维护全局最大值，最后一次推导式筛选；yiduobo 分两轮'],
    ),
)
