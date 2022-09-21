from apscheduler.schedulers.background import BackgroundScheduler
from .functions import (
    set_aaset_group_info, 
    set_investment_info,
)


def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    # scheduler.add_job(set_aaset_group_info, 'cron', hour="0")
    # scheduler.add_job(set_investment_info, 'cron', hour="0")
   
    # scheduler.add_job(set_aaset_group_info, 'interval', seconds=20)
    # scheduler.add_job(set_investment_info, 'interval', seconds=20)
    scheduler.start()