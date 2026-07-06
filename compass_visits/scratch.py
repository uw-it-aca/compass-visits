from compass_visits.dao.sws import get_class_list
from compass_visits.dao.pws import get_regid_by_netid

regid = get_regid_by_netid("javerage")
get_class_list("202401", regid)
