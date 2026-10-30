CONFIG = dict(
    num=447, title='回旋镖的数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举点 + 距离分组 n(n-1)',
    code='''
class Solution(object):
    def numberOfBoomerangs(self, points):

        ans = 0
        for x1, y1 in points:
            dis_dict = {}
            for x2, y2 in points:
                if x1 == x2 and y1 == y2:
                    continue
                dis = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
                dis_dict[dis] = dis_dict.get(dis, 0) + 1
            
            for dis, cnt in dis_dict.items():
                ans += cnt * (cnt - 1)

        return ans
''',
    call='Solution().numberOfBoomerangs([[0,0],[1,0],[2,0],[1,1]])',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: f"点 i = `({S['x1']}, {S['y1']})`" + (f"，其他点 `({S['x2']}, {S['y2']})`" if 'x2' in S else '') if 'x1' in S else '', h=60),
        dict(type='text', fn=lambda S: f"当前分组：距离 `{S['dis']}`，`{S['cnt']}` 个点 → `{S['cnt']} × {S['cnt']-1}` = =={S['cnt']*(S['cnt']-1)}==" if S.get('_line') == 14 else '', h=60),
        dict(type='map', var='dis_dict', fmt=lambda k, v: f'{k}: {v}', h=300, label='dis_dict：距离平方 → 点的个数'),
    ],
    watch=[('ans', 'ans', 'green')],
    captions={
        'dis_dict = {}': '换一个点 i，重新用字典记录“到 i 距离为 dis 的点有几个”',
        'continue': '这个点就是 i 自己，跳过',
        'dis = ': '到点 i 的距离平方 = =={dis}==，坐标是整数，不开方就没有精度问题',
        'dis_dict[dis] =': '距离 `{dis}` 的点现在有 `{dis_dict[dis]}` 个',
        'ans += cnt': '距离 `{dis}` 的 `{cnt}` 个点两两有序组合，共 `{cnt} × ({cnt}-1)` = {cnt*(cnt-1)} 组 → `ans` = =={ans}==',
        'return ans': '共 `{ans}` 个回旋镖',
    },
    cards=dict(
        one_liner='先按距离给点分组，每组 n 个点有 n(n-1) 个回旋镖',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['平面上 `n` 个互不相同的点，找所有 `(i, j, k)`，i 到 j 的距离等于 i 到 k',
                 '元组有顺序，`(i,j,k)` 和 `(i,k,j)` 不同',
                 '本视频：`[[0,0],[1,0],[2,0],[1,1]]` → `8`'],
        quote='先枚举点i，然后计算其他所有点到点i的距离，并将这个距离保存在dict中。……距离为dis的回旋镖一共有n * (n - 1)组。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定 i，用字典数出到 i 距离为 dis 的点有 `n` 个',
              '这 n 个点任取有序两个：`n × (n-1)`，再带上 i 就是回旋镖',
              '先分组再统一计算，和灵神边扫边累加的写法不同'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '距离不开方，避免精度问题',
                 '`continue` 跳过 i 自己；灵神的写法不跳过，因为距离 0 只出现一次，贡献为 0',
                 '代码本身 Python 3 可直接运行，未做修改'],
    ),
)
