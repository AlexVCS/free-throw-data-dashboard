import json
import os

def load_trial(trial_name):
    """Load a single trial JSON file
    trial_name format: 'P0001/BB_FT_P0001_T0001'
    """
    file_path = os.path.join('data', f'{trial_name}.json')
    with open(file_path) as f:
        trial = json.load(f)
    return trial

def list_all_trials():
    """List all available trials from nested folders"""
    trials = []
    data_dir = 'data'
    
    # Iterate through participant folders
    for participant_folder in sorted(os.listdir(data_dir)):
        participant_path = os.path.join(data_dir, participant_folder)
        
        # Only process directories (skip files)
        if not os.path.isdir(participant_path):
            continue
        
        # Look for JSON files in each participant folder
        for file in sorted(os.listdir(participant_path)):
            if file.endswith('.json'):
                trial_name = file.replace('.json', '')
                # Store as 'P0001/BB_FT_P0001_T0001'
                full_trial_name = os.path.join(
                    participant_folder, 
                    trial_name
                )
                trials.append(full_trial_name)
    
    return trials

if __name__ == '__main__':
    trials = list_all_trials()
    print(f"Found {len(trials)} trials\n")
    
    if trials:
        trial = load_trial(trials[0])
        
        # Get first frame with actual ball data
        for frame in trial['tracking'][:10]:
            ball = frame['data']['ball']
            if ball != [float('nan'), float('nan'), float('nan')]:
                print(f"Frame {frame['frame']}: Ball position = {ball}")
                break
        
        # Show a keypoint example
        first_frame = trial['tracking'][0]
        player_data = first_frame['data']['player']
        print(f"\nSample keypoint (R_SHOULDER): {player_data['R_SHOULDER']}")
        print(f"All keypoints available: {list(player_data.keys())}")