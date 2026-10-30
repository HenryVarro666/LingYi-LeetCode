def _vfmt(k, v):
    return f'{k} → "{v.content}"  播放{v.views} 赞{v.likes} 踩{v.dislikes}'


CONFIG = dict(
    num=2254, title='设计视频共享平台', difficulty='Hard', category='设计',
    author='yiduobo', technique='哈希表 + 最小堆（回收 id）',
    tags=['堆'],
    code='''
class Video(object):

    def __init__(self, content):
        self.content = content
        self.content_len = len(content)
        self.views = 0
        self.likes = 0
        self.dislikes = 0

class VideoSharingPlatform(object):

    def __init__(self):
        self.next_id = 0
        self.idle_id = []
        self.videos = {}

    def upload(self, video):
        if self.idle_id:
            id = heapq.heappop(self.idle_id)
        else:
            id = self.next_id
            self.next_id += 1
        
        self.videos[id] = Video(video)
        return id

    def remove(self, videoId):
        if videoId in self.videos:
            self.videos.pop(videoId)
            heapq.heappush(self.idle_id, videoId)

    def watch(self, videoId, startMinute, endMinute):
        if videoId not in self.videos:
            return "-1"
        
        video = self.videos[videoId]
        video.views += 1
        return video.content[startMinute : min(endMinute + 1, video.content_len)]

    def like(self, videoId):
        if videoId not in self.videos:
            return -1
        
        video = self.videos[videoId]
        video.likes += 1

    def dislike(self, videoId):
        if videoId not in self.videos:
            return -1
        
        video = self.videos[videoId]
        video.dislikes += 1

    def getLikesAndDislikes(self, videoId):
        if videoId not in self.videos:
            return [-1]
        
        video = self.videos[videoId]
        return [video.likes, video.dislikes]

    def getViews(self, videoId):

        if videoId not in self.videos:
            return -1
        
        video = self.videos[videoId]
        return video.views
''',
    call='''p = VideoSharingPlatform()
r = []
r.append(p.upload("123"))
r.append(p.upload("456"))
p.remove(0)
r.append(p.upload("789"))
r.append(p.watch(1, 0, 1))
p.like(1)
r.append(p.getLikesAndDislikes(1))
r''',
    expect=[0, 1, 0, '45', [1, 0]],
    skip=['self.content = content', 'self.content_len', 'self.views = 0', 'self.likes = 0', 'self.dislikes = 0',
          'self.idle_id = []', 'self.videos = {}'],
    views=[
        dict(type='map', var='self.videos', label='videos（id → 视频：内容 / 播放 / 赞 / 踩）', fmt=_vfmt, h=190),
        dict(type='heap', var='self.idle_id', label='idle_id（被回收、可重用的 id，最小堆）', h=140),
        dict(type='text', fn=lambda S: f"下一个从未用过的 id：`next_id = {S['self.next_id']}`" if 'self.next_id' in S else '', size=26, h=60),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=[('videoId', 'videoId', 'blue'), ('idle_id', 'self.idle_id', 'pink'), ('next_id', 'self.next_id'),
           ('views', 'video.views', 'green'), ('likes', 'video.likes', 'green')],
    captions={
        'self.next_id = 0': '`next_id`：下一个==从未用过==的自然数 id',
        'self.idle_id = []': '`idle_id`：用过、但已被删除的 id，用最小堆存放',
        'self.videos = {}': '哈希表：id → 视频，增删都是 `O(1)`',
        'if self.idle_id': lambda S, B, r: ('堆不空 → 堆顶就是最小的可用 id' if B['self.idle_id'] else '堆是空的 → 用 `next_id`'),
        'heapq.heappop': '弹出堆顶 `{id}`：回收过的 id 里最小的，优先重用',
        'id = self.next_id': '没有回收的 id，就用从未用过的 `{id}`',
        'self.next_id += 1': '`next_id` 往后挪一位 → {self.next_id}',
        'self.videos[id] = Video(video)': '新建视频 `"{video}"`，和 id `{id}` 关联起来',
        'return id': '返回分配的 id `{ret}`',
        'if videoId in self.videos': lambda S, B, r: ('视频 `{}` 存在，可以删除'.format(S.videoId) if S.videoId in B['self.videos'] else '视频不存在，什么也不做'),
        'self.videos.pop': '删除只需==解除关联==：把 `{videoId}` 从哈希表中拿掉',
        'heapq.heappush': '把 id `{videoId}` 放回堆，下次上传时最小的先被重用',
        'if videoId not in self.videos': lambda S, B, r: ('视频 `{}` 不存在 → 直接返回'.format(S.videoId) if S.videoId not in B['self.videos'] else '视频 `{}` 存在'.format(S.videoId)),
        'video = self.videos[videoId]': '哈希表取出视频对象',
        'video.views += 1': '观看一次：`views` → {video.views}',
        'video.likes += 1': '点赞：`likes` → {video.likes}',
        'video.dislikes += 1': '点踩：`dislikes` → {video.dislikes}',
        'return video.content[': '观看区间是闭区间 `[{startMinute}, {endMinute}]`，所以右端取 `min(endMinute + 1, 长度)` 防止越界 → `"{ret}"`',
        'return [video.likes': '返回 `[赞, 踩]` = `{ret}`',
        'return video.views': '返回播放次数 `{ret}`',
    },
    cards=dict(
        one_liner='哈希表存视频，最小堆回收 id：删掉的 id 优先重用',
        complexity='上传/删除 `O(log n)`，其余操作 `O(1)`',
        problem=['视频平台：`upload` 分配==最小的未使用==自然数作 id',
                 '`remove` 删除视频并释放 id；`watch(id, s, e)` 返回第 s 到 e 分钟的内容并播放量 +1',
                 '另有 `like`、`dislike`、`getLikesAndDislikes`、`getViews`；id 不存在时返回 -1 / [-1] / "-1"'],
        quote='使用一个堆来储存之前被使用过，但目前已经限制的id，同时使用一个变量记录下一个从未使用过的自然数。',
        quote_src='—— yiduobo 题解原文',
        idea=['需求分两类：视频的==增删==，和对视频的==行为==',
              '增删：哈希表 id → 视频；最小可用 id = 堆顶，堆空就用 `next_id`',
              '行为：`Video` 类里存内容、播放、赞、踩，更新成员变量即可'],
        summary=['`upload` / `remove` 各 `O(log n)`，观看、点赞等 `O(1)`',
                 '易错：删除的 id 要放回堆，上传时==先看堆再用 next_id==',
                 '易错：`watch` 的 `endMinute` 可能超出视频长度，要取 `min(endMinute + 1, 长度)`',
                 '不存在的视频：`watch` 返回字符串 "-1"，`getLikesAndDislikes` 返回 `[-1]`'],
    ),
)
