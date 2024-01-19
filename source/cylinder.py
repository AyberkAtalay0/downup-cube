import plotly.offline
import plotly.graph_objs as go
import numpy as np

def slice_triangles(z, n, i, j, k, l):
    return [[z, j, i], [i, j, l], [l, j, k], [k, n, l]]

def cylinder_mesh(r, xs, ys, zs, h, n_slices=40):
    theta = np.linspace(0, 2 * np.pi, n_slices + 1)
    x = xs + r * np.cos(theta)
    y = ys + r * np.sin(theta)
    z1 = zs + 0 * np.ones_like(x)
    z2 = (zs + h) * np.ones_like(x)
    n = n_slices * 2 + 1
    triangles = []
    for s in range(1, n_slices + 1):
        j = (s + 1) if (s <= n_slices - 1) else 1
        k = j + n_slices if (s <= n_slices - 1) else n_slices + 1
        l = s + n_slices
        triangles += slice_triangles(0, n, s, j, k, l)
    triangles = np.array(triangles)
    x_coords = np.hstack([xs, x[:-1], x[:-1], xs])
    y_coords = np.hstack([ys, y[:-1], y[:-1], ys])
    z_coords = np.hstack([zs, z1[:-1], z2[:-1], (zs + h)])
    vertices = np.stack([x_coords, y_coords, z_coords]).T
    return vertices, triangles, x, y, z1, z2

def cylinder_traces(r, xs, ys, zs, h, n_slices=40, show_mesh=True, n_sub=4, surface_kw={}, line_kw={}):
    vertices, triangles, x, y, z1, z2 = cylinder_mesh(r, xs, ys, zs, h, n_slices)
    surface = go.Mesh3d(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], i=triangles[:, 0], j=triangles[:, 1], k=triangles[:, 2], facecolor=(["magenta"]*(len(triangles)))[:len(triangles)], **surface_kw)
    traces = [surface]
    zsubs = np.linspace(zs, zs + h, n_sub + 1)
    a = [True] + [False for i in range(len(zsubs)-2)] + [True]
    for zc, _a in zip(zsubs, a):
        if _a: traces.append(go.Scatter3d(x=x, y=y, z=zc*np.ones_like(x), mode="lines", **line_kw))
    a = [True if i%4==0 else False for i in range(1, len(y)+1)]
    for _x, _y, _a in zip(x, y, a):
        if _a:  traces.append(go.Scatter3d(x=[_x, _x], y=[_y, _y], z=[zs, zs + h], mode="lines", **line_kw))
    return traces

fig = go.Figure()
fig.add_traces(
    cylinder_traces(3, 5, 3, 1, 8, 20, n_sub=4, line_kw=dict(line_color="black", line_width=3, hoverinfo="skip"), surface_kw=dict(showscale=False, lighting_ambient=0.99, lighting=dict(specular=0.5), hoverinfo="skip"))
)

R = 1.5
fig.update_layout(scene=dict(domain_x=[0, 0], camera_eye=dict(x=-0.76*R, y=1.8*R, z=0.92*R)), showlegend=False, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="#EBF2F7", paper_bgcolor="#EBF2F7")
fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)

plotly.offline.plot(fig, config={"displayModeBar": False, "responsive": True})

with open("temp-plot.html", "r", encoding="utf-8") as fr: readed = fr.read()
with open("temp-plot.html", "w", encoding="utf-8") as fw: 
    raw = readed.split('class="plotly-graph-div" style="')
    raw[0] = raw[0].replace('<body>', '<body style="background-color: #EBF2F7;">')
    raw[1] = raw[1].split('"', maxsplit=1)
    raw[1][0] = "margin: auto; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); height: calc(min(100vh, 100vw) - 16px); width: calc(min(100vh, 100vw) - 16px);"
    fw.write(raw[0] + 'class="plotly-graph-div" style="' + raw[1][0] + '"' + raw[1][1])
