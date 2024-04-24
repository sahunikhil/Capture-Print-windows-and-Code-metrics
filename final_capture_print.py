import win32evtlog
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone


def is_current(given_time: str) -> bool:
    """
    Check if the given time is within the last 3 minutes of the current time in IST (Indian
    Standard Time).

    Parameters
    ----------
    given_time : str
        A string in the format "YYYY-MM-DDTHH:MM:SS.ssssssZ" where the last three characters
        are the UTC offset and the "Z" indicates UTC time.

    Returns
    -------
    bool
        True if the given time is within the last 3 minutes of the current time in IST, False
        otherwise.
    """
    given_time_dt: datetime = datetime.fromisoformat(given_time[:-1]).replace(
        tzinfo=timezone.utc
    )
    current_time: datetime = datetime.now(timezone.utc).astimezone(
        timezone(timedelta(hours=5, minutes=30))
    )
    before_current_time: datetime = current_time - timedelta(minutes=3)
    return before_current_time <= given_time_dt <= current_time


def get_events() -> None:
    """
    Get print events from Windows event log and copy the file.

    This function gets the most recent 10 events from the "Microsoft-Windows-PrintService/Operational"
    event log and checks if the event is from the last 3 minutes. If the event is from the last 3
    minutes, it checks if the event id is 307 or 308 and if the record/event ID is not already in
    the done list. If all the conditions are met, it copies the file and adds the record/event ID to
    the done list.

    The events are in reverse chronological order, so the function starts from the end of the
    list of events and works its way backwards.

    The done list is used to prevent copying the same file multiple times.
    """
    done: list = []
    while True:
        handle = win32evtlog.EvtQuery(
            "Microsoft-Windows-PrintService/Operational",  # event log
            win32evtlog.EvtQueryReverseDirection,  # direction
            "*",  # query
        )
        event = win32evtlog.EvtNext(handle, 1000, -1, 0)  # get 1000 events
        # if there are less than 10 events, start from the beginning
        if len(event) <= 10:
            start = -10
        else:
            start = 0

        for i in event[start:]:  # loop through events
            xml_string = win32evtlog.EvtRender(i, win32evtlog.EvtRenderEventXml)
            tree = ET.fromstring(xml_string)

            if (
                is_current(tree[0][7].attrib["SystemTime"])
                and tree[0][1].text in ("307", "308")
                and tree[0][8].text not in done
            ):
                print(tree[0][1].tag.split("}")[-1], tree[0][1].text)
                print(tree[0][7].tag.split("}")[-1], tree[0][7].attrib["SystemTime"])
                print(tree[1][0][5].tag.split("}")[-1], tree[1][0][5].text)
                print(tree[0][8].tag.split("}")[-1], tree[0][8].text)

                # copy the file
                shutil.copy(tree[1][0][5].text, r"C:\Nik\copied_files_from_printer")
                print(
                    f"Successfully copied file {tree[1][0][5].text} to C:\\Nik\\copied_files_from_printer.\n"
                )
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n")
                done.append(tree[0][8].text)


if __name__ == "__main__":
    get_events()
