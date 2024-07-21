# from apscheduler.schedulers.background import BackgroundScheduler
# import random
# from flask_app.socketio_events.bbbw import bbbwSessionInfo_updateVolumeLevel
# from flask_app import app

# scheduler = BackgroundScheduler()


# simulated_time_stamp = 0
# def core_per_second():
#     with app.app_context():
#         global simulated_time_stamp #fake data for timestamp
#         simulated_volume_level = random.randint(0, 30)
#         simulated_time_stamp += 1
#         data = {'volume_level': simulated_volume_level, 'time_stamp': simulated_time_stamp}
#         # Simulates a socketio event emitted from bbbw_SessionInfo
#         bbbwSessionInfo_updateVolumeLevel(data)
#         print(f"Volume level: {simulated_volume_level}")

# scheduler.add_job(core_per_second, 'cron', second='*')
# scheduler.start()

