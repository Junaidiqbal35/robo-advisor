
import datetime

# for TOKEN- POST METHOD
tokenUrl = "https://openapigw.tase.co.il/tase/prod/oauth/oauth2/token"

# key and secret of ofer
# key = '7e247414e7047349d83b7b8a427c529c'
# secret = '7a809c498662c88a0054b767a92f0399'

# "key and secret of yarden - "tel_aviv_academic"
# key = '42599cb8bae3df12b563c85e4fb5a208'
# secret = 'cf7f46fcd91865d0f9c457e37bd7e726'

# key and secret of yarden - "roboadvisor-mta"
key = '9791b4a859c4650efe0d77c2ed9d6919'
secret = 'e8d0264a8472c411443a6dfbcdf0992f'

# for getting data - GET METHOD
baseUrl = "https://openapigw.tase.co.il/tase/prod/api/v1"
prefixUrl = "/tase/prod/api/v1"
payload = 'grant_type=client_credentials&scope=tase'
language = 'he-IL'

indexName=142 #  telaviv35=142, telbondgeneral=602,allbondgeneral=601,telbondmaagar=715

#SET WEIGHTS FOR WEIGHTED INDEXES
weights=[0]*3
weights=[[0.1,0.5,0.4],[0.3,0.3,0.4],[0.5,0.1,0.4]]

# apps names with date
basicIndexComponents="basic-indices/index-components-basic/"+str(indexName) # alredy have-all security stock- not need to do again 
basicSecuritiesCompnayTrade="basic-securities/trade-securities-list"#not working

#past 10 years
indexEndOfDayHistoryTenYearsUpToday ="indices/eod/history/ten-years/by-index?indexId="
#past 5 years
indexEndOfDayHistoryFiveYearsUpToday ="indices/eod/history/five-years/by-index?indexId="
#indexEndOfDayHistoryFiveYearsSpecificDate=prefixUrl+"/indices/eod/history/five-years/by-date?date="+str(year)+"-"+str(month)+"-"+str(day)+"&indexId="+str(indexName)
#past 7 days
indexEndOfDayHistorySevenDaysUpToday = prefixUrl+"/indices/eod/seven-days/by-index?indexId="+str(indexName)
#indexEndOfDayHistorySevenDaySpecificDate = prefixUrl+"/indices/eod//seven-days/by-date?date="+str(year)+"-"+str(month)+"-"+str(day)+"&indexId="+str(indexName)
#past day
#indexEndOfDay=prefixUrl+"/indices/eod/history/ten-years/by-date?date="+str(year)+"-"+str(month)+"-"+str(day)+"&indexId="+str(indexName) #specific day


OTC_transaction_name = "transactions/otc-transactions"
endOfDayTransactionName = "transactions/transactions-end-of-day"
mayaNoticeByDay = "maya-reports-online/tase-messages-by-date"
fundHistoryDataName = "mutual-fund/history-data"

# apps names without date
basicIndexList="basic-indices/indices-list"# a list of all basic indices in tase-already have-not need to do again
basicSecuritiesList="basic-securities/securities-types"# not need to do again
basicSecuritiesCompnayList="basic-securities/companies-list"

shortSalesWeeklyBalanceName = "short-sales/weekly-balance"
shortSalesHistoricalData = "short-sales/history"
fundListName = "fund/fund-list"