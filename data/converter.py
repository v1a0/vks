

def convert(log=True):

    from PIL import Image, ImageDraw, ImageFont
    import sqlite3
    import datetime
    import json
    from os import walk, makedirs
    import time


    class statistic:
        activity_percent = 0
        max_session_time = 0
        min_session_time = 9223372036854775806
        date = ''

    class person(statistic):
        user_id = ''
        pic = ''
        profpic = 'data/pic/'
        about = {}

        def mk_statistic(self, date, path, alt):
            return f"""
                <details>
                    <summary>{date}</summary>
                    <img class = "stat" src = "data/pic/{path}" alt = "{alt}" width=75%>
                    <div class="dayinfo">
                    Online activity percentage: {self.activity_percent} %
                    </div>
                    
                    <div class="dayinfo">
                    Maximum session duration: {self.max_session_time} minutes
                    </div>
                                    
                    <div class="dayinfo">
                    Minimum session duration: {self.min_session_time} minutes
                    </div>
                </details>
    """

        def mk_hat(self, content):
            return_ = f"""
                <div class="userinfo">
                    <div class="username">{content.get('Name')}</div>
    """

            for title in content:
                if title != 'Name':
                    return_ += f"""
                    <div class="Menu__itemTitle">
                        {title}:   <a class="Menu__itemCount">{content[title]}</a>
                    </div>"""



            return_ += f"""
                </div>
            
                <div class="profpic">
                    <img src = "data/pic/{self.pic}" alt = "{self.pic}" class="profpic">
                </div>
            """

            return return_


    def mkspic():
        class data:
            hour = 0
            minute = 0
            stat = 0

            def __init__(self, args):
                self.hour, self.minute, self.stat = args[0], args[1], args[2]

        if log: print("\n1. Visualising data to graphics...\n")

        db_list = []
        pic_list = []
        exist_list = []

        for (dirpath, dirnames, filenames) in walk('data/db'):
            db_list.extend(filenames)
            break

        # SEARCHING ALREADY EXISTING PICTURES EXCEPT TODAY'S  #
        for (dirpath, dirnames, filenames) in walk('data/pic'):
            pic_list.extend(filenames)
            break

        for i in pic_list:
            if not (i[1:11] in exist_list) and (i[1:11] != time.strftime("%d_%m_%Y")): exist_list.append(i[1:11])

        # ################################################### #

        for db_file_name in db_list:
            try:
                conn = sqlite3.connect('data/db/' + db_file_name)
                db = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
                for tab in db:
                    if tab[0][0] == 'T' and not (tab[0][1:11] in exist_list):
                        items = []
                        try:
                            cursor = conn.execute('SELECT HOURS, MINUTES, STATE FROM ' + tab[0])
                        except sqlite3.OperationalError:
                            cursor = ''

                        for item in cursor:
                            items.append(data(item))

                        makedirs('data/pic', exist_ok=True)
                        pic = Image.open('data/pic/defaultpic.png')
                        draw = ImageDraw.Draw(pic)

                        font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 90)
                        date_obj = datetime.datetime.strptime(tab[0], "T%d_%m_%Y")
                        text = date_obj.strftime("%d %b %Y")
                        draw.text((540, 10), text, (0, 0, 0), font=font)
                        draw.text((535, 5), text, (255, 255, 255), font=font)

                        sx = 4
                        sy = 0
                        for i in range(len(items)):
                            x, y = (73, 401) if items[i].hour < 6 else (73, 699) if items[i].hour < 12 \
                                else (73, 1053) if items[i].hour < 18 else (73, 1351)

                            x += (items[i].hour % 6) * 60 * 4 + (items[i].minute * 4)

                            if items[i].stat == 1:
                                sy = 8 if items[i - 1].stat == 2 else sy + 1 if sy == 176 else sy + 8 if sy < 176 else sy

                                draw.rectangle((x + 1, y, x + sx, y - sy), fill=(0 + sy, 255 - (sy // 5), 0))

                            elif items[i].stat == 0:
                                sy = 8
                                draw.rectangle((x + 1, y, x + sx, y - 2), fill=(0, 0, 120))

                            elif items[i].stat == 2:
                                sy = 8
                                draw.rectangle((x + 1, y, x + sx, y - 177), fill=(255, 50, 0))

                        pic_name = 'data/pic/P' + tab[0][1:] + 'U' + db_file_name[5:-3] + '.png'
                        pic.save(pic_name)

                        if log: print(f'{pic_name} is CREATED')

            except sqlite3.DatabaseError:
                pass

        # 74x402
        # 74x700
        # 74x1054
        # 74x1352


    def mkstat():
        if log: print('\n2. Analysing data...\n')
        db_list = []
        exist_list = []

        for (dir_path, dir_names, file_names) in walk('data/db'):
            db_list.extend(file_names)
            break

        # SEARCHING ALREADY EXISTING PICTURES EXCEPT TODAY'S  #
        for (dir_path, dir_names, file_names) in walk('data/info'):
            stat_list = []
            stat_list.extend(file_names)
            for file_name in stat_list:
                if '_stat' in file_name[:-5]:
                    exist_list.append(file_name[5:-10])
            break

        for db_file_name in db_list:

            try:
                with open(f'data/info/{db_file_name[:-3]}_stat.json', 'r') as file:
                    final_stat = json.load(file)
            except FileNotFoundError:
                final_stat = {}

            try:
                conn = sqlite3.connect('data/db/' + db_file_name)
                db = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
                users_stat_list = [statistic for _ in range(60 * 24)]
                N = 0

                for tab in db:
                    if tab[0][0] == 'T' and ((final_stat.get(tab[0][1:]) is None) or (tab[0][1:] == time.strftime("%d_%m_%Y"))):
                        if log: print(f'{db_file_name[:-3]}: {tab[0][1:]} is DONE')

                        day_data = []
                        try:
                            cursor = conn.execute('SELECT STATE FROM ' + tab[0])
                        except sqlite3.OperationalError:
                            cursor = ''

                        for item in cursor:
                            day_data.append(item[0])

                        users_stat_list[N].date = str(tab[0][1:])
                        current_sesion_time = 0
                        all_time = 0
                        users_stat_list[N].max_session_time = 0
                        users_stat_list[N].min_session_time = 9223372036854775806

                        # SEARCHING MAX AND MIN VALUES #
                        for state in day_data:
                            if state != 0 and state != 2:
                                current_sesion_time += 1
                                all_time += 1
                            else:
                                if users_stat_list[N].max_session_time < current_sesion_time:
                                    users_stat_list[N].max_session_time = current_sesion_time
                                if users_stat_list[N].min_session_time > current_sesion_time != 0:
                                    users_stat_list[N].min_session_time = current_sesion_time
                                current_sesion_time = 0
                        # ############################# #

                        users_stat_list[N].activity_percent = all_time / len(day_data) if len(day_data) != 0 else 0

                        if users_stat_list[N].min_session_time == 9223372036854775806:
                            stat_result = ['00.00', '00', '00']
                        else:
                            stat_result = [
                                        str(users_stat_list[N].activity_percent * 100)[:5],
                                        str(users_stat_list[N].max_session_time),
                                        str(users_stat_list[N].min_session_time)
                                        ]

                        final_stat[users_stat_list[N].date] = stat_result
                        N += 1

            except sqlite3.DatabaseError:
                pass

            with open(f'data/info/{db_file_name[:-3]}_stat.json', 'w') as outfile:
                json.dump(final_stat, outfile)



    def mkhtml():

        if log: print('\n3. Combining all parts to html...\n')
        id_list = []
        for (dirpath, dirnames, filenames) in walk('data/db'):
            id_list.extend(filenames)
            break

        pic_list = []
        for (dirpath, dirnames, filenames) in walk('data/pic'):
            pic_list.extend(filenames)
            break

        for _id in id_list:
            try:
                p = person()
                p.user_id = _id[5:-3]
                p.pic = f'profpic_{p.user_id}.jpeg'
                p.profpic = f'data/pic/user_{p.user_id}'
                p.about = json.load(open(f'data/info/user_{p.user_id}.json', 'r'))

                with open(f'data/info/user_{p.user_id}_stat.json', 'r') as file:
                    stat_data = json.load(file)

                html = open('user_' + p.user_id + '.html', 'w', encoding="utf8")
                example = open('templates/defaultpage.html', 'r', encoding="utf8")
                hat = p.mk_hat(p.about)

                for line in example.readlines():
                    if '<!-- %USERDATA% -->\n' in line:
                        html.write(hat)
                    elif '<!-- %STATDATA% -->\n' in line:
                        for (stat_line, data) in {a: b for a,b in sorted(stat_data.items(),
                                                                         reverse=True,
                                                                         key=lambda item: int(item[0][0:2]) +
                                                                                          int(item[0][3:5])*31 +
                                                                                          int(item[0][6:10])*666)}.items():
                            element = stat_line.replace('_', ' ').split()
                            day = element[0]
                            mon = element[1]
                            year = element[2]
                            p.activity_percent = data[0]
                            p.max_session_time = data[1]
                            p.min_session_time = data[2]

                            date = day + '/' + mon + '/' + year
                            path = 'P' + day + '_' + mon + '_' + year + 'U' + p.user_id + '.png'
                            alt = date + '_user_' + p.user_id

                            daystat = p.mk_statistic(date=date, path=path, alt=alt)

                            html.write(daystat)
                    else:
                        html.write(line)

                html.close()
                example.close()
                if log: print('user_' + p.user_id + '.html', 'is DONE')
            
            except FileNotFoundError:
                pass

    mkspic()
    mkstat()
    mkhtml()
    if log: print('\nAll data successfully converted to HTML')

if __name__ == '__main__':
    convert()