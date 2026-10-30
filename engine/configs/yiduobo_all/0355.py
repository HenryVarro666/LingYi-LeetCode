def _tw(k, v):
    return f"用户{k}: " + ' '.join(f't{-t}→{tid}' for t, tid in v)


def _heapfmt(x):
    return f't{-x[0]}:{x[1]}'


CONFIG = dict(
    num=355, title='设计推特', difficulty='Medium', category='设计',
    author='yiduobo', technique='每人一个推文栈 + 堆多路归并',
    tags=['labuladong'],
    code='''
import heapq

class Twitter(object):

    def __init__(self):
        self.tweet_dict = {}
        self.time_cnt = 0
        self.follow_dict = {}

    def postTweet(self, userId, tweetId):
        if userId not in self.tweet_dict:
            self.tweet_dict[userId] = []

        self.tweet_dict[userId].append([-self.time_cnt, tweetId])

        self.time_cnt += 1

    def getNewsFeed(self, userId):

        merge_id_list = []
        pos_list = []
        heap = []
        target_set = self.follow_dict.get(userId, set())
        target_set.add(userId)
        for followee in target_set:
            if followee in self.tweet_dict:
                merge_id_list.append(followee)
                heap.append(self.tweet_dict[followee][-1] + [len(merge_id_list) - 1])
                pos_list.append(len(self.tweet_dict[followee]) - 2)

        heapq.heapify(heap)

        res = []
        while len(res) < 10 and heap:
            author_time, tweetId, fromId = heapq.heappop(heap)
            res.append(tweetId)
            if pos_list[fromId] >= 0:
                heapq.heappush(heap, self.tweet_dict[merge_id_list[fromId]][pos_list[fromId]] + [fromId])
                pos_list[fromId] -= 1
        return res

    def follow(self, followerId, followeeId):
        if followerId not in self.follow_dict:
            self.follow_dict[followerId] = set()
        self.follow_dict[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        if followeeId in self.follow_dict.get(followerId, set()):
            self.follow_dict[followerId].remove(followeeId)
''',
    call='''tw = Twitter()
tw.postTweet(1, 5); tw.postTweet(2, 6); tw.postTweet(1, 7); tw.follow(1, 2); tw.postTweet(2, 8)
a = tw.getNewsFeed(1)
tw.unfollow(1, 2)
b = tw.getNewsFeed(1)
[a, b]''',
    expect=[[8, 7, 6, 5], [7, 5]],
    views=[
        dict(type='map', var='self.tweet_dict', label='tweet_dict：每人一个推文栈（t时间→推文）', fmt=_tw, h=130),
        dict(type='map', var='self.follow_dict', label='follow_dict：关注集合', fmt=lambda k, v: f'用户{k} 关注 {sorted(v)}', h=110),
        dict(type='heap', var='heap', label='heap 候选（时间:推文）', fmt=_heapfmt, top_color='pink', h=130),
        dict(type='array', var='res', label='res：信息流（新 → 旧）', cell=80, h=130),
    ],
    watch=[('time_cnt', lambda S: S.get('self.time_cnt'), 'purple'), ('userId', 'userId', 'blue'),
           ('pos_list', 'pos_list', 'orange')],
    captions={
        'self.tweet_dict = {}': '`tweet_dict`：用户 → 他发过的推文（当栈用，栈顶最新）',
        'self.time_cnt = 0': '`time_cnt`：全局发推计时器',
        'self.follow_dict = {}': '`follow_dict`：用户 → 关注的人的集合',
        'self.tweet_dict[userId] = []': '用户{userId} 第一次发推，建一个空栈',
        'self.tweet_dict[userId].append': '用户{userId} 发推 `{tweetId}`：存 `[-{B["self.time_cnt"]}, {tweetId}]`，==时间取负==让最小堆先弹最新的',
        'self.time_cnt += 1': '时钟 +1 → `{self.time_cnt}`',
        'target_set = self.follow_dict.get': '用户{userId} 关注的人：`{sorted(target_set)}`',
        'target_set.add(userId)': '==别忘了带上自己==：`{sorted(target_set)}`',
        'for followee in target_set': lambda S, B, r: ('要归并的人都看过了' if B.get('followee') == S.get('followee')
                                                       else f'看用户{S.followee} 的推文栈'),
        'if followee in self.tweet_dict': lambda S, B, r: (f'用户{S.followee} 发过推文' if S.followee in S['self.tweet_dict']
                                                          else f'用户{S.followee} 没发过推文，跳过'),
        'heap.append(': '用户{followee} 的==栈顶==（最新一条）`{heap[-1][1]}` 进候选堆，附上来源编号 `{heap[-1][2]}`',
        'pos_list.append': '`pos_list[{len(pos_list) - 1}] = {pos_list[-1]}`：下一条待取推文在栈里的下标',
        'heapq.heapify': '建堆：堆顶是所有人里==最新==的那条',
        'while len(res) < 10 and heap': lambda S, B, r: (f'`res` 有 {len(S.res)} 条 < 10 且堆不空 → 继续归并' if len(S.res) < 10 and S.heap
                                                         else ('堆空了，所有推文都取完' if not S.heap else '已经 10 条了')),
        'author_time, tweetId, fromId = heapq.heappop': '弹出堆顶 `{tweetId}`（时间 `{-author_time}`）：当前候选里==最新==的一条',
        'res.append(tweetId)': '`{tweetId}` 加入信息流 → `{res}`',
        'if pos_list[fromId] >= 0': lambda S, B, r: (f'来源用户{S.merge_id_list[S.fromId]} 还有更早的推文（下标 {S.pos_list[S.fromId]}）'
                                                    if S.pos_list[S.fromId] >= 0 else f'来源用户{S.merge_id_list[S.fromId]} 的推文取完了'),
        'heapq.heappush(heap, self.tweet_dict': '把用户{merge_id_list[fromId]} 的下一条补进堆 → 堆顶 `{heap[0][1]}`',
        'return res': '返回信息流 =={ret}==',
        'self.follow_dict[followerId] = set()': '用户{followerId} 第一次关注别人，建空集合',
        'self.follow_dict[followerId].add': '用户{followerId} 关注用户{followeeId}',
        'if followeeId in self.follow_dict.get': lambda S, B, r: (
            f'用户{S.followerId} 确实关注了用户{S.followeeId}，可以取关' if S.followeeId in S['self.follow_dict'].get(S.followerId, set())
            else '没关注过 → 什么都不做（防止 remove 报错）'),
        'self.follow_dict[followerId].remove': '用户{followerId} 取关用户{followeeId} → `{sorted(self.follow_dict[followerId])}`',
    },
    skip=['merge_id_list = []', 'pos_list = []', 'heap = []', 'merge_id_list.append', 'pos_list[fromId] -= 1',
          'res = []', 'if userId not in self.tweet_dict', 'if followerId not in self.follow_dict'],
    max_steps=75,
    cards=dict(
        one_liner='每人一个推文栈；刷新时用堆把关注者的栈做多路归并',
        complexity='发推/关注/取关 `O(1)`；刷新 `O(k + 10 log k)`，k 为关注数',
        problem=['设计简化版推特：`postTweet(userId, tweetId)` 发推，`follow` / `unfollow` 关注、取关',
                 '`getNewsFeed(userId)`：返回自己和关注的人==最近 10 条==推文 ID，按时间从新到旧',
                 '本视频：1 发 5、2 发 6、1 发 7、1 关注 2、2 发 8 → 刷新 `[8,7,6,5]`；取关后 `[7,5]`'],
        quote='检索推文。这一步相当于对用户自身以及其关注的人，以发推时间为key，进行十次多路归并。对于多路归并问题，使用堆来处理是经典的做法。',
        quote_src='—— yiduobo 题解原文',
        idea=['发推：存进自己的栈 `[-时间, 推文]`，==时间取负==，最小堆就能先弹出最新的',
              '刷新：每人的栈顶进堆；弹出一条，就把同一个人的下一条补进来，最多 10 次',
              '关注列表用 `set`，取关前先判断是否关注过'],
        summary=['发推、关注、取关 `O(1)`；刷新 `O(k + 10 log k)`',
                 '易错：刷新要==带上自己==；取关没关注过的人不能报错',
                 '注意：`target_set.add(userId)` 会把自己写进 `follow_dict`（get 到的是同一个集合），不影响答案',
                 '原文提到可只保留每人最近 10 条（循环栈），代码里直接用 list',
                 '原文为 Python 2 风格：删去了 `:type` 文档字符串，代码未改'],
    ),
)
