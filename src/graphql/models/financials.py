
import graphene

from src.graphql import custom_types


class FinancialStatements:
    INCOME_STATEMENT = 'income_statement'
    BALANCE_SHEET = 'balance_sheet'


class IncomeStatement(graphene.ObjectType):
    # Standard filing info
    fiscal_year = graphene.String()
    end_date = graphene.Field(custom_types.DateType)
    start_date = graphene.Field(custom_types.DateType)
    fiscal_period = graphene.String()
    filing_date = graphene.String()

    # Income statement items
    # https://docs.google.com/spreadsheets/d/1SnEVxlCoYeCcU0IBL8GT2709ZmNFSkD4VZfvkaa_Wi8/edit#gid=0
    operatingrevenue = graphene.Float()
    otherrevenue = graphene.Float()
    totalrevenue = graphene.Float()
    operatingcostofrevenue = graphene.Float()
    othercostofrevenue = graphene.Float()
    totalcostofrevenue = graphene.Float()
    totalgrossprofit = graphene.Float()
    sgaexpense = graphene.Float()
    marketingexpense = graphene.Float()
    rdexpense = graphene.Float()
    explorationexpense = graphene.Float()
    depreciationexpense = graphene.Float()
    amortizationexpense = graphene.Float()
    depletionexpense = graphene.Float()
    otheroperatingexpenses = graphene.Float()
    impairmentexpense = graphene.Float()
    restructuringcharge = graphene.Float()
    otherspecialcharges = graphene.Float()
    totaloperatingexpenses = graphene.Float()
    totaloperatingincome = graphene.Float()
    totalinterestexpense = graphene.Float()
    totalinterestincome = graphene.Float()
    otherincome = graphene.Float()
    totalotherincome = graphene.Float()
    totalpretaxincome = graphene.Float()
    incometaxexpense = graphene.Float()
    othergains = graphene.Float()
    netincomecontinuing = graphene.Float()
    netincomediscontinued = graphene.Float()
    extraordinaryincome = graphene.Float()
    otheradjustmentstoconsolidatednetincome = graphene.Float()
    netincome = graphene.Float()
    preferreddividends = graphene.Float()
    netincometononcontrollinginterest = graphene.Float()
    otheradjustmentstonetincometocommon = graphene.Float()
    netincometocommon = graphene.Float()
    weightedavebasicsharesos = graphene.Float()
    basiceps = graphene.Float()
    weightedavedilutedsharesos = graphene.Float()
    dilutedeps = graphene.Float()
    cashdividendspershare = graphene.Float()

    # Not in docs
    basicdilutedeps = graphene.Float()
    weightedavebasicdilutedsharesos = graphene.Float()


class BalanceSheet(graphene.ObjectType):
    # Standard filing info
    fiscal_year = graphene.String()
    end_date = graphene.Field(custom_types.DateType)
    start_date = graphene.Field(custom_types.DateType)
    fiscal_period = graphene.String()
    filing_date = graphene.String()

    # Balance sheet items
    # : https://docs.google.com/spreadsheets/d/1SnEVxlCoYeCcU0IBL8GT2709ZmNFSkD4VZfvkaa_Wi8/edit#gid=1222559697
    cashandequivalents = graphene.Float()
    restrictedcash = graphene.Float()
    fedfundssold = graphene.Float()
    interestbearingdepositsatotherbanks = graphene.Float()
    timedepositsplaced = graphene.Float()
    tradingaccountsecurities = graphene.Float()
    loansandleases = graphene.Float()
    allowanceforloanandleaselosses = graphene.Float()
    netloansandleases = graphene.Float()
    loansheldforsale = graphene.Float()
    accruedinvestmentincome = graphene.Float()
    customerandotherreceivables = graphene.Float()
    netpremisesandequipment = graphene.Float()
    mortgageservicingrights = graphene.Float()
    unearnedpremiumsdebit = graphene.Float()
    deferredacquisitioncost = graphene.Float()
    separateaccountbusinessassets = graphene.Float()
    goodwill = graphene.Float()
    intangibleassets = graphene.Float()
    otherassets = graphene.Float()
    totalassets = graphene.Float()
    noninterestbearingdeposits = graphene.Float()
    interestbearingdeposits = graphene.Float()
    fedfundspurchased = graphene.Float()
    shorttermdebt = graphene.Float()
    bankersacceptances = graphene.Float()
    accruedinterestpayable = graphene.Float()
    othershorttermpayables = graphene.Float()
    longtermdebt = graphene.Float()
    capitalleaseobligations = graphene.Float()
    claimsandclaimexpenses = graphene.Float()
    futurepolicybenefits = graphene.Float()
    unearnedpremiumscredit = graphene.Float()
    policyholderfunds = graphene.Float()
    participatingpolicyholderequity = graphene.Float()
    separateaccountbusinessliabilities = graphene.Float()
    otherlongtermliabilities = graphene.Float()
    totalliabilities = graphene.Float()
    commitmentsandcontingencies = graphene.Float()
    redeemablenoncontrollinginterest = graphene.Float()
    totalpreferredequity = graphene.Float()
    commonequity = graphene.Float()
    retainedearnings = graphene.Float()
    treasurystock = graphene.Float()
    aoci = graphene.Float()
    otherequity = graphene.Float()
    totalcommonequity = graphene.Float()
    totalequity = graphene.Float()
    noncontrollinginterests = graphene.Float()
    totalequityandnoncontrollinginterests = graphene.Float()
    totalliabilitiesandequity = graphene.Float()

    # Extra, not in docs
    shortterminvestments = graphene.Float()
    accruedexpenses = graphene.Float()
    noncurrentdeferredrevenue = graphene.Float()
    othernoncurrentliabilities = graphene.Float()
    accountspayable = graphene.Float()
    currentdeferredrevenue = graphene.Float()
    notereceivable = graphene.Float()
    totalcurrentliabilities = graphene.Float()
    othernoncurrentassets = graphene.Float()
    totalcurrentassets = graphene.Float()
    totalnoncurrentliabilities = graphene.Float()
    netinventory = graphene.Float()
    accountsreceivable = graphene.Float()
    totalnoncurrentassets = graphene.Float()
    netppe = graphene.Float()
    longterminvestments = graphene.Float()
    othercurrentassets = graphene.Float()
    currentdeferredtaxassets = graphene.Float()
    noncurrentdeferredtaxliabilities = graphene.Float()
    currentemployeebenefitliabilities = graphene.Float()
    currentdeferredtaxliabilities = graphene.Float()
    noncurrentdeferredtaxassets = graphene.Float()
    prepaidexpenses = graphene.Float()
    customerdeposits = graphene.Float()

