from _KAHN_PROJECT_SLUG_.settings import TIME_ZONE
import pytz

core_timezone = pytz.timezone(TIME_ZONE)

utc_timezone = pytz.timezone("UTC")
