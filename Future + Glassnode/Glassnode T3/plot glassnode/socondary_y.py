import plotly.graph_objects as go
from plotly.subplots import make_subplots

#  https://studio.glassnode.com/images/watermark/black-default.png?v=27102021
def secondary_yaxis(df, ohlc_x,ohlc_y,factor_x,factor_y:list,
                    y_axis_title='price data',secondary_y_axis_title='factor',
                    x_axis_title='datetime',
                    main_title='',
                    factor_opacity=0.7):


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]],shared_xaxes=True)
    fig.update_xaxes(showspikes=True, spikecolor="grey", spikethickness=1,spikesnap="cursor", spikemode="across",spikedash="solid")
    fig.update_yaxes(showspikes=True, spikecolor="grey", spikethickness=1,spikesnap="cursor", spikemode="across",spikedash="solid")

    # 新增浮水印
    fig.layout.annotations = [
        dict(
            name="draft watermark",
            text="Glassnode",
            textangle=0,
            opacity=0.18,
            font=dict(color="black", size=110),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
    ]


    # Add traces
    fig.add_trace(
        go.Scatter(x=ohlc_x, y=ohlc_y, name=y_axis_title,showlegend=False),
        secondary_y=False,
    )
    # 更改線條顏色和粗細
    fig.update_traces(
        selector={'name': y_axis_title},
        line={'color': 'black', 'width': 0.8}
    )

    for i in factor_y:
        fig.add_trace(
            go.Scatter(x=factor_x, y=df[i], name=f'{secondary_y_axis_title}_{i}',opacity=factor_opacity),
            secondary_y=True,
        )

    # Add figure title
    fig.update_layout(
        title_text=main_title
    )
    fig.update_layout(hovermode='x',hoverlabel_namelength=100)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="black",
            font_size=16,
            font_family="Rockwell"
        )
    )

    # Set x-axis title
    fig.update_xaxes(title_text=f"<b>{x_axis_title}</b>")

    # Set y-axes titles
    fig.update_yaxes(title_text=f"<b>{y_axis_title}</b>", secondary_y=False)
    fig.update_yaxes(title_text=f"<b>{secondary_y_axis_title}</b>", secondary_y=True)

    fig.show()