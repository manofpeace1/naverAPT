from timeit import default_timer
from datetime import timedelta
import script
import config


if __name__ == '__main__':
    script.select_area_code()
    timer_start = default_timer()
    print("\nCollecting...")
    script.collect_apt_code()
    script.collect_apt_details()
    script.export_to_file()
    timer_end = default_timer()
    time_record = timedelta(seconds=timer_end - timer_start)

    print(f"""
    DONE! ({time_record})

    Folder path: {config.folder_path}
    File name: {script.area_name + config.file_name}
    """)
