from data_replay import *
from influx_helpers import *
import os
import subprocess

'''
Command to stich videos together via ffmpeg
 ffmpeg -i hotfire_06202021_2.mp4 -i lox_inj_view1.mp4 -i prop_inj_view1.mp4 -filter_complex "[0:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [left]; [1:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [right]; [2:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [right2]; [left][right] overlay=main_w/2:0 [tmp]; [tmp][right2] overlay=0:main_h/2 " -b:v 768k test.mp4

 ffmpeg -i hotfire_06202021_2.mp4 -i lox_inj_view1.mp4 -i prop_inj_view1.mp4 -filter_complex "[0:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [main]; [1:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data1]; [2:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data2]; [main][data1] overlay=0:main_h/2 [tmp]; [tmp][data2] overlay=overlay_w:main_h/2 " -b:v 768k test2.mp4

 ffmpeg -i hotfire_06202021_2.mp4 -i lox_inj_view1.mp4 -i prop_inj_view1.mp4 -filter_complex "[0:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [main]; [1:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data1]; [2:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data2]; [2:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data3]; [main][data1] overlay=0:main_h/2 [tmp]; [tmp][data2] overlay=overlay_w:main_h/2 [tmp2]; [tmp2][data3] overlay=overlay_w*2:main_h/2 " -b:v 768k test2.mp4

 ffmpeg -i hotfire_06202021_1.mp4 -i hotfire_06202021_2.mp4 -i lox_inj_view1.mp4 -i prop_inj_view1.mp4 -filter_complex "[0:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [view1]; [1:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [view2]; [2:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data1]; [3:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data2]; [3:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data3]; [view1][view2] overlay=main_w/2:0 [main]; [main][data1] overlay=0:main_h/2 [tmp]; [tmp][data2] overlay=overlay_w:main_h/2 [tmp2]; [tmp2][data3] overlay=overlay_w*2:main_h/2 " -b:v 768k test2.mp4

ffmpeg -i {view1} -i {view2} -i {data1} -i {data2} -i {data3} -filter_complex "[0:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [view1]; [1:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [view2]; [2:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data1]; [3:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data2]; [4:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data3]; [view1][view2] overlay=main_w/2:0 [main]; [main][data1] overlay=0:main_h/2 [tmp]; [tmp][data2] overlay=overlay_w:main_h/2 [tmp2]; [tmp2][data3] overlay=overlay_w*2:main_h/2 " -b:v 768k {output}

'''

def stitch_videos(views, data_graphs, output_file, remove_existing=False):

    if len(views) > 2:
        raise ValueError(f"'views' must be a list of length 1 or 2. Got list of length {len(views)}")

    if len(data_graphs) < 1 or len(data_graphs) > 3:
        raise ValueError(f"'data_graphs must be a list with length between 1 and 3. Got list of length {len(data_graphs)}'")


    if output_file in ['output/' + x for x in os.listdir('output')]:
        if not remove_existing:
            raise ValueError(f"File '{output_file}' already exists!")
        else:
            print(f"Removing file '{output_file}'")
            os.remove(output_file)

    cmd = 'ffmpeg '

    # Set the right import files for all the input media
    for source in views + data_graphs:
        cmd += f'-i {source} '
    cmd += '-filter_complex '
    cmd += '"'

    # Add input filtering lines for GoPro footage and Generated Data Video
    for i, view in enumerate(views):
        cmd += f"[{i}:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2, pad=2*iw:2*ih [view{i+1}]; "

    for i, data_graph in enumerate(data_graphs):
        cmd += f"[{len(views)+i}:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [data{i+1}]; "

    # if there are two views, stich them together on the top half of the screen
    if len(views) == 2:
        cmd += "[view1][view2] overlay=main_w/2:0 [main]; "
        first_overlay_base = "main"
    else:
        first_overlay_base = "view1"

    # Add an overaly command for each unique data view
    for i in range(len(data_graphs)):
        if i == 0:
            start = first_overlay_base
        else:
            start = f"tmp{i-1}"

        if i == len(data_graphs) - 1:
            end = '"'
        else:
            end = f"[tmp{i}]; "

        cmd += f"[{start}][data{i+1}] overlay={i}*overlay_w:main_h/2 {end}"

    cmd += f" -b:v 768k {output_file}"

    print(f"Creating output file {output_file} using:")
    print(f"Views: {', '.join(views)}")
    print(f"Data Graphs: {', '.join(data_graphs)}")
    output = subprocess.run(args=cmd, shell=True, capture_output=True)

    # print(output.stdout)