import os
import pandas as pd
from pyecharts.charts import Bar, HeatMap, Grid, Page, Pie, Line, Scatter, WordCloud
import pyecharts.options as opts
import re
from pyecharts.globals import ThemeType


def add_line(sentence, interval=6):
    sentence = sentence.replace(" ", "")
    string = "(.{" + str(interval) + "})"
    sentence = re.sub(string, "\\1\n", sentence)
    return sentence


def add_line_eng(sentence):
    sentence = sentence.replace(" ", "\n")
    return sentence


def create_bar_chart(title, x_data, y_data, y_label, width="1200px"):
    return (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.SHINE, width=width))
            .add_xaxis(x_data)
            .add_yaxis(y_label, y_data)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, pos_left='center', pos_top='5%'),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0, font_size=10)),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )


def create_line_chart(title, x_data, y_data, y_label, width="1200px"):
    return (
        Line(init_opts=opts.InitOpts(theme=ThemeType.SHINE, width=width))
            .add_xaxis(x_data)
            .add_yaxis(y_label, y_data, is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2))
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, pos_left='center', pos_top='5%'),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0, font_size=10)),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )


def create_scatter_chart(title, x_data, y_data, y_label, width="1200px"):
    return (
        Scatter(init_opts=opts.InitOpts(theme=ThemeType.SHINE, width=width))
            .add_xaxis(x_data)
            .add_yaxis(y_label, y_data, symbol_size=8)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, pos_left='center', pos_top='5%'),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0, font_size=10)),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )


def show_view_data(video_data_csv, up_data_csv, base_dir):
    video_data = pd.read_csv(video_data_csv)
    video_data['title'] = [add_line(i) for i in video_data['title']]
    up_data = pd.read_csv(up_data_csv)
    up_data['up'] = [add_line(i) for i in up_data['up']]

    video_line = create_line_chart('播放量最多的视频', video_data['title'].tolist(), video_data['view_data'].tolist(), '观看次数')
    up_line = create_line_chart('播放量累计的up主', up_data['up'].tolist(), up_data['view_data'].tolist(), '观看次数')

    save_dir = os.path.join(base_dir, 'view_data.html')
    page = Page(layout=Page.DraggablePageLayout)
    page.add(video_line, up_line)
    page.render(save_dir)


def show_coin_data(video_data_csv, up_data_csv, base_dir):
    video_data = pd.read_csv(video_data_csv)
    video_data['title'] = [add_line(i) for i in video_data['title']]
    up_data = pd.read_csv(up_data_csv)
    up_data['up'] = [add_line(i) for i in up_data['up']]

    video_scatter = create_scatter_chart('投币最多的视频', video_data['title'].tolist(), video_data['coin_data'].tolist(),
                                         '投币数')
    up_scatter = create_scatter_chart('投币最多的up主', up_data['up'].tolist(), up_data['coin_data'].tolist(), '投币数')

    save_dir = os.path.join(base_dir, 'coin_data.html')
    page = Page(layout=Page.DraggablePageLayout)
    page.add(video_scatter, up_scatter)
    page.render(save_dir)


def show_danmaku_data(video_data_csv, up_data_csv, base_dir):
    video_data = pd.read_csv(video_data_csv)
    video_data['title'] = [add_line(i) for i in video_data['title']]
    up_data = pd.read_csv(up_data_csv)
    up_data['up'] = [add_line(i) for i in up_data['up']]

    video_bar = create_bar_chart('弹幕数最多的视频', video_data['title'].tolist(), video_data['danmaku_data'].tolist(), '弹幕数')
    up_bar = create_bar_chart('弹幕总数最多的up主', up_data['up'].tolist(), up_data['danmaku_data'].tolist(), '弹幕数')

    save_dir = os.path.join(base_dir, 'danmaku_data.html')
    page = Page(layout=Page.DraggablePageLayout)
    page.add(video_bar, up_bar)
    page.render(save_dir)


def show_favorite_data(video_data_csv, up_data_csv, base_dir):
    video_data = pd.read_csv(video_data_csv)
    video_data['title'] = [add_line(i) for i in video_data['title']]
    up_data = pd.read_csv(up_data_csv)
    up_data['up'] = [add_line(i) for i in up_data['up']]

    video_bar = create_bar_chart('收藏最多的视频', video_data['title'].tolist(), video_data['favorite_data'].tolist(), '收藏数')
    up_bar = create_bar_chart('收藏次数最多的up主', up_data['up'].tolist(), up_data['favorite_data'].tolist(), '收藏数')

    save_dir = os.path.join(base_dir, 'favorite_data.html')
    page = Page(layout=Page.DraggablePageLayout)
    page.add(video_bar, up_bar)
    page.render(save_dir)


def show_like_data(video_data_csv, up_data_csv, base_dir):
    video_data = pd.read_csv(video_data_csv)
    video_data['title'] = [add_line(i) for i in video_data['title']]
    up_data = pd.read_csv(up_data_csv)
    up_data['up'] = [add_line(i) for i in up_data['up']]

    video_line = create_line_chart('点赞数最多的视频', video_data['title'].tolist(), video_data['like_data'].tolist(), '点赞数')
    up_line = create_line_chart('点赞数最多的up主', up_data['up'].tolist(), up_data['like_data'].tolist(), '点赞数')

    save_dir = os.path.join(base_dir, 'like_data.html')
    page = Page(layout=Page.DraggablePageLayout)
    page.add(video_line, up_line)
    page.render(save_dir)


def show_reply_data(video_data_csv, up_data_csv, base_dir):
    video_data = pd.read_csv(video_data_csv)
    video_data['title'] = [add_line(i) for i in video_data['title']]
    up_data = pd.read_csv(up_data_csv)
    up_data['up'] = [add_line(i) for i in up_data['up']]

    video_scatter = create_scatter_chart('评论最多的视频', video_data['title'].tolist(), video_data['reply_data'].tolist(),
                                         '评论数')
    up_scatter = create_scatter_chart('评论最多的up主', up_data['up'].tolist(), up_data['reply_data'].tolist(), '评论数')

    save_dir = os.path.join(base_dir, 'reply_data.html')
    page = Page(layout=Page.DraggablePageLayout)
    page.add(video_scatter, up_scatter)
    page.render(save_dir)


def show_share_data(video_data_csv, up_data_csv, base_dir):
    video_data = pd.read_csv(video_data_csv)
    video_data['title'] = [add_line(i) for i in video_data['title']]
    up_data = pd.read_csv(up_data_csv)
    up_data['up'] = [add_line(i) for i in up_data['up']]

    video_line = create_line_chart('转发次数最多的视频', video_data['title'].tolist(), video_data['share_data'].tolist(), '转发次数')
    up_line = create_line_chart('转发次数最多的up主', up_data['up'].tolist(), up_data['share_data'].tolist(), '转发次数')

    save_dir = os.path.join(base_dir, 'share_data.html')
    page = Page(layout=Page.DraggablePageLayout)
    page.add(video_line, up_line)
    page.render(save_dir)


def show_popular_subject(data_dir, base_dir):
    video_data_csv = os.path.join(data_dir, 'top_popular_subject.csv')
    video_data = pd.read_csv(video_data_csv)
    save_dir = os.path.join(base_dir, 'view_popular_subject.html')
    video_data_short = [add_line(i, 2) for i in video_data['tname']]

    video_popular_bar = create_bar_chart('上榜次数前十的话题', video_data_short, video_data['popular_subject_times'].tolist(),
                                         '上榜次数', '600px')

    video_popular_pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
            .add(
            "",
            [list(z) for z in zip(video_data['tname'].tolist(), video_data['popular_subject_times'].tolist())],
            radius=["30%", "55%"],
            center=["25%", "50%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=3,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "top"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "50%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "50%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 3],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="上榜次数前十的话题占比", pos_left='20%', pos_top='5%'),
            legend_opts=opts.LegendOpts(is_show=False, type_="scroll", orient='vertical', pos_top='10%',
                                        pos_right='50%')
        )
    )

    grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.SHINE, width='1400px'))
    grid.add(video_popular_bar, grid_opts=opts.GridOpts(pos_left="60%"))
    grid.add(video_popular_pie, grid_opts=opts.GridOpts(pos_left="50%"))
    grid.render(save_dir)


def show_popular_up(data_dir, base_dir):
    up_data_csv = os.path.join(data_dir, 'top_popular_up.csv')
    up_data = pd.read_csv(up_data_csv)
    save_dir = os.path.join(base_dir, 'view_popular_up.html')
    up_data_short = [add_line(i, 2) for i in up_data['up']]

    video_popular_bar = create_bar_chart('上榜次数前十的up主', up_data_short, up_data['popular_up_times'].tolist(), '上榜次数',
                                         '600px')

    video_popular_pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
            .add(
            "",
            [list(z) for z in zip(up_data['up'].tolist(), up_data['popular_up_times'].tolist())],
            radius=["30%", "55%"],
            center=["25%", "50%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=3,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "top"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "50%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "50%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 3],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="上榜次数前十的up主占比", pos_left='20%', pos_top='5%'),
            legend_opts=opts.LegendOpts(is_show=False, type_="scroll", orient='vertical', pos_top='10%',
                                        pos_right='50%')
        )
    )

    grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.SHINE, width='1400px'))
    grid.add(video_popular_bar, grid_opts=opts.GridOpts(pos_left="60%"))
    grid.add(video_popular_pie, grid_opts=opts.GridOpts(pos_left="50%"))
    grid.render(save_dir)


def show_popular(data_dir, base_dir):
    show_popular_up(data_dir, base_dir)
    show_popular_subject(data_dir, base_dir)


def show_statistic(base_dir, render_save_dir):
    video_coin_data = os.path.join(base_dir, 'video_coin_data.csv')
    up_coin_data = os.path.join(base_dir, 'up_coin_data.csv')
    show_coin_data(video_coin_data, up_coin_data, render_save_dir)

    video_danmaku_data = os.path.join(base_dir, 'video_danmaku_data.csv')
    up_danmaku_data = os.path.join(base_dir, 'up_danmaku_data.csv')
    show_danmaku_data(video_danmaku_data, up_danmaku_data, render_save_dir)

    video_favorite_data = os.path.join(base_dir, 'video_favorite_data.csv')
    up_favorite_data = os.path.join(base_dir, 'up_favorite_data.csv')
    show_favorite_data(video_favorite_data, up_favorite_data, render_save_dir)

    video_like_data = os.path.join(base_dir, 'video_like_data.csv')
    up_like_data = os.path.join(base_dir, 'up_like_data.csv')
    show_like_data(video_like_data, up_like_data, render_save_dir)

    video_reply_data = os.path.join(base_dir, 'video_reply_data.csv')
    up_reply_data = os.path.join(base_dir, 'up_reply_data.csv')
    show_reply_data(video_reply_data, up_reply_data, render_save_dir)

    video_share_data = os.path.join(base_dir, 'video_share_data.csv')
    up_share_data = os.path.join(base_dir, 'up_share_data.csv')
    show_share_data(video_share_data, up_share_data, render_save_dir)

    video_view_data = os.path.join(base_dir, 'video_view_data.csv')
    up_view_data = os.path.join(base_dir, 'up_view_data.csv')
    show_view_data(video_view_data, up_view_data, render_save_dir)


def map_to_list(df):
    word = df['word'].tolist()
    count = df['count'].tolist()
    data_list = [(w, c) for w, c in zip(word, count)]
    return data_list


def show_word_cloud(base_dir, render_save_dir):
    save_dir = os.path.join(render_save_dir, 'wordcloud.html')

    title_words = pd.read_csv(os.path.join(base_dir, 'title_word.csv'))
    title_words_freq = map_to_list(title_words)
    title_wc = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
            .add(
            series_name="",
            shape='circle',
            data_pair=title_words_freq,
            word_size_range=[16, 66],
            textstyle_opts=opts.TextStyleOpts(color='#dcdada'),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="标题常见词", title_textstyle_opts=opts.TextStyleOpts(font_size=23),
                                      pos_right='center'),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0))
    )

    desc_words = pd.read_csv(os.path.join(base_dir, 'desc_word.csv'))
    desc_words_freq = map_to_list(desc_words)
    desc_wc = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
            .add(
            series_name="",
            shape='circle',
            data_pair=desc_words_freq,
            word_size_range=[16, 66],
            textstyle_opts=opts.TextStyleOpts(color='#dcdada'),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="视频简介常见词", title_textstyle_opts=opts.TextStyleOpts(font_size=23),
                                      pos_right='center'),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0))
    )

    rcmd_reason_words = pd.read_csv(os.path.join(base_dir, 'rcmd_reason_word.csv'))
    rcmd_reason_words_freq = map_to_list(rcmd_reason_words)
    rcmd_reason_wc = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
            .add(
            series_name="",
            shape='circle',
            data_pair=rcmd_reason_words_freq,
            word_size_range=[16, 66],
            textstyle_opts=opts.TextStyleOpts(color='#dcdada'),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="推荐理由常见词", title_textstyle_opts=opts.TextStyleOpts(font_size=23),
                                      pos_right='center'),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0))
    )

    page = Page(layout=Page.DraggablePageLayout)
    page.add(title_wc, desc_wc, rcmd_reason_wc)
    page.render(save_dir)

if __name__ == '__main__':
    rendered_data = './data'
    render_html = './html'
    os.makedirs(render_html, exist_ok=True)

    show_statistic(rendered_data, render_html)
    show_popular(rendered_data, render_html)
    show_word_cloud(rendered_data, render_html)
