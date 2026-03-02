import json

#work_inf = {'work_id': ['pub_year','micro_clu']}

work_inf = {'372785': ['2005', '137'],
            '372355': ['2005', '137'],
            '351297': ['2005', '137'],
            '372781': ['2005', '138'],
            '372352': ['2005', '138'],
            '351293': ['2005', '138']
            }
ncs_baseline = {}

# work_ref = {'work_id': {'cited_year':cited_count}}
work_ref = {"372355": {"2013": 1, "2014": 1},
            "351297": {"2013": 1, "2019": 1},
            "372785": {"2007": 1, "2009": 3, "2014": 1, "2014": 1},
            "372781": {"2011": 1, "2012": 2},
            "372352": {"2010": 2, "2016": 1},
            "351293": {"2007": 1, "2008": 3, "2009": 1, "2016": 1}
            }

cnt = 0
for id, years in work_ref.items():
    if id in work_inf:
        y = int(work_inf[id][0])
        clu = work_inf[id][1]
    else:
        continue

    cum_ref = {}
    sorted_years = sorted(years.keys())
    cumulative_sum = 0

    for year in range(y, 2023):
        year = str(year)
        if year in years:
            cumulative_sum += years[year]
        else:
            cumulative_sum += 0
        cum_ref[year] = cumulative_sum

    y = str(y)
    if clu not in ncs_baseline:
        ncs_baseline[clu] = {y: {}}
        for yy in cum_ref:
            ncs_baseline[clu][y][yy] = [cum_ref[yy], 1]
    else:
        if y not in ncs_baseline[clu]:
            ncs_baseline[clu][y] = {}
            for yy in cum_ref:
                ncs_baseline[clu][y][yy] = [cum_ref[yy], 1]
        else:
            for yy in cum_ref:
                if yy in ncs_baseline[clu][y]:
                    ncs_baseline[clu][y][yy][0] += cum_ref[yy]
                    ncs_baseline[clu][y][yy][1] += 1
                else:
                    ncs_baseline[clu][y][yy] = [cum_ref[yy], 1]

# ret: {'micro_clu_id: {'work_pub_year':{'cited_year':[cited_count, paper_num]}
for micro_clu in ncs_baseline:
    print(f"micro_clu={micro_clu}")
    for pub_year in ncs_baseline[micro_clu]:
        print(f"pub_year={pub_year}")
        for cited_year in ncs_baseline[micro_clu][pub_year]:
            cited_cnt = ncs_baseline[micro_clu][pub_year][cited_year][0]
            paper_num = ncs_baseline[micro_clu][pub_year][cited_year][1]
            print(f"cited_year={cited_year}\t cited_count_sum={cited_cnt} \t paper_num={paper_num} \t mean value = {cited_cnt/paper_num}")

    print('*'*60)

