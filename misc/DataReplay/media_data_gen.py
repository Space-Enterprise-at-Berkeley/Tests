from data_replay import *
from video_gen import *
import json

def data_replay_setup(data_replay_loc):
    # if data replay storage folder doesn't exist in tmp directory, make it
    if data_replay_loc not in [x for x in os.listdir('tmp')]:
        os.mkdir('tmp/' + data_replay_loc)
    
def sort_channels(tmp_dir, channels, measurements):
    tmp_dir = 'tmp/' + tmp_dir
    # determine if any channels already have data replays
    data_graphs = []
    fetch_channels = []
    existing_clips = os.listdir(tmp_dir)
    for ch in channels:
        name = ch['channel']
        # TODO: check for whether channel name is valid channel name
        # if channel video doesn't exist, add it to list to be fetched and generated
        if name + ".mp4" not in existing_clips:
            fetch_channels.append(ch)
        # otherwise mark that data video has already been generated
        else:
            data_graphs.append(f"{tmp_dir}/{name}.mp4")
    return fetch_channels, data_graphs

def main(cfg):
    
    infl_cfg = cfg['influx_connection']
    
    client = DataFrameClient(infl_cfg['url'], infl_cfg['port'], infl_cfg['username'], 
        infl_cfg['password'], ssl=infl_cfg['remote'],database=cfg['database'])
    
    data_replay_setup(cfg['data_replay_loc'])
    
    fetch_channels, data_graphs = sort_channels(cfg['data_replay_loc'], cfg['channels'], client.get_list_measurements())
    
    times = cfg['times']
    data_start = pd.to_datetime(times['data_start'], format="%Y-%m-%dT%H:%M:%S.%fZ")
    data_duration  = times['data_duration']
    data_end = times['data_end']
    t0 = times['t0']
    
    # if data_end is not None, convert to pandas timestamp object, otherwise calculate using duration
    if data_end:
        data_end = pd.to_datetime(times['data_end'], format="%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        data_end = data_start + pd.Timedelta(data_duration)
    
    print(fetch_channels)
    
    # # Get data of interest, if necessary
    # if len(fetch_channels) > 0:
    #     channel_names = [ch['channel'] for ch in fetch_channels]
    #     print(f"Retreiving channels {', '.join(channel_names)} from influx")
    #     data_query = f"select value from {', '.join(channel_names)} where time > '{influx_str(data_start)}' and time < '{influx_str(data_end)}'"
    #     channel_data = client.query(data_query)
    # 
    #     if t0:
    #         pass
    #         # offset_index_time(channel_data, t0)
    #     print("Generating Data Replays")
    #     for ch in fetch_channels:
    #         ch_name = ch['channel']
    #         create_data_replay(channel_data[ch_name], data_start, data_end, ch_name, ch['unit'], f"{tmp_dir}/{ch_name}.mp4",fixed_scale=ch['fixed'])
    #         data_graphs.append(f"{tmp_dir}/{ch_name}.mp4")


def old_main():
    remove_temp_files = False

    max_burntime = 7
    burn_num = 2


    database = '2021_11_20_hotfire'
    tmp_dir = f'tmp/hotfire4_burn{burn_num}'
    
    # if remote:
    #     url = 'influx.andycate.com'
    #     port = 443
    #     username = 'videoGenClient'
    #     password = 'xasdah-Jemfk82-doxko6'
    # 
    # else:
    #     url = '127.0.0.1'
    #     port = 8086
    #     username = ''
    #     password = ''

    # Connect to Influx
    
    client = DataFrameClient(url,port,username,password,ssl=remote,database=database)

    client.get_list_measurements()

    fcEvents = client.query('select value from fcEvent')['fcEvent']['value']
    removeDuplicates(fcEvents)
    groupings = getGroupings(fcEvents, max_spacing=max_burntime+1)
    
    burns = [x for x in groupings if in_grouping(x,"Close Fuel")]
    burn = burns[burn_num-1]

    t0 = get_event_time(burn, 'Open Fuel')
    
    burn_rel = deepcopy(burn)
    offset_index_time(burn_rel, t0, series=True)
    ignite_offset = get_event_time(burn_rel, "Turn On Igniter & Open 2 Way")
    
    channel_info = [
            {'channel':'loxInjectorPT', 'unit':'psi', 'fixed':True},
            {'channel':'fuelInjectorPT', 'unit':'psi', 'fixed':True},
            {'channel':'totalThrust', 'unit':'kg', 'fixed':True}
        ]
    
    if tmp_dir not in ['tmp/' + x for x in os.listdir('tmp')]:
        os.mkdir(tmp_dir)
    
    data_graphs = []
    fetch_channels = []
    existing_clips = os.listdir(tmp_dir)
    for ch in channel_info:
        name = ch['channel']
        # if channel video doesn't exist, add it to list to be fetched and generated
        if name + ".mp4" not in existing_clips:
            fetch_channels.append(ch)
        # otherwise mark that data video has already been generated
        else:
            data_graphs.append(f"{tmp_dir}/{name}.mp4")
    
    # Get data of interest
    # TODO: check if videos for given channels already exist
    if len(fetch_channels) > 0:
        channel_names = [ch['channel'] for ch in fetch_channels]
        print('NAMES',channel_names)
        print(f"Retreiving channels {', '.join(channel_names)} from influx")
        data_query = f"select value from {', '.join(channel_names)} where time > '{influx_str(t0,ignite_offset)}' and time < '{influx_str(t0,30)}'"
        channel_data = client.query(data_query)
        offset_index_time(channel_data, t0)
        
        print("Generating Data Replays")
        for ch in fetch_channels:
            ch_name = ch['channel']
            create_data_replay(channel_data[ch_name], ignite_offset, ignite_offset+14, ch_name, ch['unit'], f"{tmp_dir}/{ch_name}.mp4",fixed_scale=ch['fixed'])
            data_graphs.append(f"{tmp_dir}/{ch_name}.mp4")
        

    # graph_channel(channel_data['loxInjectorPT'],ignite_offset,12, show=True)


    views = ['~/Media/SEB/T69B/hotfire4_t2_view1.mp4', '~/Media/SEB/T69B/hotfire4_t2_ibeam.mp4']


    output_file = "output/hotfire4_burn2_view1_ibeam.mp4"

    stitch_videos(views, data_graphs, output_file)

    print(f"Video '{output_file}' completed")


    if remove_temp_files:
        for ch_name in channel_names:
            os.remove(f"{tmp_name}/{ch_name}.mp4")


if __name__ == '__main__':
    with open('example.json', 'r') as f:
        data = f.read()
    main(json.loads(data))