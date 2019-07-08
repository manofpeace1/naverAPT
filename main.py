from timeit import default_timer
from datetime import timedelta
import script
import config


if __name__ == '__main__':
    script.select_area_code()
    script.select_sale_type()
    timer_start = default_timer()
    print("\n" + "긁어오는 중...")
    script.collect_apt_code()
    script.collect_apt_details()
    script.export_to_file()
    timer_end = default_timer()
    time_record = timedelta(seconds=timer_end - timer_start)
    print(f"""
    완료! ({time_record})

    폴더 위치: {config.folder_path}
    파일명: {script.export_file_name}
    """)
