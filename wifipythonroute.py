from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")

time_out = 0.4


def enter():  # Вход в аккаунт
    global browser
    browser = webdriver.Chrome(options=options)
    browser.get('http://192.168.1.1')
    elem1 = browser.find_element(By.NAME, 'Frm_Username')  # Find the search box
    elem2 = browser.find_element(By.NAME, 'Frm_Password')
    elem1.send_keys('user' + Keys.RETURN)
    elem2.send_keys('werthvfy' + Keys.ENTER)
    sleep(time_out)


def other_session(butt):  # На случай если сессию занял другой пользователь
    try:
        browser.find_element(By.ID, butt).click()
    except:
        browser.find_element(By.NAME, 'Btn_apply').click()
        sleep(time_out)
        browser.find_element(By.ID, butt).click()
    sleep(time_out)


def list_local_user():  # Возвращает словарь со всеми подключёнными пользователями
    # localnet
    global time_out
    enter()
    other_session('localnet')
    browser.find_element(By.ID, 'lanConfig').click()
    sleep(time_out)
    dict_user = {}
    for i in range(50):
        try:
            dict_user[i] = browser.find_element(By.ID, f'template_DHCPHostInfo_{i}').text.replace(' ', ', ')

        except:
            break
    browser.quit()
    return dict_user


def info_device():  # Возвращает список данных об устройстве
    # mgrAndDiag
    enter()
    other_session('mgrAndDiag')
    ModelName_text = browser.find_element(By.ID, 'ModelName_text').text
    ModelName = browser.find_element(By.ID, 'ModelName').text
    div_SerialNumber = browser.find_element(By.ID, 'div_SerialNumber').text.replace(' ', ': ')
    dev_sVerExtent = browser.find_element(By.ID, 'dev_sVerExtent').text.replace(' ', ': ')
    div_HardwareVer = browser.find_element(By.ID, 'div_HardwareVer').text.replace(' ', ': ')
    div_SoftwareVer = browser.find_element(By.ID, 'div_SoftwareVer').text.replace(' ', ': ')
    div_BootVer = browser.find_element(By.ID, 'div_BootVer').text.replace(' ', ': ')
    res_list = [ModelName_text + ': ' + ModelName, div_SerialNumber, dev_sVerExtent, div_HardwareVer, div_SoftwareVer,
                div_BootVer]
    browser.quit()
    return res_list


def okr_sreda():  # Возвращает список wifi роутеров в округе в виде кортежа со списками на 2.4g и на 5g
    enter()
    other_session('localnet')
    browser.find_element(By.ID, 'wlanConfig').click()
    sleep(time_out)
    browser.find_element(By.ID, 'wlanStaScanAP').click()
    sleep(time_out)
    browser.find_element(By.ID, 'WLANScanAP').click()
    browser.find_element(By.ID, 'Btn_scanap').click()
    sleep(10)
    # template_WLANScanAP_0
    list_wifi = []
    list_wifi2_4g = []
    for j in range(50):
        try:
            name = browser.find_element(By.ID, f'template_WLANScanAP_{j}').text.split()
            if len(name) < 7:
                name = ['None'] + name
            l = ['Имя SSID: ', 'MAC Адрес: ', 'Канал: ', 'Сигнал(дБм): ', 'Шум (дБм): ', 'Beacon Интервал (мс): ',
                 'Режим Авторизации: ']
            for i in range(0, 7):
                list_wifi.append(l[i] + name[i])
            list_wifi2_4g.append(list_wifi)
            list_wifi = []
        except:
            break
    browser.find_element(By.ID, 'WLAN5gScanAPBar').click()
    browser.find_element(By.ID, 'Btn_scanap5g').click()
    sleep(10)
    # template_WLANScanAP5g_0
    list_wifi = []
    list_wifi5g = []
    for j in range(50):
        try:
            name = browser.find_element(By.ID, f'template_WLANScanAP5g_{j}').text.split()
            if len(name) < 7:
                name = ['None'] + name
            l = ['Имя SSID: ', 'MAC Адрес: ', 'Канал: ', 'Сигнал(дБм): ', 'Шум (дБм): ', 'Beacon Интервал (мс): ',
                 'Режим Авторизации: ']
            for i in range(0, 7):
                list_wifi.append(l[i] + name[i])
            list_wifi5g.append(list_wifi)
            list_wifi = []
        except:
            break
    browser.quit()
    return list_wifi2_4g, list_wifi5g


def status_wan():
    # internet
    enter()
    other_session('internet')
    browser.find_element(By.ID, 'ethWanStatus').click()
    sleep(time_out)
    list_data = browser.find_element(By.ID, 'EthStateDev').text.split("\n")[2::]
    list_title = ['Тип', 'IP-версия', 'NAT', 'IP Адрес',
                  'DNS',
                  'IPv4 шлюз',
                  'Оставшееся время аренды адреса (Remaining lease)',
                  'Статус подключения IPv4',
                  'IPv4 время онлайн',
                  'Причина отключения',
                  'LLA',
                  'GUA',
                  'DNS',
                  'IPv6 шлюз',
                  'PD',
                  'Статус подключения IPv6',
                  'IPv6 время онлайн',
                  'WAN MAC']

    for i in range(len(list_data)):
        if i == 7:
            list_data[i] = list_data[i].replace('Обновление | Сброс', '')
        list_data[i] = list_data[i].replace(list_title[i], f"{list_title[i]}: ")
    browser.quit()
    return list_data


def parent_control(name, macadr, but):  # отключат(включат) интернет пользователю по mac создавая запись по имени и
    # выводит список отключенных и результат выполнения
    enter()
    mac = macadr.split(':')
    other_session('internet')
    browser.find_element(By.ID, 'parentCtrl').click()
    sleep(time_out)
    list_bloked_user = []
    list_bloked_user1 = []
    list_users = []
    count = 0
    flag = 0
    for i in range(20):
        macadrinsite = ''
        try:
            browser.find_element(By.ID, f'instName_ParentCtrl:{i}').click()
            name_user = browser.find_element(By.ID, f'instName_ParentCtrl:{i}').text
            for j in range(6):
                maca = browser.find_element(By.ID, f'sub_ChildId{j}:{i}').get_attribute('value')
                macadrinsite = macadrinsite + ':' + maca
            list_bloked_user.append(macadrinsite[1::])
        except:
            count = i - 1
            break
    if but == 1 and macadr not in list_bloked_user:
        flag = 1
        number = count
        browser.find_element(By.ID, 'addInstBar_ParentCtrl').click()
        sleep(time_out)
        browser.find_element(By.ID, f'Enable1:ParentCtrl:{number + 1}').click()
        name_from = browser.find_element(By.ID, f'Name:ParentCtrl:{number + 1}')
        name_from.send_keys(name + Keys.RETURN)
        for i in range(6):
            mac_form = browser.find_element(By.ID, f'sub_ChildId{i}:{number + 1}')
            mac_form.send_keys(mac[i] + Keys.RETURN)
        browser.find_element(By.ID, f'EveryDay:{number + 1}').click()
        browser.find_element(By.ID, f'a_allday:{number + 1}').click()
        browser.find_element(By.ID, f'Btn_apply_ParentCtrl:{number + 1}').click()
    elif but == 0 and macadr in list_bloked_user:
        flag = 2
        index = list_bloked_user.index(macadr)
        browser.find_element(By.ID, f'instDelete_ParentCtrl:{index}').click()
    for i in range(20):
        macadrinsite = ''
        try:
            browser.find_element(By.ID, f'instName_ParentCtrl:{i}').click()
            name_user = browser.find_element(By.ID, f'instName_ParentCtrl:{i}').text
            for j in range(6):
                maca = browser.find_element(By.ID, f'sub_ChildId{j}:{i}').get_attribute('value')
                macadrinsite = macadrinsite + ':' + maca
            list_bloked_user1.append(macadrinsite[1::])
            list_users.append(name_user + '-' + macadrinsite[1::])
        except:
            count = i - 1
            break
    status = ''
    if but == 1:
        if len(list_bloked_user1) > len(list_bloked_user) and flag == 1:
            status = "Success"
        elif flag == 0:
            status = 'Already have'
        else:
            status = 'Error'
    elif but == 0:
        if len(list_bloked_user1) < len(list_bloked_user) and flag == 2:
            status = 'Success'
        elif flag == 0:
            status = 'Absent'
        else:
            status = 'Error'
    browser.quit()
    return list_users, status

# fl = True
# while fl:
#     r = input('Enter: ')
#     if r == 'local':
#         llu = list_local_user()
#         print('List Local Users')
#         for i in range(len(llu)):
#             print(f'{i} {llu[i]}')
#     elif r == 'info':
#         inf_dev = info_device()
#         print('Info device')
#         for i in inf_dev:
#             print(i)
#     elif r == 'wan':
#         sr_wan = status_wan()
#         print('Status Wan')
#         for i in sr_wan:
#             print(i)
#     elif r == 'okr':
#         g2_4, g_5 = okr_sreda()
#         print('2.4G wifi around')
#         for i in g2_4:
#             rout = ''
#             for j in i:
#                 rout = rout + ' ' + j+';'
#             print(rout)
#         print('5G wifi around')
#         for i in g_5:
#             rout = ''
#             for j in i:
#                 rout = rout + ' ' + j+';'
#             print(rout)
#     elif r == 'par':
#         p = input('name 00:00:00:00:00:00 1(0): ').split()
#         lis, re = parent_control(p[0], p[1], int(p[2]))
#         print(f'List: {lis}')
#         print(f'Result: {re}')
#     else:
#         fl = False
