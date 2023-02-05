_format_dict = {
    '$objPDate.today_PM': 'today_pm:yyyyMMdd',
    '$objPDate.today': 'today:yyyyMMdd',
    'Get-Date -format ': 'today:',
    '$objPDate.priorwday': 'priorwday:',
    'lbdom -1 yyyyMMdd y WFAM': 'lbdom:yyyyMMdd',
    'dayoffset -1 yyyyMMdd': 'yesterday:yyyyMMdd',
    'dayoffset 0 yyMMdd PD 20': 'today:yyMMdd'
}


class LegacyTranslator:
    """ translate legacy FTM custom and powershell date string to the new standard
    keep all the file_name prefix and suffix, etc.
    Below are input examples:
    ("statestreet_") + (dayoffset -1 yyyyMMdd) + (".txt")
    RIC_APX_Securities_*
    ("bondedge_") + ($objPDate.today_PM) + (".txt")
    ("f2456af4.ext.") + (Get-Date -format yyMMdd) + (".1")
    ("fitrec2rdr") + ($objPDate.today)  + ("*.txt")
    ("f2456cashflow.ext.") + (dayoffset 0 yyMMdd PD 20) + (".1")
    ("RADAR_BRC_*") + ($objPDate.priorwday) + (".csv")
    ("PRODConningEquity_") + (Get-Date -format yyyy-MM-dd) + (".txt")
    (bizday 1 yyyyMMdd n NA PD 20) + ("_WalnutCreekDailyNAVExtract.csv")
    ($objPDate.today_PM) + ("_WalnutCreekNAVExtract.csv")
    ($objPDate.priorwday) + ("_RiskSum_LehmanMTDER5.csv")
    ("COMP_GLOBAL_") + (lbdom -1 yyyyMMdd y WFAM) + (".csv")
    """

    @staticmethod
    def __find_replace(name_part: str) -> str:
        for key, value in _format_dict.items():
            if (key in name_part):
                return '${' + name_part.replace(key, value) + '}'
        return name_part

    @staticmethod
    def translate(old_filename: str) -> str:

        name_parts = old_filename.split('+')
        name_parts = [part.strip('()"\' ') for part in name_parts]
        # create a map object
        x = map(LegacyTranslator.__find_replace, name_parts)
        return ''.join(list(x))


in_str = input('enter a legacy string: ')
print(LegacyTranslator.translate(in_str))
