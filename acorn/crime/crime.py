# coding: utf-8
import requests
from bs4 import BeautifulSoup

step_two_base= 'http://www.ucrdatatool.gov/Search/Crime/Local/OneYearofDataStepTwo.cfm'
crimebase = 'http://www.ucrdatatool.gov/Search/Crime/Local/DownCrimeOneYearofData.cfm/LocalCrimeOneYearofData.csv'
def fetch_ccids(stateid):
    payload_state = {'StateId': stateid, 'BJSPopulationGroupId': ''}
    r = requests.post(step_two_base, data=payload_state)
    s = BeautifulSoup(r.text)
    selected = s.find('select')
    x = selected.findAll('option')
    ids = [int(i.get('value')) for i in x]

    return ids


def fetch_by_ccid(id):
    payload = {'CrimeCrossId': id, 'YearStart': 2012, 'YearEnd': 2012, 'DataType': [1,2,3,4]}
    r = requests.post(crimebase, payload)
    return r.text

