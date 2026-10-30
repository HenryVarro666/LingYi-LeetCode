CONFIG = dict(
    num=3386, title='按下时间最长的按钮', difficulty='Easy', category='模拟',
    author='yiduobo', technique='哈希表记录每个按钮的最长按压',
    tags=[],
    code='''
class Solution(object):
    def buttonWithLongestTime(self, events):
        
        pre_index, pre_time = events[0]
        cnt = {pre_index: pre_time}
        for index, time in events[1:]:
            cnt[index] = max(cnt.get(index, 0), time - pre_time)
            pre_index, pre_time = index, time

        max_time = 0
        res = None
        for index in cnt:
            if cnt[index] > max_time or (cnt[index] == max_time and (res is None or res > index)):
                res = index
                max_time = cnt[index]
        return res
''',
    call='Solution().buttonWithLongestTime([[1,2],[2,5],[3,9],[1,15]])',
    expect=1,
    views=[
        dict(type='grid', var='events', label='events = [按钮下标, 时间]', h=300,
             rows=lambda S: [f'事件{k}' for k in range(len(S['events']))], cols=['idx', 'time'],
             color=lambda S, i, j, v: 'blue' if 'index' in S and 'time' in S and S['events'][i] == [S['index'], S['time']] else None),
        dict(type='map', var='cnt', label='cnt：按钮 → 最长按压时间', h=250, fmt=lambda k, v: f'按钮 {k} → {v}'),
        dict(type='text', fn=lambda S: f"当前最优：按钮 `res = {S['res']}`，`max_time = {S['max_time']}`" if 'res' in S else '', size=26),
    ],
    watch=[('pre_time', 'pre_time', 'cyan'), 'index', 'time', ('max_time', 'max_time', 'orange'), ('res', 'res', 'green')],
    captions={
        'pre_index, pre_time = events[0]': '第一个按钮的按压时间就是时间戳 `{pre_time}`',
        'cnt = {': '哈希表 `cnt` 记录每个按钮的最长按压时间：`{cnt}`',
        'for index, time in events[1:]': lambda S, B, r: ('所有事件处理完，`cnt = ' + str(S.cnt) + '`' if B.get('time') == S.time and B.get('pre_time') == S.pre_time
                                                          else f'这次按下按钮 `{S.index}`，时间 `{S.time}`，上一次时间 `{S.pre_time}`'),
        'cnt[index] = max': '按压时间 = `{time} − {pre_time}` = {time - pre_time}，和按钮 `{index}` 之前的记录取较大 → `cnt[{index}] = {cnt[index]}`',
        'pre_index, pre_time = index, time': '把这次事件当作“上一次”：`pre_time = {pre_time}`',
        'max_time = 0': '第二趟：遍历哈希表找按压最久、下标最小的按钮，`max_time` 初值 0',
        'res = None': '`res` 还没有候选',
        'for index in cnt': lambda S, B, r: ('哈希表遍历完了' if B.get('index') == S.index and S.index == 3 and B.get('max_time') == S.max_time and S._line == 12 and S.res == 1 and 'index' in B and list(S.cnt)[-1] == S.index and B.get('index') == list(S.cnt)[-1]
                                             else f'检查按钮 `{S.index}`，按压 `{S.cnt[S.index]}`'),
        'if cnt[index] > max_time': lambda S, B, r: (
            f'`{S.cnt[S.index]} > {S.max_time}` → ==更长==，成为新答案' if S.cnt[S.index] > S.max_time
            else f'`{S.cnt[S.index]} == {S.max_time}` 且 `res = {S.res} > {S.index}` → ==并列取下标小的==' if S.cnt[S.index] == S.max_time and (S.res is None or S.res > S.index)
            else f'`{S.cnt[S.index]}` 不比 `max_time = {S.max_time}` 长（并列时下标也不更小）→ 跳过'),
        'res = index': '`res = {res}`',
        'max_time = cnt[index]': '`max_time = {max_time}`',
        'return res': '按压最久的按钮：`{res}`',
    },
    cards=dict(
        one_liner='先用哈希表统计每个按钮最长按压，再扫一遍取最大且下标最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`events[i] = [index, time]`，按压时间 = 与上一次按下的时间差，第一个是时间戳',
                 '求按压时间最长、并列时下标最小的按钮',
                 '示例 `[[1,2],[2,5],[3,9],[1,15]]` → `1`'],
        quote='首先对于events进行一趟遍历，使用当前的时间戳和上一个时间戳之差计算按下当前按钮的时间，并使用哈希表统计每种按钮按下的总时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：算出每次按压时间，按钮重复出现就保留较大值',
              '第二趟：遍历哈希表，找按压最长的；并列时下标小的优先',
              '`res is None` 处理第一个候选'],
        summary=['时间 `O(n)`，空间 `O(n)`（哈希表）',
                 '原文哈希表写的是“总时间”，代码里实际是取 `max`，按压时间不累加',
                 '易错：并列取下标最小，所以条件里要加 `res > index`',
                 '代码原样照搬，没有 Python 2 专有写法'],
    ),
)
