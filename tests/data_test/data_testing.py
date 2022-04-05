from datetime import datetime
from pathlib import Path

lines_dict = {
    datetime(2022, 2, 3, 0, 1, 13, 623000): "Error [http-nio-8625-exec-7]",
    datetime(2022, 3, 5, 0, 6, 13, 838000): "[http-nio-8625-exec-8]",
    datetime(2022, 4, 7, 0, 8, 13, 922000): "Error [http-nio-8625-exec-9]",
}
unhappy_log = Path("../unhappy_invalid2.log")

search_happy = "2022-02-03 00:01:13.623000\nError [http-nio-8625-exec-7]\n2022-04-07 00:08:13.922000\nError [http-nio-8625-exec-9]\n"

date_no_found = "2999-02-03 00:01:13.623000\nThe date not found\n"
