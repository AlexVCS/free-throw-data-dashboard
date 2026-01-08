import numpy as np

def get_frames_with_ball(trial):
    """Find frames where ball is actually tracked (not NaN)"""
    frames_with_ball = []
    for frame in trial['tracking']:
        ball = frame['data']['ball']
        # Check if any value is not NaN
        if not (np.isnan(ball[0]) or np.isnan(ball[1]) 
                or np.isnan(ball[2])):
            frames_with_ball.append(frame)
    return frames_with_ball

def calculate_joint_angle(point1, point2, point3):
    """
    Calculate angle at point2 formed by point1-point2-point3
    Returns angle in degrees
    """
    v1 = np.array(point1) - np.array(point2)
    v2 = np.array(point3) - np.array(point2)
    
    # Calculate angle
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    # Clamp to [-1, 1] to avoid numerical errors
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle = np.arccos(cos_angle)
    
    return np.degrees(angle)

def extract_trial_metrics(trial):
    """Extract biomechanical metrics from a trial"""
    metrics = []
    
    for frame in trial['tracking']:
        player = frame['data']['player']
        ball = frame['data']['ball']
        
        # Right elbow angle (shoulder-elbow-wrist)
        r_elbow_angle = calculate_joint_angle(
            player['R_SHOULDER'],
            player['R_ELBOW'],
            player['R_WRIST']
        )
        
        # Left elbow angle
        l_elbow_angle = calculate_joint_angle(
            player['L_SHOULDER'],
            player['L_ELBOW'],
            player['L_WRIST']
        )
        
        # Right knee angle
        r_knee_angle = calculate_joint_angle(
            player['R_HIP'],
            player['R_KNEE'],
            player['R_ANKLE']
        )
        
        metrics.append({
            'frame': frame['frame'],
            'time': frame['time'],
            'r_elbow_angle': r_elbow_angle,
            'l_elbow_angle': l_elbow_angle,
            'r_knee_angle': r_knee_angle,
            'ball_x': ball[0],
            'ball_y': ball[1],
            'ball_z': ball[2],
        })
    
    return metrics


if __name__ == '__main__':
    from data_loader import load_trial
    
    trial = load_trial('P0001/BB_FT_P0001_T0001')
    
    # Test
    frames_with_ball = get_frames_with_ball(trial)
    print(f"Frames with ball tracked: {len(frames_with_ball)}")
    
    metrics = extract_trial_metrics(trial)
    print(f"Extracted metrics for {len(metrics)} frames")
    print(f"Sample metric: {metrics[0]}")