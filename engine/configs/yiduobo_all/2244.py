CONFIG = dict(
    num=2244, title='完成所有任务需要的最少轮数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='分类统计 + 模 3 讨论',
    tags=['灵神题单', '难度分 1372'],
    code='''
class Solution(object):
    def minimumRounds(self, tasks):

        cnt_dict = {}
        for task in tasks:
            cnt_dict[task] = cnt_dict.get(task, 0) + 1
        
        res = 0
        for cnt in cnt_dict.values():
            if cnt == 1:
                return -1
            
            res += cnt // 3
            if cnt % 3 > 0:
                res += 1
        
        return res
''',
    call='Solution().minimumRounds([2,2,3,3,2,4,4,4,4,4])',
    expect=4,
    views=[
        dict(type='array', var='tasks', label='tasks', h=190,
             color=lambda S, i, v: 'yellow' if 'task' in S and v == S['task'] and 'cnt' not in S else ('yellow' if 'cnt' in S and False else None)),
        dict(type='map', var='cnt_dict', label='cnt_dict：每种任务的数量', fmt=lambda k, v: f'{k}: {v}', h=250),
        dict(type='text', h=110, size=30, fn=lambda S: f"cnt = {S['cnt']}：`{S['cnt']} // 3` = {S['cnt']//3}，余 {S['cnt']%3}" if 'cnt' in S else ''),
    ],
    watch=['task', 'cnt', ('res', 'res', 'green')],
    captions={
        'cnt_dict[task] =': '难度 `{task}` 的数量加 1 → `{cnt_dict[task]}`',
        'for task in tasks': '扫描任务 `{task}`',
        'if cnt == 1': lambda S, B, r: ('只有 1 个任务，每轮至少做 2 个，做不了 → 返回 -1' if S.cnt == 1 else f'`cnt = {S.cnt}`，不是 1，可以完成'),
        'res += cnt': '先尽量 3 个一轮：`cnt // 3 = {cnt // 3}` 轮 → `res = {res}`',
        'if cnt % 3 > 0': lambda S, B, r: (f'`{S.cnt} % 3 = {S.cnt % 3}`，有剩余 → 还要额外 1 轮（余 1 时从一轮 3 个里拿一个，凑成 2+2）'
                                          if S.cnt % 3 > 0 else '正好整除，不用额外一轮'),
        'res += 1': '额外加一轮 → `res = {res}`',
        'return res': '全部安排完，最少 `{res}` 轮',
    },
    cards=dict(
        one_liner='尽量三个一轮，有零头就多加一轮',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每轮完成 2 个或 3 个==相同难度==的任务，求最少轮数，做不到返回 `-1`',
                 '示例：`[2,2,3,3,2,4,4,4,4,4]` → `4`'],
        quote='为了使得轮数尽量少，就应该尽可能多地3个3个一轮来执行任务。',
        quote_src='—— yiduobo 题解原文',
        idea=['每种任务互不相关，先用字典分别统计数量 `cnt`',
              '`cnt = 1` 直接 -1；余 0：`cnt/3` 轮；余 2：多 1 轮装两个',
              '余 1：拿出一轮 3 个只放 2 个，剩下 1+1 凑一轮 → 也是多 1 轮'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去类型说明',
                 '易错：`cnt = 1` 要先判无解；余 1 不是多 2 轮',
                 '对比灵神：灵神一个公式 `(c+2)//3`，这里分「整除 + 余数」两步'],
    ),
)
