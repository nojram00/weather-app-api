
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI', 'localhost:27017')

TODAY = datetime.utcnow()
LAST_SEVEN_DAYS = TODAY - timedelta(days=7)
LAST_THIRTY_DAYS = TODAY - timedelta(days=30)

# 7 days from now
SEVEN_DAYS_FROM_NOW = TODAY + timedelta(days=7)

# Last 30 days starting from 7 days from now
THIRTY_DAYS_FROM_LAST_WEEK_START = SEVEN_DAYS_FROM_NOW
THIRTY_DAYS_FROM_LAST_WEEK_END = SEVEN_DAYS_FROM_NOW - timedelta(days=30)